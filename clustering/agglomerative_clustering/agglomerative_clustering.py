import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import numpy as np
import string
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
import imageio
import os

dataSet = {
    'x': [61,72,23,14,55,96,17,8,59,40,14,18,93,27,35,46,11,22,33,77,99],
    'y': [1,2,3,4,5,6,7,8,9,10,14,18,43,67,85,46,32,65,87,23,57]
    }
dataSet['color'] = 'black'
colorSet = []
dataSet = pd.DataFrame(dataSet)
k = len(dataSet)
clusters = {}
new_clusters = {}
colorMap = {}
screenNumber = 0

def createDendogram(dataSet):   
    xCoordinates = []
    yCoordinates = []
    dataSetCoordinates = []
    
    xCoordinates = dataSet['x']
    yCoordinates = dataSet['y']
    for i in range(len(xCoordinates)):
        dataSetCoordinates.append([xCoordinates[i], yCoordinates[i]]) 
    y = pdist(dataSetCoordinates)
    Z = hierarchy.linkage(y, 'centroid')
    plt.figure()
    hierarchy.dendrogram(Z)


plt.ion()
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
xlim=(0,100)
ylim=(0,100)
scatter1 = ax.scatter(x = dataSet['x'], y = dataSet['y'], color = dataSet['color'])
plt.show()
plt.pause(0.2)

for i in range(k):
    colorSet.append('#{}'.format(''.join(rd.choice(string.digits) for _ in range(6))))
    
for i in range(k):
    clusters[colorSet[i]] = {'x': dataSet.loc[i,'x'],
                             'y': dataSet.loc[i,'y']
                            }  
    
clusters = pd.DataFrame(clusters).transpose()
clusters['min_cluster'] = 'b'

scatter1 = ax.scatter(x = dataSet['x'], y = dataSet['y'], color = dataSet['color'])
scatter2 = ax.scatter(x = clusters['x'], y = clusters['y'], facecolor = 'w', edgecolor = clusters.index, alpha = 1)
plt.show()
plt.savefig('images/sampleFileName.png')

for i in range(len(dataSet)):
    dataSet.loc[i, 'color'] = clusters.index[i]  
plt.pause(0.1)

while(True):
    screenNumber+=1
    for i in range(len(clusters)):
        min_cluster = ''
        min_dist = 999999
        for k in range(len(clusters)):       
            if i != k:
                dist = np.sqrt((clusters.loc[clusters.index[i], 'x'] - clusters.loc[clusters.index[k],'x']) ** 2 + (clusters.loc[clusters.index[i], 'y'] - clusters.loc[clusters.index[k], 'y']) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    min_cluster = clusters.index[k]          
        clusters.loc[clusters.index[i],'min_cluster'] = min_cluster
    
    for i in range(len(clusters)):
        if clusters.index[i] == clusters.loc[clusters.loc[clusters.index[i],'min_cluster'], 'min_cluster']:
            new_clusters[clusters.index[i]] = {'x': (clusters.loc[clusters.index[i],'x'] + clusters.loc[clusters.loc[clusters.index[i],'min_cluster'], 'x']) /2,
                                         'y': (clusters.loc[clusters.index[i],'y'] + clusters.loc[clusters.loc[clusters.index[i],'min_cluster'], 'y']) /2
                                         }
            colorMap[clusters.index[i]] = clusters.loc[clusters.loc[clusters.index[i],'min_cluster']].name
        
        else:
            new_clusters[clusters.index[i]] = {'x': clusters.loc[clusters.index[i],'x'],
                                         'y': clusters.loc[clusters.index[i],'y']
                                        }
            
    clusters = pd.DataFrame(new_clusters).transpose().copy()
    new_clusters.clear()
    dropped_colors = clusters[clusters.duplicated(subset = ['x','y'], keep = 'first')]
    clusters.drop_duplicates(subset = ['x','y'], inplace = True)
       
    tempColorMap = {}
       
    for i in range(len(dropped_colors)):
        if dropped_colors.index[i] in colorMap:
            tempColorMap[dropped_colors.index[i]] = colorMap[dropped_colors.index[i]]
    
    colorMap = tempColorMap.copy()
    tempColorMap.clear()   
    dataSet['color'] = dataSet['color'].map(lambda x: colorMap[x] if x in colorMap else x)
    
    scatter2.set_offsets(np.c_[clusters['x'], clusters['y']])
    scatter2.set_edgecolors(clusters.index)
    
    scatter1.set_facecolors(dataSet['color'])
    scatter1.set_edgecolors(dataSet['color'])
    
    fig.canvas.draw_idle()
    plt.savefig('images/sampleFileName{}.png'.format(screenNumber))
    plt.pause(0.1)

    if len(clusters) == 3:
        break

files = os.listdir('images')
image_path = [os.path.join('images',file) for file in files]
images = []

for img in image_path:
    images.append(imageio.imread(img))
    
imageio.mimwrite('result/result.gif', images, fps = 2)

createDendogram(dataSet)

