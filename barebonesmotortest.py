import RPi.GPIO as GPIO
from time import sleep
def SetSpeed(speed):
	duty = speed
	GPIO.output(MotorPin, True)
	pwm.ChangeDutyCycle(duty)
	sleep(2)
	GPIO.output(MotorPin, False)
	pwm.ChangeDutyCycle(0)
GPIO.setmode(GPIO.BOARD) #
MotorPin = 32
GPIO.setup(MotorPin, GPIO.OUT)

pwm = GPIO.PWM(MotorPin, 800)
pwm.start(0)
speed = input("enter a speed")
speed = int(speed)
SetSpeed(speed)
sleep(2)
# Need this to make sure process ends properly.
pwm.stop()
GPIO.cleanup()


