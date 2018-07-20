import cv2
import numpy as np
import copy

path = './sample/1.jpg'

def getPixel(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:    
        print("x : " + str(x))
        print("y : " + str(y))
img = cv2.imread(path)

cv2.imshow('image',img)
cv2.setMouseCallback('image',getPixel)
k = cv2.waitKey(0) & 0xFF
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()