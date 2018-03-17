# -*- coding: utf-8 -*-
from PIL import Image

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length=len(ascii_char)
    gray = int(0.2126*r + 0.7152*g + 0.0722*b)

    unit = (256.0+1)/length
    return ascii_char[int(gray/unit)]    #灰度值小的用前面的符号，大的用后面的符号




if __name__ =='__main__':
    im = Image.open('shi.png')
    im = im.resize((100,100), Image.NEAREST)

    txt = ""

    for i in range(100):
        for j in range(100):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'

    f=open('text.txt','w')
    f.write(txt)
    f.close()






