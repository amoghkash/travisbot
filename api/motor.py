import RPi.GPIO as GPIO
import time
from gpiozero import Servo, PWMOutputDevice

# Pin definitions
PWMA = 18   # PWM pin for speed
AIN1 = 23   # Direction pin 1
AIN2 = 24   # Direction pin 2
STBY = 25   # Standby pin

# Setup
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)

# Initialize PWM at 50,000Hz
pwmA = GPIO.PWM(PWMA, 50000)
pwmA.start()
pwmA.ChangeDutyCycle(0.0)

# Throttle Control

def standby(enable=True):
    global GPIO
    GPIO.output(STBY, GPIO.HIGH if enable else GPIO.LOW)

def motor_forward(speed):
    global pwmA
    global GPIO
    standby(True)
    print(f'Setting Speed to {speed}%')
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speed)

def motor_reverse(speed):
    global pwmA
    global GPIO
    standby(True)
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speed)

def motor_stop():
    global pwmA
    pwmA.ChangeDutyCycle(0)

def motor_brake():
    global pwmA
    global GPIO
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(0)

# Steering Control
def steerLeft(value:int=100):
    #global servo
    #servo.max()
    pass

def steerRight(value:int=100):
    #global servo
    #servo.min()
    pass

def steerStraight():
    #global servo
    #servo.mid()
    pass

def cleanup():
    global pwmA
    global GPIO
    motor_stop()
    standby(False)
    pwmA.stop()
    GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    try:
        print("Motor forward")
        motor_forward(70)
        time.sleep(2)

        print("Motor reverse")
        motor_reverse(70)
        time.sleep(2)

        print("Motor brake")
        motor_brake()
        time.sleep(1)

        print("Motor stop")
        motor_stop()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
