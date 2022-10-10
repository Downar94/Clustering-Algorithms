import pandas as pd
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import imageio
import os

dataSet = {
    'x': [61,72,23,14,55,96,17,8,59,40,14,18,93,27,35,46,11,22,33,77,99],
    'y': [1,2,3,4,5,6,7,8,9,10,14,18,43,67,85,46,32,65,87,23,57]
    }
colorSet = ['r','g','b','w']
kmeans = {}
shortestDistances = pd.DataFrame({})
k = 3
oldKmeans = {}
screenNumber = 0

dataSet = pd.DataFrame(dataSet)

for i in range(k):
    kmeans[colorSet[i]] = {'x' : rd.random() * 100, 'y' : rd.random() * 100}
    
kmeans = pd.DataFrame(kmeans).transpose()

plt.ion()
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
xlim=(0,100)
ylim=(0,100)
scatter1 = ax.scatter(x = dataSet['x'], y = dataSet['y'], color = 'black')
scatter2 = ax.scatter(x = kmeans['x'], y = kmeans['y'], s = 150, color = [colorSet[i] for i in range(k)])
plt.show()
plt.savefig('images/sampleFileName.png')


while(True):
    screenNumber+=1
    for i in range(len(kmeans)):
        shortestDistances['dist_from_{}'.format(i)] = np.sqrt((dataSet['x'] - kmeans.iloc[i]['x']) ** 2 + (dataSet['y'] - kmeans.iloc[i]['y']) ** 2)
        dataSet['nearest_mean'] = shortestDistances.idxmin(axis=1).str.replace('dist_from_','').astype('int')
        dataSet['color'] = dataSet['nearest_mean'].map(lambda x: colorSet[x])


    oldKmeans = kmeans.copy()

    for i in range(len(kmeans)):
        kmeans.iloc[i]['x'] = dataSet.loc[dataSet['color'] == colorSet[i]]['x'].mean()
        kmeans.iloc[i]['y'] = dataSet.loc[dataSet['color'] == colorSet[i]]['y'].mean()
    
    scatter2.set_offsets(np.c_[kmeans['x'], kmeans['y']])
    
    scatter1.set_facecolors(dataSet['color'])
    scatter1.set_edgecolors(dataSet['color'])
    
    fig.canvas.draw_idle()
    plt.savefig('images/sampleFileName{}.png'.format(screenNumber))
    plt.pause(0.1)
    
    if kmeans.equals(oldKmeans):
        break
files = os.listdir('images')
image_path = [os.path.join('images',file) for file in files]
images = []

for img in image_path:
    images.append(imageio.imread(img))
    
imageio.mimwrite('result/result.gif', images, fps = 2)

