# -*-coding: utf-8 -*-
from PIL import Image

def treatImageByCenter(filename, x, y, width, length, level):
    x1 = x - width/2
    y1 = y - length/2
    x2 = x1 + width
    y2 = y1 + length
    treatImageByTwoPoint(filename, x1, y1, x2, y2, level)

def treatImageByTwoPoint(filename, x1, y1, x2, y2, level):
    target = Image.open(filename)    
    data = target.getdata()
    width = target.size[0]  # horizontal pixel number
    length = target.size[1]  # vertiacl pixel number
    newData = []
        
    if x1 > width or x2 > width or y1 > length or y2 > length or x1 >= x2 or y1 >= y2:
        print 'Wrong coordinates'
        return
        
    if (x2 - x1)*(y2 - y1)/level >= 50000:
        print 'The blur level is too little, the effect will not be very evident'
    elif (x2 - x1)*(y2 - y1)/level <= 2000: 
        print 'The blur level is too big, the effect will not be very good'
        
    # init the new data
    print 'Begin to init the new picture'
    for i in range(0, len(data)):
        newData.append(data[i])
    print 'Finish init the new data'
    
    print 'Begin to treat the picture'
    for i in range(x1, x2, level):
        for j in range(y1, y2, level):
            listPixel = []
            for m in range(0, level):
                for n in range(0, level):
                    if ((j + n) <= y2) and ((i + m) <= x2):  # to avoid the problem of out of range
                        listPixel.append(data[(j + n - 1)*width + i + m - 1])
                        
            if (len(listPixel)):
                mergedPixel = mergePixel(listPixel)
                for m in range(0, level):
                    for n in range(0, level):
                        if ((j + n) <= y2) and ((i + m) <= x2):
                            newData[(j + n - 1)*width + i + m - 1] = mergedPixel
    print 'Finish the treat process'
    
    newFilename = 'new_' + filename
    target.putdata(newData)
    target.save(newFilename)
    print 'All done!'
    
# calculate the merged pixel
def mergePixel(listPixel):
    if (len(listPixel[0]) == 4):
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
        
    elif (len(listPixel[0]) == 3):  # no data of A(transparence), ex: jpg
        R = 0
        G = 0
        B = 0
        length = len(listPixel)
        
        for i in range(length):
            R += listPixel[i][0]
            G += listPixel[i][1]
            B += listPixel[i][2]
        R = R/length
        G = G/length
        B = B/length
        
        return (R, G, B)
    else:
        print 'Wrong with the pixel format'
        return (0, 0, 0)

if __name__ == "__main__":
    # treatImageByTwoPoint('test2.jpg', 4000, 3000, 5000, 4000, 100)
    treatImageByCenter('test2.jpg', 4000, 3000, 1000, 1000, 100)
    
    
    
    