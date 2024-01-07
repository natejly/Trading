from sklearn.cluster import KMeans
from dataframe import getdata
import pandas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def getClusters(df):
    targetrsi = [30, 45, 55, 70]
    initial_centroids = np.zeros((len(targetrsi),18))
    initial_centroids[:,6] = targetrsi
    df['cluster'] = KMeans(n_clusters = 4, random_state=0, init=initial_centroids, n_init=10).fit(df).labels_ #n_init on 10 to bypass warnings
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
def visualize(data):
    plt.style.use('ggplot')
    for x in data.index.get_level_values('date').unique().tolist():
        g = data.xs(x, level=0)
        plt.title(f'date {x}')
        plot_clusters(g)
        
def dofilter(data):

    #data = data.drop('cluster', axis = 1)
    data = data.dropna().groupby('date', group_keys=False).apply(getClusters)

    #visualize(data)

    #cluster 3 data
    filtered_df = data[data['cluster']==3].copy()
    filtered_df = filtered_df.reset_index(level=1)
    filtered_df.index = filtered_df.index+pd.DateOffset(1)
    filtered_df = filtered_df.reset_index().set_index(['date', 'ticker']).unstack().stack()
    return filtered_df
def getdates(filtered_df):
    dates = filtered_df.index.get_level_values('date').unique().tolist()
    fixed_dates = {}
    for date in dates:
        fixed_dates[date.strftime('%Y-%m-%d')] = filtered_df.xs(date, level=0).index.tolist()
    return fixed_dates

if __name__ == "__main__":
    dofilter(getdata())