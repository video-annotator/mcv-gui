import pyforms, cv2, numpy as np
from pyforms import BaseWidget
from pyforms.Controls import ControlCheckBox
from pyforms.Controls import ControlSlider
#from mcvapi.filters.background_detector import BackgroundDetector as Class
from mcvapi.filters.morphologyex_open import MorphologyExOpen as Class

class MorphologyExOpen(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'MorphologyEx open')
		Class.__init__(self, **kwargs)

		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(50)

		self._use_morphologyexopen 				 = ControlCheckBox('Use MorphologyEx Open')
		self._param_morphologyexopen_kernel_size = ControlSlider('Kernel size', 3, 3, 51)

		self._formset = [
			('_use_morphologyexopen','_param_morphologyexopen_kernel_size')
		]

		self._param_morphologyexopen_kernel_size.changed_event = self.__update_param_morphologyex_kernel_size
		
	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	def __update_param_morphologyex_kernel_size(self):
		kernel_size = self._param_morphologyexopen_kernel_size.value 

		if (kernel_size % 2)==0: kernel_size += 1

		self._param_morphologyexopen_kernel = np.ones((kernel_size,kernel_size),np.uint8)


	def process(self, frame):
		if self._use_morphologyexopen.value:
			return Class.process(self, frame)
		else:
			return frame