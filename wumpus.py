#!/usr/bin/python3
#wumpus.py
#Daphne Groot, Hennie Veldthuis, Roos Vermeulen

import sys
from collections import namedtuple
from PyQt4 import QtGui

black = ["black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black",]

XY = namedtuple("XY", "x, y")

class Tile(QtGui.QWidget):
    """Creates a field tile and all of its atributes."""

    def __init__(self, parent, name, position):
        super(Tile, self).__init__()
        self.parent = parent
        self.name = name
        self.position = position

    def findCenter(self):
        self.center = self.geometry().center()

class GameField(QtGui.QWidget):
    """Creates the game field with a list of tile names predetermined by the programmer."""

    def __init__(self, tile_list):
        super(GameField, self).__init__()
        self.setGeometry(400,200,500,400)

        positions = []
        for y in range(4):
            for x in range(5):
                positions.append(XY(x,y))

        self.tile_dic = {}
        for i in range(20):
            self.tile_dic[positions[i]] = Tile(self, black[i], positions[i])

        self.initUI()

    def initUI(self):
        for key in self.tile_dic:
            o = self.tile_dic[key]
            o.setGeometry(o.position.x*100, o.position.y*100, 100, 100)
            o.findCenter()

        print(self.tile_dic[(4,3)].center)#Test function, this is how you get the center of a 'coordinate'

def main():
    
    app = QtGui.QApplication(sys.argv)
    window = GameField(black)
    window.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
