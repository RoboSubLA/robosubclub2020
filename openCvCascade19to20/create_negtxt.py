import numpy as np
import os
import cv2

path = 'negatives'
    
for img in os.listdir(path):
    line = path+'/'+img+'\n'
    with open('bg.txt','a') as f:
        f.write(line)
