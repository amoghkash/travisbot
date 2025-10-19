import multiprocessing as mp
import api.motor as motor
from enum import Enum
import time

class ControlType(Enum):
    FORWARD = 1
    BACKWARD = 2
    STOP = 3
    LEFT = 4
    RIGHT = 5
    STRAIGHT = 6

def motor_control(q:mp.Queue):
    while True:
        try:
            item = None
            if(not q.empty()):
                item = q.get()
            else:
                pass

            match item[0]:
                case ControlType.FORWARD:
                    motor.motor_forward(int(item[1]))
                case ControlType.BACKWARD:
                    motor.motor_reverse(int(item[1]))
                case ControlType.STOP:
                    motor.motor_brake()
                case ControlType.LEFT:
                    motor.steerLeft(int(item[1]))
                case ControlType.LEFT:
                    motor.steerRight(int(item[1]))
                case ControlType.STRAIGHT:
                    motor.steerStraight()


        except:
            print("Exiting Process")
            break

def input_control(q:mp.Queue):
    counter = 0
    while True:
        try:     
            q.put([ControlType.FORWARD, counter % 100])
            time.sleep(0.5)
            counter += 1
        except:
            print("Exiting Input")
            break

if __name__ == "__main__":
	# Setup Queue
    # Input is [ControlType, Value]
    q = mp.Queue()

	# Setup Motor and Input Processes
    motor_process = mp.Process(target=motor_control, args=(q,))
    input_process = mp.Process(target=input_control, args=(q,))

    # Start Processes
    motor_process.start()
    input_process.start()

    motor_process.join()
    input_process.join()
