# Semester Project - Computer Vision
This is a multi-use computer vision project created by Ariana Beeby, Max Figura, and Jason Jopp as a semester-long project for CSC443 Software Engineering. The basic functionality of the program is to scan an image and detect a given item within it based on color and shape. The project in its current form uses Python, with the NumPy and OpenCV libraries to perform its functionality and PySide6 to create a Qt interface.

## USAGE
The program can be used by running `python3 main.py`. This will create a user interface through which the program's functionalities can be accessed.\
Within the interface, the user can select a file from their machine, pick a color to detect, and set any other options as desired. After hitting the "Analyse" button, a copy of the image will be shown, outlining each selected item in green. The user can then save the output image, choosing a save location, image size, and image format.

## STRUCTURE
```
semester-project-computer-vision/
| contours.py
| detect.py
| gen_mask.py
| gui_colorpicker.py
| images/
| | shapes.png
| | ...
| main.py
| plot.py
| read_write_image.py
| README.md
| user_interface.py
```

### main.py
The main driver which runs the program; all functionalities should be passed through it.

### user_interface.py
Uses Qt through the PySide library to create a GUI window class with an event-driven loop.

### gui_colorpicker.py
Defines a custom color picker widget, based on Qt's QColorDialog but modified to better fit the functionality.

### contours.py, detect.py and gen_mask.py
Functional scripts which perform the object detection and image markup.

### read_write_image.py
Used by the model to convert between image files and processable NumPy arrays.

### plot.py
Used to generate data visualizations, currently it's only function is to generate a plot which displays the current color space being searched for.

### images/
Contains a collection of image files that can be used to test various aspects of the program. Currently, image detection only works effectively on flat-color svg-type images, such as images/shapes.png.

## Project Resources
### OpenCV Installation:
https://opencv.org/get-started/
<br> https://pypi.org/project/opencv-python/

### OpenCV Tutorials:
https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
<br> https://www.geeksforgeeks.org/opencv-python-tutorial/

### Computer Vision Concepts
Kernel Image Processing
<br>https://en.wikipedia.org/wiki/Kernel_(image_processing)

### GUI Tools
PySide library for Qt
<br> https://doc.qt.io/qtforpython-6/gettingstarted.html
Original Qt documentation (C++)
<br> https://doc.qt.io/qt-6/index.html

### Python Tutorials
Python virtual env. primer, useful for isolating libraries for to a specific project.
<br>https://realpython.com/python-virtual-environments-a-primer/#deactivate-it
