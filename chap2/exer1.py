import os
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)


def create_data(a):
    mean = np.array([3, 5])
    cov = np.array([[10, a], [a, 0.0001]])
    data = np.random.multivariate_normal(mean, cov, size=100)

    return data


def plot_data(data):
    print("data shape = ", data.shape)
    plt.scatter(data[:, 0], data[:, 1])
    plt.xlim(-6, 14)
    plt.ylim(3, 7)
    plt.show()


def main():
    data = create_data(0.8)
    plot_data(data)


if __name__ == '__main__':
    main()