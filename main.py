#!/usr/bin/env python3

from kivy.app import App
from kivy.factory import Factory
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Line

from ObjectManager import ObjectManager
from DraftingTool import DraftingTool

class MainLayout(RelativeLayout):
	
	def __init__(self, **kwargs):
		super(MainLayout, self).__init__(**kwargs)
		
		self.object_manager = ObjectManager()
		self.drafting_tool = DraftingTool()
		
		self.bind(pos = self.update_canvas)
		self.bind(size = self.update_canvas)
		
	def update_canvas(self, *args):
		self.take_menu()
		pass
	
	def run_user_command(self):
		self.ids.command_label.text = "> " + self.ids.prompt.text
		self.ids.prompt.text = ""
		
	def change_active_tool(self, tool):
		self.object_manager.active_tool = tool
	
	def undo_last(self):
		self.object_manager.undone_objects.append(self.object_manager.objects.pop())
		self.ids.drawing_area.canvas.remove(self.object_manager.undone_objects[-1])
		
	def redo_last(self):
		if len(self.object_manager.undone_objects) > 0:
			self.object_manager.objects.append(self.object_manager.undone_objects.pop())
			self.ids.drawing_area.canvas.add(self.object_manager.objects[-1])
		else:
			print("There is nothing to redo")
	def zoom_in(self):
		pass
	
	def zoom_out(self):
		pass
		
	def move_drawing(self):
		self.object_manager.active_tool = "Move Drawing"
		
	def show_credits(self):
		pass
	
	def take_command_layout(self):
		if self.ids.command_layout.pos_hint["top"] == 1:
			self.ids.command_layout.pos_hint["top"] += self.ids.command_layout.size_hint[1]
			self.ids.drawing_area.pos_hint["top"] = 1
			self.ids.drawing_area.size_hint[1] = 1
		elif self.ids.command_layout.pos_hint["top"] > 1:
			self.ids.command_layout.pos_hint["top"] = 1
			self.ids.drawing_area.pos_hint["top"] = 1 - self.ids.command_layout.size_hint[1]
			self.ids.drawing_area.size_hint[1] = 1 - self.ids.command_layout.size_hint[1]
		
	def take_menu(self):
		# Method to make the Button Panel appear or dissappear
		if self.ids.main_menu.pos_hint["x"] < 0:
			self.ids.command_layout.size_hint[0] = 1 - 0.05 * self.height / self.width
			self.ids.command_layout.pos_hint["x"] = self.ids.main_menu.size_hint[0]
			self.ids.main_menu.pos_hint["x"] = 0
			if self.ids.command_layout.pos_hint["top"] == 1:
				self.ids.drawing_area.size_hint[1] = 1 - self.ids.command_layout.size_hint[1]
				self.ids.drawing_area.pos_hint["top"] = 1 - self.ids.command_layout.size_hint[1]
			elif self.ids.command_layout.pos_hint["top"] > 1:
				self.ids.drawing_area.size_hint[1] = 1
				self.ids.drawing_area.pos_hint["top"] = 1
		elif self.ids.main_menu.pos_hint["x"] >= 0:
			self.ids.command_layout.size_hint[0] = 1
			self.ids.command_layout.pos_hint["x"] = 0
			self.ids.drawing_area.pos_hint["x"] = 0
			if self.ids.command_layout.pos_hint["top"] == 1:
				self.ids.drawing_area.pos_hint["top"] = 1 - self.ids.command_layout.size_hint[1]
				self.ids.drawing_area.size_hint[1] = 1 - self.ids.command_layout.size_hint[1]
			elif self.ids.command_layout.pos_hint["top"] > 1:
				self.ids.drawing_area.pos_hint["top"] = 1
				self.ids.drawing_area.size_hint[1] = 1
			self.ids.drawing_area.size_hint[0] = 1
			self.ids.main_menu.pos_hint["x"] = -self.ids.main_menu.size_hint[0]
	def is_cursor_on_drawing_area(self, touch):
		return touch.x >= self.ids.drawing_area.pos[0] and touch.x <= self.ids.drawing_area.pos[0] + self.ids.drawing_area.width and touch.y >= self.ids.drawing_area.pos[1] and touch.y <= self.ids.drawing_area.pos[1] + self.ids.drawing_area.height

	def is_cursor_on_take_menu_button(self, touch):
		return touch.x >= self.ids.take_menu_button_layout.pos[0] and touch.x <=self.ids.take_menu_button_layout.pos[0] + self.ids.take_menu_button_layout.width and touch.y >= self.ids.take_menu_button_layout.pos[1] and touch.y <= self.ids.take_menu_button_layout.pos[1] + self.ids.take_menu_button_layout.height
	
	def on_touch_down(self, touch):
		# Method to specify what to do when there is a touch down event
		if self.is_cursor_on_drawing_area(touch) and not self.is_cursor_on_take_menu_button(touch):
			self.ids.drawing_area.canvas.add(Color(1, 1, 1))
			if self.object_manager.active_tool == "Line":
				self.object_manager.undone_objects.clear()
				self.object_manager.objects.append(Line(points = [touch.x - self.ids.drawing_area.pos_hint["x"] * self.width, touch.y, touch.x - self.ids.drawing_area.pos_hint["x"] * self.width, touch.y], width = self.drafting_tool.width))
				self.ids.drawing_area.canvas.add(self.object_manager.objects[-1])
			if self.object_manager.active_tool == "Free Hand Drawing":
				self.object_manager.objects.append(Line(points = [touch.x - self.ids.drawing_area.pos_hint["x"] * self.width, touch.y], width = self.drafting_tool.width))
			if self.object_manager.active_tool == "Move Drawing":
				pass
		return super(MainLayout, self).on_touch_down(touch) # Retaking the button behaviors for the on touch down event
	
	def on_touch_move(self, touch):
		# Method to specify what to do when an on touch down event happens
		if self.is_cursor_on_drawing_area(touch) and not self.is_cursor_on_take_menu_button(touch):
			if self.object_manager.active_tool == "Line":
				#  Changing the end point of the previously created line
				self.object_manager.objects[-1].points = [self.object_manager.objects[-1].points[0] - self.ids.main_menu.pos[0], self.object_manager.objects[-1].points[1], touch.x - self.ids.drawing_area.pos_hint["x"] * self.width, touch.y]
				#  Removing and adding the modified line to canvas to update the drawing
				self.ids.drawing_area.canvas.remove(self.object_manager.objects[-1])
				self.ids.drawing_area.canvas.add(self.object_manager.objects[-1])
			if self.object_manager.active_tool == "Free Hand Drawing":
				self.object_manager.objects[-1].points += [touch.x - self.ids.drawing_area.pos_hint["x"] * self.width, touch.y]
				#  Removing and adding the modified line to canvas to update the drawing
				self.ids.drawing_area.canvas.remove(self.object_manager.objects[-1])
				self.ids.drawing_area.canvas.add(self.object_manager.objects[-1])
	
	def on_touch_up(self, touch):
		# Method to specify what to do when an on touch up event happens
		
		return super(MainLayout, self).on_touch_up(touch) # Retaking the button behaviors for the on touch up event
	
class MyVectorialDrawingApp(App): # defining the app class

	def build(self): # using MyRelativeLayout in the app
		return MainLayout() # returning MyRelativeLayout

	def on_pause(self):
		# Method to do something when pausing the application
		return True

	def on_resume(self):
		# Method to do something when resuming the application
		pass


vector = MyVectorialDrawingApp()
vector. run()
