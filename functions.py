from sklearn.metrics import silhouette_samples
import numpy as np
import pandas as pd
import category_encoders as ce
from sklearn import metrics
import gower


def plot_silhouette(data,clusters):
    #plt.figure(figsize=(10, 10))
    cluster_labels = np.unique(clusters) # kume etiketlerini cekelim

    print('Labels')
    print(cluster_labels)

    print('Shape')
    print(cluster_labels.shape)

    n_clusters = cluster_labels.shape[0]  

    print('Kume sayisi')
    print(n_clusters)
    
    silhouette_vals = silhouette_samples(data, clusters, metric='euclidean')

    print('silhouette vals:')
    #print(silhouette_vals)

    y_ax_lower, y_ax_upper = 0, 0
    yticks = []
    for i, c in enumerate(cluster_labels):  # her bir kume icin 0,1,2 ...
        c_silhouette_vals = silhouette_vals[clusters == c] # su anki küme için
        c_silhouette_vals.sort() # değerleri sırala
        y_ax_upper += len(c_silhouette_vals) 
        color = cm.jet(float(i) / n_clusters) # bir renk sec
        plt.barh(range(y_ax_lower, y_ax_upper),
                c_silhouette_vals,
                height=1.0,
                edgecolor='none',
                color=color)
        yticks.append((y_ax_lower + y_ax_upper) / 2.)
        y_ax_lower += len(c_silhouette_vals)
    silhouette_avg = np.mean(silhouette_vals)

    
    print(silhouette_avg)
    
    plt.axvline(silhouette_avg, color="red", linestyle="--")
    plt.yticks(yticks, cluster_labels + 1)   # 0.ci yazmasin, 1den baslasin
    plt.ylabel('Küme')
    plt.xlabel('Silhouette katsayısı')
    plt.show()



def _ordinal_encode(data):
  encoding_data=data.copy()
  encoder=ce.OrdinalEncoder(encoding_data)
  data_encoded=encoder.fit_transform(encoding_data)
  return data_encoded

def _overlap(data):
    data = _ordinal_encode(data)
    (row_amount,feature_amount) = data.shape 
    
    overlap = np.zeros(shape=(row_amount,row_amount))
    for row1_index in range(row_amount - 1):
        for row2_index in range(row1_index + 1, row_amount):
            
            agreement = 0

            for feature_index in range(feature_amount):
                if data.iat[row1_index, feature_index] == data.iat[row2_index, feature_index]:
                    agreement += 1

                overlap[row1_index][row2_index] = 1 - (1/feature_amount * (agreement))
                overlap[row2_index][row1_index] = overlap[row1_index][row2_index]
    return pd.DataFrame(overlap)


def evaluate_clusters(X, clusters):
    distances = _overlap(X)
    return metrics.silhouette_score(distances,clusters,metric="precomputed")