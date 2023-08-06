#! /Users/michael/anaconda3/bin/python3

from PIL import Image
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file') # input file
    parser.add_argument('--width', type=int, default=80) # 字符画宽度
    parser.add_argument('--height', type=int, default=40) # 字符画高度

    args = parser.parse_args() # 获取参数
    image = args.file
    width = args.width
    height = args.height

    chs = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    ascii_char = list(chs)

    def get_char(r, g, b, alpha=256): 
        if alpha == 0:
            return ' '
        length = len(ascii_char)
        grey = int(0.2126*r + 0.7152*g + 0.0722*b)
        unit = (257)/length
        return ascii_char[int(grey/unit)]


    im = Image.open(image)
    im = im.resize((width, height), Image.Resampling.LANCZOS)

    txt = ''
    for i in range(height):
        for j in range(width):
            txt += get_char(*im.getpixel((j, i)))
        txt += '\n'

    print(txt)
    
if __name__ == "__main__":
    main()