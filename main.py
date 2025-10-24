import multiprocessing as mp
import api.motor as motor
from enum import Enum
import time
import evdev
import signal
import sys

class ControlType(Enum):
    FORWARD = 1
    BACKWARD = 2
    STOP = 3
    LEFT = 4
    RIGHT = 5
    STRAIGHT = 6

def input_control(q:mp.Queue):
    counter = 20
    device = evdev.InputDevice('/dev/input/event4') # Replace eventX with the correct device path
    counter = 0
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            print(evdev.categorize(event))
        elif event.code == 3:
            print(f'Got a value of {event.value} from left trigger')
        elif event.code == 5:
            q.put([ControlType.FORWARD, (100* (event.value/1024))])

def signal_handler(sig, frame):
    global input_process
    print("SigINT Recieved")
    input_process.terminate()
    input_process.join()
    motor.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    motor.initialize_motor()
    while True:
        item = None
        device = evdev.InputDevice('/dev/input/event4') # Replace eventX with the correct device path
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                print(evdev.categorize(event))
            elif event.code == 3:
                print(f'Got a value of {event.value} from left trigger')
            elif event.code == 5:
                item = [ControlType.FORWARD, (100* (event.value/1024))]
                break

        match item[0]:
            case ControlType.FORWARD:
                print(f"Setting Speed to {item[1]}")
                motor.motor_forward(int(item[1]))
            case ControlType.BACKWARD:
                print(f"Setting Reverse Speed to {item[1]}")
                motor.motor_reverse(int(item[1]))
            case ControlType.STOP:
                motor.motor_brake()
            case ControlType.LEFT:
                motor.steerLeft(int(item[1]))
            case ControlType.LEFT:
                motor.steerRight(int(item[1]))
            case ControlType.STRAIGHT:
                motor.steerStraight()