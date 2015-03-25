#!/usr/bin/env python
#mc.py
#Roos Vermeulen, Hennie Veldthuis, Daphne Groot

import sys
import random
import time
from PyQt4 import QtCore, QtGui

class McView (QtGui.QGraphicsView):
    def __init__(self, parent = None):
        super(McView, self).__init__(parent)

    def keyPressEvent(self, e):
        self.parentWidget().keyPressEvent(e)


class Mc (QtGui.QWidget):
    """Makes player and arrows"""    
    def __init__(self, parent, initial_mc_position):
        super(Mc, self).__init__(parent)
        self.parent      = parent
        self.mc_position = initial_mc_position
        self.mc_coords   = [self.mc_position.x*100+49, self.mc_position.y*100+49]
        self.initUI()
        
    def initUI(self):
        self.controlMc()
        self.setGeometry(0, 0, 500, 400)
        
    def controlMc(self):
        """ Assign mc attributes. """
        #Initialize attributes
        self.mc_walking        = False
        self.arrow_shooting    = False
        self.times_arrow_moved = 0
        self.tile_width        = 100
        self.space_pressed     = False
        self.arrow_path        = []
        
        #Show image player
        self.pixmap   = QtGui.QPixmap("images/mc.png")
        self.mc_view  = McView(self)
        self.mc_scene = QtGui.QGraphicsScene(QtCore.QRectF(0,0,500,400), self.mc_view)
        self.mc_view.setScene(self.mc_scene)
        self.mc_view.setStyleSheet("background: transparent")

        self.mc_char  = self.mc_scene.addPixmap(self.pixmap)
        self.mc_char.setTransformOriginPoint(self.pixmap.width() / 2, self.pixmap.height() / 2)        
        self.mc_char.setPos(self.mc_coords[0]-10, self.mc_coords[1]-10)
        
        
    def keyPressEvent(self, e):
        """ Define actions for all key press events. """
        if self.mc_walking == False and self.arrow_shooting == False: # no input allowed while mc is walking
            #--- left arrow --#
            if e.key() == QtCore.Qt.Key_Left:                
                if self.space_pressed == False:
                    if self.parent.tile_dic[self.mc_position].W_open:
                        # move player position
                        self.mc_walking = True
                        self.mc_char.setRotation(180)
                        self.animateMc(0, -1)
                        self.parent.parent.endTurn()
                    else:
                        pass
                else:
                    # move arrow position
                    self.arrow_shooting = True
                    self.moveArrow("left")
                    pass
            
            #--- right arrow ---#
            if e.key() == QtCore.Qt.Key_Right:
                if self.space_pressed == False:
                    if self.parent.tile_dic[self.mc_position].E_open:
                        # move player position
                        self.mc_walking = True
                        self.mc_char.setRotation(0)
                        self.animateMc(0, 1)
                        self.parent.parent.endTurn()
                    else:
                        pass
                else:
                    # move arrow position
                    self.arrow_shooting = True
                    self.moveArrow("right")
                    pass
        
            #--- up arrow ---#
            if e.key() == QtCore.Qt.Key_Up:            
                if self.space_pressed == False:
                    if self.parent.tile_dic[self.mc_position].N_open:
                        # move player position
                        self.mc_walking = True
                        self.mc_char.setRotation(270)
                        self.animateMc(1, -1)
                        self.parent.parent.endTurn()
                    else:
                        pass
                else:
                    # move arrow position
                    self.arrow_shooting = True
                    self.moveArrow("up")
                    pass
            
            #--- down arrow ---#
            if e.key() == QtCore.Qt.Key_Down:
                if self.space_pressed == False:
                    if self.parent.tile_dic[self.mc_position].S_open:
                        # move player position
                        self.mc_walking = True
                        self.mc_char.setRotation(90)
                        self.animateMc(1, 1)
                        self.parent.parent.endTurn()
                    else:
                        pass
                else:
                    # move arrow position
                    self.arrow_shooting = True
                    self.moveArrow("down")
                    pass
            
            #--- space ---#    
            if e.key() == QtCore.Qt.Key_Space:
                self.parent.parent.sidebar.label_arrow_too_far.setText("")
                if self.parent.parent.sidebar.arrow > 0:
                    if self.space_pressed == True:
                        self.space_pressed = False
                        self.initializeArrow(False) # remove arrow
                        self.arrow_path    = [] # remove content arrow_path
                    else:
                        self.space_pressed = True
                        self.initializeArrow(True) # create arrow
                
            #--- return ---#
            if e.key() == QtCore.Qt.Key_Return:
                if self.space_pressed == True:
                    self.parent.parent.sidebar.label_arrow_too_far.setText("")
                    self.parent.parent.sidebar.arrow -= 1
                    self.parent.parent.sidebar.updateSidebar()
                    self.space_pressed = False
                    
                    game_over = False
                    
                    #Checks if player or Wumpus is hit by an arrow
                    for coords in self.arrow_path:
                        if coords == self.mc_coords:
                            self.parent.parent.gameOver("lose", self.parent.parent.sidebar.gold,"arrow")
                            game_over = True
                            break
                        elif coords == [self.parent.coordinates_wumpus_list_move[0][0],self.parent.coordinates_wumpus_list_move[0][1]]:
                            self.parent.parent.gameOver("win", self.parent.parent.sidebar.gold,"")
                            game_over = True
                            break
                            
                    if not game_over:
                        self.arrow_path    = [] # remove content arrow_path
                        self.initializeArrow(False)
                        self.parent.parent.endTurn()
            

    def animateMc(self, x_or_y, direction):
        """Moves the player to new position"""
        self.stepcounter = 0
        while self.mc_walking == True:
            time.sleep(0.01)
            self.mc_coords[x_or_y] += direction
            self.stepcounter += 1
            self.mc_char.setPos(self.mc_coords[0]-10, self.mc_coords[1]-10) # change mc position to new coordinates
            QtGui.QApplication.processEvents() # needed to update gui, normally won"t update during loop
            if self.stepcounter == self.tile_width: # stop loop when the mc has traveled the length of one tile
                self.mc_walking = False

    def animateArrow(self, x_or_y, direction):
        """Moves the arrow to new position"""
        self.stepcounter = 0        
        while self.arrow_shooting == True:    
            time.sleep(0.01)
            self.arrow_coords[x_or_y] += direction
            self.stepcounter += 1
            self.arrow.setPos(self.arrow_coords[0]-10, self.arrow_coords[1]-10) # change arrow position to new coordinates
            QtGui.QApplication.processEvents() # needed to update gui, normally won"t update during loop
            if self.stepcounter == self.tile_width: # stop loop when the arrow has traveled the length of one tile
                self.arrow_path.append(self.arrow_coords[:])
                self.arrow_shooting = False
                
    def initializeArrow(self, create_arrow):
        """Creates and deletes arrow upon pressing space"""
        self.times_arrow_moved = 0
        if create_arrow == True:
            self.arrow_pixmap = QtGui.QPixmap("images/arrow2.png")
            self.arrow  = self.mc_scene.addPixmap(self.arrow_pixmap)
            self.arrow.setTransformOriginPoint(self.arrow_pixmap.width() / 2, self.arrow_pixmap.height() / 2)
            self.arrow_coords = self.mc_coords[:] # copy mc coordinates
            self.arrow.setPos(self.arrow_coords[0]-10, self.arrow_coords[1]-10)
            self.current_arrow_position = self.mc_position
        else:
            self.mc_scene.removeItem(self.arrow) # deletes arrow
        
    def moveArrow(self, key):
        """Rotate arrow to match movement direction"""
        if self.times_arrow_moved >= 5:
            self.arrow_shooting = False
            self.arrow_path    = [] # remove content arrow_path
            self.parent.parent.sidebar.label_arrow_too_far.setText("You can't move your arrow\nany further")
            self.parent.parent.sidebar.label_arrow_too_far.adjustSize()
        else:
            self.current_arrow_position = ((self.arrow_coords[0]-49)/100,(self.arrow_coords[1]-49)/100)
            if key == "left" and self.parent.tile_dic[self.current_arrow_position].W_open:
                self.times_arrow_moved += 1
                self.arrow.setRotation(180)
                self.animateArrow(0, -1)
            elif key == "right" and self.parent.tile_dic[self.current_arrow_position].E_open:
                self.times_arrow_moved += 1
                self.arrow.setRotation(0)
                self.animateArrow(0, 1)
            elif key == "up" and self.parent.tile_dic[self.current_arrow_position].N_open:
                self.times_arrow_moved += 1
                self.arrow.setRotation(270)
                self.animateArrow(1, -1)
            elif key == "down" and self.parent.tile_dic[self.current_arrow_position].S_open:
                self.times_arrow_moved += 1
                self.arrow.setRotation(90)
                self.animateArrow(1, 1)
            else:
                self.arrow_shooting = False
                
    def updateMcPosition(self):
        self.mc_position = ((self.mc_coords[0]-49)/100, (self.mc_coords[1]-49)/100)
            


def main():
    app = QtGui.QApplication(sys.argv)
    mc = Mc()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
