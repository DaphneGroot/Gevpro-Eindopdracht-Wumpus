#!/usr/bin/python3
#wumpus.py
#Daphne Groot, Hennie Veldthuis, Roos Vermeulen

import sys
from random import randrange
from collections import namedtuple
from PyQt4 import QtGui, QtCore

from Wumpus_bewegen import Bewegen
from mc import Mc

classic_5x4 = ["es","esw","esw","esw","sw","nes","nesw","nesw","nesw","nsw","nes","nesw","nesw","nesw","nsw","ne","new","new","new","nw"]
black_5x4 = ["black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black","black",]
#You can create a field by making a list of 20 tile names (5x4), and setting the properties of the names in Tile().setType(name). The tiles' order is first from left to right and then from top to bottom:
#   1,  2,  3,  4,  5,
#   6,  7,  8,  9,  10,
#   11, 12, 13, 14, 15,
#   16, 17, 18, 19, 20

XY = namedtuple("XY", "x, y")

class Window(QtGui.QWidget):
    """Generates main window and navigates between screens"""

    def __init__(self):
        super(Window, self).__init__()

        self.startscreen = StartScreen(self)
        self.setGeometry(400,200,700,400)
        self.setWindowTitle("Hunt the Wumpus")

        self.show()

    def toStartScreen(self):
        self.startscreen = StartScreen(self)
        self.startscreen.show()

    def toGameScreen(self, level):
        self.gamescreen = GameScreen(self, level)
        self.gamescreen.show()

    def toEndScreen(self, result, gold):
        self.endscreen = EndScreen(self, result, gold)
        self.endscreen.show()

#============================================================================================

class StartScreen(QtGui.QWidget):
    """Generates start screen"""

    def __init__(self, parent):
        super(StartScreen, self).__init__(parent)
        self.parent = parent

        self.classic_button = QtGui.QPushButton("Classic", self)
        self.classic_button.clicked.connect(self.chooseLevel)

    def chooseLevel(self):
        self.parent.toGameScreen(classic_5x4)
        self.close()

class GameScreen(QtGui.QWidget):
    """Generates game screen"""

    def __init__(self, parent, level):
        super(GameScreen, self).__init__(parent)
        self.parent = parent

        self.sidebar = SideBar(self)
        self.gamefield = GameField(self, level)

    def quitGame(self):
        self.parent.toStartScreen()
        self.close()

class EndScreen(QtGui.QWidget):
    """Generates end screen"""

    def __init__(self, parent, result, gold):
        super(EndScreen, self).__init__(parent)
        self.parent = parent

        text_label = QtGui.QLabel(self)
        gold_label = QtGui.QLabel(self)
        main_button = QtGui.QPushButton("Main", self)

        text_label.move(250,150)
        gold_label.move(270,230)

        if result == "win":
            text_label.setText("Many who entered these caves,\nfell pray to the Wumpus and were never seen again...\nUntil you heroically hunted him down and killed the feared beast!\nCongratulations! You killed the Wumpus!")
        else:
            text_label.setText("Many who entered these caves,\nfell pray to the Wumpus and were never seen again...\nAnd you blindly followed them in their fate.\nYou died, and the Wumpus will continue to terrorize these caves!")

        gold_label.setText("Gold: " + str(gold))

        main_button.clicked.connect(self.newGame)
        
    def newGame(self):
        self.parent.toStartScreen()
        self.close()
        
#============================================================================================

class SideBar(QtGui.QWidget):
    """Creates left side bar in game screen"""

    def __init__(self, parent):
        super(SideBar, self).__init__(parent)
        self.parent = parent

        self.setGeometry(0,0,200,400)
        self.quitbutton = QtGui.QPushButton("Quit", self)
        self.quitbutton.clicked.connect(self.parent.quitGame)

class GameField(QtGui.QWidget):
    """Creates the game field with a list of tile names predetermined by the programmer."""

    def __init__(self, parent, level):
        super(GameField, self).__init__(parent)

        self.initUI(level)

    def initUI(self, level):
        self.width = 5
        self.height = 4
        self.size = self.width*self.height
        self.field = level

        self.setGeometry(200,0,self.width*100,self.height*100)

        #- Create list with positions 0,0-4,4 -#
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                positions.append(XY(x,y)) 

        #- Create tiles in dictionary with positions and selected level -#
        self.tile_dic = {}
        for i in range(self.size):
            self.tile_dic[positions[i]] = Tile(self, self.field[i], positions[i])

        #- Place tiles correctly in field and save center coordinates -#
        for key in self.tile_dic:
            o = self.tile_dic[key]
            o.setGeometry(o.position.x*100, o.position.y*100, 100, 100)
            o.findCenter()

        #print(self.tile_dic[(4,3)].center) Test function, this is how you get the center of a 'coordinate'
        #print(self.tile_dic[(4,3)].W_open) Test function, this is how you can see if that direction is open for Jack and Wumpus (True) or if there's a wall (False)

        #- Initialize positions items, player and wumpus -#
        self.placeItemsRandomly()
        self.position_wumpus = self.placeWumpusRandomly()
        initial_player_position = self.placePlayerRandomly(True)

        #- Intergrate mc.py -#
        self.player = Mc()
        self.player.mc_coords = [initial_player_position.x, initial_player_position.y]
        self.player.tile_width = 1
        print(self.tile_dic[(self.player.mc_coords[0],self.player.mc_coords[1])].center)
        
    def placeItemsRandomly(self):
        new_gold_amount = 5
        new_hole_amount = 1
        new_bats_amount = 1
        
        positions_list = []
        
        while len(positions_list) < new_gold_amount+new_hole_amount+new_bats_amount:
                x = randrange(self.width)
                y = randrange(self.height)
                
                if not ((x,y) in positions_list):
                        positions_list.append((x,y))
        
        for position in positions_list:
                if new_gold_amount > 0:
                        self.tile_dic[position].setItem("gold")
                        new_gold_amount = new_gold_amount - 1
                elif new_hole_amount > 0:
                        self.tile_dic[position].setItem("hole")
                        new_hole_amount = new_hole_amount - 1
                elif new_bats_amount > 0:
                        self.tile_dic[position].setItem("bats")
                        new_bats_amount = new_bats_amount - 1

    def placeWumpusRandomly(self):
        return XY(randrange(self.width),randrange(self.height))

    def placePlayerRandomly(self, avoid_obstacles):
        if avoid_obstacles:
            available_positions = []
            for key in self.tile_dic:
                o = self.tile_dic[key]
                if not (o.bats or o.hole or o.gold or o.position == self.position_wumpus):
                    available_positions.append(o.position)
            return available_positions[randrange(len(available_positions))]
        else:
            return XY(randrange(self.width),randrange(self.height))
        
#============================================================================================

class Tile(QtGui.QWidget):
    """Creates a field tile and all of its atributes."""

    def __init__(self, parent, name, position):
        super(Tile, self).__init__(parent)
        self.parent = parent
        self.position = position
        self.bats = False
        self.gold = False
        self.hole = False

        self.setType(name)
        
    def setItem(self, item):#item is: bats, hole, gold
        if item == "bats":
                self.bats = True
        elif item == "gold":
                self.gold = True
        elif item == "hole":
                self.hole = True
        else:
                pass
		
    def removeItem(self, item):#item is: bats, hole, gold
        if item == "bats":
                self.bats = False
        elif item == "gold":
                self.gold = False
        elif item == "hole":
                self.hole = False
        else:
                pass

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
        
#============================================================================================

def main():
    
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
