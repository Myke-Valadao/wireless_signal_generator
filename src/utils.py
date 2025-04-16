import numpy as np

def euclidean_distance(x1, x2, y1, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def compute_distance(seconds, speed, samples_second, max_distance):
    if samples_second <= 0:
        raise ValueError("samples_second deve ser positivo.")
    if seconds < 0:
         raise ValueError("seconds não pode ser negativo.")

    dt = 1.0 / samples_second  # Intervalo de tempo entre amostras
    num_steps = int(seconds * samples_second)

    # Define limites da área para posição inicial (melhor usar contínuo)
    min_coord = -max_distance / 2.0
    max_coord = max_distance / 2.0

    # Posições iniciais aleatórias dentro da área
    initial_pos_su = [np.random.uniform(min_coord, max_coord),
                      np.random.uniform(min_coord, max_coord)]
    initial_pos_pu = [np.random.uniform(min_coord, max_coord),
                      np.random.uniform(min_coord, max_coord)]

    # Listas para armazenar as trajetórias completas
    # Armazenamos cópias para evitar problemas com mutabilidade de listas
    SU_trajectory = [list(initial_pos_su)]
    PU_trajectory = [list(initial_pos_pu)]

    # Lista para armazenar as distâncias
    distances = []

    # Posições atuais (começam nas iniciais)
    current_pos_su = list(initial_pos_su)
    current_pos_pu = list(initial_pos_pu)

    # Calcula a distância inicial
    distances.append(euclidean_distance(current_pos_su[0], current_pos_pu[0],
                                        current_pos_su[1], current_pos_pu[1]))

    # Simulação passo a passo
    # O loop roda num_steps-1 vezes porque o passo inicial já foi calculado
    for _ in range(max(0, num_steps - 1)): # max(0,...) para o caso de seconds muito pequeno
        # Movimento aleatório do SU
        # Deslocamento em X e Y entre [-speed*dt, +speed*dt]
        dx_su = np.random.uniform(-speed * dt, speed * dt)
        dy_su = np.random.uniform(-speed * dt, speed * dt)
        current_pos_su[0] += dx_su
        current_pos_su[1] += dy_su
        SU_trajectory.append(list(current_pos_su)) # Adiciona cópia da nova posição

        # Movimento aleatório do PU
        dx_pu = np.random.uniform(-speed * dt, speed * dt)
        dy_pu = np.random.uniform(-speed * dt, speed * dt)
        current_pos_pu[0] += dx_pu
        current_pos_pu[1] += dy_pu
        PU_trajectory.append(list(current_pos_pu)) # Adiciona cópia da nova posição

        # Calcula a distância Euclidiana entre as posições atuais
        dist = euclidean_distance(current_pos_su[0], current_pos_pu[0],
                                  current_pos_su[1], current_pos_pu[1])
        distances.append(dist)

    # Retorna as distâncias, posições iniciais e trajetórias completas
    return distances, initial_pos_su, initial_pos_pu, SU_trajectory, PU_trajectory


def awgn_noise(length, noise_power, bandwidth):
    sigma = np.sqrt(bandwidth * 10 ** (noise_power / 10))
    noise = np.random.normal(0, sigma, 2 * length).view(np.complex128)
    return noise
