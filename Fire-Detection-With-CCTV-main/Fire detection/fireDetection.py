import cv2         # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib
from plyer import notification

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml') # To access xml file which includes positive and negative images of fire. (Trained images)
                                                                         # File is also provided with the code.

vid = cv2.VideoCapture(0) # To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attahed camera
runOnce = True # created boolean

Alarm_Status = False
sms_Status = False

def notify_firealert():
    notification.notify(
        title = "fire Alert... !!!",
        message="In CCTV camera 0 is under fire...",
        timeout =60

    )
def play_alarm_sound_function(): # defined function to play alarm post fire detection using threading
    playsound.playsound('fire_alarm.mp3',True) # to play alarm # mp3 audio file is also provided with the code.
    print("Fire alarm end") # to print in consol

def send_mail_function(): # defined function to send mail post fire detection using threading
    
    recipientmail = "add recipients mail" # recipients mail
    recipientmail = recipientmail.lower() # To lower case mail
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("add senders mail", 'add senders password') # Senders mail ID and password
        server.sendmail('add recipients mail', recipientmail, "Warning fire accident has been reported") # recipients mail with mail message
        print("Alert mail sent sucesfully to {}".format(recipientmail)) # to print in consol to whome mail is sent
        server.close() ## To close server
        
    except Exception as e:
        print(e) # To print error if any
		
while(True):
    
    ret, frame = vid.read() # Value in ret is True # To read video frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # To convert frame into gray color

    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) # to provide frame resolution

    ## to highlight fire with square 
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0))

        # font
        font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
        org = (50, 50)
  
# fontScale
        fontScale = 1
   
# Blue color in BGR
        color = (238, 75, 43)
  
# Line thickness of 2 px
        thickness = 2
   
# Using cv2.putText() method
        image = cv2.putText(frame, 'Fire', org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
        #cv2.putText(frame,'Fire',(50,50),cv2.FONT_HERSHEY_SIMPLEX,(255, 0, 0))
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        if Alarm_Status == False:
            print("Fire alarm initiated")
            threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread
            Alarm_Status = True

        if runOnce == False:
            print("Mail send initiated")
            threading.Thread(target=notify_firealert).start() # To call alarm thread
            runOnce = True
        
        if sms_Status == False:
            from twilio.rest import Client
            account_sid = "ACdb47011b46e1f9b7aff33661dba5a4e8"
            auth_token = "03f99e1fc1883b410703e516d218fde1"
            twilio_number = '+14406717757'
            target_number = '+918925068983'

            client = Client(account_sid, auth_token)
            message = client.messages \
                  .create(
                  body="🅰🅻🅴🆁🆃!!! Fire Warning... At Cam 0.",
                  from_=twilio_number,
                  to=target_number
            )
            print(message.body)
            sms_Status = True
            

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
