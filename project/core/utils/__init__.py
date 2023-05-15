import imageio
from pathlib import Path
import numpy as np

from core.dataobject import Point3D, DataVector

def load_image(path: str):
    image_path = Path(path)
    # image = imageio.imread(image_path)
    img = np.array(imageio.imread(image_path), dtype=np.float64) / 255
    return img

def prepare_image(image):
    w, h, d = image.shape
    image_array = image.reshape(w * h, d)
    
    data = [Point3D(*rgb) for rgb in image_array]
        
    return DataVector(data)

def recreate_image(centroids, labels, w, h):
    """Recreate the (compressed) image from the code book & labels"""
    d = centroids.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = centroids[labels[label_idx]]
            label_idx += 1
    return image