import cv2
import numpy as np
import copy

path = './sample_video/1.avi'
cap = cv2.VideoCapture(path)


#default red setting
#lower_red=np.array([0, 50, 50])             
#upper_red=np.array([5, 255, 255])

lower_red=np.array([0, 50, 50])             
upper_red=np.array([5, 255, 255])


kernel = np.ones((10,10), np.uint8)
is_first_frame = True

def getPixel(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:    
        print("x : " + str(x) + " , y : " + str(y))
        print(hsv[y][x])
        print("filter set")
        global lower_red
        global upper_red
        lower_red=np.array([max(hsv[y][x][0]-3,0), max(hsv[y][x][1]-100,50), max(hsv[y][x][2]-100,50)])             
        upper_red=np.array([min(hsv[y][x][0]+3,255), min(hsv[y][x][1]+100,255), min(hsv[y][x][2]+100,255)])

while(cap.isOpened()):    
    ret, frame = cap.read()
    img = cv2.GaussianBlur(frame,(5,5),0)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 
    
    if is_first_frame:
        is_first_frame = False
        r = int(np.sqrt(np.size(img))/100)
        cv2.imshow('image',img)
        cv2.setMouseCallback('image',getPixel)
        k = cv2.waitKey(0) & 0xFF
        if k == 27:         # wait for ESC key to exit   
            continue

    mask_red=cv2.inRange(hsv,lower_red,upper_red)
    res_red=cv2.bitwise_and(img,img,mask=mask_red)
    img_dilation = cv2.dilate(mask_red, kernel, iterations=1)
    img_erosion = cv2.erode(img_dilation, kernel, iterations=1)


    imgray = img_erosion
    ret,thresh = cv2.threshold(imgray,10,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours_ = []

    #reject small contour areas
    for c in contours:
        if cv2.contourArea(c) >= 250:
            contours_.append(c)
    length = len(contours_)
    cv2.drawContours(img, contours_, -1, (0,255,0), 3)

    points = np.array(contours_)
    center = []
    if length:
        for i in range(0, length):
            x = int(np.mean(points[i][:,0,0]))
            y = int(np.mean(points[i][:,0,1]))
            cv2.circle(img, (x, y),r,(0,255,0),-1)

    cv2.imshow('g',img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
'''
while(cap.isOpened()):
    ret, frame = cap.read()
    
    
    
    


   
    
    cv2.imshow('frame',img)
'''