import argparse
from matplotlib import pyplot as plt

import numpy as np
from core.clustering import MeanShiftClustering
from core.kernel import FlatKernel, GaussianKernel
from core.utils import load_image, prepare_image
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Path for the input image, e.g: ./data/example.png",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        type=bool,
        default=True,
        help="Enable verbose mode",
        action=argparse.BooleanOptionalAction
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        # default="output.jpg",
        help="Path for output highlighted image",
    )

    parser.add_argument(
        "-k",
        "--kernel",
        type=str,
        help="Kernel Function to use. Available options: flat, gaussian",
    )

    parser.add_argument(
        "-bd",
        "--bandwidth",
        type=float,
        default=0.5,
        help="Bandwidth for the kernel function",
    )

    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.01,
        help="Threshold for stopping the clustering",
    )

    args = parser.parse_args()

    if args.kernel == "flat":
        kernel = FlatKernel(h=args.bandwidth)

    elif args.kernel == "gaussian":
        kernel = GaussianKernel(sigma=args.bandwidth)

    else:
        raise ValueError("Invalid kernel function")

    mean_shift = MeanShiftClustering(kernel=kernel, threshold=args.threshold)
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"File {args.input} not found")

    print("Loading image...")
    image = load_image(args.input)
    image_array = prepare_image(image)

    print("Image loaded successfully. Dimension of image are: ", image.shape)

    print("Fitting data...")
    mean_shift.fit_predict(image_array, verbose=args.verbose)
    
    print("Fitting done. Number of clusters found: ", len(mean_shift.centroids))

    labels = mean_shift.labels
    plt.imshow(np.array(labels).reshape(image.shape[0], image.shape[1]))

    print("Saving output image to", args.output)

    if args.output:
        plt.title(f"{args.kernel} kernel with bandwidth={args.bandwidth}")
        plt.savefig(args.output)
