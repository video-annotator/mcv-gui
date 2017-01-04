from pyforms import BaseWidget
from pyforms.Controls import ControlSlider
from mcvapi.masks.path_mask import PathMask as Class


class PathMask(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Path mask')
		Class.__init__(self, **kwargs)

		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(55)

		self._param_path_mask_radius = ControlSlider('Mask radius', 30, 1, 600)

		self._formset = ['_param_path_mask_radius']

	@property
	def mask_radius(self): return self._param_path_mask_radius.value
        