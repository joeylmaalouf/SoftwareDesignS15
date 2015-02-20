""" Experiment with face detection and image filtering using OpenCV
	Joey L. Maalouf
"""

#  import things
import numpy as np
import cv2

#  create things
cap = cv2.VideoCapture(0)
cam_width, cam_height = int(cap.get(3)), int(cap.get(4))
face_cascade = cv2.CascadeClassifier("/usr/include/opencv2/data/haarcascades/haarcascade_frontalface_alt.xml")
kernel = np.ones((8, 8), "uint8")

#  read, modify, and display things
while(True):
	ret, frame = cap.read()
	faces = face_cascade.detectMultiScale(frame, minSize=(cam_width/30, cam_height/30))
	for (x, y, w, h) in faces:
		frame[y:y+h, x:x+w, :] = cv2.dilate(frame[y:y+h, x:x+w, :], kernel)
		cv2.circle(frame, (x+w*1/3, y+h*2/5), h*1/8, (255, 255, 255), -1)
		cv2.circle(frame, (x+w*2/3, y+h*2/5), h*1/8, (255, 255, 255), -1)
		cv2.circle(frame, (x+w*1/3, y+h*5/12), h*1/20, (0, 0, 0), -1)
		cv2.circle(frame, (x+w*2/3, y+h*5/12), h*1/20, (0, 0, 0), -1)
		cv2.ellipse(frame, (x+w*1/2, y+h*3/4), (w*1/4, h*1/8), 0, 0, 180, (0, 0, 0), -1)
	cv2.imshow("Video Feed", frame)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

#  end things
cap.release()
cv2.destroyAllWindows()
