#!/usr/bin/env python

import sys
import random
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui

class McView (QtGui.QGraphicsView):
    def __init__(self, parent = None):
        super(McView, self).__init__(parent)

    def keyPressEvent(self, e):
        self.parentWidget().keyPressEvent(e)

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
        
        self.mc_walking    = False
        self.tile_width    = 20
        self.space_pressed = False
        self.mc_coords     = [20, 20] #---> change default player coordinates to random

        self.pixmap   = QtGui.QPixmap("mc_ph.png")
        self.mc_view  = McView(self)
        self.mc_scene = QtGui.QGraphicsScene(QtCore.QRectF(0,0,500,400), self.mc_view)
        self.mc_view.setScene(self.mc_scene)

        self.mc_char  = self.mc_scene.addPixmap(self.pixmap)
        
        self.moveMc()
        
    def keyPressEvent(self, e):
        """ Define actions for all key press events. """

        if self.mc_walking == False: # no input allowed while mc is walking
            #--- left arrow --#
            if e.key() == QtCore.Qt.Key_Left:
                print("--Left Arrow")
                
                if self.space_pressed == False:
                    self.mc_walking = True
                    self.animateMc(0, -1)
                else:
                    # move arrow position
                    pass
                
                print(self.mc_coords)
            
            #--- right arrow ---#
            if e.key() == QtCore.Qt.Key_Right:
                print("--Right Arrow")
                
                if self.space_pressed == False:
                    self.mc_walking = True
                    self.animateMc(0, 1)
                else:
                    # move arrow position
                    pass
            
                print(self.mc_coords)
        
            #--- up arrow ---#
            if e.key() == QtCore.Qt.Key_Up:
                print("--Up Arrow")
            
                if self.space_pressed == False:
                    self.mc_walking = True
                    self.animateMc(1, -1)
                else:
                    # move arrow position
                    pass
            
                print(self.mc_coords)
            
            #--- down arrow ---#
            if e.key() == QtCore.Qt.Key_Down:
                print("--Down Arrow")
                
                if self.space_pressed == False:
                    self.mc_walking = True
                    self.animateMc(1, 1)
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
        else:
            pass

    def animateMc(self, l_or_r, u_or_d):
        self.stepcounter = 0
        while self.mc_walking == True:
            time.sleep(0.02)
            self.mc_coords[l_or_r] += u_or_d
            self.stepcounter += 1
            self.mc_char.setOffset(self.mc_coords[0], self.mc_coords[1])
            #self.moveMc()
            QtGui.QApplication.processEvents()
            if self.stepcounter == self.tile_width:
                self.mc_walking = False
        
    def moveMc(self):
        print('moving')
        self.mc_char.setOffset(self.mc_coords[0], self.mc_coords[1])
        #self.mc_view.centerOn(self.mc_coords[0], self.mc_coords[1])
            


def main():
    app = QtGui.QApplication(sys.argv)
    mc = Mc()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()