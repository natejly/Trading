from sklearn.cluster import KMeans
from dataframe import getdata
import pandas
import matplotlib.pyplot as plt
import numpy as np


def getClusters(df):
    df['cluster'] = KMeans(n_clusters = 4, random_state=0, init=initial_centroids).fit(df).labels_
    return df

def plot_clusters(data):
    cluster_0 = data[data['cluster']==0]
    cluster_1 = data[data['cluster']==1]
    cluster_2 = data[data['cluster']==2]
    cluster_3 = data[data['cluster']==3]
    
    plt.scatter(cluster_0.iloc[:,0], cluster_0.iloc[:,6], color = 'red', label = 'cluster0')
    plt.scatter(cluster_1.iloc[:,0], cluster_1.iloc[:,6], color = 'green', label = 'cluster1')
    plt.scatter(cluster_2.iloc[:,0], cluster_2.iloc[:,6], color = 'blue', label = 'cluster2')
    plt.scatter(cluster_3.iloc[:,0], cluster_3.iloc[:,6], color = 'black', label = 'cluster3')
    
    plt.legend(
    )
    plt.show()
    return
targetrsi = [30, 45, 55, 70]
initial_centroids = np.zeros((len(targetrsi),18))
initial_centroids[:,6] = targetrsi
data = getdata()
#data = data.drop('cluster', axis = 1)
data = data.dropna().groupby('date', group_keys=False).apply(getClusters)





print(data)
print(initial_centroids)
plt.style.use('ggplot')
for x in data.index.get_level_values('date').unique().tolist():
    g = data.xs(x, level=0)
    plt.title(f'date {x}')
    plot_clusters(g)
