import socket
import time
# from imutils.video import VideoStream
import imagezmq
import cv2
import PIL.Image, PIL.ImageTk
import tkinter

from tkinter import *

# https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/

# this is the learner

# next step:
# finish text bar
# get more ui
# get slides

class App:

	def __init__(self, window):



		self.delay = 100

		self.window = window
		self.window.title("appSender: Learner")

		self.vid = cv2.VideoCapture(0)

		self.sender = imagezmq.ImageSender('tcp://Tianyus-MBP:5555')
		# self.sender = imagezmq.ImageSender('tcp://127.0.0.1:5555')

		self.image_hub = imagezmq.ImageHub('tcp://*:5556')
		
		self.rpi_name = socket.gethostname()

		self.data = dict()
		self.data['myMousePos'] = [0, 0]
		self.data['coachMousePos'] = [0,0]
		self.data['myText'] = ""
		self.data["coachText"] = ""

		self.canvas = tkinter.Canvas(window, width=1200, height=800)

		self.canvas.bind("<Motion>", self.mouseMotion)
		self.canvas.pack()
		
		# ------ canvas entry box ----
		self.entry1 = tkinter.Entry(self.window)
		# self.canvas.create_window(1100,750, window=self.entry1)
		self.entry1.pack()

		# ----- canvas button --------
		self.button1 = tkinter.Button(self.window,text="enter message", command=self.buttonPress)
		# self.canvas.create_window(1100, 780, window=self.button1)
		self.button1.pack()

		

		# ------ scrollbar -------
		self.scrollbar = Scrollbar(self.window)
		self.scrollbar.pack( side = RIGHT, fill = Y )

		self.mylist = Listbox(self.window, yscrollcommand = self.scrollbar.set )
		# for line in range(5):
		# 	self.mylist.insert(END, "This is line number " + str(line))

		self.mylist.pack(padx=5, pady=20, side=tkinter.RIGHT)
		# scrollbar.config( command = mylist.yview )

		self.imageWidget = None

		self.redrawAll()
		self.update()

		self.window.mainloop()


	def mouseMotion(self, event):

		self.data['myMousePos'] = (event.x, event.y)
		# print(event.x, event.y)

	def buttonPress(self):
		self.data["myText"] = self.entry1.get()
		# self.mylist.insert(END, self.data["myText"])

	def redrawAll(self):


		try:
			myX = self.data["myMousePos"][0]
			myY = self.data["myMousePos"][1]
		except:
			myX = 10
			myY = 10
		
		self.myMouseWidget = self.canvas.create_oval(myX-5, myY-5, myX+5, myY+5, fill="red")

		try:
			coachX = self.data["coachMousePos"][0]
			coachY = self.data["coachMousePos"][1]
		except:
			coachX = 10
			coachY = 10
		
		self.coachMouseWidget = self.canvas.create_oval(coachX-5, coachY-5, coachX+5, coachY+5, fill="blue")


			

	def update(self):

		self.canvas.delete(self.myMouseWidget)
		self.canvas.delete(self.coachMouseWidget)
		if self.imageWidget != None:
			self.canvas.delete(self.imageWidget)

		ret, frame = self.vid.read()

		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
		self.imageWidget = self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)


		
		# send everything: image + mouse pos + text
		self.sender.send_image_data(self.rpi_name, frame, self.data)

		
		# receiver everything
		_, _, md = self.image_hub.recv_image_data()

		self.data["coachText"] = md["myText"]
		self.data["coachMousePos"][0] = md["myMousePos"][0]
		self.data["coachMousePos"][1] = md["myMousePos"][1]

		self.image_hub.send_reply(b'OK')

		if self.data["coachText"] != "":
			self.mylist.insert(END, self.data["coachText"])

		if self.data["myText"] != "":
			self.mylist.insert(END, self.data["myText"])

		self.data["myText"] = ""
		self.data["coachText"] = ""
		

		
		# update the frame, maybe should in redrawall?
		
		self.redrawAll()


		self.window.after(self.delay, self.update)




App(tkinter.Tk())
















