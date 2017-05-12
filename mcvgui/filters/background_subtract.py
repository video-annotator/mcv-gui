import pyforms, cv2, numpy as np
from pyforms import BaseWidget
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlSlider
#from mcvapi.filters.background_detector import BackgroundDetector as Class
from mcvapi.filters.background_subtract import BackgroundSubtract as Class

class BackgroundSubtract(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Background subtract')
		Class.__init__(self, **kwargs)

		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(100)

		self._param_background_subtract_threshold   = ControlSlider('Threshold', 10, 1, 255)
		
		self._formset = [
			'_param_background_subtract_threshold',			
		]

		
	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	@property
	def background_subtract_threshold(self): return self._param_background_subtract_threshold.value