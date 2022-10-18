# Clustering-Algorithms

The set of self-made algorithms for Cluster Analysis (Clustering). Clustering is the technique that aims to grouping set of objects (data points). The objects in one group are more similar to each other, than to objects in another group. Technically speaking, Clustering is the Machine unsupervised learning method used for grouping unlabeled data and main method for the statistical data analysis. There are plenty of clustering algorithms with are based on the different clustering models. For my purpose i have used the most popular ones, including:

- [Agglomerative Hierarchical](#agg)

- [Mean-Shift](#mean-s)

- [K-Means](#kmean)

- [DBSCAN](#dbsc)
<a name="agg"></a>
## Agglomerative Hierarchical Clustering
1. Set each data point as a separate cluster. This means, that the number of clusters and their coordinates at the beginning are the same as the number of data points and their coordinates.
2. Set distance metric between two clusters, usually average linkage. It means that the distance between the two clusters is the average distance between data points in one cluster and data points in the other cluster.
3. In each iteration we are combining two clusters with the shortage average linkage - smallest distance between data points.
4. Repeat step 3 until we have only one cluster containing all data points. Now you can choose the optimal number of clusters at the end, in our case - 3 clusters.
### Sample result:
![result](https://user-images.githubusercontent.com/44844566/194873845-e181ffeb-44a5-4344-8b00-56cfd6087672.gif)
<a name="mean-s"></a>
## Mean-Shift
1. Create sliding windows with the randomly selected coordinates and set it radius - R.
2. Move sliding windows into the areas with higher density. Density is proportional to the number of data points, the new slinding window center is the mean of the data points inside.
3. Repeat step 2 until the moment, that sliding window can't detect higher density areas.
4. The data points are clustered according to the sliding window in which interior they are. If 2 sliding windows overlap, the points belong to the sliding window with a greater number of data points.
### Sample result:
![result](https://user-images.githubusercontent.com/44844566/194872357-62ad9c9a-4cae-45f1-9aba-1e0d8cad2654.gif)
<a name="kmean"></a>
## K-Means
1. Set the number of clusters(k) intuitively by looking at the dataset. In our case k = 3. The cluster center is randomly set.
2. Compute the distance between each data point and the cluster center. Each data point is assigned to the cluster, according to the shortest distance.
3. Calculate the new cluster center according to the mean of the data points belonging to this cluster.
4. Repeat steps 2-3 until the cluster centers don't change.
### Sample result:
![result](https://user-images.githubusercontent.com/44844566/194873362-cb474495-9a8f-4c88-9394-56141a6ebf01.gif)
<a name="dbsc"></a>
## DBSCAN
1. Set the epsilon distance and the minPoints measures. 
2. Visit each unvisited data points, if the number of neighbors data points within epsilon distance is more or equal minPoints number, then this point is treated as a initial point of the new cluster and all the neighbors points belong to this cluster. Oterwise the point is treated as a 'noise'. The point is marked as 'visited'.
3. 
### Sample result:
![result](https://user-images.githubusercontent.com/44844566/194877560-e2a9f245-69fc-45b7-8f74-8c7667d001d0.gif)
