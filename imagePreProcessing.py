# facial recognition screenshotter application using face/eye cascade classifiers 
# opencv and python3 
# developed by Kamran Choudhry

import cv2, sys, os
if not os.path.exists('images/'):
	os.makedirs('images/')

getPixels = True ; i = 1 ; data_dir = cv2.data.haarcascades
face_cascade = cv2.CascadeClassifier(data_dir + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(data_dir + 'haarcascade_eye.xml')
camera = cv2.VideoCapture(i-1)

# loop continuously reading frame-by-frame
while getPixels:
	success, frame = camera.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	# if faces is populated with data, then save image of frame
	#print(faces)

	for (x,y,z,q) in faces:
		cv2.rectangle(frame, (x,y), (x+z, y+q), (0,0,255), 3)
		#cv2.rectangle(frame, (x,y), (x+z, y-q), (255,0,0), 3)
		k = int(((2*x)+z)/2)
		cv2.circle(frame, (k,y-60), int(abs(((x+z)-x))/3), (255,0,0), -1)
		#print(str(x) + ' ' + str(y) + ' ' + str(z) + ' ' +  str(q))
		roi_gray = gray[y: y+q,x: x+z]
		roi_color = frame[y: y+q,x: x+z]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)

	cv2.imshow("Live Video (Facial Recognition)", frame)
	#cv2.imshow("Live Video (Facial Recognition)", gray)

	# if the 'esc' key is pressed, exit loop
	if cv2.waitKey(1) & 0xFF == 27:
		camera.release()
		getPixels = False
	# every 10th frame is saved into the images folder
	else:
		if i % 10 == 0:
			z = int(i/10)
			#print(z)
			cv2.imwrite('images/' + str(z) + '_capture.jpg', frame)
		i += 1

sys.exit()
