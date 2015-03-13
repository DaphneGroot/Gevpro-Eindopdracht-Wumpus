#!/usr/bin/env python


import sys
from random import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import sleep


class Bewegen(QtGui.QWidget):
	def __init__(self,coordinatesPlayerList,coordinatesWumpusListMove,coordinatesWumpusList):
		super(Bewegen, self).__init__()
		self.coordinatesPlayerList = coordinatesPlayerList
		self.coordinatesWumpusListMove = coordinatesWumpusListMove
		self.coordinatesWumpusList = coordinatesWumpusList
		
		self.setGeometry(400, 200, 600, 500)
		self.setWindowTitle('Unigrammen')
		self.show()
		
		
	def paintEvent(self,event):
		"""Makes the circles which represent the player, the Wumpus where it is when it moved and the original spot of the Wumpus"""
		for i in range(len(self.coordinatesPlayerList)):

			#circle Player
			paintPlayer = QPainter()
			paintPlayer.begin(self)
			
			radx = 10
			rady = 10
			paintPlayer.setPen(Qt.red)
			centerPlayer = QPoint(self.coordinatesPlayerList[i][0],self.coordinatesPlayerList[i][1])
			paintPlayer.setBrush(Qt.yellow)
			paintPlayer.drawEllipse(centerPlayer, radx, rady)
			paintPlayer.end()
			
			
			#circle Wumpus Verplaatst
			paintWumpus = QPainter()
			paintWumpus.begin(self)
			
			radx = 10
			rady = 10
			paintWumpus.setPen(Qt.blue)
			centerWumpus = QPoint(self.coordinatesWumpusListMove[i][0],self.coordinatesWumpusListMove[i][1])
			paintWumpus.setBrush(Qt.green)
			paintWumpus.drawEllipse(centerWumpus, radx, rady)
			paintWumpus.end()


			#circle Wumpus original
			paintWumpusOriginal = QPainter()
			paintWumpusOriginal.begin(self)
			
			radx = 10
			rady = 10
			paintWumpusOriginal.setPen(Qt.black)
			centerWumpusOriginal = QPoint(self.coordinatesWumpusList[i][0],self.coordinatesWumpusList[i][1])
			paintWumpusOriginal.setBrush(Qt.black)
			paintWumpusOriginal.drawEllipse(centerWumpusOriginal, radx, rady)
			paintWumpusOriginal.end()



def coordinatesListWumpus():
	
	coordinatesPlayerList = []
	coordinatesWumpusList = []
	coordinatesWumpusListMove = []

	#random position of player
	coordinatesPlayer = (randrange(100,600,100),randrange(100,500,100))
	print("coordinaten speler: ",coordinatesPlayer)
	
	#random original position of Wumpus
	coordinatesWumpus = (randrange(100,600,100),randrange(100,500,100))
	print("Originele coordinaten Wumpus: ",coordinatesWumpus)
	
	#check if position Player isn't the same as position Wumpus
	if coordinatesPlayer != coordinatesWumpus:
		coordinatesWumpusList.append(coordinatesWumpus)
		
	else:
		coordinatesWumpus = (randrange(100,600,100),randrange(100,500,100))
		coordinatesWumpusList.append(coordinatesWumpus)
		print("Originele coordinaten Wumpus: ",coordinatesWumpus)
	
	
	"""Calculates the coordinates of the Wumpus' new location"""
	posible_coordinatesWumpus = []
	
	
	#checks if x or y coordinates aren't the same for the player and the Wumpus
	if coordinatesPlayer[0] != coordinatesWumpus[0] and coordinatesPlayer[1] != coordinatesWumpus[1]:
		
		if coordinatesPlayer[0] > coordinatesWumpus[0] and coordinatesPlayer[1] > coordinatesWumpus[1]:
			posible_coordinatesWumpus.append((coordinatesWumpus[0]+100,coordinatesWumpus[1]))
			posible_coordinatesWumpus.append((coordinatesWumpus[0],coordinatesWumpus[1]+100))
			
		elif coordinatesPlayer[0] > coordinatesWumpus[0] and coordinatesPlayer[1] < coordinatesWumpus[1]:
			posible_coordinatesWumpus.append((coordinatesWumpus[0]+100,coordinatesWumpus[1]))
			posible_coordinatesWumpus.append((coordinatesWumpus[0],coordinatesWumpus[1]-100))
			
		elif coordinatesPlayer[0] < coordinatesWumpus[0] and coordinatesPlayer[1] > coordinatesWumpus[1]:
			posible_coordinatesWumpus.append((coordinatesWumpus[0]-100,coordinatesWumpus[1]))
			posible_coordinatesWumpus.append((coordinatesWumpus[0],coordinatesWumpus[1]+100))
			
		elif coordinatesPlayer[0] < coordinatesWumpus[0] and coordinatesPlayer[1] < coordinatesWumpus[1]:
			posible_coordinatesWumpus.append((coordinatesWumpus[0]-100,coordinatesWumpus[1]))
			posible_coordinatesWumpus.append((coordinatesWumpus[0],coordinatesWumpus[1]-100))
	
	
	else:
		
		if coordinatesPlayer[0] == coordinatesWumpus[0] and coordinatesPlayer[1] > coordinatesWumpus[1]:
			posible_coordinatesWumpus.append((coordinatesWumpus[0],coordinatesWumpus[1]+100))
			
		elif coordinatesPlayer[0] == coordinatesWumpus[0] and coordinatesPlayer[1] < coordinatesWumpus[1]:
			posible_coordinatesWumpus.append((coordinatesWumpus[0],coordinatesWumpus[1]-100))
			
		elif coordinatesPlayer[1] == coordinatesWumpus[1] and coordinatesPlayer[0] > coordinatesWumpus[0]:
			posible_coordinatesWumpus.append((coordinatesWumpus[0]+100,coordinatesWumpus[1]))
			
		elif coordinatesPlayer[1] == coordinatesWumpus[1] and coordinatesPlayer[0] < coordinatesWumpus[0]:
			posible_coordinatesWumpus.append((coordinatesWumpus[0]-100,coordinatesWumpus[1]))
			
			
	#Picks the new spot of the Wumpus out an list with the options
	coordinatesWumpusMove = choice(posible_coordinatesWumpus)
	print("Verplaatste coordinaten Wumpus: ",coordinatesWumpusMove, "\n")
	
	coordinatesPlayerList.append(coordinatesPlayer)
	coordinatesWumpusListMove.append(coordinatesWumpusMove)

	return coordinatesPlayerList,coordinatesWumpusListMove,coordinatesWumpusList


	
def main(argv):
	coordinatesPlayerList,coordinatesWumpusListMove,coordinatesWumpusList = coordinatesListWumpus()
	
	app = QtGui.QApplication(sys.argv)
	ex = Bewegen(coordinatesPlayerList,coordinatesWumpusListMove,coordinatesWumpusList)
	sys.exit(app.exec_())
	

if __name__ == "__main__":
	main(sys.argv)
