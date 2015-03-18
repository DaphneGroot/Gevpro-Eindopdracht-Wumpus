#!/usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui

class Mc (QtGui.QWidget):
	
	def __init__(self):
		
		super(Mc, self).__init__()
		self.initUI()
		
	def initUI(self):
		#--- simple placeholder - to be changed ---#
		self.controlMc()
		
		
				
		self.setWindowTitle("Test")
		self.setGeometry(300, 300, 500, 400)
		self.show()
		
	def controlMc(self):
		""" Assign mc attributes. """
		
		self.tile_width = 10
		self.space_pressed = False
		self.mc_coords = [10, 10] #---> change default player coordinates to random
		
		pixmap = QtGui.QPixmap("mc_ph.xcf")
		self.mc_label = QtGui.QLabel(self)
		self.mc_label.setPixmap(pixmap)
		self.mc_label.move(self.mc_coords[0], self.mc_coords[1])
		#frame.addWidget(label)
		
		self.moveMc()
		
	def keyPressEvent(self, e):
		""" Define actions for all key press events. """
		
		#--- left arrow --#
		if e.key() == QtCore.Qt.Key_Left:
			print("--Left Arrow")
			
			if self.space_pressed == False:
				self.mc_coords[0] -= self.tile_width
				self.moveMc()
			else:
				# move arrow position
				pass
				
			print(self.mc_coords)
			
		#--- right arrow ---#
		if e.key() == QtCore.Qt.Key_Right:
			print("--Right Arrow")
			
			if self.space_pressed == False:
				self.mc_coords[0] += self.tile_width
				self.moveMc()
			else:
				# move arrow position
				pass
			
			print(self.mc_coords)
		
		#--- up arrow ---#
		if e.key() == QtCore.Qt.Key_Up:
			print("--Up Arrow")
			
			if self.space_pressed == False:
				self.mc_coords[1] -= self.tile_width
				self.moveMc()
			else:
				# move arrow position
				pass
			
			print(self.mc_coords)
			
		#--- down arrow ---#
		if e.key() == QtCore.Qt.Key_Down:
			print("--Down Arrow")
			
			if self.space_pressed == False:
				self.mc_coords[1] += self.tile_width
				self.moveMc()
			else:
				# move arrow position
				pass
			
			print(self.mc_coords)
		
		#--- space ---#	
		if e.key() == QtCore.Qt.Key_Space:
			print("--Space")
			
			if self.space_pressed == True:
				self.space_pressed = False
				print("Arrow canceled")
			else:
				self.space_pressed = True
				print("Arrow ready")
				
			print(self.space_pressed == True)
				
		#--- return ---#
		if e.key() == QtCore.Qt.Key_Return:
			print("--Return")
			if self.space_pressed == True:
				self.space_pressed = False
				print("Arrow shot")
	
	def moveMc(self):
		self.mc_label.move(self.mc_coords[0], self.mc_coords[1])
		pass	

def main():
	app = QtGui.QApplication(sys.argv)
	mc = Mc()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
