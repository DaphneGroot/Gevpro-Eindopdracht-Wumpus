#!/usr/bin/env python

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
    
    def __init__(self, parent, initial_mc_position):
        
        super(Mc, self).__init__(parent)
        self.parent      = parent
        self.mc_position = initial_mc_position
        self.mc_coords   = [self.mc_position.x*100+49, self.mc_position.y*100+49]
        self.initUI()
        
    def initUI(self):
        #--- simple placeholder - to be changed ---#
        self.controlMc()
        
        #self.setWindowTitle("Test")
        self.setGeometry(0, 0, 500, 400)
        #self.show()
        
    def controlMc(self):
        """ Assign mc attributes. """
        
        self.mc_walking        = False
        self.arrow_shooting    = False
        self.times_arrow_moved = 0
        self.tile_width        = 100
        self.space_pressed     = False

        self.pixmap   = QtGui.QPixmap("mc_ph.png")
        self.mc_view  = McView(self)
        self.mc_scene = QtGui.QGraphicsScene(QtCore.QRectF(0,0,500,400), self.mc_view)
        self.mc_view.setScene(self.mc_scene)
        self.mc_view.setStyleSheet("background: transparent")

        self.mc_char  = self.mc_scene.addPixmap(self.pixmap)
        
        self.mc_char.setPos(self.mc_coords[0], self.mc_coords[1])
        
    def keyPressEvent(self, e):
        """ Define actions for all key press events. """

        if self.mc_walking == False and self.arrow_shooting == False: # no input allowed while mc is walking
            #--- left arrow --#
            if e.key() == QtCore.Qt.Key_Left:
                print("--Left Arrow")
                
                if self.space_pressed == False and self.parent.tile_dic[self.mc_position].W_open:
                    # move player position
                    self.mc_walking = True
                    self.animateMc(0, -1)
                    self.parent.parent.endTurn()
                else:
                    # move arrow position
                    self.arrow_shooting = True
                    self.moveArrow("left")
                    pass
                
                print(self.mc_coords)
            
            #--- right arrow ---#
            if e.key() == QtCore.Qt.Key_Right:
                print("--Right Arrow")
                
                if self.space_pressed == False and self.parent.tile_dic[self.mc_position].E_open:
                    # move player position
                    self.mc_walking = True
                    self.animateMc(0, 1)
                    self.parent.parent.endTurn()
                else:
                    # move arrow position
                    self.arrow_shooting = True
                    self.moveArrow("right")
                    pass
            
                print(self.mc_coords)
        
            #--- up arrow ---#
            if e.key() == QtCore.Qt.Key_Up:
                print("--Up Arrow")
            
                if self.space_pressed == False and self.parent.tile_dic[self.mc_position].N_open:
                    # move player position
                    self.mc_walking = True
                    self.animateMc(1, -1)
                    self.parent.parent.endTurn()
                else:
                    # move arrow position
                    self.arrow_shooting = True
                    self.moveArrow("up")
                    pass
            
                print(self.mc_coords)
            
            #--- down arrow ---#
            if e.key() == QtCore.Qt.Key_Down:
                print("--Down Arrow")
                
                if self.space_pressed == False and self.parent.tile_dic[self.mc_position].S_open:
                    # move player position
                    self.mc_walking = True
                    self.animateMc(1, 1)
                    self.parent.parent.endTurn()
                else:
                    # move arrow position
                    self.arrow_shooting = True
                    self.moveArrow("down")
                    pass
                
                print(self.mc_coords)
            
            #--- space ---#    
            if e.key() == QtCore.Qt.Key_Space:
                print("--Space")
                
                if self.space_pressed == True:
                    self.space_pressed = False
                    self.initializeArrow(False) # remove arrow
                    print("Arrow canceled")
                else:
                    self.space_pressed = True
                    self.initializeArrow(True) # create arrow
                    print("Arrow ready")
                
                print(self.space_pressed == True)
                
            #--- return ---#
            if e.key() == QtCore.Qt.Key_Return:
                print("--Return")
                if self.space_pressed == True:
                    self.space_pressed = False
                    print("Arrow shot")
                    self.parent.parent.endTurn()
            

    def animateMc(self, x_or_y, direction):
        self.stepcounter = 0
        while self.mc_walking == True:
            time.sleep(0.01)
            self.mc_coords[x_or_y] += direction
            self.stepcounter += 1
            self.mc_char.setPos(self.mc_coords[0], self.mc_coords[1]) # change mc position to new coordinates
            QtGui.QApplication.processEvents() # needed to update gui, normally won"t update during loop
            if self.stepcounter == self.tile_width: # stop loop when the mc has traveled the length of one tile
                self.mc_walking = False

    def animateArrow(self, x_or_y, direction):
        self.stepcounter = 0        
        while self.arrow_shooting == True:    
            time.sleep(0.01)
            self.arrow_coords[x_or_y] += direction
            self.stepcounter += 1
            self.arrow.setPos(self.arrow_coords[0], self.arrow_coords[1]) # change arrow position to new coordinates
            QtGui.QApplication.processEvents() # needed to update gui, normally won"t update during loop
            if self.stepcounter == self.tile_width: # stop loop when the arrow has traveled the length of one tile
                self.arrow_shooting = False
                
    def initializeArrow(self, create_arrow):
        self.times_arrow_moved = 0
        if create_arrow == True:
            self.arrow_pixmap = QtGui.QPixmap("images/arrow.png")
            self.arrow  = self.mc_scene.addPixmap(self.arrow_pixmap)
            self.arrow.setTransformOriginPoint(self.arrow_pixmap.width() / 2, self.arrow_pixmap.height() / 2)
            self.arrow_coords = self.mc_coords[:] # copy mc coordinates
            self.arrow.setPos(self.arrow_coords[0], self.arrow_coords[1])
        else:
            # needs to remove arrow
            self.mc_scene.removeItem(self.arrow)
            pass
        
    def moveArrow(self, key):        
        if self.times_arrow_moved >= 5:
            self.arrow_shooting = False
            print("Arrow too far, can't move any further")
        else:
            self.times_arrow_moved += 1
            if key == "left":
                self.arrow.setRotation(180)
                self.animateArrow(0, -1)
            if key == "right":
                self.arrow.setRotation(0)
                self.animateArrow(0, 1)
            if key == "up":
                self.arrow.setRotation(270)
                self.animateArrow(1, -1)
            if key == "down":
                self.arrow.setRotation(90)
                self.animateArrow(1, 1)

    def updateMcPosition(self):
        self.mc_position = ((self.mc_coords[0]-49)/100, (self.mc_coords[1]-49)/100)
            


def main():
    app = QtGui.QApplication(sys.argv)
    mc = Mc()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
