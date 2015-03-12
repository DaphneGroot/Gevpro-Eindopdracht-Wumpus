#!/usr/bin/python3
#wumpus.py
#Daphne Groot, Hennie Veldthuis, Roos Vermeulen

import sys
from collections import namedtuple
from PyQt4 import QtGui

black_5x4 = ["black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black",]
#You can create a field by making a list of 20 tile names (5x4), and setting the properties of the names in Tile().setType(name). The tiles' order is first from left to right and then from top to bottom:
#   1,  2,  3,  4,  5,
#   6,  7,  8,  9,  10,
#   11, 12, 13, 14, 15,
#   16, 17, 18, 19, 20

XY = namedtuple("XY", "x, y")

class Tile(QtGui.QWidget):
    """Creates a field tile and all of its atributes."""

    def __init__(self, parent, name, position):
        super(Tile, self).__init__(parent)
        self.parent = parent
        self.position = position

        self.setType(name)

    def setImage(self, image_name):
        """Sets and show image of tile"""
        pixmap = QtGui.QPixmap(image_name)
        pixlabel = QtGui.QLabel(self)
        pixlabel.setPixmap(pixmap)

    def findCenter(self):
        """Returns center of tile as QPoint()"""
        self.center = self.geometry().center()

    def setType(self, name):
        """Sets tile type by name"""
        if name == "black":
            self.image = self.setImage("images/black.jpg")
            self.N_open = True
            self.E_open = True
            self.S_open = True
            self.W_open = True
        elif name == "n":
            #picture = images/n_tile.jpg
            self.N_open = True
            self.E_open = False
            self.S_open = False
            self.W_open = False
        elif name == "e":
            #picture = images/e_tile.jpg
            self.N_open = False
            self.E_open = True
            self.S_open = False
            self.W_open = False
        elif name == "s":
            #picture = images/s_tile.jpg
            self.N_open = False
            self.E_open = False
            self.S_open = True
            self.W_open = False
        elif name == "w":
            #picture = images/w_tile.jpg
            self.N_open = False
            self.E_open = False
            self.S_open = False
            self.W_open = True
        elif name == "ne":
            #picture = images/ne_tile.jpg
            self.N_open = True
            self.E_open = True
            self.S_open = False
            self.W_open = False
        elif name == "ns":
            #picture = images/ns_tile.jpg
            self.N_open = True
            self.E_open = False
            self.S_open = True
            self.W_open = False
        elif name == "nw":
            #picture = images/nw_tile.jpg
            self.N_open = True
            self.E_open = False
            self.S_open = False
            self.W_open = True
        elif name == "es":
            #picture = images/es_tile.jpg
            self.N_open = False
            self.E_open = True
            self.S_open = True
            self.W_open = False
        elif name == "ew":
            #picture = images/ew_tile.jpg
            self.N_open = False
            self.E_open = True
            self.S_open = False
            self.W_open = True
        elif name == "sw":
            #picture = images/sw_tile.jpg
            self.N_open = False
            self.E_open = False
            self.S_open = True
            self.W_open = True
        elif name == "nes":
            #picture = images/nes_tile.jpg
            self.N_open = True
            self.E_open = True
            self.S_open = True
            self.W_open = False
        elif name == "new":
            #picture = images/new_tile.jpg
            self.N_open = True
            self.E_open = True
            self.S_open = False
            self.W_open = True
        elif name == "nsw":
            #picture = images/nsw_tile.jpg
            self.N_open = True
            self.E_open = False
            self.S_open = True
            self.W_open = True
        elif name == "esw":
            #picture = images/esw_tile.jpg
            self.N_open = False
            self.E_open = True
            self.S_open = True
            self.W_open = True
        elif name == "nesw":
            #picture = images/nesw_tile.jpg
            self.N_open = True
            self.E_open = True
            self.S_open = True
            self.W_open = True

class GameField(QtGui.QWidget):
    """Creates the game field with a list of tile names predetermined by the programmer."""

    def __init__(self):
        super(GameField, self).__init__()

        self.initUI()

    def initUI(self):
        self.width = 5
        self.height = 4
        self.seize = self.width*self.height
        self.field = black_5x4

        self.setGeometry(400,200,self.width*100,self.height*100)
        
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                positions.append(XY(x,y)) 
        
        self.tile_dic = {}
        for i in range(self.seize):
            self.tile_dic[positions[i]] = Tile(self, self.field[i], positions[i])
            
        for key in self.tile_dic:
            o = self.tile_dic[key]
            o.setGeometry(o.position.x*100, o.position.y*100, 100, 100)
            o.findCenter()

        print(self.tile_dic[(4,3)].center)#Test function, this is how you get the center of a 'coordinate'
        print(self.tile_dic[(4,3)].W_open)#Test function, this is how you can see if that direction is open for Jack and Wumpus (True) or if there's a wall (False)

def main():
    
    app = QtGui.QApplication(sys.argv)
    window = GameField()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
