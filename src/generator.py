import numpy as np
import pandas as pd
import os
from .utils import compute_distance, awgn_noise

def generate_data(
    seconds, samples_second, speed, max_distance,
    noise_power_levels, bw, P, beta, alfa, variance, n,
    data_size, output_path
):
    records = []

    for _ in range(data_size):
        d, su_init, pu_init, _, _ = compute_distance(seconds, speed, samples_second, max_distance)
        h = np.random.normal(0, variance, seconds * samples_second)
        k = np.sqrt(P / (beta * (np.array(d) ** alfa) * 10 ** (h / 10)))

        for noise_power in noise_power_levels:
            w = awgn_noise(seconds * samples_second, noise_power, bw)
            y = k * np.random.randn(2 * seconds * samples_second).view(np.complex128) *                 np.random.normal(1, variance, seconds * samples_second) + w
            records.append({
                "signal": y,
                "noise_power": noise_power,
                "initial_distance": d[0],
                "final_distance": d[-1],
                "label": "BP"
            })

            wn = awgn_noise(seconds * samples_second, noise_power, bw)
            yn = np.sqrt(n) * k * np.random.randn(2 * seconds * samples_second).view(np.complex128) *                  np.random.normal(1, variance, seconds * samples_second) + wn
            records.append({
                "signal": yn,
                "noise_power": noise_power,
                "initial_distance": d[0],
                "final_distance": d[-1],
                "label": "BA"
            })

    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("CSV gerado em:", output_path)
