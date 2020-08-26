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

# taken a list representing the photo and rotates it 90 degrees CCW
def rotatePhoto(rows):
    return asarray(np.rot90(np.array(rows))).tolist()

# sorts, rotates 90 degrees, then sorts again
    # NOTE: ONLY WORKS FOR SMALLER IMAGES (Memory problems when using larger photos)
def doubleSortRotate(rows):
    return rotatePhoto(mergesort(rotatePhoto(mergesort(rows))))

# multiplies each color value of each pixel by 
def multiply(filter, rows):
    if (isinstance(filter, int)):
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                rows[i][j][filter] = 255
    else:
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                for k in range(len(rows[i][j])):
                    rows[i][j][k] = filter[i][j][k] / 255 * rows[i][j][k]
    return rows
            
# transforms each pixel into either red, green, or blue, depending on which color was most present in the original picture 
def maxrgb(rows):
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            brightest = (rows[i][j]).index(max(rows[i][j]))
            for k in range(len(rows[i][j])):
                if k == brightest: 
                    rows[i][j][k] = 255
                else:
                    rows[i][j][k] = 0
    return rows
    
# blurs the photo with a given blur radius (not very efficient but it works so better for small images) 
def blur(radius, rows):
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            avePixel = [0, 0, 0]
            count = 0
            for n in range(-1 * radius, radius + 1):
                for m in range(-1 * radius, radius + 1):
                    if i + n in range(len(rows)) and j + m in range(len(rows[0])):
                        avePixel[0] += rows[i + n][j + m][0]
                        avePixel[1] += rows[i + n][j + m][1]
                        avePixel[2] += rows[i + n][j + m][2]
                        count += 1
            avePixel[0] /= count 
            avePixel[1] /= count 
            avePixel[2] /= count 
            rows[i][j] = avePixel
    return rows

# changes each pixel into the average RGB value of that pixel to convert the photo to black and white
def bw(rows):
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = (rows[i][j][0] + rows[i][j][1] + rows[i][j][2])/3
    return rows

# takes a list representing the image and puts it in a format the PIL can read to an image
def toImage(rows):
    return Image.fromarray((np.array(rows)).astype(np.uint8))

folder = 'TestImages'
directory = os.fsencode(folder)

# iterate through each photo in a given folder
for file in os.listdir(directory):
    filepath = os.fsdecode(file)
    if filepath.endswith(".jpg"):
        path = folder + '/' + filepath
        originalImage = Image.open(path)
        fileSize = os.stat(path).st_size
        # makes a folder based on the image name that all manipulated photos are saved to
        os.mkdir(folder + '/' + filepath[:-4])
        # reads the image as a numpy array and converts to a list, then saves the image
            # repeated for every method to generate the original image
        dataCopy = asarray(originalImage).tolist()
        newImage = toImage(mergesort(dataCopy))
        newImage.save(folder + '/' + filepath[:-4] + '/' + filepath[:-4] + 'Merge.jpg', "JPEG")
        print (filepath[:-4] + " mergesort finished")

        dataCopy = asarray(originalImage).tolist()
        newImage = toImage(maxrgb(dataCopy))
        newImage.save(folder + '/' + filepath[:-4] + '/' + filepath[:-4] + 'madRGB.jpg', "JPEG")
        print (filepath[:-4] + " maxRGB finished")

        dataCopy = asarray(originalImage).tolist()
        newImage = toImage(bw(dataCopy))
        newImage.save(folder + '/' + filepath[:-4] + '/' + filepath[:-4] + 'BW.jpg', "JPEG")
        print (filepath[:-4] + " black and white finished")

        dataCopy = asarray(originalImage).tolist()
        newImage = toImage(multiply(0, dataCopy))
        newImage.save(folder + '/' + filepath[:-4] + '/' + filepath[:-4] + 'RED.jpg', "JPEG")
        print (filepath[:-4] + " RED finished")
        dataCopy = asarray(originalImage).tolist()
        newImage = toImage(multiply(1, dataCopy))
        newImage.save(folder + '/' + filepath[:-4] + '/' + filepath[:-4] + 'GREEN.jpg', "JPEG")
        print (filepath[:-4] + " GREEN finished")
        dataCopy = asarray(originalImage).tolist()
        newImage = toImage(multiply(2, dataCopy))
        newImage.save(folder + '/' + filepath[:-4] + '/' + filepath[:-4] + 'BLUE.jpg', "JPEG")
        print (filepath[:-4] + " BLUE finished")

        # blur and double sort are very time intensive so we only limit this to smaller photos
        if fileSize < 350000 or len(dataCopy) < 1500:

            dataCopy = asarray(originalImage).tolist()
            newImage = toImage(blur(3, dataCopy))
            newImage.save(folder + '/' + filepath[:-4] + '/' + filepath[:-4] + 'blur3.jpg', "JPEG")
            print (filepath[:-4] + " blur radius 3 finished")

            dataCopy = asarray(originalImage).tolist()
            lowpass = asarray(originalImage).tolist()
            lowpass = doubleSortRotate(lowpass)
            newImage = toImage(lowpass)
            newImage.save(folder + '/' + filepath[:-4] + '/' + filepath[:-4] + 'Merge.jpg', "JPEG")
            print (filepath[:-4] + " merge finished")
            newImage = toImage(multiply(lowpass, dataCopy))
            newImage.save(folder + '/' + filepath[:-4] + '/' + filepath[:-4] + 'MergeFilter.jpg', "JPEG")
            print (filepath[:-4] + " merge filter finished")

        print ("FINISHED: " + filepath[:-4])

print ("IMAGE MANIPULATION FINISHED")