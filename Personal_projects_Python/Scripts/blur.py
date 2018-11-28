# -*-coding: utf-8 -*-
from PIL import Image

def treatImage(filename, x1, y1, x2, y2, level):
    target = Image.open(filename)    
    data = target.getdata()
    width = target.size[0]  # horizontal pixel number
    length = target.size[1]  # vertiacl pixel number
    newData = []
    
    if x1 > width or x2 > width or y1 > length or y2 > length:
        print 'Wrong coordinates'
        return
    
    # init the new data
    for i in range(0, len(data)):
        newData.append(data[i])
    
    print 'Begin to treat the picture'
    for i in range(x1, x2, level):
        for j in range(y1, y2, level):
            listPixel = []
            for m in range(0, level):
                for n in range(0, level):
                    # print '**********************************'
                    # print i
                    # print j
                    # print m
                    # print n
                    # print (j + n - 1)*width + i + m
                    if ((j + n) <= y2) and ((i + m) <= x2):
                        listPixel.append(data[(j + n - 1)*width + i + m - 1])

            mergedPixel = mergePixel(listPixel)
            for m in range(0, level):
                for n in range(0, level):
                    if ((j + n) <= y2) and ((i + m) <= x2):
                        newData[(j + n - 1)*width + i + m - 1] = mergedPixel
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
    treatImage('1.png', 0, 00, 100, 150, 7)
    print 'All done!'
    
    
    
    