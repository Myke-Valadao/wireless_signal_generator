import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


def parse_complex_array(raw_str):
    """
    Extrai números complexos do formato '[a+bj a-bj ...]' em array NumPy
    """
    try:
        # Regex para encontrar números complexos como 0.1+0.2j ou -0.3-0.4j
        complex_regex = re.findall(r'([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)([-+]\d*\.?\d+(?:[eE][-+]?\d+)?)j', raw_str)
        complex_array = [complex(float(re), float(im)) for re, im in complex_regex]
        return np.array(complex_array)
    except Exception as e:
        print(f"⚠️ Erro ao processar sinal: {e}")
        return np.array([], dtype=np.complex64)


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df['signal'] = df['signal'].apply(parse_complex_array)
    return df


def plot_time_and_freq(signal, title=""):
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))

    axs[0].plot(np.real(signal), label="Real")
    axs[0].plot(np.imag(signal), label="Imag", linestyle='--')
    axs[0].set_title("Time Domain")
    axs[0].legend()

    spectrum = np.fft.fftshift(np.fft.fft(signal))
    freq_axis = np.fft.fftshift(np.fft.fftfreq(len(signal)))
    axs[1].plot(freq_axis, 20 * np.log10(np.abs(spectrum) + 1e-10))
    axs[1].set_title("Frequency Domain (FFT)")

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()


def loop_signals(df, label_filter=None):
    filtered_df = df if label_filter is None else df[df['label'] == label_filter]

    for idx, row in filtered_df.iterrows():
        signal = row['signal']
        label = row['label']
        noise = row['noise_power']
        if signal.size > 0:
            plot_time_and_freq(signal, title=f"Label: {label} | Noise: {noise} dB")
        else:
            print(f"⚠️ Sinal inválido na linha {idx}")


def compare_signals(df, label_filter=None):
    filtered_df = df if label_filter is None else df[df['label'] == label_filter]
    grouped = filtered_df.groupby('noise_power')

    plt.figure(figsize=(10, 6))
    for noise_level, group in grouped:
        signal = group.iloc[0]['signal']
        if signal.size == 0:
            continue
        spectrum = np.fft.fftshift(np.fft.fft(signal))
        freq_axis = np.fft.fftshift(np.fft.fftfreq(len(signal)))
        plt.plot(freq_axis, 20 * np.log10(np.abs(spectrum) + 1e-10), label=f"{noise_level} dB")

    plt.title("Frequency Comparison by Noise Level")
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude (dB)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize wireless signals")
    parser.add_argument("--csv_path", type=str, required=True, help="Path to CSV with signals")
    parser.add_argument("--mode", choices=["loop", "compare"], default="loop", help="Visualization mode")
    parser.add_argument("--label", type=str, choices=["BP", "BA"], help="Filter by signal label")
    args = parser.parse_args()

    df = load_data(args.csv_path)

    if args.mode == "loop":
        loop_signals(df, label_filter=args.label)
    elif args.mode == "compare":
        compare_signals(df, label_filter=args.label)

