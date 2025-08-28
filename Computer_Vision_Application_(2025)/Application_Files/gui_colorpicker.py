# gui_colorpicker.py
# Created by Ariana Beeby, Max Figura, and Jason Jopp for CSC443
# Custom color-picker interface for Computer Vision project

# NOTE: some functionalities modified from Qt source for QColorDialog

import sys

from PySide6 import QtCore as qc
from PySide6 import QtWidgets as qw
from PySide6 import QtGui as qg

class ColorPicker(qw.QWidget):
    
    # Sends a signal to the main GUI to connect to functionality
    colorChanged = qc.Signal()
    
    def __init__(self, window=None, gui_parent=None):
        """ Constructs the color-picker widget
        """
        super().__init__(gui_parent)
        self.window = window 
        self.gui_parent = gui_parent
        
        # 1 for RGB, 2 for HSV (default RGB)
        self.color_mode = 1
        self.stored_color = qg.QColor(0, 0, 0)
        self.using_range = False
        self.second_color = qg.QColor(0, 0, 0)
        self.preview_file = ""
        self.do_get_range_preview = lambda x, y: print("Get preview file functionality not connected")
        # 1 for first color, 2 for second color, 0 for neither
        self.sample_requestor = 0
        
        # Manual color inputs
        self.num1_text = qw.QLabel("Red:", alignment=qc.Qt.AlignRight|qc.Qt.AlignVCenter)
        self.num1_entry = qw.QSpinBox()
        self.num1_entry.setValue(0)
        self.num1_entry.setRange(0,255)
        self.num1_entry.valueChanged.connect(self.updateNum1)
        self.num2_text = qw.QLabel("Green:", alignment=qc.Qt.AlignRight|qc.Qt.AlignVCenter)
        self.num2_entry = qw.QSpinBox()
        self.num2_entry.setValue(0)
        self.num2_entry.setRange(0,255)
        self.num2_entry.valueChanged.connect(self.updateNum2)
        self.num3_text = qw.QLabel("Blue:", alignment=qc.Qt.AlignRight|qc.Qt.AlignVCenter)
        self.num3_entry = qw.QSpinBox()
        self.num3_entry.setValue(0)
        self.num3_entry.setRange(0,255)
        self.num3_entry.valueChanged.connect(self.updateNum3)
        
        # 2nd block of color inputs - not enabled by default
        self.num4_entry = qw.QSpinBox()
        self.num4_entry.setValue(0)
        self.num4_entry.setRange(0,255)
        self.num4_entry.valueChanged.connect(self.updateNum4)
        self.num5_entry = qw.QSpinBox()
        self.num5_entry.setValue(0)
        self.num5_entry.setRange(0,255)
        self.num5_entry.valueChanged.connect(self.updateNum5)
        self.num6_entry = qw.QSpinBox()
        self.num6_entry.setValue(0)
        self.num6_entry.setRange(0,255)
        self.num6_entry.valueChanged.connect(self.updateNum6)
        
        # Preview - fills a small Pixmap with the selected color and places it in a Label
        self.preview_lab = qw.QLabel(alignment=qc.Qt.AlignCenter)
        self.preview_pix = qg.QPixmap(50, 50)
        self.preview_pix.fill(qg.QColor(0,0,0))
        self.preview_lab.setPixmap(self.preview_pix)
        self.preview2_lab = qw.QLabel(alignment=qc.Qt.AlignCenter)
        self.preview2_pix = qg.QPixmap(50, 50)
        self.preview2_pix.fill(qg.QColor(0,0,0))
        self.preview2_lab.setPixmap(self.preview2_pix)
        
        # Sampler button
        self.sample_but = qw.QPushButton("Sample")
        self.sample2_but = qw.QPushButton("Sample")
        self.sample_but.clicked.connect(self.startSampleMode)
        self.sample2_but.clicked.connect(self.startSample2Mode)
        
        # Grid layout for individual colors - numerical input, then preview, then sampler
        self.color_inp_layout = qw.QGridLayout()
        self.color_inp_layout.addWidget(self.num1_text, 0, 0)
        self.color_inp_layout.addWidget(self.num1_entry, 0, 1)
        self.color_inp_layout.addWidget(self.num2_text, 1, 0)
        self.color_inp_layout.addWidget(self.num2_entry, 1, 1)
        self.color_inp_layout.addWidget(self.num3_text, 2, 0)
        self.color_inp_layout.addWidget(self.num3_entry, 2, 1)
        self.color_inp_layout.addWidget(self.preview_lab, 3, 1)
        self.color_inp_layout.addWidget(self.sample_but, 4, 1)
        
        # 2nd color inputs in same grid but hidden by default
        self.color_inp_layout.addWidget(self.num4_entry, 0, 2)
        self.color_inp_layout.addWidget(self.num5_entry, 1, 2)
        self.color_inp_layout.addWidget(self.num6_entry, 2, 2)
        self.color_inp_layout.addWidget(self.preview2_lab, 3, 2)
        self.color_inp_layout.addWidget(self.sample2_but, 4, 2)
        self.num4_entry.hide()
        self.num5_entry.hide()
        self.num6_entry.hide()
        self.preview2_lab.hide()
        self.sample2_but.hide()
        
        # Buttons to swap color mode and activate range mode
        self.mode_but = qw.QPushButton("Input HSV")
        self.mode_but.clicked.connect(self.toggleColorMode)
        self.twocolor_but = qw.QPushButton("Use two-color range selection")
        self.twocolor_but.clicked.connect(self.toggleTwocolor)
        
        # Color inputs on top of input options
        self.main_layout = qw.QVBoxLayout()
        self.main_layout.addLayout(self.color_inp_layout)
        self.main_layout.addWidget(self.mode_but)
        self.main_layout.addWidget(self.twocolor_but)
        
        # Range display - render takes a few seconds, so user should prompt when desired
        self.range_render_but = qw.QPushButton("Update Range")
        self.range_render_but.clicked.connect(self.updateRange)
        self.range_lab = qw.QLabel(alignment=qc.Qt.AlignCenter)
        self.range_pix = qg.QPixmap(50, 50)
        self.range_pix.fill(qg.QColor(255,255,255))
        self.range_lab.setPixmap(self.range_pix)
        # Spacer seems to mess up layout, somehow
        #self.range_spacer = qw.QSpacerItem(0, 0, vData=qw.QSizePolicy.MinimumExpanding)
        
        # Render button over label, but both hidden by default
        self.range_layout = qw.QVBoxLayout()
        self.range_layout.addWidget(self.range_render_but)
        self.range_layout.addWidget(self.range_lab)
        #self.range_layout.addSpacerItem(self.range_spacer)
        self.range_render_but.hide()
        self.range_lab.hide()
        
        # Input next to sampler and preview
        self.layout = qw.QHBoxLayout(self.gui_parent if self.gui_parent else self)
        self.layout.addLayout(self.main_layout)
        self.layout.addLayout(self.range_layout)
        
        # Event filter to process color sampling inputs
        self.event_filter = ColorSampleEventFilter(self)
        self.window.installEventFilter(self.event_filter)
        
    def connectGetRangePreview(self, grp_fun):
        """ Sets up the ColorPicker to use a function to get a color range map
        
        Parameters
        ----------
        grp_fun : function
            The function by which to retrieve a color range map
        """
        self.do_get_range_preview = grp_fun
        return
        
    def getColor(self):
        return self.stored_color
    
    def usingRange(self):
        return self.using_range
    
    def getSecondColor(self):
        return self.second_color
    
    def setColor(self, color=qg.QColor(0, 0, 0)):
        """ Updates the selected color
        
        Parameters
        -------
        color : QColor
            The color selected by the user (or leave blank to reset to black)
        """
        self.stored_color = color
        # Update display
        if self.color_mode==1:
            self.num1_entry.setValue(self.stored_color.red())
            self.num2_entry.setValue(self.stored_color.green())
            self.num3_entry.setValue(self.stored_color.blue())
        elif self.color_mode==2:
            self.num1_entry.setValue(self.stored_color.hue())
            self.num2_entry.setValue(self.stored_color.saturation())
            self.num3_entry.setValue(self.stored_color.value())
        self.updatePreview()
        
        # Signal parent GUI
        self.colorChanged.emit()
        return
    
    def setColor2(self, color=qg.QColor(0, 0, 0)):
        """ Updates the selected second color
        
        Parameters
        -------
        color : QColor
            The color selected by the user (or leave blank to reset to black)
        """
        self.second_color = color
        # Update display
        if self.color_mode==1:
            self.num4_entry.setValue(self.second_color.red())
            self.num5_entry.setValue(self.second_color.green())
            self.num6_entry.setValue(self.second_color.blue())
        elif self.color_mode==2:
            self.num4_entry.setValue(self.second_color.hue())
            self.num5_entry.setValue(self.second_color.saturation())
            self.num6_entry.setValue(self.second_color.value())
        self.updatePreview2()
        
        # Signal parent GUI
        self.colorChanged.emit()
        return
    
    def updatePreview(self):
        """ Updates the preview box to display the current first color
        """
        self.preview_pix.fill(self.stored_color)
        self.preview_lab.setPixmap(self.preview_pix)
        return
    
    def updatePreview2(self):
        """ Updates the preview box to display the current second color
        """
        self.preview2_pix.fill(self.second_color)
        self.preview2_lab.setPixmap(self.preview2_pix)
        return
    
    @qc.Slot()
    def updateRange(self):
        """ Updates the preview box to display the current range of colors
        
        Called by range-render button (or when two-color mode is activated)
        """
        # Request color range map
        self.range_pix = self.do_get_range_preview(self.stored_color, self.second_color)
        if self.range_pix:
            self.range_lab.setPixmap(self.range_pix)
            return
        
    @qc.Slot()
    def updateNum1(self, new_num1):
        """ Updates the red/hue value from numerical input
        
        Called when the num1 entry is updated
        
        Parameters
        -------
        new_num1 : int
            The new value of the num1 entry
        """
        if self.color_mode==1:
            # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num1!=self.stored_color.red():
                # Using toRgb to clone stored_color
                new_color = self.stored_color.toRgb()
                new_color.setRed(new_num1)
                self.setColor(new_color)
        elif self.color_mode==2:
             # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num1!=self.stored_color.hue():
                new_color = qg.QColor.fromHsv(new_num1, self.stored_color.saturation(), self.stored_color.value())
                self.setColor(new_color)
        return
    
    @qc.Slot()
    def updateNum2(self, new_num2):
        """ Updates the green/saturation value from numerical input
        
        Called when the num2 entry is updated
        
        Parameters
        -------
        new_num2 : int
            The new value of the num2 entry
        """
        if self.color_mode==1:
            # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num2!=self.stored_color.green():
                # Using toRgb to clone stored_color
                new_color = self.stored_color.toRgb()
                new_color.setGreen(new_num2)
                self.setColor(new_color)
        elif self.color_mode==2:
             # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num2!=self.stored_color.saturation():
                new_color = qg.QColor.fromHsv(self.stored_color.hue(), new_num2, self.stored_color.value())
                self.setColor(new_color)
        return
    
    @qc.Slot()
    def updateNum3(self, new_num3):
        """ Updates the blue/value value from numerical input
        
        Called when the num3 entry is updated
        
        Parameters
        -------
        new_num3 : int
            The new value of the num3 entry
        """
        # Should evaluate to True if caused by user entry, False if caused by color update
        if self.color_mode==1:
            if new_num3!=self.stored_color.blue():
                # Using toRgb to clone stored_color
                new_color = self.stored_color.toRgb()
                new_color.setBlue(new_num3)
                self.setColor(new_color)
        elif self.color_mode==2:
             # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num3!=self.stored_color.value():
                new_color = qg.QColor.fromHsv(self.stored_color.hue(), self.stored_color.saturation(), new_num3)
                self.setColor(new_color)
        return
    
    @qc.Slot()
    def updateNum4(self, new_num4):
        """ Updates the second red/hue value from numerical input
        
        Called when the num4 entry is updated
        
        Parameters
        -------
        new_num4 : int
            The new value of the num4 entry
        """
        if self.color_mode==1:
            # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num4!=self.second_color.red():
                # Using toRgb to clone stored_color
                new_color = self.second_color.toRgb()
                new_color.setRed(new_num4)
                self.setColor2(new_color)
        elif self.color_mode==2:
             # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num4!=self.second_color.hue():
                new_color = qg.QColor.fromHsv(new_num4, self.second_color.saturation(), self.second_color.value())
                self.setColor2(new_color)
        return
    
    @qc.Slot()
    def updateNum5(self, new_num5):
        """ Updates the second green/saturation value from numerical input
        
        Called when the num5 entry is updated
        
        Parameters
        -------
        new_num5 : int
            The new value of the num5 entry
        """
        if self.color_mode==1:
            # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num5!=self.second_color.green():
                # Using toRgb to clone stored_color
                new_color = self.second_color.toRgb()
                new_color.setGreen(new_num5)
                self.setColor2(new_color)
        elif self.color_mode==2:
             # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num5!=self.second_color.saturation():
                new_color = qg.QColor.fromHsv(self.second_color.hue(), new_num5, self.second_color.value())
                self.setColor2(new_color)
        return
    
    @qc.Slot()
    def updateNum6(self, new_num6):
        """ Updates the second blue/value value from numerical input
        
        Called when the num6 entry is updated
        
        Parameters
        -------
        new_num6 : int
            The new value of the num6 entry
        """
        # Should evaluate to True if caused by user entry, False if caused by color update
        if self.color_mode==1:
            if new_num6!=self.second_color.blue():
                # Using toRgb to clone stored_color
                new_color = self.second_color.toRgb()
                new_color.setBlue(new_num6)
                self.setColor2(new_color)
        elif self.color_mode==2:
             # Should evaluate to True if caused by user entry, False if caused by color update
            if new_num6!=self.second_color.value():
                new_color = qg.QColor.fromHsv(self.second_color.hue(), self.second_color.saturation(), new_num6)
                self.setColor2(new_color)
        return
    
    @qc.Slot()
    def toggleColorMode(self):
        """ Switches between RGB and HSV input
        
        Called when toggle mode button is clicked
        """
        if self.color_mode==1:
            self.color_mode = 2
            # Update labels
            self.num1_text.setText("Hue:")
            self.num2_text.setText("Saturation:")
            self.num3_text.setText("Value:")
            self.mode_but.setText("Input RGB")
            # Hue has different value space
            self.num1_entry.setRange(0,359)
            self.num4_entry.setRange(0,359)
        elif self.color_mode==2:
            self.color_mode = 1
            # Update labels
            self.num1_text.setText("Red:")
            self.num2_text.setText("Green:")
            self.num3_text.setText("Blue:")
            self.mode_but.setText("Input HSV")
            # Hue has different value space
            self.num1_entry.setRange(0,255)
            self.num4_entry.setRange(0,255)
        self.setColor(self.stored_color)
        self.setColor2(self.second_color)
        
    @qc.Slot()
    def toggleTwocolor(self):
        """ Switches between single-color and range input
        
        Called when toggle twocolor button is clicked
        """
        if self.using_range:
            self.using_range = False
            self.num4_entry.hide()
            self.num5_entry.hide()
            self.num6_entry.hide()
            self.preview2_lab.hide()
            self.sample2_but.hide()
            self.range_render_but.hide()
            self.range_lab.hide()
            self.twocolor_but.setText("Use two-color range selection")
        else:
            self.using_range = True
            self.num4_entry.show()
            self.num5_entry.show()
            self.num6_entry.show()
            self.preview2_lab.show()
            self.sample2_but.show()
            self.range_render_but.show()
            self.range_lab.show()
            self.twocolor_but.setText("Select single color")
            self.updateRange()
        # Notify parent GUI that color range setting has changed
        self.colorChanged.emit()
        return
    
    @qc.Slot()
    def startSampleMode(self):
        """ Enables color-sampling mode for first color
        
        Called when sample button is clicked
        """
        # Enable filter to capture color sampling
        self.sample_requestor = 1
        self.event_filter.setActive(True)
        
        # Disable mouse from making other inputs
        self.window.grabMouse(qc.Qt.CrossCursor)
        return
    
    @qc.Slot()
    def startSample2Mode(self):
        """ Enables color-sampling mode for second color
        
        Called when sample2 button is clicked
        """
        # Enable filter to capture color sampling
        self.sample_requestor = 2
        self.event_filter.setActive(True)
        
        # Disable mouse from making other inputs
        self.window.grabMouse(qc.Qt.CrossCursor)
        return
    
    def takeSample(self):
        """ Samples the color at the current mouse position and then ends sample mode
        """
        if self.sample_requestor==1:
            self.setColor(self.screenColorAt(qg.QCursor.pos()))
        elif self.sample_requestor==2:
            self.setColor2(self.screenColorAt(qg.QCursor.pos()))
        self.endSampleMode()
        return
    
    def endSampleMode(self):
        """ Exits color sampling mode
        """
        self.event_filter.setActive(False)
        self.sample_requestor = 0
        self.window.releaseMouse()
        return

    def screenColorAt(self, point):
        """ Finds the color of a pixel on the user's screen
    
        Parameters
        ----------
        point : QPoint
            A location on the screen
        
        Returns
        -------
        sampled_color : QColor
            The color of the pixel at the given point
        """
        screen = qg.QGuiApplication.screenAt(point)
        if (not screen):
            screen = qgQGuiApplication.primaryScreen()
        screen_rect = screen.geometry()
        
        # Turn the screen into a pixmap consisting only of the single pixel, then find the color of that pixel.
        pixmap = screen.grabWindow(0, point.x() - screen_rect.x(), point.y() - screen_rect.y(), 1, 1)
        sampled_color = pixmap.toImage().pixelColor(0, 0)
        return sampled_color
                
""" Helper class for ColorPicker - intercepts input events during color sample mode
"""
class ColorSampleEventFilter(qc.QObject):
    
    def __init__(self, picker=None):
        super().__init__(picker)
        self.picker = picker
        
        # Event filter is active when in color-sampling mode
        self.active = False
    
    def setActive(self, state):
        self.active = state
    
    def eventFilter(self, source, event):
        """ Intercepts input events in sample mode
    
        Parameters
        ----------
        source : QWidget
            The application reporting the event (unused)
        event : QEvent
            The GUI event detected
        
        Returns
        -------
        processed : bool
            Whether the input event was processed or ignored
        """
        if(not self.active):return False
        if(event.type()==qc.QEvent.MouseButtonRelease):
            # Update color according to current mouse location
            self.picker.takeSample()
            return True
        if(event.type()==qc.QEvent.KeyPress):
            # Cancel color selection mode
            self.picker.endSampleMode()
            return True
        return False
