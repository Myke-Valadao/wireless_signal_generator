# 📡 Wireless Signal Generator

This project simulates wireless signal transmissions, generating synthetic signal data under varying noise levels and mobility conditions. It can be used for developing and testing machine learning models or communication algorithms under controlled conditions.

---

## 🧠 Project Overview

The simulation models:

- A **Secondary User (SU)** moving through a 2D space over time.
- A **Primary User (PU)** placed at a fixed random location.
- **Signal propagation** affected by distance, fading, and noise.
- Two types of signals:
  - **BP** (Main Band)
  - **BA** (Adjacent Band)
- Additive White Gaussian Noise (AWGN) is introduced at multiple power levels.

---

## 🗂️ Project Structure

```
wireless_signal_generator/
├── src/
│   ├── __init__.py
│   ├── config.py                 # Default parameters for the simulation
│   ├── utils.py                  # Helper functions (noise, distance)
│   └── generator.py              # Core logic to generate wireless signal data
├── scripts/
    └── visualize.py              # Script to visualize signal data
├── main.py                       # CLI interface using argparse                 
├── requirements.txt              # Project dependencies
└── README.md                     # You're here!
```

---

## 🚀 How to Use

### ▶️ Run with Default Parameters

```bash
python main.py
```

This will create a file at `data/wireless_signals.csv` containing the generated signal samples.

---

### ⚙️ Customize Parameters

You can pass parameters via CLI:

```bash
python main.py --seconds 10 --samples_second 2048 --speed 1.0 \
               --max_distance 300 --data_size 50 \
               --output_path "output/signals.csv"
```

Use `--noise_power_levels` as a comma-separated list:

```bash
python main.py --noise_power_levels -110,-120,-130
```

---

## 🔧 Parameters Explained

| Parameter            | Description                                                              | Default          |
|----------------------|--------------------------------------------------------------------------|------------------|
| `seconds`            | Total duration (in seconds) of signal generation                         | 5                |
| `samples_second`     | Number of samples per second                                             | 1024             |
| `speed`              | Speed of the moving SU (secondary user)                                  | 0.83             |
| `max_distance`       | Size of the 2D area (square region)                                      | 250              |
| `noise_power_levels` | List of noise power levels to simulate AWGN                              | [-114,...,-174]  |
| `bw`                 | Bandwidth of the signal (Hz)                                              | 10,000,000       |
| `P`                  | Transmission power (dBm)                                                | 23               |
| `beta`               | Path loss constant (environment-specific)                                | 10^3.453         |
| `alfa`               | Path loss exponent                                                        | 3.8              |
| `variance`           | Variance used for shadowing/fading                                       | 7.9              |
| `n`                  | Scaling factor for adjacent channel signal                               | 0.01             |
| `data_size`          | Number of simulation iterations                                           | 10               |
| `output_path`        | Path to save the resulting CSV                                            | data/wireless_signal.csv |

---

## 📂 Files Explained

- **`main.py`**: Entry point. Parses CLI arguments and triggers signal generation.
- **`src/config.py`**: Contains the default parameters for simulation.
- **`src/utils.py`**: Implements utility functions for distance and AWGN noise modeling.
- **`src/generator.py`**: Core logic. Computes distances, generates signals, adds noise, saves CSV.
- **`visualize.py`**: Allows visualization of generated signals by label, FFT, and noise comparison.

---

## 📦 Installation

Install dependencies via pip:

```bash
pip install -r requirements.txt
```

---

## 📊 Output Format

Each row in the CSV represents one signal:

| Column           | Description                                  |
|------------------|----------------------------------------------|
| `signal`         | Complex-valued signal samples                |
| `noise_power`    | Noise level used for the sample              |
| `initial_distance`| Distance from SU to PU at start time        |
| `final_distance` | Distance from SU to PU at end time           |
| `label`          | "BP" (Main Band) or "BA" (Adjacent Band)     |

---

## 🧪 Example Use Cases

- Wireless communication system simulation
- Machine learning datasets for signal classification
- Spectrum sensing and dynamic channel allocation
- Noise resilience testing

---

## 🔢 How Many Signals Are Generated?

For each simulation iteration (`data_size`), the generator produces:

- 2 signals per noise power level (1 for the main band **BP**, and 1 for the adjacent band **BA**)
- For `n` noise levels, that results in: `2 × n` signals per iteration

So the total number of signals in the dataset is:

```
total_signals = data_size × 2 × len(noise_power_levels)
```

📝 **Example:**  
If `data_size = 10` and `noise_power_levels = [-114, -124, ..., -174]` (7 levels), then:
```
10 × 2 × 7 = 140 signals
```

Each row in the CSV file represents **one signal**, but due to the complex signal array stored as a string, it may visually span multiple lines when opened in text editors or Excel.  
To get the true number of signals, use `len(df)` in pandas.

---

## 📈 Signal Visualization

You can visualize the generated signals using the provided `visualize.py` script. It supports:

- **Sequential inspection** of signals (time and frequency domain)
- **Spectral visualization (FFT)**
- **Noise level comparison**
- **Label filtering** (BP or BA)

### ▶️ Run the Visualizer

```bash
python visualize.py --csv_path data/wireless_signals.csv --mode loop
```

### 🧪 Visualization Modes

| Mode     | Description                                                           |
|----------|-----------------------------------------------------------------------|
| `loop`   | Shows signals one-by-one (real/imaginary and FFT)                     |
| `compare`| Compares FFT of signals with different noise levels side-by-side      |

### 🔍 Optional Arguments

- `--label BP` or `--label BA` to filter by band
- `--csv_path <path>` to specify the signal file (required)

### 💡 Examples

1. **Visualize all signals:**
   ```bash
   python scripts/visualize.py --csv_path data/wireless_signals.csv --mode loop
   ```

2. **Visualize only BP signals:**
   ```bash
   python scripts/visualize.py --csv_path data/wireless_signals.csv --mode loop --label BP
   ```

3. **Compare signals across noise levels (BP only):**
   ```bash
   python scripts/visualize.py --csv_path data/wireless_signals.csv --mode compare --label BP
   ```

---

## 🤝 Contributions

Feel free to fork the repository, suggest improvements, or contribute features!

---

## 📚 References

```bibtex
@article{valadao2021deep,
  title={Deep cooperative spectrum sensing based on residual neural network using feature extraction and random forest classifier},
  author={Valad{\~a}o, Myke DM and Amoedo, Diego and Costa, Andr{'e} and Carvalho, Celso and Sabino, Waldir},
  journal={Sensors},
  volume={21},
  number={21},
  pages={7146},
  year={2021},
  publisher={MDPI}
}

@inproceedings{valadao2022cooperative,
  title={Cooperative spectrum sensing system using residual convolutional neural network},
  author={Valad{\~a}o, Myke DM and Amoedo, Diego A and Pereira, Ant{\^o}nio MC and Tavares, Samuel A and Furtado, Rafael S and Carvalho, Celso B and Da Costa, Andr{'e} LA and J{'u}nior, Waldir SS},
  booktitle={2022 IEEE International Conference on Consumer Electronics (ICCE)},
  pages={1--5},
  year={2022},
  organization={IEEE}
}

@article{valadao2024noise,
  title={Noise Power Density Estimation Based on Deep Learning Using Spectrograms Extracted from Wireless Signals},
  author={Valad{\~a}o, Myke and Costa, Andr{'e} and Amoedo, Diego and Carvalho, Celso},
  journal={ResearchGate Preprint},
  year={2024},
  url={https://www.researchgate.net/publication/384913613}
}
```
