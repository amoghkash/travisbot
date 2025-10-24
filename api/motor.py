import RPi.GPIO as GPIO
import time

# Pin definitions
PWMA = 18   # PWM pin for speed
AIN1 = 23   # Direction pin 1
AIN2 = 24   # Direction pin 2
STBY = 25   # Standby pin

# filepath: /Users/amoghkashyap/Documents/travisbotcontainer/travisbot/api/motor.py
def initialize_motor():
    global pwmA
    global GPIO
    pwmA = GPIO.PWM(PWMA, 1000)
    pwmA.start(0)

def standby(enable=True):
    pass

def motor_forward(speed):
    global pwmA
    print(f'Setting Speed to {speed}%')
    pwmA.ChangeDutyCycle(speed)

def motor_reverse(speed):
    global pwmA
    pwmA.ChangeDutyCycle(speed)

def motor_stop():
    global pwmA
    pwmA.ChangeDutyCycle(0)

def motor_brake():
    global pwmA
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
        print("slowing down")
        motor_forward(20)
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
