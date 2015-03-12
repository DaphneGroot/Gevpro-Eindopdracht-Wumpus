#!/usr/bin/python3
#wumpus.py
#Daphne Groot, Hennie Veldthuis, Roos Vermeulen

import sys
from collections import namedtuple
from PyQt4 import QtGui

classic_5x4 = ["es","esw","esw","esw","sw","nes","nesw","nesw","nesw","nsw","nes","nesw","nesw","nesw","nsw","ne","new","new","new","nw"]
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
            self.image = self.setImage("images/n_tile.png")
            self.N_open = True
            self.E_open = False
            self.S_open = False
            self.W_open = False
        elif name == "e":
            self.image = self.setImage("images/e_tile.png")
            self.N_open = False
            self.E_open = True
            self.S_open = False
            self.W_open = False
        elif name == "s":
            self.image = self.setImage("images/s_tile.png")
            self.N_open = False
            self.E_open = False
            self.S_open = True
            self.W_open = False
        elif name == "w":
            self.image = self.setImage("images/w_tile.png")
            self.N_open = False
            self.E_open = False
            self.S_open = False
            self.W_open = True
        elif name == "ne":
            self.image = self.setImage("images/ne_tile.png")
            self.N_open = True
            self.E_open = True
            self.S_open = False
            self.W_open = False
        elif name == "ns":
            self.image = self.setImage("images/ns_tile.png")
            self.N_open = True
            self.E_open = False
            self.S_open = True
            self.W_open = False
        elif name == "nw":
            self.image = self.setImage("images/nw_tile.png")
            self.N_open = True
            self.E_open = False
            self.S_open = False
            self.W_open = True
        elif name == "es":
            self.image = self.setImage("images/es_tile.png")
            self.N_open = False
            self.E_open = True
            self.S_open = True
            self.W_open = False
        elif name == "ew":
            self.image = self.setImage("images/ew_tile.png")
            self.N_open = False
            self.E_open = True
            self.S_open = False
            self.W_open = True
        elif name == "sw":
            self.image = self.setImage("images/sw_tile.png")
            self.N_open = False
            self.E_open = False
            self.S_open = True
            self.W_open = True
        elif name == "nes":
            self.image = self.setImage("images/nes_tile.png")
            self.N_open = True
            self.E_open = True
            self.S_open = True
            self.W_open = False
        elif name == "new":
            self.image = self.setImage("images/new_tile.png")
            self.N_open = True
            self.E_open = True
            self.S_open = False
            self.W_open = True
        elif name == "nsw":
            self.image = self.setImage("images/nsw_tile.png")
            self.N_open = True
            self.E_open = False
            self.S_open = True
            self.W_open = True
        elif name == "esw":
            self.image = self.setImage("images/esw_tile.png")
            self.N_open = False
            self.E_open = True
            self.S_open = True
            self.W_open = True
        elif name == "nesw":
            self.image = self.setImage("images/nesw_tile.png")
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
        self.field = classic_5x4

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