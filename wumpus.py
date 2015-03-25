#!/usr/bin/python3
#wumpus.py
#Daphne Groot, Hennie Veldthuis, Roos Vermeulen

import sys
from random import *
from collections import namedtuple
from PyQt4 import QtGui, QtCore
from mc import Mc

classic_5x4 = ["es","esw","esw","esw","sw","nes","nesw","nesw","nesw","nsw","nes","nesw","nesw","nesw","nsw","ne","new","new","new","nw"]
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

        self.setStyleSheet("""
            QPushButton {
                background: #C4C0A7;
                color: black;
                font-family: Verdana, sans-serif;
                
            }
            QLabel {
                color : #1C1209;
            }
            """)

        self.show()

    def toStartScreen(self):
        self.startscreen = StartScreen(self)
        self.startscreen.show()

    def toGameScreen(self, level):
        self.gamescreen = GameScreen(self, level)
        self.gamescreen.show()

    def toEndScreen(self, result, gold, cause, steps):
        self.endscreen = EndScreen(self, result, gold, cause, steps)
        self.endscreen.show()

#============================================================================================

class StartScreen(QtGui.QWidget):
    """Generates start screen"""

    def __init__(self, parent):
        super(StartScreen, self).__init__(parent)
        self.setGeometry(0,0,700,400)
        self.parent = parent
        start_pixmap = QtGui.QPixmap("images/Start.png")
        self.start_label = QtGui.QLabel(self)
        self.start_label.setPixmap(start_pixmap)

        self.classic_button = QtGui.QPushButton("Start", self)
        self.classic_button.move(7,7)
        self.classic_button.setStyle(QtGui.QStyleFactory.create('motif'))
        self.classic_button.setStyleSheet("""
            QPushButton {
                background: #42120D;
                color: #D9D5C1;
                font-family: Verdana, sans-serif;
            }
            """)
        
        self.classic_button.clicked.connect(self.startGame)

    def startGame(self):
        self.parent.toGameScreen(classic_5x4)
        self.close()


class GameScreen(QtGui.QWidget):
    """Generates game screen"""

    def __init__(self, parent, level):
        super(GameScreen, self).__init__(parent)
        self.parent = parent

        self.gamefield = GameField(self, level)
        self.sidebar = SideBar(self)

    def quitGame(self):
        self.parent.toStartScreen()
        self.close()
        
    def gameOver(self, result, gold, cause):
        self.parent.toEndScreen(result, gold, cause, self.sidebar.steps)
        self.close()
        
    def endTurn(self):
        """Is called at the end of every turn"""
        self.gamefield.player.updateMcPosition()
        
        #moves wumpus towards player
        coordinates_wumpus = GameField.coordinates_wumpus_list_move
        GameField.placeWumpus(self.gamefield,coordinates_wumpus)
        
        self.sidebar.sendMessages(self.gamefield.player.mc_position, self.gamefield.tile_dic) #creates messages for sidebar
        
        self.gamefield.checkMcPosition(self.gamefield.player.mc_position) #checks if something collides with player
        
        self.sidebar.steps += 1
        self.sidebar.updateSidebar() #arrows, gold
        


class EndScreen(QtGui.QWidget):
    """Generates end screen"""
    def __init__(self, parent, result, gold, cause, steps):
        super(EndScreen, self).__init__(parent)
        self.parent = parent

        #Makes labels for text,steps,gold and button to start again
        self.text_label = QtGui.QLabel(self)
        self.steps_label = QtGui.QLabel(self)
        self.gold_label = QtGui.QLabel(self)
        self.main_button = QtGui.QPushButton("Main", self)
        self.main_button.move(7,7)
        self.main_button.setStyle(QtGui.QStyleFactory.create('motif'))

        self.text_label.move(200,150)
        self.gold_label.move(200,230)
        self.steps_label.move(200, 250)
        
        #checks if won or lost and sets appropriate text
        if result == "win":
            self.text_label.setText("CONGRATULATIONS!!!\nYour arrow pierced the Wumpus through his tiny, slimy brain.")
            self.text_label.adjustSize()
            self.parent.setStyleSheet("color: green; background-color: black;")
            self.main_button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    color: #D6CBC3;
                }
                """)
        if result == "lose":
            if cause == "wumpus":
                self.text_label.setText("Many who entered these caves,\nfell pray to the Wumpus and were never seen again...\nAnd you blindly followed them in their fate.\nYou died, and the Wumpus will continue to terrorize these caves!\n")
                self.text_label.adjustSize()
                self.parent.setStyleSheet("color: #AD0000; background-color: black;")
                self.main_button.setStyleSheet("""
                    QPushButton {
                        background-color: #AD0000;
                        color: #D6CBC3;
                    }
                    """)
            elif cause == "arrow":
                self.text_label.setText("*Sigh*\nYou silly human, you shot yourself.")
                self.text_label.adjustSize()
                self.parent.setStyleSheet("color: #AD0000; background-color: black;")
                self.main_button.setStyleSheet("""
                    QPushButton {
                        background-color: #8C0000;
                        color: #D6CBC3;
                    }
                    """)
            elif cause == "pit":
                self.text_label.setText("Mwuahahahahah!\nYou fell into a bottomless pit. Enjoy falling forever!")
                self.text_label.adjustSize()
                self.parent.setStyleSheet("color: #AD0000; background-color: black;")
                self.main_button.setStyleSheet("""
                    QPushButton {
                        background-color: #8C0000;
                        color: #D6CBC3;
                    }
                    """)

        self.gold_label.setText("Gold:  " + str(gold))
        self.steps_label.setText("Steps: " + str(steps))

        self.main_button.clicked.connect(self.newGame)
        
    def newGame(self):
        self.parent.toStartScreen()
        self.parent.setStyleSheet("""
            QPushButton {
                background: #C4C0A7;
                color: black;
                font-family: Verdana, sans-serif;
                border-width: 5px;
            }
            QLabel {
                color : #1C1209;
            }
            """)
        self.close()
        
#============================================================================================

class SideBar(QtGui.QWidget):
    """Creates left side bar in game screen"""
    

    def __init__(self, parent):
        super(SideBar, self).__init__(parent)
        self.parent = parent
        
        
        #sets initial amount of gold, arrows and steps
        self.gold  = 0
        self.arrow = 4
        self.steps = 0
        
        self.setGeometry(0,0,200,400)
        self.quitbutton = QtGui.QPushButton("Quit", self)
        self.quitbutton.move(7,7)
        self.quitbutton.setStyle(QtGui.QStyleFactory.create('motif'))
        self.quitbutton.clicked.connect(self.parent.quitGame)
        
        
        #label with messages, amount of gold, amount of arrows left, steps
        self.label_messages = QtGui.QLabel(self)
        self.label_messages.move(10,120)
        
        self.label_gold = QtGui.QLabel("Gold:  "+str(self.gold),self)
        self.label_gold.move(10,40)
        
        self.label_arrow = QtGui.QLabel("Arrows: "+str(self.arrow),self)
        self.label_arrow.move(70,40)
        
        self.label_steps = QtGui.QLabel("Steps: "+str(self.steps),self)
        self.label_steps.move(10,60)
        
        self.sendMessages(self.parent.gamefield.player.mc_position, self.parent.gamefield.tile_dic)
        
        self.label_arrow_too_far = QtGui.QLabel("",self)
        self.label_arrow_too_far.move(10,350)
        
        
        
        
    def updateSidebar(self):
        #Update text in sidebar
        self.label_gold.setText("gold: "+str(self.gold))
        self.label_arrow.setText("arrows: "+str(self.arrow))
        self.label_steps.setText("steps: "+str(self.steps))
        self.label_steps.adjustSize()

        
    def sendMessages(self, player_position, tile_dic):
        wumpus_present     = False
        wumpus_present_far = False
        bats_present       = False
        hole_present       = False
        gold_present       = False
        
        
        #Determines surrounding positions of player and checks if something is close to the player
        surrounding_tiles = [(int(player_position[0]), int(player_position[1]-1)),(int(player_position[0]), int(player_position[1]+1)),(int(player_position[0]-1), int(player_position[1])),(int(player_position[0]+1), int(player_position[1]))]
        surrounding_tiles_wumpus_far = [(int(player_position[0]), int(player_position[1]-2)),(int(player_position[0]-1), int(player_position[1]-1)),(int(player_position[0]+1), int(player_position[1]-1)),(int(player_position[0]-2), int(player_position[1])),(int(player_position[0]+2), int(player_position[1])),(int(player_position[0]+1), int(player_position[1]+1)),(int(player_position[0]+1), int(player_position[1]+1)),(int(player_position[0]), int(player_position[1]+2))]
        
        surrounding_tiles = [tile for tile in surrounding_tiles if tile in tile_dic]
        surrounding_tiles_wumpus_far = [tile for tile in surrounding_tiles_wumpus_far if tile in tile_dic]
        
        for pos in surrounding_tiles:
            if tile_dic[pos].bats:
                bats_present = True
            if tile_dic[pos].hole:
                hole_present = True
            if tile_dic[pos].gold:
                gold_present = True
            if pos == self.parent.gamefield.position_wumpus:
                wumpus_present = True
                
        for pos in surrounding_tiles_wumpus_far:
            if pos == self.parent.gamefield.position_wumpus:
                wumpus_present_far = True            
            

        self.label_messages.setText("") 
           
        messages = ""
                
        #Generates appropriate messages
        if wumpus_present:
            messages += "You can smell the foul\nstench of the Wumpus\n\n"
            
        if bats_present:
            messages += "You hear the flapping\nof wings\n\n"

        if hole_present:
            messages += "You feel the draft from\nthe pit\n\n"
        
        if gold_present:
            messages += "You can detect a glimmer\n\n"
        
        if wumpus_present_far:
            messages += "You faintly smell something\nunpleasant\n\n"
               
        self.label_messages.setText(messages)
        self.label_messages.adjustSize()

        self.label_messages.show()
        

class GameField(QtGui.QWidget):
    """Creates the game field with a list of tile names predetermined by the programmer."""

    def __init__(self, parent, level):
        super(GameField, self).__init__(parent)
        self.parent = parent

        self.initUI(level)


    def initUI(self, level):
        self.width  = 5
        self.height = 4
        self.seize  = self.width*self.height
        self.field  = level

        self.setGeometry(200,0,self.width*100,self.height*100)
        self.size = self.width*self.height

        #- Create list with positions 0,0-4,4 -#
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                positions.append(XY(x,y)) 

        self.tile_dic = {}
        for i in range(self.seize):
            self.tile_dic[positions[i]] = Tile(self, self.field[i], positions[i])
            
        #- Create tiles in dictionary with positions and selected level -#
        self.tile_dic = {}
        for i in range(self.size):
            self.tile_dic[positions[i]] = Tile(self, self.field[i], positions[i])

        #- Place tiles correctly in field and save center coordinates -#
        for key in self.tile_dic:
            o = self.tile_dic[key]
            o.setGeometry(o.position.x*100, o.position.y*100, 100, 100)
            o.findCenter()

        #- Initialize positions items, player and wumpus -#
        self.placeItemsRandomly()
        GameField.coordinates_wumpus_list_move = self.placeWumpusRandomly()
        initial_player_position = self.placePlayerRandomly(True)
        
        #- Create player -#
        GameField.player = Mc(self, initial_player_position)

        
        
        
    def placeItemsRandomly(self):
        """Places the gold, bats and pit"""
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
                        
                        

    def placeWumpus(self,coordinates_wumpus):
        """Wumpus is placed into the field"""
        coordinates_wumpus_list      = []
        coordinates_wumpus_list_move = []        
        
        #check if position Player isn't the same as position Wumpus
        if GameField.player.mc_coords != coordinates_wumpus:
            coordinates_wumpus_list.append(coordinates_wumpus)
            
        else:
            self.position_wumpus = XY(randrange(self.width),randrange(self.height))
            coordinates_wumpus = [self.position_wumpus.x*100+49, self.position_wumpus.y*100+49]
            coordinates_wumpus_list.append(coordinates_wumpus)
        
        
        
        #Calculates the coordinates of the Wumpus' new location
        posible_coordinates_wumpus = []
       
        for element in range(len(coordinates_wumpus)):
            coordinates_wumpus_X = coordinates_wumpus[element][0]
            coordinates_wumpus_Y = coordinates_wumpus[element][1]
            
                    
        #checks if x or y coordinates aren't the same for the player and the Wumpus
        if GameField.player.mc_coords[0] != coordinates_wumpus_X and GameField.player.mc_coords[1] != coordinates_wumpus_Y:
            if GameField.player.mc_coords[0] > coordinates_wumpus_X and GameField.player.mc_coords[1] > coordinates_wumpus_Y:
                posible_coordinates_wumpus.append((coordinates_wumpus_X+100,coordinates_wumpus_Y))
                posible_coordinates_wumpus.append((coordinates_wumpus_X,coordinates_wumpus_Y+100))
                
            elif GameField.player.mc_coords[0] > coordinates_wumpus_X and GameField.player.mc_coords[1] < coordinates_wumpus_Y:
                posible_coordinates_wumpus.append((coordinates_wumpus_X+100,coordinates_wumpus_Y))
                posible_coordinates_wumpus.append((coordinates_wumpus_X,coordinates_wumpus_Y-100))
                
            elif GameField.player.mc_coords[0] < coordinates_wumpus_X and GameField.player.mc_coords[1] > coordinates_wumpus_Y:
                posible_coordinates_wumpus.append((coordinates_wumpus_X-100,coordinates_wumpus_Y))
                posible_coordinates_wumpus.append((coordinates_wumpus_X,coordinates_wumpus_Y+100))
                
            elif GameField.player.mc_coords[0] < coordinates_wumpus_X and GameField.player.mc_coords[1] < coordinates_wumpus_Y:
                posible_coordinates_wumpus.append((coordinates_wumpus_X-100,coordinates_wumpus_Y))
                posible_coordinates_wumpus.append((coordinates_wumpus_X,coordinates_wumpus_Y-100))
        else:
            
            if GameField.player.mc_coords[0] == coordinates_wumpus_X and GameField.player.mc_coords[1] > coordinates_wumpus_Y:
                posible_coordinates_wumpus.append((coordinates_wumpus_X,coordinates_wumpus_Y+100))
                
            elif GameField.player.mc_coords[0] == coordinates_wumpus_X and GameField.player.mc_coords[1] < coordinates_wumpus_Y:
                posible_coordinates_wumpus.append((coordinates_wumpus_X,coordinates_wumpus_Y-100))
                
            elif GameField.player.mc_coords[1] == coordinates_wumpus_Y and GameField.player.mc_coords[0] > coordinates_wumpus_X:
                posible_coordinates_wumpus.append((coordinates_wumpus_X+100,coordinates_wumpus_Y))
                
            elif GameField.player.mc_coords[1] == coordinates_wumpus_Y and GameField.player.mc_coords[0] < coordinates_wumpus_X:
                posible_coordinates_wumpus.append((coordinates_wumpus_X-100,coordinates_wumpus_Y))
                
                
        #Picks the new spot of the Wumpus out an list with the options
        try:
            coordinates_wumpus_move = choice(posible_coordinates_wumpus)
            coordinates_wumpus_list_move.append(coordinates_wumpus_move)
            
            #Makes coordinates available to use in antother class
            GameField.coordinates_wumpus_list_move = coordinates_wumpus_list_move
            
            self.position_wumpus = XY(int((coordinates_wumpus_list_move[0][0]-49)/100), int((coordinates_wumpus_list_move[0][1]-49)/100))

        except IndexError:
            pass
            
            
        return GameField.coordinates_wumpus_list_move




    def placeWumpusRandomly(self):
        #random original position of Wumpus
        self.position_wumpus = XY(randrange(self.width),randrange(self.height))
        coordinates_wumpus = [(self.position_wumpus.x*100+49, self.position_wumpus.y*100+49)]
        
        return coordinates_wumpus




    def placePlayerRandomly(self, avoid_obstacles):
        """Avoids player being placed randomly on obstacles"""
        if avoid_obstacles:
            available_positions = []
            for key in self.tile_dic:
                o = self.tile_dic[key]
                if not (o.bats or o.hole or o.gold or o.position == self.position_wumpus):
                    available_positions.append(o.position)
            return available_positions[randrange(len(available_positions))]
        else:
            return XY(randrange(self.width),randrange(self.height))
            
            
    def checkMcPosition(self,player_position):
        """Checks if anything is at the tile the player is standing on"""
        if self.tile_dic[player_position].gold: #gold
            self.parent.sidebar.gold += 1
            self.parent.sidebar.updateSidebar()
            self.tile_dic[player_position].removeItem("gold")
            
        if self.tile_dic[player_position].bats: #bats
            new_position = self.placePlayerRandomly(True)
            self.player.mc_coords = [new_position.x*100+49, new_position.y*100+49]
            self.player.mc_char.setPos(new_position.x*100+39,new_position.y*100+39)
            self.player.updateMcPosition()
            
        else:
            if self.tile_dic[player_position].hole: #hole
                self.parent.gameOver("lose",self.parent.sidebar.gold,"pit")
            
            else:
                if self.position_wumpus == player_position: #wumpus
                    self.parent.gameOver("lose",self.parent.sidebar.gold,"wumpus")
            
        
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
    app.setStyle('cleanlooks')
    window = Window()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
