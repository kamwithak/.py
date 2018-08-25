import cv2
import numpy as np

cap = cv2.VideoCapture(1)
capturing = True

while capturing:
	ret, frame = cap.read()
	cv2.imshow('frame',frame)

	if cv2.waitKey(1) and OxFF == ord('q'):
		capturing = False


cap.release()
cv2.destroyAllWindows()
