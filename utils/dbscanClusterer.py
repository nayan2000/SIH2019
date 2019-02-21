from sklearn.cluster import DBSCAN
import pandas as pd
# For the centermost point func
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
import numpy as np
import sqlite3
# standard
from time import time

start_time = time()

#Connect with database
db_connection = sqlite3.connect(database='../db.sqlite3')
# db_connection = sql.connect(host='hostname', database='db_name', user='username', password='password')
df = pd.read_sql('SELECT lat, long FROM main_userprofile', con=db_connection)
print(df)

KMS_PER_RADIAN = 6371.0088
epsilon = 250 / KMS_PER_RADIAN


def plot_elbow(kmean, X):
    centroids = [k.cluster_centers_ for k in kmean]
    D_k = [cdist(X, center, 'euclidean') for center in centroids]
    dist = [np.min(D,axis=1) for D in D_k]


def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)


df = df.values
print(df)
db = DBSCAN(
        eps=epsilon,
        min_samples=1,
        algorithm='ball_tree',
        metric='haversine',
    ).fit(np.radians(.astype(np.float32)))

cluster_labels = db.labels_
print(cluster_labels)
cluster_labels = pd.Series(cluster_labels)
df.iloc[:, 3] = cluster_labels
df.to_csv(fname, header=False, index=False, sep='|')

num_clusters = len(set(cluster_labels))
print('Number of clusters: {}'.format(num_clusters))

# all done, print time
print('Done in ', time()-start_time, ' secs')
