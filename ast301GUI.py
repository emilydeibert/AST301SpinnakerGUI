### Simple GUI based on the Spinnaker SDK for a FLIR camera for AST301 ###
## Summer 2020, Emily Deibert ##

# importing necessary packages
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from simple_pyspin import Camera
from PIL import Image

# create global parameters
# global parameter for upate frequency of camera image in live view
global update_freq
update_freq = 5 # milliseconds

# global parameter for camera acquisition
global running
running = True

global savename
savename = 'image'

global cmap
cmap='Greys_r'

global image
image = np.zeros((964, 1288))

global zoomMode
zoomMode = False

ColorMapOptions = ['Greys', 'inferno', 'viridis', 'jet']

# running camera through simple_pyspin wrapper for PySpin (in turn a wrapper for the Spinnaker C++ framework)

# reset camera to default parameters
# the camera will remember parameters from the last run, so it's important to reset them here
with Camera() as cam:

	cam.init()

	cam.AcquisitionMode = 'Continuous'
	cam.SharpnessEnabled = True
	cam.SharpnessAuto = 'Off'
	cam.Sharpness = 0	
	cam.ExposureAuto='Off'
	cam.ExposureTime = 10000
	cam.GainAuto = 'Off'
	gain = min(5, cam.get_info('Gain')['max'])
	cam.Gain = gain
	cam.AcquisitionFrameRateEnabled = False
	cam.pgrExposureCompensationAuto = 'Off'

# run camera for GUI
# reset the parameters again, for safety
with Camera() as cam:

	cam.init() # initialize the camera

	cam.AcquisitionMode = 'Continuous' # continuous acquisition mode

	cam.SharpnessEnabled = True # allow sharpness to be controlled
								# if we turn this off, need to comment out the next two lines
	cam.SharpnessAuto = 'Off'   # turn off auto sharpness
	cam.Sharpness = 0			# set the sharpness to zero to start

	cam.GainAuto = 'Off'						# turn automatic gain off
	gain = min(5, cam.get_info('Gain')['max'])	# don't allow the gain to exceed the max gain of 20
	cam.Gain = gain 							# set the camera gain to 3

	cam.ExposureAuto = 'Off' # turn off auto exposure
	cam.ExposureTime = 10000 # microseconds

	cam.AcquisitionFrameRateEnabled = False # if True, can uncomment the next two lines
	#cam.AcquisitionFrameRateAuto = 'Off'
	#cam.AcquisitionFrameRate = 20

	cam.pgrExposureCompensationAuto = 'Off'

	def update_im():
		""" A function to continuously update the image while in live viewing mode.
		The global parameter update_freq (milliseconds) sets the update frequency.
		"""
		if running: # this will be set to True when you click the live viewing mode button
			global image
			image = cam.get_array()
			if zoomMode:
				image = image[422:542, 563:724]
			#global image
			#image = root.image
			im.set_data(image)
			im.set_cmap(cmap)
			canvas.draw()
			root.after(update_freq, update_im) # this is units of milliseconds

	def update_gain(event):
		""" A function to update the camera gain, and change the text in the GUI.
		"""
		val = int(Gain_Entry.get())
		cam.Gain = min(val, cam.get_info('Gain')['max']) # don't allow it to exceed the camera max of 20
		Current_Gain.configure(text='Current Gain = %.3f' % float(cam.Gain))

	def update_exp(event):
		""" A function to update the exposure time, and change the text in the GUI.
		Currently, this will only actually do anything if you're not in live viewing mode. 
		"""
		val = int(Exp_Entry.get())
		cam.ExposureTime = val
		Current_Exp_Micro.configure(text='Current Exposure Time = %.3f microseconds' % (cam.ExposureTime))
		Current_Exp_Milli.configure(text='Current Exposure Time = %.3f milliseconds' % (float(cam.ExposureTime)*0.001))
		Current_Exp_Sec.configure(text='Current Exposure Time = %.3f seconds' % (float(cam.ExposureTime)*1e-6))

	def update_sharp(event):
		""" A function to update the sharpness, and change the text in the GUI.
		"""
		val = int(Sharp_Entry.get())
		cam.Sharpness = val ### add in functionality to prevent user from exceeding the max
		Current_Sharp.configure(text='Current Sharpness = %.3f' % float(cam.Sharpness))

	def update_savename(event):
		global savename
		savename = str(Save_Entry.get())
		Save_Current.configure(text='(%s.png)' % savename)

	cam.start() # now start acquiring data with the camera

	root = tkinter.Tk() # set up the GUI
	root.wm_title("AST301")

	settingsFrame = tkinter.Frame(root)
	settingsFrame.grid(row=0, column=0, padx=10, pady=5)

	imageFrame = tkinter.Frame(root)
	imageFrame.grid(row=0, column=1, padx=10, pady=5)

	cmapFrame = tkinter.Frame(root)
	cmapFrame.grid(row=0, column=2, padx=10, pady=5)

	# set up the figure
	fig = Figure()
	ax = fig.add_subplot(111)
	ax.set_yticks([])
	ax.set_xticks([])

	#global image
	image = cam.get_array()
	im = ax.imshow(image, cmap=cmap) # by default, we start showing the first image the camera was looking at

	canvas = FigureCanvasTkAgg(fig, master=imageFrame)  # A tk.DrawingArea.
	canvas.draw()
	canvas.get_tk_widget().grid(row=0, column=4, columnspan=6, rowspan=6)


	def _quit():
		""" A function to exit the program.
		"""
		root.quit()     # stops mainloop
		root.destroy()  # this is necessary on Windows to prevent
	                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

	def _live():
		""" A function for live viewing mode in the GUI.
		"""
		cam.stop() # just in case
		cam.AcquisitionMode = 'Continuous' # set acquisition mode to continuous
		cam.start() # start acquiring data
		global running
		running = True # need this for the uodate_im function, to keep updating the image
		cam.ExposureTime = 10000 # we force set an exposure time. If not, the update may be buggy
		if running:
			cam.AcquisitionMode = 'Continuous'
			global update_freq
			update_freq = 5
			update_im() # updates the image every 5 milliseconds

	def _single():
		""" A function to switch to single image viewing mode in the GUI.
		"""
		cam.stop()
		cam.AcquisitionMode = 'SingleFrame' # Switch the acquisition mode, so the camera isn't continuously taking data.
		cam.start()
		global running
		running = False 				# stops the update_im functionality
		global image					
		image = cam.get_array() 				# gets current image
		if zoomMode:
			image = image[422:542, 563:724]
		im.set_data(image)	  				# sets view to current image
		im.set_cmap(cmap)
		canvas.draw()
		cam.stop()							# stop acquiring data while displaying a single image

	def _zoomIn():
		global zoomMode
		zoomMode = True
		if not running:
			_single()

	def _zoomOut():
		global zoomMode
		zoomMode = False
		if not running:
			_single()

	def _save():
		""" Just saves the current image.
		NEED TO:
		- set up functionality for changing the name
		- set up functionality for acquiring many images
		"""
		#fig.savefig(savename+'.png', bbox_inches='tight', pad_inches=0)
		#image.dump('test.npy')
		save_im = Image.fromarray(image)
		save_im.save(savename+'.png')

	def _cmapGreys():
		global cmap
		cmap = 'Greys_r'

	def _cmapInferno():
		global cmap
		cmap = 'inferno'

	def _cmapJet():
		global cmap
		cmap = 'jet'


	button_quit = tkinter.Button(master=root, text="Quit", command=_quit)
	button_quit.grid(row=13, column=0)

	Gain_Label = tkinter.Label(master=settingsFrame, text='Gain: ', font=('TkDefaultFont', 14, 'bold'))
	Gain_Label.grid(row=0, sticky=tkinter.W)
	Gain_Entry = tkinter.Entry(master=settingsFrame)
	Gain_Entry.bind("<Return>", update_gain)
	Gain_Entry.grid(row=1, column=0)
	Current_Gain = tkinter.Label(master=settingsFrame, text='Current Gain = %.3f' % float(cam.Gain))
	Current_Gain.grid(row=2, column=0, sticky=tkinter.W)

	Exp_Label = tkinter.Label(master=settingsFrame, text='Exposure Time (microseconds): ', font=('TkDefaultFont', 14, 'bold'))
	Exp_Label.grid(row=3, sticky=tkinter.W)
	Exp_Entry = tkinter.Entry(master=settingsFrame)
	Exp_Entry.bind("<Return>", update_exp)
	Exp_Entry.grid(row=4, column=0)
	Current_Exp_Micro = tkinter.Label(master=settingsFrame, text='Current Exposure Time = %.3f microseconds' % (cam.ExposureTime))
	Current_Exp_Micro.grid(row=5, column=0, sticky=tkinter.W)#, columnspan=6)
	Current_Exp_Milli = tkinter.Label(master=settingsFrame, text='Current Exposure Time = %.3f milliseconds' % (float(cam.ExposureTime)*0.001))
	Current_Exp_Milli.grid(row=6, column=0, sticky=tkinter.W)# columnspan=6)
	Current_Exp_Sec = tkinter.Label(master=settingsFrame, text='Current Exposure Time = %.3f seconds' % (float(cam.ExposureTime)*1e-6))
	Current_Exp_Sec.grid(row=7, column=0, sticky=tkinter.W)#, columnspan=6)

	Sharp_Label = tkinter.Label(master=settingsFrame, text='Sharpness: ', font=('TkDefaultFont', 14, 'bold'))
	Sharp_Label.grid(row=8, sticky=tkinter.W)
	Sharp_Entry = tkinter.Entry(master=settingsFrame)
	Sharp_Entry.bind("<Return>", update_sharp)
	Sharp_Entry.grid(row=9, column=0)
	Current_Sharp = tkinter.Label(master=settingsFrame, text='Current Sharpness = %.3f' % float(cam.Sharpness))
	Current_Sharp.grid(row=10, column=0, sticky=tkinter.W)

	button_live = tkinter.Button(master=imageFrame, text="Live Viewing Mode", command=_live)
	button_live.grid(row=11, column=6)

	button_singleImage = tkinter.Button(master=imageFrame, text="Single Image Mode", command=_single)
	button_singleImage.grid(row=11, column=7)

	button_zoomIn = tkinter.Button(master=imageFrame, text='Zoom In', command=_zoomIn)
	button_zoomIn.grid(row=6, column=6)

	button_zoomOut = tkinter.Button(master=imageFrame, text='Zoom Out', command=_zoomOut)
	button_zoomOut.grid(row=6, column=7)

	Save_Name = tkinter.Label(master=imageFrame, text='Save As: ')
	Save_Name.grid(row=9, column=8)
	Save_Entry = tkinter.Entry(master=imageFrame)
	Save_Entry.bind("<Return>", update_savename)
	Save_Entry.grid(row=9, column=8)
	button_saveSingle = tkinter.Button(master=imageFrame, text='Save Current Image', command=_save)
	button_saveSingle.grid(row=11, column=8) 
	Save_Current = tkinter.Label(master=imageFrame, text='(%s.png)' % savename)
	Save_Current.grid(row=12, column=8)

	CMapLabel = tkinter.Label(master=cmapFrame, text='Colour Scheme:')
	CMapLabel.grid(row=1, column=11)
	button_greys = tkinter.Button(master=cmapFrame, text='Greys', fg='black', command=_cmapGreys)
	button_greys.grid(row=2, column=11)
	button_inferno = tkinter.Button(master=cmapFrame, text='Inferno', fg='red', command=_cmapInferno)
	button_inferno.grid(row=3, column=11)
	button_jet = tkinter.Button(master=cmapFrame, text='Jet', fg='blue', command=_cmapJet)
	button_jet.grid(row=4, column=11)

	#update_im()
	tkinter.mainloop()

	cam.stop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
