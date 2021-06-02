import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

class MenuBox(pg.GraphicsObject):
    """
    This class draws a rectangular area. Right-clicking inside the area will
    raise a custom context menu which also includes the context menus of
    its parents.
    """
    def __init__(self, name):
        self.name = name
        self.pen = pg.mkPen('r')

        # menu creation is deferred because it is expensive and often
        # the user will never see the menu anyway.
        self.menu = None
        self.mode=name


        # note that the use of super() is often avoided because Qt does not
        # allow to inherit from multiple QObject subclasses.
        pg.GraphicsObject.__init__(self)


    # All graphics items must have paint() and boundingRect() defined.
    def boundingRect(self):
        # return  pg.RectROI(pos=[0,0], size=[100, 200])
        return QtCore.QRectF(0, 0, 100, 200)

    def paint(self, p, *args):
        p.setPen(self.pen)
        p.drawRect(self.boundingRect())


    # On right-click, raise the context menu
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            if self.raiseContextMenu(ev):
                ev.accept()

    def raiseContextMenu(self, ev):
        menu = self.getContextMenus()

        # Let the scene add on to the end of our context menu
        # (this is optional)
        menu = self.scene().addParentContextMenus(self, menu, ev)

        pos = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))
        return True

    # This method will be called when this item's _children_ want to raise
    # a context menu that includes their parents' menus.
    def getContextMenus(self, event=None):
        if self.menu is None:
            self.menu = QtGui.QMenu()
            self.menu.setTitle(self.name)

            if self.mode=='filter':
                bandpass = QtGui.QAction("Bandpass", self.menu)
                bandpass.triggered.connect(self.setGreen)
                self.menu.addAction(bandpass)
                self.menu.bandpass = bandpass

                bandstop = QtGui.QAction("Bandstop", self.menu)
                bandstop.triggered.connect(self.setRed)
                self.menu.addAction(bandstop)
                self.menu.bandstop = bandstop


                    # self.menu.green = blue
            elif self.mode=='background':
                newFilter = QtGui.QAction("New Filter", self.menu)
                newFilter.triggered.connect(self.newFilter)
                self.menu.addAction(newFilter)

            elif self.mode=='slider':
                alpha = QtGui.QWidgetAction(self.menu)
                alphaSlider = QtGui.QSlider()
                alphaSlider.setOrientation(QtCore.Qt.Horizontal)
                alphaSlider.setMaximum(255)
                alphaSlider.setValue(255)
                alphaSlider.valueChanged.connect(self.setAlpha)
                alpha.setDefaultWidget(alphaSlider)
                self.menu.addAction(alpha)
                self.menu.alpha = alpha
                self.menu.alphaSlider = alphaSlider

        return self.menu

    # Define context menu callbacks
    def setGreen(self):
        self.pen = pg.mkPen('g')
        # inform Qt that this item must be redrawn.
        self.update()

    def setBlue(self):
        self.pen = pg.mkPen('b')
        self.update()

    def setRed(self):
        self.pen = pg.mkPen('r')
        self.update()

    def newFilter(self):
        print('add new filter')

    def setAlpha(self, a):
        self.setOpacity(a/255.)
