# -*- coding: UTF-8 -*-

from PIL import Image
import argparse

ascii_char = list("$@#%&WM8&WMZQOI|**<>(){},,..'''''''     ")

#命令行输入参数处理
parser = argparse.ArgumentParser()

parser.add_argument('file')     #输入文件
parser.add_argument('-o', '--output')   #输出文件
parser.add_argument('--width', type = int, default = 100) #输出字符画宽
parser.add_argument('--height', type = int, default = 50) #输出字符画高

#获取参数
args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

# 将256灰度映射到70个字符上
def get_char(r,b,g,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.3 * r + 0.6 * g + 0.1 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

if __name__ == '__main__':

    im = Image.open(IMG)
    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)

    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j,i))) # 加*表示不知道参数数量，输入的参数在一个元祖之中,这里因为getpixel返回三个数字，但是如果没有*那么python以为只有一个参数，所以返回多个参数的使用时都要加*
            # 一个*是元素，两个**表示参数以字典的形式出现，还可以通过for x,y in arg.items(): 来得到参数的名字(就是x[0]，y就是对应的参数值)来进行一些选择操作
        txt += '\n'
        
    print txt

    #字符画输出到文件
    # if OUTPUT:
        # with open(OUTPUT,'w') as f:
            # f.write(txt)
    # else:
        # with open("output.txt",'w') as f:
            # f.write(txt)