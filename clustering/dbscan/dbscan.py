import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import numpy as np
import string
import imageio
import os

dataSet = {
    'x': [61,72,23,14,55,96,17,8,59,40,14,18,93,27,35,46,11,22,33,77,99],
    'y': [1,2,3,4,5,6,7,8,9,10,14,18,43,67,85,46,32,65,87,23,57]
    }
dataSet['visited'] = False
dataSet['unvisited'] = True
dataSet['cluster_label'] = 'black'
epsilon = 15
minPoints = 1
clusters = {}
temp_cluster_points = []
cluster_points = []
flag = True
screenNumber = 0

dataSet = pd.DataFrame(dataSet)

plt.ion()
fig = plt.figure(figsize=(6,6))
ax = plt.axes([0.1, 0.1, 0.8, 0.8])
xlim=(0,100)
ylim=(0,100)
scatter = ax.scatter(x = dataSet['x'], y = dataSet['y'], color = 'k')
plt.show()
plt.savefig('images/sampleFileName.png')

while flag == True:
    color = '#{}'.format(''.join(rd.choice(string.digits) for _ in range(6)))
    for i in range(len(dataSet)):
        flag = False
        cluster_points.clear()  
        if i != len(dataSet) - 1:
            counter = i + 1
        else:
            counter = 0
        while(counter != i):
            if(np.sqrt((dataSet.iloc[i]['x'] - dataSet.iloc[counter]['x']) ** 2 + (dataSet.iloc[i]['y'] - dataSet.iloc[counter]['y']) ** 2) <= epsilon):
                cluster_points.append(counter)
            counter += 1
            if counter == len(dataSet):
                counter = 0
        if len(cluster_points) >= minPoints and dataSet.loc[i,'visited'] == False:
            flag = True
            dataSet.loc[i,'visited'] = True
            dataSet.loc[i,'unvisited'] = False
            dataSet.loc[i,'cluster_label'] = color
            dataSet.loc[cluster_points,'cluster_label'] = color
            break
    while len(cluster_points) != 0:
        i = 0
        counter = 0
        temp_cluster_points.clear()
        dataSet.loc[cluster_points[i],'visited'] = True
        dataSet.loc[cluster_points[i],'unvisited'] = False
        for k in range(len(dataSet)):
            if k == cluster_points[i]:
                continue
            else:
                if(np.sqrt((dataSet.loc[cluster_points[i],'x'] - dataSet.loc[k, 'x']) ** 2 + (dataSet.loc[cluster_points[i],'y'] - dataSet.loc[k, 'y']) ** 2) <= epsilon):
                    counter += 1
                    if k not in cluster_points and dataSet.loc[k,'visited'] == False:
                        temp_cluster_points.append(k)
        if counter >= minPoints:
            dataSet.loc[temp_cluster_points,'cluster_label'] = color
            cluster_points.extend(temp_cluster_points)
        cluster_points.pop(i)
        
        scatter.set_facecolors(dataSet['cluster_label'])
        scatter.set_edgecolors(dataSet['cluster_label'])
        fig.canvas.draw_idle()
        plt.savefig('images/sampleFileName{}.png'.format(screenNumber))
        plt.pause(0.1)
        screenNumber += 1

files = os.listdir('images')
image_path = [os.path.join('images',file) for file in files]
images = []

for img in image_path:
    images.append(imageio.imread(img))
    
imageio.mimwrite('result/result.gif', images, fps = 2)