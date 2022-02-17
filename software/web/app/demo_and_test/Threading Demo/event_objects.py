# #Event objects let threads communicate with one another.

import threading

# event = threading.Event()

# event.set() # Set event to true

# event.clear() # Set event to false

# event.wait() # Blocks until event flag is true. 

# event.is_set() # Checks if event flag is true.

import queue
import numpy as np
import time

event = threading.Event()

def flag():
    time.sleep(3)
    event.set() # set flag to true
    print("Starting countdown!")
    time.sleep(7)
    print("Event is cleared.")
    event.clear() # Triggers start_operations to stop.

def start_operations():
    event.wait() # Waits until event flag is true
    while event.is_set():
        print("Starting random integer task")
        x = np.random.randint(1,30)
        time.sleep(0.5)
        if x == 29:
            print("True")
    print("Event has been cleared. Random operation stops")

t1 = threading.Thread(target = flag)
t2 = threading.Thread(target = start_operations)

t1.start()
t2.start()