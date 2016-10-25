from pyforms import BaseWidget
from mcvapi.blobs.track_path import TrackPath as Class



class TrackPath(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Track path')
		Class.__init__(self, **kwargs)

		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(55)