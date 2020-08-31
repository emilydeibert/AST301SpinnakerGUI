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

    `pip install simple-pyspin`

