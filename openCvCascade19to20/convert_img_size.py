import PIL 
from PIL import Image
import os, sys

#path = "/home/gonzo/Desktop/cvCascade/bottleOg/"
#path = "/home/gonzo/Downloads/"
#path = "/home/gonzo/Desktop/cvCascade/imgs/bottleImg/"
path = "/home/gonzo/Desktop/imgNames/"

dirs = os.listdir( path )
base_width = 256

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            wpercent = (base_width/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            imResize = im.resize((base_width,hsize), Image.ANTIALIAS)
            imResize.save(f + ' resized.jpg', 'JPEG', quality=90)

resize()
