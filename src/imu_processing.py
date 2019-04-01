import numpy as np
import scipy


epsilon = 0.5


def rotation_matrix(alpha, beta, gamma):
    return np.ndarray([[np.cos(alpha) * np.cos(beta),
                        np.sin(alpha) * np.cos(beta),
                        -np.sin(beta)],
                       [np.cos(alpha) * np.sin(beta) * np.sin(gamma) - np.sin(alpha) * np.cos(gamma),
                        np.sin(alpha) * np.sin(beta) * np.sin(gamma) + np.cos(alpha) * np.cos(gamma),
                        np.cos(beta) * np.sin(gamma)],
                       [np.cos(alpha) * np.sin(beta) * np.cos(gamma) + np.sin(alpha) * np.sin(gamma),
                        np.sin(alpha) * np.sin(beta) * np.cos(gamma) - np.cos(alpha) * np.sin(gamma),
                        np.cos(beta) * np.cos(gamma)]])


def update_gravity(grav, gyro, t):
    t_step = t / len(gyro)
    for i in range(len(gyro)):
        grav = grav * rotation_matrix(gyro[i, 0] * t_step, gyro[i, 1] * t_step, gyro[i, 2] * t_step)
    return grav


def project(v, n):
    return v - np.dot((np.dot(v, n) / np.linalg.norm(n) ** 2), n)


def is_stable(acc):
    mu = sum(acc) / len(acc)
    for i in range(1, len(acc), 1):
        diff = np.linalg.norm(scipy.spacial.distance.euclidian(acc[i], mean))
        if diff < epsilon:
            return False
    return True


