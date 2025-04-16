import numpy as np
import math

def euclidean_distance(x1, x2, y1, y2):
    x1, x2, y1, y2 = np.array(x1), np.array(x2), np.array(y1), np.array(y2)
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def compute_distance(seconds, speed, max_angle_change, samples_second, max_distance):
    if samples_second <= 0:
        raise ValueError("samples_second deve ser positivo.")
    if seconds < 0:
         raise ValueError("seconds não pode ser negativo.")

    dt = 1.0 / samples_second  # Intervalo de tempo entre amostras
    num_steps = int(seconds * samples_second)

    # Define limites da área para posição inicial
    min_coord = -max_distance / 2.0
    max_coord = max_distance / 2.0

    # Posições iniciais aleatórias
    initial_pos_su = [np.random.uniform(min_coord, max_coord),
                      np.random.uniform(min_coord, max_coord)]
    initial_pos_pu = [np.random.uniform(min_coord, max_coord),
                      np.random.uniform(min_coord, max_coord)]

    # Ângulos iniciais aleatórios (em radianos)
    theta_su = np.random.uniform(0, 2 * math.pi)
    theta_pu = np.random.uniform(0, 2 * math.pi)

    # Listas para armazenar as trajetórias
    SU_trajectory = [list(initial_pos_su)]
    PU_trajectory = [list(initial_pos_pu)]

    # Lista para armazenar as distâncias
    distances = []

    # Posições atuais
    current_pos_su = list(initial_pos_su)
    current_pos_pu = list(initial_pos_pu)

    # Calcula a distância inicial
    distances.append(euclidean_distance(current_pos_su[0], current_pos_pu[0],
                                        current_pos_su[1], current_pos_pu[1]))

    # Simulação passo a passo
    for _ in range(max(0, num_steps - 1)):
        # --- Movimento SU ---
        # Calcula deslocamento baseado na velocidade e ângulo atual
        vx_su = speed * math.cos(theta_su)
        vy_su = speed * math.sin(theta_su)
        current_pos_su[0] += vx_su * dt
        current_pos_su[1] += vy_su * dt
        SU_trajectory.append(list(current_pos_su))

        # Atualiza o ângulo do SU aleatoriamente
        delta_theta_su = np.random.uniform(-max_angle_change * dt, max_angle_change * dt)
        theta_su += delta_theta_su
        # Normaliza o ângulo para ficar entre -pi e pi (opcional, mas bom)
        # theta_su = (theta_su + math.pi) % (2 * math.pi) - math.pi

        # --- Movimento PU ---
        # Calcula deslocamento
        vx_pu = speed * math.cos(theta_pu)
        vy_pu = speed * math.sin(theta_pu)
        current_pos_pu[0] += vx_pu * dt
        current_pos_pu[1] += vy_pu * dt
        PU_trajectory.append(list(current_pos_pu))

        # Atualiza o ângulo do PU aleatoriamente
        delta_theta_pu = np.random.uniform(-max_angle_change * dt, max_angle_change * dt)
        theta_pu += delta_theta_pu
        # Normaliza o ângulo
        # theta_pu = (theta_pu + math.pi) % (2 * math.pi) - math.pi

        # --- Calcula Distância ---
        dist = euclidean_distance(current_pos_su[0], current_pos_pu[0],
                                  current_pos_su[1], current_pos_pu[1])
        distances.append(dist)

    return distances, initial_pos_su, initial_pos_pu


def awgn_noise(length, noise_power, bandwidth):
    sigma = np.sqrt(bandwidth * 10 ** (noise_power / 10))
    noise = np.random.normal(0, sigma, 2 * length).view(np.complex128)
    return noise
