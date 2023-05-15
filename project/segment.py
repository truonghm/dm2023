import argparse
from matplotlib import pyplot as plt

import numpy as np
from core.clustering import MeanShiftClustering
from core.kernel import FlatKernel, GaussiantKernel
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
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.jpg",
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
        help="Bandwidth for the flat kernel function",
    )

    args = parser.parse_args()

    if args.kernel == "flat":
        kernel = FlatKernel(h=args.bandwidth)

    elif args.kernel == "gaussian":
        kernel = GaussiantKernel()

    else:
        raise ValueError("Invalid kernel function")

    mean_shift = MeanShiftClustering(kernel=kernel, threshold=0.001)
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"File {args.input} not found")

    if args.verbose:
        print("Loading image...")
    image = load_image(args.input)
    image_array = prepare_image(image)
    if args.verbose:
        print("Image loaded successfully. Dimension of image are: ", image.shape)

    if args.verbose:
        print("Fitting data...")
    mean_shift.fit(image_array, verbose=args.verbose)
    
    if args.verbose:
        print("Fitting done. Number of clusters found: ", len(mean_shift.centroids))

    labels = mean_shift.predict(image_array)
    plt.imshow(np.array(labels).reshape(image.shape[0], image.shape[1]))

    if args.verbose:
        print("Saving output image to", args.output)

    plt.savefig(args.output)
