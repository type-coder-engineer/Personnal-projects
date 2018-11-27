# -*-coding: utf-8 -*-
from PIL import Image

def treatImage(filename, x1, y1, x2, y2, level):
    target = Image.open(filename)    
    data = target.getdata()
    width = target.size[0]
    length = target.size[1]
    newData = []
    
    if x1 > width or x2 > width or y1 > length or y2 > length:
        print 'Wrong coordinates'
        return
    
    # init the new data
    for i in range(0, len(data)):
        newData.append(data[i])
    
    print 'Begin to treat the picture'
    count = 1
    for i in range(x1, x2, level):
        for j in range(y1, y2, level):
            listPixel = []
            for m in range(0, level):
                for n in range(0, level):
                    # print count
                    # print m
                    # print n
                    # print (j + n)*width + i + m
                    # print data[(j + n)*width + i + m]
                    listPixel.append(data[(j + n)*width + i + m])
                    count += 1
            mergedPixel = mergePixel(listPixel)
            # print mergedPixel
            # print '**********************************'
            for m in range(0, level):
                for n in range(0, level):
                    newData[(j + n)*width + i + m] = mergedPixel
    print 'Finish process'
    
    newFilename = 'new_' + filename;
    target.putdata(newData)
    target.save(newFilename)
    
# calculate the merged pixel
def mergePixel(listPixel):
    R = 0
    G = 0
    B = 0
    A = 0
    length = len(listPixel)
   
    for i in range(length):
        # print listPixel[i]
        R += listPixel[i][0]
        G += listPixel[i][1]
        B += listPixel[i][2]
        A += listPixel[i][3]
    R = R/length
    G = G/length
    B = B/length
    A = A/length
    return (R, G, B, A)


if __name__ == "__main__":
    treatImage('1.png', 10, 10, 100, 100, 8)
    print 'All done!'
    
    
    
    