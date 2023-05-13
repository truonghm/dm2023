import json
import random
import matplotlib.pyplot as plt

REVIEW_PATH = "../data/yelp_academic_dataset_review.json"

REVIEW_PATH = "../data/yelp_academic_dataset_review.json"


def read_data(limit: int):
    lengths = []
    reviews = []
    with open(REVIEW_PATH) as f:
        for idx, line in enumerate(f):
            if idx >= limit:
                break
            review = json.loads(line)["text"]
            lengths.append(len(review))
            reviews.append(review)
    return lengths, reviews


def calculate_manhattan_distance(point1, point2):
    return abs(point1 - point2)


def flat_kernel(point1, point2, h, dist_func):
    return 1 if dist_func(point1, point2) <= h else 0


def shift_mode(point, data, h, dist_func):
    total_weights = 0
    weighted_sum = 0
    for i in range(len(data)):
        weight = flat_kernel(point, data[i], h, dist_func)
        total_weights += weight
        weighted_sum += weight * data[i]

    if total_weights != 0:
        return weighted_sum / total_weights
    else:
        return point


def mean_shift(data, h, dist_func, threshold: float = 1e-5):
    mode = [[] for _ in range(len(data))]
    for i in range(len(data)):
        m = 0
        mode[i].append(data[i])
        while True:
            mode[i].append(shift_mode(mode[i][m], data, h, dist_func))
            m += 1
            if abs(mode[i][m] - mode[i][m - 1]) < threshold:
                break
        mode[i][0] = mode[i][m]

    centroids = []
    for i in range(len(data)):
        if mode[i][0] not in centroids:
            centroids.append(mode[i][0])

    labels = []
    for i in range(len(data)):
        labels.append(centroids.index(mode[i][0]))

    return centroids, labels


lengths, reviews = read_data(1000)
centroids, labels = mean_shift(lengths, 500, calculate_manhattan_distance)

clusters = {}
for i, label in enumerate(labels):
    if label not in clusters:
        clusters[label] = [reviews[i]]
    else:
        clusters[label].append(reviews[i])

for i, (k, v) in enumerate(clusters.items()):
    print(
        f"Cluster {i} with centroid {centroids[k]}: {len(v)} reviews, average length is {sum([len(review) for review in v]) / len(v)}"
    )
    print("######################")
    for review in v[:10]:
        print(review)
        print("---")
