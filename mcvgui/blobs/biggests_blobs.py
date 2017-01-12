import pyforms, cv2
from pyforms import BaseWidget
from pyforms.Controls import ControlSlider
from mcvapi.blobs.biggests_blobs import BiggestsBlobs as Class


class BiggestsBlobs(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Biggests blobs')
		Class.__init__(self, **kwargs)

		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(55)

		self._n_blobs = ControlSlider('Find n blobs', 1, 1, 10)
		self._formset = ['_n_blobs']

	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	@property
	def biggests_blobs_n(self): return self._n_blobs.value