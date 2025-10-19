import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
ServoPin = 13
GPIO.setup(ServoPin, GPIO.OUT)

pwm = GPIO.PWM(ServoPin, 50)
pwm.ChangeDutyCycle(2.5)
sleep(2)
pwm.ChangeDutyCycle(10)

# Need this to make sure process ends properly.
pwm.stop()
GPIO.cleanup()
