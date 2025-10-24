import RPi.GPIO as GPIO
from time import sleep
def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(3, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(3, False)
	pwm.ChangeDutyCycle(0)
GPIO.setmode(GPIO.BOARD) #
ServoPin = 3
GPIO.setup(ServoPin, GPIO.OUT)

pwm = GPIO.PWM(ServoPin, 75000)
pwm.start(0)
angle = input("enter an angle")
angle = int(angle)
SetAngle(angle)
sleep(2)
# Need this to make sure process ends properly.
pwm.stop()
GPIO.cleanup()


