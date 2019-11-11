####################### STACKING USING THE FUNCTION #####################

import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
    
while True:
    success, img = cap.read()
    kernel = np.ones((5,5),np.uint8)
    print(kernel)
    #path = "Resources/lena.png"
    #img =  cv2.imread(path)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)
    imgCanny = cv2.Canny(imgBlur,100,200)
    imgDilation = cv2.dilate(imgCanny,kernel , iterations = 2)
    imgEroded = cv2.erode(imgDilation,kernel,iterations=2)

    #imgBlank = np.zeros((200,200),np.uint8)
    StackedImages = stackImages(0.6,([img,imgGray,imgBlur],
                                   [imgCanny,imgDilation,imgEroded]))
    cv2.imshow("Staked Images", StackedImages)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


################### Stacking images without Function ################
# import cv2
# import numpy as np
# img1 = cv2.imread('../Resources/lena.png',0)
# img2 = cv2.imread('../Resources/land.jpg')
# print(img1.shape)
# print(img2.shape)
# img1 = cv2.resize(img1, (0, 0), None, 0.5, 0.5)
# img2 = cv2.resize(img2, (0, 0), None, 0.5, 0.5)
# img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
# hor= np.hstack((img1, img2))
# ver = np.vstack((img1, img2))
# cv2.imshow('Vertical', ver)
# cv2.imshow('Horizontal', hor)
# cv2.waitKey(0)
