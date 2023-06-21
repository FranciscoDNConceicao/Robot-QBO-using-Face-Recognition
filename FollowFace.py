import cv2
import serial
import sys
from QboSay import TextToSpeech
import threading
import speech_recognition as sr
from QboListen import SpeechToText
sys.path.insert(0, '/opt/qbo/')
import time
from controller.QboController3 import Controller

Kpx = 1
Kpy = 1
Ksp = 40

Xmax = 725
Xmin = 290
Ymax = 550
Ymin = 420

## Initial Head position

Xcoor = 511
Ycoor = 450
Facedet = 0

## Time head wait turned
touch_wait = 2

no_face_tm = time.time()
face_det_tm = time.time()
touch_tm = 0
touch_samp = time.time()
qbo_touch = 0
touch_det = False
Listening = False
listen_thd = 0

Step_x = ([2, 5, 10])
Step_y = ([1, 3, 7])

def ServoHome(controller):
    global Xcoor, Ycoor, touch_tm

    Xcoor = 511
    Ycoor = 450
    controller.SetServo(1, Xcoor, 100)
    controller.SetServo(2, Ycoor, 100)
    touch_tm = time.time()

    return


def CamLeft(distance, speed, controller):  # To move left, we are provided a distance to move and a speed to move.
    global Xcoor, Xmin, touch_tm

    Xcoor = Xcoor - Kpx * distance

    if Xcoor < Xmin:
        Xcoor = Xmin

    controller.SetServo(1, Xcoor, Ksp * speed)
    touch_tm = time.time()

    return


def CamRight(distance, speed, controller):  # Same logic as above
    global Xcoor, Xmax, touch_tm

    Xcoor = Xcoor + Kpx * distance

    if Xcoor > Xmax:
        Xcoor = Xmax

    controller.SetServo(1, Xcoor, Ksp * speed)
    touch_tm = time.time()

    return


def CamDown(distance, speed, controller):  # Same logic as above
    global Ycoor, Ymax, touch_tm

    Ycoor = Ycoor + Kpy * distance

    if Ycoor > Ymax:
        Ycoor = Ymax

    # print "DOWN:",distance, Xcoor, Ycoor
    controller.SetServo(2, Ycoor, Ksp * speed)
    touch_tm = time.time()

    return


def CamUp(distance, speed, controller):  # Same logic as above
    global Ycoor, Ymin, touch_tm

    Ycoor = Ycoor - Kpy * distance

    if Ycoor < Ymin:
        Ycoor = Ymin

    # print "UP:",distance, Xcoor,Ycoor
    controller.SetServo(2, Ycoor, Ksp * speed)
    touch_tm = time.time()

    return

def PiFace():
    global Kpx, Kpt, Ksp, Xmax, Xmin, Ymax, Ymin, Xcoor, Ycoor, Facedet, touch_wait, no_face_tm, face_det_tm
    global face_det_tm, touch_tm, touch_samp, qbo_touch, touch_det, Listening, listen_thd, Step_x, Step_y 

    TextToSpeech("Quanto tempo é que o programa irá funcionar em minutos?")
    while True:
        temp = SpeechToText()
        TextToSpeech("Confirme por favor, o tempo estimado é de " + str(temp) + "  minutos ?")
        ConfName = SpeechToText()
        if ConfName == "sim":
            break
        elif ConfName == "Não":
            TextToSpeech("Por favor, informe o tempo novamente")
        else:
            TextToSpeech("Não entendi a confirmação, por favor informe o tempo novamente")
    
    if(temp == "um"):
        temp=1
    elif(temp == "dois"):
        temp=2
    else:
        temp = int(temp)
    tempoSeg = temp * 60
    tempo_inicial = time.time()

    

    ## Head X and Y angle limits


    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = '/dev/serial0'

    try:
        # Open serial port
        ser = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, rtscts=False, dsrdtr=False, timeout=0)
        print("Open serial port sucessfully.")
        print(ser.name)

    except:
        print ("Error opening serial port.")
        sys.exit()
    
    
    controller = Controller(ser)
    print(controller)
    controller.SetServo(1, Xcoor, 100)
    controller.SetServo(2, Ycoor, 100)
    controller.SetNoseColor(0)  # Off QBO nose brigth

    webcam = cv2.VideoCapture(0)  # Get ready to start getting images from the webcam
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # I have found this to be about the highest-
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # resolution you'll want to attempt on the pi
    webcam.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    frontalface = cv2.CascadeClassifier("/opt/qbo/haarcascades/haarcascade_frontalface_alt2.xml")  # frontal face pattern detection
    profileface = cv2.CascadeClassifier("/opt/qbo/haarcascades/haarcascade_profileface.xml")  # side face pattern detection

    face = [0, 0, 0, 0]  # This will hold the array that OpenCV returns when it finds a face: (makes a rectangle)
    Cface = [0, 0]  # Center of the face: a point calculated from the above variable
    lastface = 0  # int 1-3 used to speed up detection. The script is looking for a right profile face,-
    # a left profile face, or a frontal face; rather than searching for all three every time,-
    # it uses this variable to remember which is last saw: and looks for that again. If it-
    # doesn't find it, it's set back to zero and on the next loop it will search for all three.-
    # This basically tripples the detect time so long as the face hasn't moved much.

    time.sleep(1)  # Wait for them to start

    touch_tm = time.time()
    
    should_exit = False
    
    while True:
        tempo_decorrido = time.time() - tempo_inicial
        if tempo_decorrido >= tempoSeg:
            break 
        ret, frame = webcam.read()
        faceFound = False  # This variable is set to true if, on THIS loop a face has already been found
        
        
        if not faceFound:
            if lastface == 0 or lastface == 1:

                aframe = webcam.read()[1]  # there seems to be an issue in OpenCV or V4L or my webcam-
                aframe = webcam.read()[1]  # driver, I'm not sure which, but if you wait too long,
                aframe = webcam.read()[1]  # the webcam consistantly gets exactly five frames behind-
                fface = frontalface.detectMultiScale(aframe, 1.3, 4, (cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH), (60, 60))

                if fface != ():  # if we found a frontal face...
                    lastface = 1  # set lastface 1 (so next loop we will only look for a frontface)
                    for f in fface:  # f in fface is an array with a rectangle representing a face
                        faceFound = True
                        face = f

        if not faceFound:  # if we didnt find a face yet...

            if lastface == 0 or lastface == 2:  # only attempt it if we didn't find a face last loop or if-
                aframe = webcam.read()[1]  # THIS method was the one who found it last loop
                aframe = webcam.read()[1]
                aframe = webcam.read()[1]  # again we grab some frames, things may have gotten stale-
                pfacer = profileface.detectMultiScale(aframe, 1.3, 4, (cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH), (80, 80))

                if pfacer != ():  # if we found a profile face...
                    lastface = 2
                    for f in pfacer:
                        faceFound = True
                        face = f

        if not faceFound:  # if no face was found...-

            lastface = 0  # the next loop needs to know
            face = [0, 0, 0, 0]  # so that it doesn't think the face is still where it was last loop
            controller.SetNoseColor(0)  # Off QBO nose brigth

            if Facedet != 0:
                Facedet = 0
                no_face_tm = time.time()
                # print "No face.!"

            elif (time.time() - no_face_tm > 10):
                ServoHome(controller)
                Cface[0] = [0, 0]
                no_face_tm = time.time()
        else:
            x, y, w, h = face

            Cface = [(w / 2 + x), (h / 2 + y)]  # we are given an x,y corner point and a width and height, we need the center
            # print str(Cface[0]) + "," + str(Cface[1])
            
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            
            if Facedet == 0:

                if Listening == False:
                    controller.SetNoseColor(4)

                Facedet = 1
                face_det_tm = time.time()
                # print "Face detected.!"

            elif Listening == False & (time.time() - face_det_tm > 2):
                face_det_tm = time.time()

                if Listening == False:
                    controller.SetNoseColor(1)
                    Listening = True

            else:

                if Listening:
                    controller.SetNoseColor(1)  # Set QBO nose blue
                else:
                    controller.SetNoseColor(4)

            if touch_det == False:

                if Cface[0] > 190:
                    CamLeft(Step_x[0], 1, controller)
                if Cface[0] > 200:
                    CamLeft(Step_x[1], 2, controller)
                if Cface[0] > 210:
                    CamLeft(Step_x[2], 3, controller)

                if Cface[0] < 150:
                    CamRight(Step_x[0], 1, controller)
                if Cface[0] < 140:
                    CamRight(Step_x[1], 2, controller)
                if Cface[0] < 130:
                    CamRight(Step_x[2], 3, controller)

                if Cface[1] > 150:
                    CamDown(Step_y[0], 1, controller)
                if Cface[1] > 160:
                    CamDown(Step_y[1], 2, controller)
                if Cface[1] > 170:
                    CamDown(Step_y[2], 3, controller)

                if Cface[1] < 130:
                    CamUp(Step_y[0], 1, controller)
                if Cface[1] < 100:
                    CamUp(Step_y[1], 2, controller)
                if Cface[1] < 90:
                    CamUp(Step_y[2], 3, controller)
        
        cv2.imshow('Face Detection', frame)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    TextToSpeech("Acabou a duração, diga outra ordem")
    webcam.release()
    cv2.destroyAllWindows()


