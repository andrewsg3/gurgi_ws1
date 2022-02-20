import cv2
import numpy

try:
	cap=cv2.VideoCapture(0)
	print("Opened camera at 0")
except:
	print("Could not open camera at 0")
	try:
		cap=cv2.VideoCapture(-1)
		print("Opened camera at -1")
	except:
		print("Could not open camera at -1")

font = cv2.FONT_HERSHEY_DUPLEX

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            print("Camera not detected")
            break
        else:
            frame = cv2.flip(frame, 1)
            frame = cv2.putText(frame, "GURGIWS Live Feed", (10,460), font, 1, (29,207,242),1,cv2.LINE_AA)
            ret, buffer = cv2.imencode(".jpg",frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n') # Concat frame and show result
