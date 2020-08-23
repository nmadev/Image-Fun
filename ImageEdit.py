from PIL import Image
from numpy import asarray
import numpy as np
import os

# merges two previously sorted lists
def merger(a, b):
    merged = []
    while (0 < len(a) and 0 < len(b)): 
        if aggregateValue(a[0]) >= aggregateValue(b[0]):
            merged.append(a[0])
            a.pop(0)
        else:
            merged.append(b[0])
            b.pop(0)
        
    for i in range(len(a)):
        merged.append(a[i])
    for i in range(len(b)):
        merged.append(b[i])
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
    return rows

# defines an aggregate value used for sorting row "brightness"
def aggregateValue(row):
    total = 0
    for pixel in row:
        total += sum(pixel)
    return total / len(row)

# taken a list representing the photo and rotates it 90 degrees
def rotatePhoto(rows):
    rotated = np.rot90(np.array(rows))
    return asarray(rotated).tolist()

def doubleSortRotate(rows):
    return mergesort(rotatePhoto(mergesort(rows)))

# testing array
testArray = [[[5, 6], [9, 8], [10, 103]],
            [[3, 4], [1, 2], [12, 230]],
            [[6, 2], [0, 0], [43, 65]],
            [[6, 6], [1, 0], [33, 85]],
            [[6, 3], [2, 0], [23, 250]],
            [[6, 5], [3, 0], [13, 55]]]


# loads image as a multi-dimensional list
image = Image.open('Images\Silliman.jpg')
dataSort = asarray(image).tolist()

# applies brightness sorting to the image and converts it to an readable format
newDataSort = np.array(doubleSortRotate(dataSort))
convertableData = (newDataSort).astype(np.uint8)

# creates image from the list and displays it
image2 = Image.fromarray(convertableData)
image2.show()