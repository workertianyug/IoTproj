
# use https://github.com/JRodrigoF/AVrecordeR to mix video and audio
import cv2
import imagezmq
image_hub = imagezmq.ImageHub()
while True:  # show streamed images until Ctrl-C
	print("here")
	rpi_name, image = image_hub.recv_image()
	cv2.imshow(rpi_name, image) # 1 window for each RPi
	cv2.waitKey(1)
	image_hub.send_reply(b'OK')

