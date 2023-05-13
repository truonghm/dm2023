import json
import random
import matplotlib.pyplot as plt

REVIEW_PATH = "../data/yelp_academic_dataset_review.json"

def read_data(limit: int) -> list:
    lengths = []
    with open(REVIEW_PATH) as f:
        for idx, line in enumerate(f):
            if idx >= limit:
                break
            lengths.append(len(json.loads(line)["text"]))

    return lengths

lengths = read_data(1000)

class KMeansClustering:
    def __init__(self, k: int, seed: int = 0):
        self.k = k
        random.seed(seed)

    def compute_mean(self, cluster: list):
        if len(cluster) == 0:
            return 0
        return sum(cluster) / len(cluster)

    def fit(self, data: list, threshold: float = 0.001):
        centroids = random.sample(data, self.k)
        clusters = {i: [] for i in range(self.k)}
        labels = []

        while True:
            labels = []
            for value in data:
                closest_centroid_idx = 0
                closest_distance = abs(centroids[0] - value)
                for idx, centroid in enumerate(centroids[1:], start=1):
                    distance = abs(centroid - value)
                    if distance < closest_distance:
                        closest_centroid_idx = idx
                        closest_distance = distance
                labels.append(closest_centroid_idx)
                clusters[closest_centroid_idx].append(value)

            new_centroids = [self.compute_mean(cluster) for cluster in clusters.values()]
            
            max_shift = max(abs(new - old) for new, old in zip(new_centroids, centroids))
            if max_shift < threshold:
                break

            centroids = new_centroids

        self.centroids = centroids
        self.labels = labels
        
def plot(data: list, labels: list):
	colors = ['red', 'green', 'blue']

	for i, cluster in enumerate(labels):
		plt.scatter(data[i], [cluster], c=colors[int(cluster)], label=f'Cluster {cluster+1}')

	plt.show()
        

lengths = read_data(1000)
kmeans = KMeansClustering(k=3)
kmeans.fit(list(lengths))


print(kmeans.centroids)
plot(lengths, kmeans.labels)
