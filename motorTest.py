import RPi.GPIO as GPIO
import time

# Pin definitions
PWMA = 18   # PWM pin for speed
AIN1 = 23   # Direction pin 1
AIN2 = 24   # Direction pin 2
STBY = 25   # Standby pin

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)

# Initialize PWM at 50,000Hz
pwm = GPIO.PWM(PWMA, 5000)
pwm.start(0)

def standby(enable=True):
    GPIO.output(STBY, GPIO.HIGH if enable else GPIO.LOW)

def motor_forward(speed=100):
    standby(True)
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def motor_reverse(speed=100):
    standby(True)
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def motor_stop():
    pwm.ChangeDutyCycle(0)

def motor_brake():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(0)

def cleanup():
    motor_stop()
    standby(False)
    pwm.stop()
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
