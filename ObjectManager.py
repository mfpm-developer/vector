#!/usr/bin/python3

class ObjectManager:
	#  Class to mange objects in the app
	def __init__(self):
		self.objects = []
		self.undone_objects = []
		self.active_tool = "Line"
		self.snap = False
