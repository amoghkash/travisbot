import evdev
import math
from gpiozero import Servo
from time import sleep
#servo = AngularServo(13, min_angle = 0, max_angle = 180, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)
servo = Servo(13)
servo.value - 0
def setAngle(angle):
    servoAngle = (angle/-90)-1
    servoAngle = round(servoAngle, 1)
    print(f"Servo Angle is {servoAngle}")
    servo.value = servoAngle
    sleep(0.5)

#for device in devices:
 #   print(device.path, device.name, device.phys)
device = evdev.InputDevice('/dev/input/event4') # Replace eventX with the correct device path
print(device)
counter = 0
for event in device.read_loop():
    # Process the event
    if(counter ==0):
        previous_righty_movement = event
        counter = 1
    print(event)
    if event.type == evdev.ecodes.EV_KEY:
        print(evdev.categorize(event))
    elif event.type == evdev.ecodes.EV_ABS:
        # Handle absolute axis events (e.g., joystick or touchscreen)
        print(f"Absolute event: code={event.code}, value={event.value}")
    if event.code== 0:
        print("this is 0, left JS x movement")
    elif event.code == 1:
        print("This is 1, a left JS y movement")
    elif event.code == 2:
        print("This is 2, a left trigger event")
    elif event.code == 3:
        print("This is 3, right JS x event")
        if(previous_righty_movement.value <=0):
            yValue = previous_righty_movement.value
            xValue = event.value
            radius = (yValue ** 2 + xValue ** 2) ** 0.5
            print(f"Radius is {radius}")
            if radius >=28000:
                angle = math.atan2(yValue, xValue)
                angle = math.degrees(angle)
                print(f"Angle is {angle}")
                setAngle(angle)


    elif event.code == 4:
        print("This is 4, right JS y movement")
        previous_righty_movement = event

# Add more conditions for other event types as needed
