import numpy as np

def euclidean_distance(a, b, c, d):
    return np.sqrt(np.sum((a - b) ** 2 + (c - d) ** 2))

def compute_distance(seconds, speed, samples_second, max_distance):
    time = np.arange(0, seconds, 1 / samples_second)
    area = np.arange(int(-max_distance / 2), int(max_distance / 2), 1)
    initial_position_su = [np.random.choice(area, 1), np.random.choice(area, 1)]
    PU = [np.random.choice(area, 1), np.random.choice(area, 1)]
    SU = []
    direction = (-1) ** (np.random.choice([1, 2], 1))
    for t in time:
        SU.append(initial_position_su + direction * (speed * t))
    distances = [
        euclidean_distance(SU[i][0], PU[0], SU[i][1], PU[1])
        for i in range(len(time))
    ]
    return distances, initial_position_su, PU

def awgn_noise(length, noise_power, bandwidth):
    sigma = np.sqrt(bandwidth * 10 ** (noise_power / 10))
    noise = np.random.normal(0, sigma, 2 * length).view(np.complex128)
    return noise
