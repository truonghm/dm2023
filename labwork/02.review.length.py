import json
import os
from typing import Any, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

REVIEW_PATH = "../data/yelp_academic_dataset_review.json"
IMAGES_PATH = "./images"

def read_data(limit: Optional[int] = None) -> np.ndarray:
    lengths = []
    with open(REVIEW_PATH) as f:
        for idx, line in enumerate(f):
            lengths.append(len(json.loads(line)["text"]))
            if limit and idx >= limit:
                break

    lengths = np.array(lengths)
    return lengths


def plot_distribution(lengths: np.ndarray):
    fig = plt.figure()
    _ = plt.hist(lengths, bins=100, density=True)
    save_path = os.path.join(IMAGES_PATH, "02.review.length.pdf")
    fig.savefig(save_path, format="pdf")


def calculate_stats(lengths: np.ndarray) -> Tuple[np.floating[Any], np.floating[Any]]:
    mean = np.mean(lengths)
    std = np.std(lengths)

    return mean, std


def calculate_phi(x: np.ndarray, mean: np.floating[Any], std: np.floating[Any]):
    return (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)


def plot_normal_distribution(
    lengths: np.ndarray, mean: np.floating[Any], std: np.floating[Any]
):
    x = np.linspace(mean - 3 * std, mean + 3 * std, 100)
    fig, ax = plt.subplots(1, 1)
    ax.hist(lengths, bins=100, density=True)
    ax.plot(x, calculate_phi(x, mean, std))
    save_path = os.path.join(IMAGES_PATH, "02.review.length.estimated.pdf")
    fig.savefig(save_path, format="pdf")


def main():
    lengths = read_data()
    plot_distribution(lengths)
    mean, std = calculate_stats(lengths)
    plot_normal_distribution(lengths, mean, std)

if __name__ == "__main__":
	main()
