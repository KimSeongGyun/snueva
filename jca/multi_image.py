import cv2
import numpy as np
import copy
import math
import matplotlib.pyplot as plt


path = './sample_video/2.avi'
cap = cv2.VideoCapture(path)


#default red setting
#lower_red=np.array([0, 50, 50])             
#upper_red=np.array([5, 255, 255])

lower_red=np.array([0, 50, 50])             
upper_red=np.array([5, 255, 255])


kernel = np.ones((10,10), np.uint8)
is_first_frame = True
filter_not_set = True
buffer = []
center= [330,259]
angles = []
angles_sum = []

last_point = []

def getPixel(event, x, y, flags, param):
    global filter_not_set
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if filter_not_set:
            filter_not_set = False
            print("x : " + str(x) + " , y : " + str(y))
            print(hsv[y][x])
            print("filter set")
            global lower_red
            global upper_red
            lower_red=np.array([max(hsv[y][x][0]-3,0), max(hsv[y][x][1]-100,50), max(hsv[y][x][2]-100,50)])             
            upper_red=np.array([min(hsv[y][x][0]+3,255), min(hsv[y][x][1]+100,255), min(hsv[y][x][2]+100,255)])
        else:    
            global center
            center = [x,y]
            print("x : " + str(x) + " , y : " + str(y))
            print("center point set")


def angle(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    cos = inner_product/(len1*len2)
    if cos >= 1:
        cos = 1
    elif cos <= -1:
        cos = -1
    return abs(math.acos(cos)) * (180 / math.pi)

plt.ion()            
fig = plt.gcf()

plt.show()
fig.canvas.draw()

while(cap.isOpened()):    
    ret, frame = cap.read()
    img = cv2.GaussianBlur(frame,(5,5),0)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 
    
    if is_first_frame:
        is_first_frame = False
        r = int(np.sqrt(np.size(img))/100)
        cv2.imshow('image',img)
        cv2.setMouseCallback('image',getPixel)
        
    

        if cv2.waitKey(0) & 0xFF == ord('q'):   
            cv2.destroyAllWindows()    
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

    if length:
        for i in range(0, length):
            x = int(np.mean(points[i][:,0,0]))
            y = int(np.mean(points[i][:,0,1]))
            buffer.append([x,y])
            cv2.circle(img, (x, y),r,(0,255,0),-1)
            if len(last_point) == 0:
                last_point = [x,y]


            

            if(len(buffer)>=10):
                buffer.pop(0)
            for points in buffer:
                cv2.circle(img, (points[0], points[1]),int(r/2),(255,255,0),-1)
                cv2.line(img,(center[0],center[1]),(points[0],points[1]),(255,255,0),int(r/5))
                
            
        cv2.circle(img, (center[0], center[1]),int(r/2),(0,255,255),-1)
        
        angle_tmp = angle([x-center[0], y-center[1]],[last_point[0]-center[0], last_point[1]-center[1]])
        angles.append(angle_tmp)

        angles_sum.append(sum(angles))


        if(len(angles_sum)>=30):
            ##polyfit
            poly_y = (np.array(angles_sum))[20:]
            poly_x = np.arange(np.size(poly_y))/30.0
            coef = np.polyfit(poly_x,poly_y,2)
            ang_vel = np.sum((np.array(angles))[-10:]) * 3
            plt.title("Angular velocity : " + str(round(ang_vel/180.0*math.pi,3)) +"Rad/s", fontsize=30)
            #plt.title("Angular velocity : " + str(round(coef[0]/180.0*math.pi,3)) +"Rad/s", fontsize=30)
            ##
        ax = fig.add_subplot(111)
        ax.scatter(range(0,len(angles_sum)), angles_sum, color='darkgreen')
        ax.set_xlim(0, len(angles_sum))
        ax.set_ylim(0, angles_sum[-1] * 1.1)
        fig.canvas.draw()
        plt.pause(0.000000000001) 
        
        last_point = [x,y]
        #plt.show()
        #######

    cv2.imshow('g',img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
'''
while(cap.isOpened()):
    ret, frame = cap.read()
    
    
    
    


   
    
    cv2.imshow('frame',img)
'''