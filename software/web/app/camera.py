import cv2
import numpy

cap=cv2.VideoCapture(0)
print("Opened camera")

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            print("Camera not detected")
            break
        else:
            frame = cv2.flip(frame, 1)
            ret, buffer = cv2.imencode(".jpg",frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n') # Concat frame and show result