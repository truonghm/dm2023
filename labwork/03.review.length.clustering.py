def manhattan_point_dist(p1, p2):
    return abs(p1 - p2)


def min_cluster_dist(c1, c2):
    min_dist = float("inf")
    for p1 in c1:
        for p2 in c2:
            dist = manhattan_point_dist(p1, p2)
            if dist < min_dist:
                min_dist = dist
    return min_dist


def hierachial_clustering(v, dist_func):
    clusters = [[i] for i in v]

    while len(clusters) > 1:
        min_dist = float("inf")
        min_i = -1
        min_j = -1
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = dist_func(clusters[i], clusters[j])
                if dist < min_dist:
                    min_dist = dist
                    min_i = i
                    min_j = j

        clusters[min_i] += clusters[min_j]
        del clusters[min_j]

    return clusters
