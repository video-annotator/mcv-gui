import pyforms, cv2
from pyforms import BaseWidget
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlSlider
from mcvapi.filters.adaptative_threshold import AdaptativeThreshold as Class


class AdaptativeThreshold(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Adaptative threshold')
		Class.__init__(self, **kwargs)

		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(100)

		self._param_adaptive_threshold_method       = ControlCombo('Method')
		self._param_adaptive_threshold_type         = ControlCombo('Type')
		self._param_adaptive_threshold_block_size   = ControlSlider('Block size', 664, 3, 2999)
		self._param_adaptive_threshold_c            = ControlSlider('C', 0, -255, 255)

		self._formset = [
			('_param_adaptive_threshold_method','_param_adaptive_threshold_type'),
			('_param_adaptive_threshold_block_size','_param_adaptive_threshold_c')
		]

		self._param_adaptive_threshold_method.add_item('ADAPTIVE_THRESH_MEAN_C', cv2.ADAPTIVE_THRESH_MEAN_C)
		self._param_adaptive_threshold_method.add_item('ADAPTIVE_THRESH_GAUSSIAN_C', cv2.ADAPTIVE_THRESH_GAUSSIAN_C)

		self._param_adaptive_threshold_type.add_item('THRESH_BINARY_INV', cv2.THRESH_BINARY_INV)
		self._param_adaptive_threshold_type.add_item('THRESH_BINARY', cv2.THRESH_BINARY)
	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	@property
	def adaptive_threshold_method(self):        return self._param_adaptive_threshold_method.value
	
	@property
	def adaptive_threshold_type(self):          return self._param_adaptive_threshold_type.value

	@property
	def adaptive_threshold_block_size(self):    
		size = self._param_adaptive_threshold_block_size.value
		return int((size+1) if (size % 2)==0 else size)

	@property
	def adaptive_threshold_block_c(self):       return int(self._param_adaptive_threshold_c.value)