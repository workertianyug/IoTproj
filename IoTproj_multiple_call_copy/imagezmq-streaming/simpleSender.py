
import socket
import time
from imutils.video import VideoStream
import imagezmq
import cv2

sender = imagezmq.ImageSender('tcp://Tianyus-MBP:5555')
 
rpi_name = socket.gethostname() # send RPi hostname with each image
# picam = VideoStream(usePiCamera=False).start()

vid = cv2.VideoCapture(0)

time.sleep(2.0)
while True:
	# image = picam.read()
	ret, image = vid.read()
	cv2.imshow(rpi_name, image)
	cv2.waitKey(1)
	sender.send_image(rpi_name, image)