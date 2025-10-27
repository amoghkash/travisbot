from evdev import InputDevice, categorize, ecodes
from math import atan2, degrees
import RPi.GPIO as GPIO
import DFRobotMP3Interface
from time import sleep
import serial
def setAngle(angle):
    duty = (angle/18)+2
    GPIO.output(ServoPin,True)
    pwm.ChangeDutyCycle(duty)
def setSpeed(value):
    duty = (value/1024) * 100
    GPIO.output(MotorPin, True)
    pwmMotor.ChangeDutyCycle(duty)
#for device in devices:
 #   print(device.path, device.name, device.phys)
device = InputDevice('/dev/input/event2') # Replace eventX with the correct device path
GPIO.setmode(GPIO.BOARD)
ServoPin = 3
MotorPin = 32
GPIO.setup(ServoPin, GPIO.OUT)
pwm = GPIO.PWM(ServoPin, 50)
pwm.start(0) 
trackNumber = 0
#ser = serial.Serial('/dev/serial0', 9600, timeout = 1) #
GPIO.setup(MotorPin, GPIO.OUT)
pwmMotor = GPIO.PWM(MotorPin, 800)
pwmMotor.start(0)
dfrobotPlayer = DFRobotMP3Interface.MP3Player() #MP3 Player object initialization
dfrobotPlayer.changeVolumeTo(15) #MP3 player function to change volume
counter = 0
for event in device.read_loop():
    # Process the event
    if(counter ==0):
        previous_righty_movement = event
        counter = 1
    #print(event)
    if event.type == ecodes.EV_KEY:
        if event.code == 304 and event.value == 1:
            #print("A Button Pressed")
            dfrobotPlayer.playTrackNumber(1)
        elif event.code == 305 and event.value == 1:
            dfrobotPlayer.playTrackNumber(2)
        elif event.code == 308 and event.value == 1:
            dfrobotPlayer.playTrackNumber(3)
        elif event.code == 307 and event.value == 1:
            dfrobotPlayer.playTrackNumber(4)
        elif event.code == 314 and event.value == 1:
            dfrobotPlayer.playTrackNumber(trackNumber) #change to play the current track
            

    elif event.type == ecodes.EV_ABS:
        # Handle absolute axis events (e.g., joystick or touchscreen)
        print(f"Absolute event: code={event.code}, value={event.value}")
    #if event.code== 0:
        #print("this is 0, left JS x movement")
    #elif event.code == 1:
        #print("This is 1, a left JS y movement")
        if event.code == 5:
            print("This is 5, a right trigger event")
            setSpeed(event.value)
        elif event.code == 3:
            print("This is 3, right JS x event")
            if(previous_righty_movement.value <=0):
                yValue = previous_righty_movement.value
                xValue = event.value
                radius = (xValue ** 2 + yValue ** 2) ** 0.5
                if radius >= 20000:
                    angle = atan2(yValue, xValue)
                    angle = degrees(angle)
                    angle = angle * -1
                    onesPlace = angle % 10
                    angle = angle - onesPlace
                    #print(f"Angle is {angle}")
                    setAngle(angle)


        elif event.code == 4:
            print("This is 4, right JS y movement")
            previous_righty_movement = event
        elif event.code == 17:
            if event.value == -1:
                dfrobotPlayer.increaseVolume()
            elif event.value == 1:
                dfrobotPlayer.decreaseVolume()
        elif event.code == 16:
            if event.value == -1:
                if trackNumber >=1:
                    trackNumber -= 1
            elif event.value == 1:
                if trackNumber <= 4: #this is the number of tracks on the sd card, change value to numsongs-1 if more are added
                    trackNumber += 1
ser.close()
pwm.stop()
GPIO.cleanup()
# Add more conditions for other event types as needed
