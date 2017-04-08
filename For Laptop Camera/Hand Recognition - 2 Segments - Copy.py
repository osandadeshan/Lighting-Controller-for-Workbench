import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)
while( cap.isOpened() ) :
    ret,img = cap.read()



    if(1):
        cv2.rectangle(img,(350,600),(0,0),(0,0,255),0)    #(x-end,y-end),(x-start,y-start),(B,G,R)
        crop_img = img[0:600,0:350]

        gray = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(35,35),0)
        ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  
        _,contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        drawing = np.zeros(crop_img.shape,np.uint8)

        max_area=0
   
        for i in range(len(contours)):

            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
        cnt=contours[ci]
        hull = cv2.convexHull(cnt)
        moments = cv2.moments(cnt)
        
        if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00']) # cy = M01/M00
              
        centr=(cx,cy)       
        cv2.circle(crop_img,centr,5,[0,0,255],2)       
        cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 

        cv2.drawContours(drawing,[hull],0,(0,0,255),2) 
          
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)
        count_defects = 0
        if(1):
               defects = cv2.convexityDefects(cnt,hull)
               mind=0
               maxd=0
               for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end  = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    dist = cv2.pointPolygonTest(cnt,centr,True)
                    cv2.line(crop_img,start,end,[0,255,0],2)
                    
                    cv2.circle(crop_img,far,5,[0,0,255],-1)
                    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                    angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                    if angle <= 90:
                         count_defects += 1
               print("image 1",i)
               if count_defects == 1:
                    cv2.putText(crop_img,"Searching", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
               if count_defects >1 and i>2:
                    cv2.putText(crop_img,"HAND 1", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
               i=0
        cv2.imshow('output1',drawing)
        cv2.imshow('input',img)
        cv2.imshow('1', crop_img)        
   
   
   
   
   
   
   
   
   
   
   
   
   
    k = cv2.waitKey(10)
    if k == 27:
        break
