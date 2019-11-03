import cv2
import imagezmq
import PIL.Image, PIL.ImageTk
import tkinter

import time

from tkinter import *

# this is the coach


class App:

	def __init__(self, window):

		self.delay = 100

		self.data = dict()

		self.data["learnerMousePos"] = [0,0]
		self.data["myMousePos"] = [0,0]
		self.data["myText"] = ""
		self.data["learnerText"] = ""

		self.image_hub = imagezmq.ImageHub('tcp://*:5555')

		self.sender = imagezmq.ImageSender('tcp://Tianyus-MBP:5556')

		self.window = window
		self.window.title("appReceiver: Coach")

		self.vid = cv2.VideoCapture(0)

		self.canvas = tkinter.Canvas(window, width=1200, height=800)

		self.canvas.bind("<Motion>", self.mouseMotion)

		# ------ canvas entry box ----
		self.entry1 = tkinter.Entry(self.window)
		self.canvas.create_window(1100,750, window=self.entry1)

		# ----- canvas button --------
		self.button1 = tkinter.Button(text="enter message", command=self.buttonPress)
		self.canvas.create_window(1100, 780, window=self.button1)

		self.canvas.pack()

		# ------ scrollbar -------
		self.scrollbar = Scrollbar(self.window)
		self.scrollbar.pack( side = RIGHT, fill = Y )

		self.mylist = Listbox(self.window, yscrollcommand = self.scrollbar.set )
		
		self.mylist.pack(padx=5, pady=20, side=tkinter.RIGHT)
		# scrollbar.config( command = mylist.yview )

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

		self.myMouseWidget = self.canvas.create_oval(myX-5, myY-5, myX+5, myY+5, fill="blue")

		try:
			learnerX = self.data["learnerMousePos"][0]
			learnerY = self.data["learnerMousePos"][1]
		except:
			learnerX = 10
			learnerY = 10

		self.learnerMouseWidget = self.canvas.create_oval(learnerX-5, learnerY-5, learnerX+5, learnerY+5, fill="red")


	def update(self):

		self.canvas.delete(self.myMouseWidget)
		self.canvas.delete(self.learnerMouseWidget)
		

		# receive frame from learner
		rpi_name, frame = self.image_hub.recv_image()
		self.image_hub.send_reply(b'OK')

		# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
		self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

		# receive mouse position from learner
		mouse_x, mouse_y, self.data["learnerText"] = self.image_hub.recv_pos()

		self.data["learnerMousePos"][0] = mouse_x
		self.data["learnerMousePos"][1] = mouse_y
		# required reply after receiving mouse pos
		self.image_hub.send_reply(b'OK')

		if self.data["learnerText"] != "":
			self.mylist.insert(END, self.data["learnerText"])

		if self.data["myText"] != "":
			self.mylist.insert(END, self.data["myText"])
		

		# send self mouse mosition to learner
		self.sender.send_pos(self.data["myMousePos"][0], self.data["myMousePos"][1], self.data["myText"])

		self.data["learnerText"] = ""
		self.data["myText"] = ""
		

		self.redrawAll()



		self.window.after(self.delay, self.update)






App(tkinter.Tk())



















