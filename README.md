# AST301SpinnakerGUI
A Python-based GUI for the AST301 lab using a FLIR camera and the Spinnaker SDK.

This GUI is currently optimized for **Python 3**, but Python 2 support will be coming soon.

## Installation of required dependencies

1. [Install the Spinnaker SDK and PySpin from FLIR.](https://www.flir.com/products/spinnaker-sdk/)
   * PySpin installation packages will be included with your Spinnaker SDK download. 
   * To install PySpin, you will have to follow the instructions provided by FLIR in these installation packages. These are available in the README.txt file that accompanies your Spinnaker SDK download. Be sure to use the PySpin installation package that matches your Spinnaker and Python verisons (for example, **spinnaker_python-2.0.0.147-cp27-cp27m-macosx_10_14_intel.tar.gz** refers to PySpin version 2.0.0.147 and Python version 2.7).

2. In addition to the Spinnaker SDK and PySpin, this GUI requires the following Python packages to be installed:
   * numpy
   * matplotlib
   * tkinter
   * PIL
   * [simple-pyspin](https://pypi.org/project/simple-pyspin/)

These packages can all be installed via pip through the command line:

    pip install simple-pyspin
    
## Opening the GUI

To open the GUI, you simply run the following command from the command line:

    python ast301GUI.py
    
## Usage

By default, many options available in the SpinView GUI that comes with the Spinnaker SDK are turned off and not viewable by users in this simple GUI. With this GUI, users are able to change several camera parameters (gain, exposure time, and sharpness), view images in a live viewing mode or in a single image mode, zoom in and out of images, modify the displayed image's colormap, and save the current image.

#### Default Setup

When the GUI opens, the gain/exposure time/sharpness have been set to default parameters, which will be displayed in the GUI. The camera will be in single image mode by default, a static image of whatever the camera was looking at when the GUI was launched will be displayed. The default colormap is set to `Greys`, and the default name for saved images is `image.png`.

![Default GUI view.](images/default.png)


