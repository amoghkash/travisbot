import RPi.GPIO as GPIO
from time import sleep

def SetSpeed(speed):
	duty = speed/1 + 5
	pwm.ChangeDutyCycle(duty)
	sleep(2)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
pwm = GPIO.PWM(16, 1000)
pwm.start(0)


speed = input("enter speed: ")
speed = float(speed)
SetSpeed(speed)

pwm.stop()
GPIO.cleanup()
