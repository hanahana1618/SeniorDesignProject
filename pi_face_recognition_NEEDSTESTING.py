# import the necessary packages
from imutils.video import VideoStream #video access
from imutils.video import FPS #frame counter
import numpy as np #lib that supports large multidimensional arrays and matrices
import face_recognition #recognize faces using deep learning
import argparse #read command line args
import imutils #allows for the 
import pickle #read and analyze encoded images
import time #implement delya
import cv2 #opencv lib
import RPi.GPIO as GPIO #GPIO access for LEDs

#LED PIN OUTPUT DECLARATION
#testing for face recon, green is face recognized and red is unrecognized
greenLed = 20
redLed = 21
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(greenLed, GPIO.OUT)
GPIO.setup(redLed, GPIO.OUT)

#LED INIT OFF
GPIO.output(redLed, GPIO.LOW)
ledRedOn = False
GPIO.output(greenLed, GPIO.LOW)
ledGreenOn = False
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
    help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
args = vars(ap.parse_args())


# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
#user specific data for face recognition
data = pickle.loads(open(args["encodings"], "rb").read())
#loads Haar cascade XML file for processing
#proloaded file for neural network recognition of what a face is
detector = cv2.CascadeClassifier(args["cascade"])
 
# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
 
# start the FPS counter
fps = FPS().start()

#code added by me
newArray=[]  #stores new Array to compare to old one
counter=0 #counter to count up tp three recognitions and then reset

# loop over frames from the video file stream
#draws square around face
while True:
    
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    
    # convert the input frame from (1) BGR to grayscale (for face
    # detection) and (2) from BGR to RGB (for face recognition)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 
    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30))
    
    # OpenCV returns bounding box coordinates in (x, y, w, h) order
    # but we need them in (top, right, bottom, left) order, so we
    # need to do a bit of reordering
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
 
    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown"
        
        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
 
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
 
            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)
           
        # update the list of names
        names.append(name)
        
        #TESTING CODE FOR LED IMPLEMENTATION
        #print(*names, sep=' ') #print entire list
        #print("\n\n")
        
        newArray.extend(names)
        #make sure the array does not get too long
        if len(newArray) > 10: 
            del newArray[0:3]
        #print("New array ")
        #print(*newArray, sep=' ')
        #print("\n")
        ##########
                
            
    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)
 
    # display the image to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    #########
    #testing for name shown three runs
    #print("This line executed")
    if counter>=5 and len(newArray)>=3:
        #print("Counter "+ str(counter)+"\n\n")
        for i,e in reversed(list(enumerate(newArray))):
            #print(str(i)+"\n\n")
            if newArray[i-1]==newArray[i-2] and newArray[i-1]==newArray[i-3]:
                #print("This went well "+ str(len(names)) + " current value of i " + str(i))
                if newArray[i-1]!="Unknown": #last three elements are the same
                    GPIO.output(redLed, GPIO.LOW)
                    GPIO.output(greenLed, GPIO.HIGH)
                    ledGreenOn = True
                    ledRedOn = False
                elif newArray[i-1]=="Unknown":
                    GPIO.output(redLed, GPIO.HIGH)
                    GPIO.output(greenLed, GPIO.LOW)
                    ledRedOn = True
                    ledGreenOn = False
            else:
                #print("Some element was not the same")
                GPIO.output(greenLed, GPIO.HIGH)
                GPIO.output(redLed, GPIO.LOW)
                ledGreenOn = True
                ledRedOn = False
        #reset counter to start over again
        counter=0
    ########
        
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
 
    counter+=1
    # update the FPS counter
    fps.update()



# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
GPIO.cleanup()
vs.stop()

