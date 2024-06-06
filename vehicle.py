import cv2
import numpy as np

#Web camera
cap = cv2.VideoCapture('video.mp4') #captures and registers the given video.

min_width_react = 80    #min width rectangle
min_height_react = 80   #min height rectangle

count_line_position = 550

#Initialise Substractor
algo = cv2.bgsegm.createBackgroundSubtractorMOG()   #separates the background with foreground


while True:
    ret,frame1=cap.read()   #returns a bool value telling if the video is read correctly
    grey = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY) #converts the video from RGB to Black n White
    blur = cv2.GaussianBlur(grey, (3,3),5)  #smooths the image by averaging the pixel values based on a set of weights, which are defined by a Gaussian filter
    #applying on each frame
    img_sub = algo.apply(blur)  #applies the gaussian blur filter
    dilat = cv2.dilate(img_sub, np.ones((5,5))) #result in a larger image with more detail in the edges and corners
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))    #applies dilation
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel) #applies erosion operation on a close kernel
    dilatadat = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
                #function to    #parameter,  #specifies     #array of pixel values
                #perform mor    #img is      #type of 
                #phological     #working on  #morphology
                #operations
    counterShape, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    #returns a vector of contour points in the image

    cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (255,127,0), 3)    #the gunction is used to draw a line on the image
            #previously #initial position       #final position of           #color       #thickness
            #set                                #drawing a line
    for(i, c) in enumerate(counterShape):   #
        (x, y, w, h) = cv2.boundingRect(c)
        validate_counter = (w>=min_width_react) and (h>=min_height_react)
        if not validate_counter:
            continue    
        cv2.rectangle(frame1, (x,y),(x+w,y+h),(0,0,255),2)


    # cv2.imshow('Video - Detected', dilatada)
    cv2.imshow('Video - Original', frame1)
    if cv2.waitKey(1) == 13:
        break
cv2.destroyAllWindows()
cap.release()