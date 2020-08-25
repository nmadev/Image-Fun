from PIL import Image
from numpy import asarray
import numpy as np
import os
import gc

# merges two previously sorted lists
def merger(a, b):
    merged = []
    while (0 < len(a) and 0 < len(b)): 
        if aggregateValue(a[0]) >= aggregateValue(b[0]):
            merged.append(a[0])
            del a[0]
        else:
            merged.append(b[0])
            del b[0]
        
    for i in range(len(a)):
        merged.append(a[i])
    for i in range(len(b)):
        merged.append(b[i])
    del a
    del b
    return merged

# sorts rows based on brightness
def mergesort(rows):
    numRows = len(rows)
    split = numRows // 2
    if (numRows > 2):
        first = rows[:split]
        second = rows[split:]
        rows = merger(mergesort(first), mergesort(second))
    elif (numRows == 2):
        if (aggregateValue(rows[0]) > aggregateValue(rows[1])):
            return [rows[0], rows[1]]
        else:
            return [rows[1], rows[0]]
    return 0

# defines an aggregate value used for sorting row "brightness"
def aggregateValue(row):
    total = 0
    for pixel in row:
        total += sum(pixel)
    return total / len(row)

# taken a list representing the photo and rotates it 90 degrees CCW
def rotatePhoto(rows):
    rows = asarray(np.rot90(np.array(rows))).tolist()
    return 0

# sorts, rotates 90 degrees, then sorts again
    # NOTE: ONLY WORKS FOR SMALLER IMAGES (Memory problems when using larger photos)
def doubleSortRotate(rows):
    rows = rotatePhoto(mergesort(rows))
    rows =  rotatePhoto(mergesort(rows))
    return 0

def multiply(filter, rows):
    if type(filter) == 'int':
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                rows[i][j][filter] = 255
    else:
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                for k in range(len(rows[i][j])):
                    rows[i][j][k] = filter[i][j][k] / 255 * rows[i][j][k]
    return 0
            

#def reduceColor(rows):
    

# loads image as a multi-dimensional list
image = Image.open('Images\Daisies.jpg')

data = asarray(image).tolist()

lowPass = doubleSortRotate(data)
multiply(lowPass, data)
data = (np.array(data)).astype(np.uint8)

# creates image from the list and displays it
image2 = Image.fromarray(data)
image2.show()