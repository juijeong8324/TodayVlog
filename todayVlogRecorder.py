import cv2 as cv
from datetime import datetime

# Setting for recorder
recorder = cv.VideoCapture(0) # Camera Index

# Frame : 640 X 480 -> 1280 X 720
recorder.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
recorder.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
width = int(recorder.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(recorder.get(cv.CAP_PROP_FRAME_HEIGHT))

# Get FPS and calculate the waiting time in millisecond
fps = recorder.get(cv.CAP_PROP_FPS)
wait_msec = int(1/fps*1000)

# Configure the recorder
format = '.avi'
fourcc = cv.VideoWriter_fourcc(*'XVID')
mode_play = False
isFlip = False

# Configure the fps
speed_table = [1/4, 1/2, 1, 1.5, 1.7]
speed_index = 2

if not recorder.isOpened():
   exit()
   
while True:
    valid, img = recorder.read() 
    if not valid:
        break        

    key = cv.waitKey(wait_msec)
    if key == 27: # Terminate if the given key is ESC 
        break
    elif key == ord(' '): # Change play mode 
        mode_play = not mode_play
        if mode_play is True: # If mode_play is true, start to record 
            fileName = datetime.today().strftime("%Y_%m_%d-%H_%M_%S")+ format # fileName
            out = cv.VideoWriter(fileName, fourcc, int(fps*speed_table[speed_index]), (width, height), True) 
        else: # stop to record
            out.release()
    elif key == ord('\t'): # Horizontal flip
        isFlip = not isFlip
        
    if isFlip is True:
        img = cv.flip(img, +1) # Althernative img = img[:, ::-1, :].copy()
        
    if mode_play: # Record Mode
        info = datetime.today().strftime("%Y_%m_%d / %H:%M:%S") # ex. 2024.03,11 / 02:03:04
        cv.putText(img, info, (10, 40), cv.FONT_HERSHEY_DUPLEX , 0.8, (255, 255, 255))
        cv.putText(img, "Record", (width-90, 40), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv.circle(img, (width-110, 30), 10, (0, 0, 255), -1)
        out.write(img) 
    else: # Preview Mode - Change FPS 
        if key == ord('>') or key == ord('.'):
            speed_index = min(speed_index+1, len(speed_table)-1)
        elif key == ord('<') or key == ord(','):
            speed_index = max(speed_index-1, 0)
        info = f'Speed: x{speed_table[speed_index]:.2g}'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
    
    cv.imshow('TodayVlog', img)

recorder.release()
cv.destroyAllWindows()
        