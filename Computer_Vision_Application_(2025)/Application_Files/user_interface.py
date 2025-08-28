# user_interface.py
# Created by Ariana Beeby, Max Figura, and Jason Jopp for CSC443
# Graphical interface program for Computer Vision project

import sys
from PySide6 import QtCore as qc
from PySide6 import QtWidgets as qw
from PySide6 import QtGui as qg
from PySide6 import QtMultimedia as qm
from PySide6.QtMultimediaWidgets import QVideoWidget

# Using self-created color picker widget
from gui_colorpicker import ColorPicker

#TODO fix file type selection?
#TODO fix offset for contour point selection
#TODO fix invalid file import

class PrimaryWindow(qw.QWidget):
    def __init__(self):
        """ Initialises the GUI window with controls for object recognition
        """
        super().__init__()
        self.setWindowTitle("Image Color Analysis Tool")
        
        # Input parameters/options
        self.bef_file = ""
        self.is_video = False
        self.aft_file = ""
        self.save_file = ""
        self.picked_color = None
        self.using_range = False
        self.second_color = None
        # 1 = blobs, 2 = contours
        self.detect_mode = 1
        self.kernel_size = 0
        self.contour_point = (0.0, 0.0)
        
        # Filetype search options
        self.filetype_str = "PNG Image Files (*.png);;JPEG Image Files (*.jpeg *.jpg);;Video Files (*.mp4 *.mov *.avi);;All Files (*)"
        
        # Functionalities (reassigned by controller with calls to model)
        self.do_analysis = lambda x, a, b, c, d, e: print("Analysis functionality not connected")
        self.do_video_analysis = lambda x, a, b, c, d: print("Video analysis functionality not connected")
        self.do_filesave = lambda x, y: print("File output functionality not connected")
        self.do_get_cp_range_file = lambda x, y: print("Get CP range file functionality not connected")
        self.do_get_video_frame = lambda x: print("Get video frame functionality not connected")
        
        # Object to read image files to pixmap
        self.image_reader = qg.QImageReader()
        
        # Automatic image display sizing - should be at most a quarter of a 1920x1080 display
        self.max_pic_h = 540
        self.max_pic_w = 960
        
        # Keep track of output image size ratio
        self.aft_size = qc.QSize()
        self.save_height = 0
        self.save_width = 0
        
        # Raw numpy array representing processed image (only passed back through main)
        self.raw_image_struct = None
        
        # ========== CONTROLS ========== #
        # File selection
        self.choose_file_text = qw.QLabel("No image selected.", alignment=qc.Qt.AlignCenter)
        self.choose_file_but = qw.QPushButton("Select File")
        self.choose_file_but.clicked.connect(self.chooseInfile)
        
        # Color choice
        self.color_picker_box = qw.QGroupBox("Color to Detect")
        self.color_picker = ColorPicker(self, self.color_picker_box)
        self.color_picker.colorChanged.connect(self.updateColor)
        self.color_picker.connectGetRangePreview(self.getCPRangeMap)
        
        # Kernel size selection
        self.kernel_size_text = qw.QLabel("Processing kernel radius:", alignment=qc.Qt.AlignRight|qc.Qt.AlignVCenter)
        self.kernel_size_inp = qw.QSpinBox()
        self.kernel_size_inp.setValue(self.kernel_size)
        self.kernel_size_inp.setRange(0,99)
        self.kernel_size_inp.valueChanged.connect(self.updateKernelSize)
        
        # Label/input side-by-side
        self.kernel_size_layout = qw.QHBoxLayout()
        self.kernel_size_layout.addWidget(self.kernel_size_text)
        self.kernel_size_layout.addWidget(self.kernel_size_inp)
        
        # Detection mode option
        self.detect_mode_text = qw.QLabel("Using blob detection", alignment=qc.Qt.AlignRight|qc.Qt.AlignVCenter)
        self.detect_mode_but = qw.QPushButton("Use contours")
        self.detect_mode_but.clicked.connect(self.updateDetectMode)
        
        # Label/input side-by-side
        self.detect_mode_layout = qw.QHBoxLayout()
        self.detect_mode_layout.addWidget(self.detect_mode_text)
        self.detect_mode_layout.addWidget(self.detect_mode_but)
        
        # Contour point selection
        self.contour_point_text = qw.QLabel("No point selected", alignment=qc.Qt.AlignRight|qc.Qt.AlignVCenter)
        self.contour_point_but = qw.QPushButton("Select a point in the image")
        self.contour_point_but.clicked.connect(self.pickContourPoint)
        
        # Label/input side-by-side
        self.contour_point_layout = qw.QHBoxLayout()
        self.contour_point_layout.addWidget(self.contour_point_text)
        self.contour_point_layout.addWidget(self.contour_point_but)
        self.contour_point_text.hide()
        self.contour_point_but.hide()
        
        # Activate button - disabled until user selects image and color
        self.activate_but = qw.QPushButton("Analyse")
        self.activate_but.setDisabled(True)
        self.activate_but.clicked.connect(self.analyseImage)
        
        # Keep input options compact apart from analyse button
        self.options_analyse_spacer = qw.QSpacerItem(0, 0, vData=qw.QSizePolicy.MinimumExpanding)
        
        # Controls laid out vertically
        self.controls_layout = qw.QVBoxLayout()
        self.controls_layout.addWidget(self.choose_file_text)
        self.controls_layout.addWidget(self.choose_file_but)
        self.controls_layout.addWidget(self.color_picker_box)
        self.controls_layout.addLayout(self.kernel_size_layout)
        self.controls_layout.addLayout(self.detect_mode_layout)
        self.controls_layout.addLayout(self.contour_point_layout)
        self.controls_layout.addSpacerItem(self.options_analyse_spacer)
        self.controls_layout.addWidget(self.activate_but)
        
        # ========== IMAGE DISPLAY ========== #
        # Label widgets to display
        self.bef_display = qw.QLabel(alignment=qc.Qt.AlignCenter)
        self.aft_display = qw.QLabel(alignment=qc.Qt.AlignCenter)
        
        # Not worrying about video player right now
        # self.bef_vid_player = qm.QMediaPlayer()
        # self.bef_vid_player.setSource(qc.QUrl.fromLocalFile("images/video_simple.mp4"))
        # self.bef_vid_display = QVideoWidget()
        # self.bef_vid_player.setVideoOutput(self.bef_vid_display)
        # self.bef_vid_display.show()
        # self.bef_vid_player.play()
        
        # Save file location selection
        self.save_file_loc = qw.QLabel("No output to save")
        self.save_file_select_but = qw.QPushButton("Change Location")
        self.save_file_select_but.setDisabled(True)
        self.save_file_select_but.clicked.connect(self.chooseOutfile)
        
        # Save file size selection
        self.save_width_text = qw.QLabel("Width:", alignment=qc.Qt.AlignRight|qc.Qt.AlignVCenter)
        self.save_width_inp = qw.QSpinBox()
        self.save_width_inp.setRange(1,10000)
        self.save_width_inp.setDisabled(True)
        self.save_width_inp.valueChanged.connect(self.updateImageSaveSize)
        self.save_height_text = qw.QLabel("Height:", alignment=qc.Qt.AlignRight|qc.Qt.AlignVCenter)
        self.save_height_inp = qw.QSpinBox()
        self.save_height_inp.setRange(1,10000)
        self.save_height_inp.setDisabled(True)
        self.save_height_inp.valueChanged.connect(self.updateImageSaveSize)
        
        # Save button
        self.save_file_but = qw.QPushButton("Save Output")
        self.save_file_but.setDisabled(True)
        self.save_file_but.clicked.connect(self.saveImage)
        
        # Initial appearance - show message
        self.bef_display.setText("Select an image using the button to the left")
        
        # Keep image save size options compact apart from location chooser
        self.outfile_size_spacer = qw.QSpacerItem(0, 0, hData=qw.QSizePolicy.MinimumExpanding)
        
        # Side-by-side buttons in save options
        self.save_opt_layout = qw.QHBoxLayout()
        self.save_opt_layout.addWidget(self.save_file_select_but)
        self.save_opt_layout.addSpacerItem(self.outfile_size_spacer)
        self.save_opt_layout.addWidget(self.save_width_text)
        self.save_opt_layout.addWidget(self.save_width_inp)
        self.save_opt_layout.addWidget(self.save_height_text)
        self.save_opt_layout.addWidget(self.save_height_inp)
        
        # Keep image save options compact apart from image displays
        self.display_save_spacer = qw.QSpacerItem(0, 0, vData=qw.QSizePolicy.MinimumExpanding)
        
        # Before/after/save displayed vertically
        self.images_layout = qw.QVBoxLayout()
        self.images_layout.addWidget(self.bef_display)
        self.images_layout.addWidget(self.aft_display)
        self.images_layout.addSpacerItem(self.display_save_spacer)
        self.images_layout.addWidget(self.save_file_loc)
        self.images_layout.addLayout(self.save_opt_layout)
        self.images_layout.addWidget(self.save_file_but)
        
        # Keep input options compact apart from images
        self.option_image_spacer = qw.QSpacerItem(0, 0, hData=qw.QSizePolicy.MinimumExpanding)
        
        # Images show next to options
        self.layout = qw.QHBoxLayout(self)
        self.layout.addLayout(self.controls_layout)
        self.layout.addSpacerItem(self.option_image_spacer)
        self.layout.addLayout(self.images_layout)
        
        # Event filter to process contour point pick inputs
        self.point_pick_filter = PointPickEventFilter(self)
        self.installEventFilter(self.point_pick_filter)
        
    def connectAnalyse(self, analyse_fun):
        """ Sets up the GUI to trigger a function through the "analyse" button
        
        Parameters
        ----------
        analyse_fun : function
            The function to trigger
        """
        self.do_analysis = analyse_fun
        return
    
    def connectVideoAnalyse(self, analyse_fun):
        """ Sets up the GUI to trigger a function through the "analyse" button when a video is input
        
        Parameters
        ----------
        analyse_fun : function
            The function to trigger
        """
        self.do_video_analysis = analyse_fun
        return
    
    def connectSave(self, save_fun):
        """ Sets up the GUI to trigger a function through the "save" button
        
        Parameters
        ----------
        analyse_fun : function
            The function to trigger
        """
        self.do_filesave = save_fun
        return
    
    def connectGetCPRangeFile(self, gcprf_fun):
        """ Sets up the GUI to use a function to get a color range file for the Color Picker
        
        Parameters
        ----------
        gcprf_fun : function
            The function to use
        """
        self.do_get_cp_range_file = gcprf_fun
        return
    
    def connectGetVideoFrame(self, gvf_fun):
        """ Sets up the GUI to use a function to get a video frame when a video is selected
        
        Parameters
        ----------
        gvf_fun : function
            The function to use
        """
        self.do_get_video_frame = gvf_fun
        return
    
    def getCPRangeMap(self, color1, color2):
        """ Retrieves a color range image for the Color Picker
        
        Parameters
        ----------
        color1 : QColor
            One bound of the colorspace
        color2 : QColor
            The other bound of the colorspace
        
        Returns
        -------
        range_image : QPixmap
            The pixmap ready to display as a color range preview
        """
        # Have to manually process colors because Qt gives hue of -1 for grey RGBs
        c1hsv = color1.getHsv()
        c2hsv = color2.getHsv()
        incolor1 = (max(c1hsv[0],0),c1hsv[1],c1hsv[2])
        incolor2 = (max(c2hsv[0],0),c2hsv[1],c2hsv[2])
        range_filename = self.do_get_cp_range_file(incolor1, incolor2)
        if not range_filename:
            # Failed to retrieve image, return None
            return None
        self.image_reader.setFileName(range_filename)
        range_image = qg.QPixmap.fromImage(self.image_reader.read())
        range_image = range_image.scaled(200, 200)
        return range_image
    
    def updateImage(self, display_file):
        """ Updates the "before" image display to reflect a new input
        """
        # Open image file
        self.image_reader.setFileName(display_file)
        bef_image = qg.QPixmap.fromImage(self.image_reader.read())
        
        # Check image size and adjust as needed
        self.bef_size = bef_image.size()
        self.bef_scale_h = self.max_pic_h/self.bef_size.height()
        self.bef_scale_w = self.max_pic_w/self.bef_size.width()
        if self.bef_scale_h<1 or self.bef_scale_w<1:
            bef_image = bef_image.scaled((self.bef_scale_h if self.bef_scale_h<=self.bef_scale_w else self.bef_scale_w)*self.bef_size)
        
        # Place in image display label
        self.bef_display.setPixmap(bef_image)
        
        return
    
    def updateResult(self, display_file):
        """ Updates the "after" image display to show an analysed image
        """
        # Check for empty filename (temporary?)
        if self.aft_file=="": return
        
        # Open image file
        self.image_reader.setFileName(display_file)
        aft_image = qg.QPixmap.fromImage(self.image_reader.read())
        
        # Check image size and adjust as needed
        self.aft_size = aft_image.size()
        self.aft_scale_h = self.max_pic_h/self.aft_size.height()
        self.aft_scale_w = self.max_pic_w/self.aft_size.width()
        if self.aft_scale_h<1 or self.aft_scale_w<1:
            aft_image = aft_image.scaled((self.aft_scale_h if self.aft_scale_h<=self.aft_scale_w else self.aft_scale_w)*self.aft_size)
            
        # Place in image display label
        self.aft_display.setPixmap(aft_image)
        
        # Update default save path
        self.save_file = self.processFilename(self.bef_file)
        self.checkValidSave()
        
        # Update save image size
        self.save_height_inp.setValue(self.aft_size.height())
        self.save_width_inp.setValue(self.aft_size.width())
        
        return
    
    def updateImageDisplaySize(self, screen_size):
        """ Resizes the images according to the size of the containing screen
    
        Parameters
        ----------
        screen_size : QSize
            The size of the screen
        """
        self.max_pic_h = 0.4*screen_size.height()
        self.max_pic_w = 0.4*screen_size.width()
        #self.updateImage()
        #self.updateResult()
        return
    
    @qc.Slot()
    def chooseInfile(self):
        """ Selects a file using QFileDialog
        
        Called when file selection button is clicked
        """
        filename = qw.QFileDialog.getOpenFileName(self, "Select An Image", self.bef_file, self.filetype_str)[0]
        if filename:
            self.bef_file = filename
            self.choose_file_text.setText(self.truncateFilename(filename, 43))
            if filename.endswith(".mp4") or filename.endswith(".mov") or filename.endswith(".avi"):
                self.is_video = True
                self.updateImage(self.do_get_video_frame(filename))
            else:
                self.is_video = False
                self.updateImage(self.bef_file)
        else:
            print("No file selected")
        
        # Change in input file may change if parameters are valid
        self.checkValidInput()
        return
    
    @qc.Slot()
    def updateColor(self):
        """ Updates stored color
        
        Called when new color is selected
        """
        # Using HSV to better integrate with openCV functionalities
        self.picked_color = self.color_picker.getColor().getHsv()
        self.using_range = self.color_picker.usingRange()
        if self.using_range:
            self.second_color = self.color_picker.getSecondColor().getHsv()
        else:
            self.second_color = None
        self.checkValidInput()
        return
    
    @qc.Slot()
    def updateDetectMode(self):
        """ Changes whether detection is being done with blobs or contours
        
        Called when detect mode button is clicked
        """
        if self.detect_mode==1:
            self.detect_mode=2
            self.detect_mode_text.setText("Using contour detection")
            self.detect_mode_but.setText("Use blobs")
            self.contour_point_text.show()
            self.contour_point_but.show()
        elif self.detect_mode==2:
            self.detect_mode=1
            self.detect_mode_text.setText("Using blob detection")
            self.detect_mode_but.setText("Use contours")
            self.contour_point_text.hide()
            self.contour_point_but.hide()
        return
    
    @qc.Slot()
    def updateKernelSize(self):
        """ Updates stored kernel size option
        
        Called when kernel size input is changed
        """
        self.kernel_size = self.kernel_size_inp.value()
        return
    
    @qc.Slot()
    def pickContourPoint(self):
        """ Updates detection point
        
        Called when contour point button is clicked
        """
        # Enable filter to capture color sampling
        self.point_pick_filter.setActive(True)
        
        # Disable mouse from making other inputs
        self.bef_display.grabMouse(qc.Qt.CrossCursor)
        return
    
    @qc.Slot()
    def analyseImage(self):
        """ Activates program functionality
        
        Called when activate button is clicked
        """
        if self.is_video:
            self.aft_file = self.do_video_analysis(self.bef_file, self.picked_color, self.second_color, self.detect_mode, self.kernel_size)
            self.updateResult(self.do_get_video_frame(self.aft_file))
        else:
            self.aft_file, self.raw_image_struct = self.do_analysis(self.bef_file, self.picked_color, self.second_color, self.detect_mode, self.kernel_size, self.contour_point)
            self.updateResult(self.aft_file)
        return
    
    @qc.Slot()
    def chooseOutfile(self):
        """ Selects a output location using QFileDialog
        
        Called when save selection button is clicked
        """
        filename = qw.QFileDialog.getSaveFileName(self, "Save Result To", self.bef_file, self.filetype_str)[0]
        if filename:
            self.save_file = filename
        else:
            print("No location selected")
        
        # Change in input file may change if parameters are valid
        self.checkValidSave()
        return
    
    @qc.Slot()
    def updateImageSaveSize(self):
        """ Update the size of the saved file
        
        Called when either dimension is updated
        """
        if self.save_height!=self.save_height_inp.value():
            # Store new height and update width according to ratio
            self.save_height = self.save_height_inp.value()
            self.save_width = (self.save_height*self.aft_size.width())//self.aft_size.height()
            self.save_width_inp.setValue(self.save_width)
        elif self.save_width!=self.save_width_inp.value():
            # Store new width and update height according to ratio
            self.save_width = self.save_width_inp.value()
            self.save_height = (self.save_width*self.aft_size.height())//self.aft_size.width()
            self.save_height_inp.setValue(self.save_height)
        
        # NOTE: A successfull call will change the value of one of the inputs, calling this method a second time. Nothing will occur during that call as both inputs will be the same as the recorded values.
        
        return
    
    @qc.Slot()
    def saveImage(self):
        """ Activates file save functionality
        
        Called when save button is clicked
        """
        self.do_filesave(self.raw_image_struct, self.save_file, (self.save_width, self.save_height))
        return
    
    def pickPoint(self):
        """ Samples the location at the current mouse position and then ends point pick mode
        """
        # Calibrate point to image display top left (note: off by 28 for some reason)
        zeroed = qg.QCursor.pos() - (self.pos() + self.bef_display.pos())
        picked_x = zeroed.x()/self.bef_display.width()
        picked_y = (zeroed.y()-28)/self.bef_display.height()
        if (picked_x>0) and (picked_x<1) and (picked_y>0) and (picked_y<1):
            self.contour_point = (picked_x, picked_y)
            self.contour_point_text.setText("({:.3f},{:.3f})".format(picked_x,picked_y))
            
        self.endPointPickMode()
        return
    
    def endPointPickMode(self):
        """ Exits point pick mode
        """
        self.point_pick_filter.setActive(False)
        self.bef_display.releaseMouse()
        return
        
    def checkValidInput(self):
        """ Verifies that the current parameters are valid and updates activate button accordingly
        """
        if self.bef_file=="" or self.picked_color==None:
            self.activate_but.setDisabled(True)
        else:
            self.activate_but.setDisabled(False)
        return
    
    def checkValidSave(self):
        """ Verifies that a valid save location has been chosen
        """
        if self.save_file=="":
            self.save_file_but.setDisabled(True)
            self.save_file_loc.setText("Please select a valid save location")
        else:
            self.save_file_but.setDisabled(False)
            self.save_file_select_but.setDisabled(False)
            # Outfile name should be as long as possible without exceeding width of other items in column
            name_length = max(self.aft_display.pixmap().width()//8, 43)
            self.save_file_loc.setText("Save to "+self.truncateFilename(self.save_file, name_length))
            self.save_height_inp.setDisabled(False)
            self.save_width_inp.setDisabled(False)
        return
    
    def processFilename(self, infile):
        """ Processes input filename into default output filename
        
        Parameters
        ----------
        infile : str
            The name of the input file
        
        Returns
        -------
        outfile : str
            infile with "out" added at the end (before the extension)
        """
        nameExt = infile.split(".")
        return nameExt[0]+"-out."+nameExt[1]
    
    def truncateFilename(self, filename, maxlen):
        """ Shortens file names/paths for display
        
        Parameters
        ----------
        filename : str
            The path to truncate
        maxlen : int
            The length at which to truncate filename
        
        Returns
        -------
        truncated : str
            The last [maxlen] characters of filename
        """
        if len(filename)<=maxlen:
            return filename
        return "..."+filename[-(maxlen-3):]

""" Helper class for PrimaryWindow - intercepts input events during contour point pick mode
"""
class PointPickEventFilter(qc.QObject):
    
    def __init__(self, primary_window=None):
        super().__init__(primary_window)
        self.primary_window = primary_window
        
        # Event filter is active when in contour point pick mode
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
            self.primary_window.pickPoint()
            return True
        if(event.type()==qc.QEvent.KeyPress):
            # Cancel color selection mode
            self.primary_window.endPointPickMode()
            return True
        return False
        
def create_gui():
    """ Creates an application and GUI object instance
    
    Returns
    -------
    QApplication
        The created application
    PrimaryWindow
        The created GUI window
    """
    app = qw.QApplication([])
    main_window = PrimaryWindow()
    main_window.updateImageDisplaySize(app.primaryScreen().size())
    
    return app, main_window
    
def start_gui(app, main_window):
    """ Begins the event-driven loop for a GUI instance
    
    Parameters
    ----------
    app : QApplication
        The running application
    main_window : PrimaryWindow
        A GUI window object
    """
    main_window.show()
    
    app.exec()
    sys.exit()
