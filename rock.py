import gower

def rock(data, eps, max_clusters, threshold = 0.5):
    degree_normalization = 1.0 + 2.0 * ( (1.0 - threshold) / (1.0 + threshold) )
    adjacency_matrix = create_adjacency_matrix(data, eps)
    clusters = [[index] for index in range(len(data))]
    
    while len(clusters) > max_clusters:
        indexes = find_pair_clusters(clusters, adjacency_matrix, degree_normalization)
        
        if (indexes == [-1, -1]):
            break

        clusters[indexes[0]] += clusters[indexes[1]]
        clusters.pop(indexes[1])
    
    return clusters


def create_adjacency_matrix(data, eps):
    size = len(data)
    
    distance_matrix = gower.gower_matrix(data)
    print(distance_matrix)
    adjacency_matrix = [ [ 0 for i in range(size) ] for j in range(size) ]

    for i in range(0, size):
        for j in range(i + 1, size):
            # distance = euclidean_distance(data[i], data[j])
            # distance = jaccard_distance(data[i], data[j])
            distance = distance_matrix[i][j]
            if (distance <= eps):
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
    
    return adjacency_matrix


def calculate_links(cluster1, cluster2, adjacency_matrix):
    number_links = 0
    
    for index1 in cluster1:
        for index2 in cluster2:
            number_links += adjacency_matrix[index1][index2]
            
    return number_links
  

def find_pair_clusters(clusters, adjacency_matrix, degree_normalization):
    maximum_goodness = 0.0
    cluster_indexes = [-1, -1]
    
    for i in range(0, len(clusters)):
        for j in range(i + 1, len(clusters)):
            goodness = calculate_goodness(clusters[i], clusters[j],
                                          adjacency_matrix, degree_normalization)
            if (goodness > maximum_goodness):
                maximum_goodness = goodness
                cluster_indexes = [i, j]
    
    return cluster_indexes          


def calculate_goodness(cluster1, cluster2, adjacency_matrix, degree_normalization):
    number_links = calculate_links(cluster1, cluster2, adjacency_matrix)
    deviser = (len(cluster1) + len(cluster2)) ** degree_normalization - len(cluster1) ** degree_normalization - len(cluster2) ** degree_normalization
    
    return (number_links / deviser)

