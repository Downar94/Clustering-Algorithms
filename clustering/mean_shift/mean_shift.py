import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import numpy as np
import math as math
import string
import imageio
import os

dataSet = {
    'x': [61,72,23,14,55,96,17,8,59,40,14,18,93,27,35,46,11,22,33,77,99],
    'y': [1,2,3,4,5,6,7,8,9,10,14,18,43,67,85,46,32,65,87,23,57]
    }
dataSet['color'] = 'black'
colorSet = []
clusters = {}
k = 10
colorTable = []
betweenXY = False
screenNumber = 0

for i in range(k):
    colorSet.append('#{}'.format(''.join(rd.choice(string.digits) for _ in range(6))))
    
dataSet = pd.DataFrame(dataSet)

for i in range(k):
    clusters[colorSet[i]] = {'x': int(round(rd.random() * 100)),
                             'y': int(round(rd.random() * 100)),
                             'r': 20,
                             'count': 0
                            }
clusters = pd.DataFrame(clusters).transpose()

plt.ion()
fig = plt.figure(figsize=(6,6))
ax = plt.axes([0.1, 0.1, 0.8, 0.8], xlim=(0,100), ylim=(0,100))
points_whole_ax = 6 * 0.8 * 72 
points_radius = 2 * clusters['r'] / 100 * points_whole_ax
scatter1 = ax.scatter(x = dataSet['x'], y = dataSet['y'], color = 'r')
scatter2 = ax.scatter(x = clusters['x'], y = clusters['y'], s = points_radius**2, color = 'k', alpha = 0.1)
plt.show()
plt.savefig('images/sampleFileName.png')

for i in range(len(clusters)):
    dataSet['label_{}'.format(colorSet[i])] = False
    for angle in range(360):
        xprim = clusters.iloc[i]['x'] + clusters.iloc[i]['r'] * math.sin((angle * math.pi) /180)
        yprim = clusters.iloc[i]['y'] + clusters.iloc[i]['r'] * math.cos((angle * math.pi) /180)
        betweenX = dataSet['x'].between(clusters.iloc[i]['x'], xprim) | dataSet['x'].between(xprim, clusters.iloc[i]['x'])
        betweenY = dataSet['y'].between(clusters.iloc[i]['y'], yprim) | dataSet['y'].between(yprim, clusters.iloc[i]['y'])
        betweenXY = betweenX & betweenY
        dataSet.loc[betweenXY,['label_{}'.format(colorSet[i])]] = True
        clusters.iloc[i]['count'] = len(dataSet[dataSet['label_{}'.format(colorSet[i])]])

        

clusters.drop(clusters[(clusters['count'] == 0)].index, inplace = True)

scatter2.set_offsets(np.c_[clusters['x'], clusters['y']])
fig.canvas.draw_idle()
plt.savefig('images/sampleFileName{}.png'.format(screenNumber))
screenNumber += 1

while(True):
    for i in range(len(clusters)):
        dataSet['label_{}'.format(colorSet[i])] = False
        for angle in range(360):
            xprim = clusters.iloc[i]['x'] + clusters.iloc[i]['r'] * math.sin((angle * math.pi) /180)
            yprim = clusters.iloc[i]['y'] + clusters.iloc[i]['r'] * math.cos((angle * math.pi) /180)
            betweenX = dataSet['x'].between(clusters.iloc[i]['x'], xprim) | dataSet['x'].between(xprim, clusters.iloc[i]['x'])
            betweenY = dataSet['y'].between(clusters.iloc[i]['y'], yprim) | dataSet['y'].between(yprim, clusters.iloc[i]['y'])
            betweenXY = betweenX & betweenY

            dataSet.loc[betweenXY,['label_{}'.format(colorSet[i])]] = True
            clusters.iloc[i]['count'] = len(dataSet[dataSet['label_{}'.format(colorSet[i])]])
               
            

    oldClusters = clusters.copy()
    for i in range(len(clusters)):
        clusters.iloc[i]['x'] = dataSet.loc[dataSet['label_{}'.format(colorSet[i])],'x'].mean()
        clusters.iloc[i]['y'] = dataSet.loc[dataSet['label_{}'.format(colorSet[i])],'y'].mean()
    if(clusters.equals(oldClusters)):
        break
clusters.drop_duplicates(subset = ['x','y'], inplace = True)

scatter2.set_offsets(np.c_[clusters['x'], clusters['y']])
fig.canvas.draw_idle()
plt.savefig('images/sampleFileName{}.png'.format(screenNumber))
screenNumber += 1

newDataSetColumns = clusters.index.tolist()
for i in range(len(newDataSetColumns)):
    newDataSetColumns[i] = 'label_{}'.format(newDataSetColumns[i])
newDataSetColumns.append('x')
newDataSetColumns.append('y')

dataSet.drop(dataSet.columns.difference(newDataSetColumns), 1, inplace=True)


for i in range(len(dataSet)):
    commonPointsLabels = []
    commonPointsLabels.clear()
    for k in range(len(clusters)):
        if(dataSet.loc[i,'label_{}'.format(clusters.index[k])]):
            commonPointsLabels.append(clusters.index[k])
    if len(commonPointsLabels) >= 1:
        maximum = 'label_{}'.format(clusters.loc[commonPointsLabels]['count'].idxmax(axis = 0))
        dataSet.loc[i, dataSet.columns.difference([maximum,'x','y'])] = False
        

dataSet['color'] = 'y'
for k in range(len(clusters)):
    dataSet.loc[dataSet['label_{}'.format(clusters.index[k])],'color'] = clusters.index[k]


scatter2.set_offsets(np.c_[clusters['x'], clusters['y']])
scatter1.set_facecolors(dataSet['color'])
scatter1.set_edgecolors(dataSet['color'])
fig.canvas.draw_idle()
plt.savefig('images/sampleFileName{}.png'.format(screenNumber))
screenNumber += 1

scatter2.remove()
fig.canvas.draw_idle()
plt.savefig('images/sampleFileName{}.png'.format(screenNumber))

files = os.listdir('images')
image_path = [os.path.join('images',file) for file in files]
images = []

for img in image_path:
    images.append(imageio.imread(img))
    
imageio.mimwrite('result/result.gif', images, fps = 2)

    



