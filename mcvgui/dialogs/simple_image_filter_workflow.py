import pyforms, cv2
from pyforms import BaseWidget
from pyforms.Controls import ControlList
from pyforms.Controls import ControlPlayer
from pyforms.Controls import ControlText
from pyforms.Controls import ControlCombo

from mcvgui.filters.adaptative_threshold import AdaptativeThreshold
from mcvgui.masks.polygons_mask import PolygonsMask
from mcvgui.blobs.find_blobs import FindBlobs
from mcvgui.blobs.biggests_blobs import BiggestsBlobs
from mcvgui.blobs.order_by_position import OrderByPosition

class SimpleImageFilterWorkflow(BaseWidget):


	def __init__(self, parent=None, video=None):
		BaseWidget.__init__(self, 'Simple workflow editor', parentWindow=parent)

		self._player   		= ControlPlayer('Player')
		self._imgfilters  	= ControlList('Image filters')
		self._defaultflows 	= ControlCombo('Default workflows')
		self._blobsfilters  = ControlList('Blobs filters')


		self._formset = [
			'_defaultflows',
			'_player',
			'=',
			'_imgfilters',
			'_blobsfilters'
		]

		self.__load_default_flows()

		self._imgfilters.selectEntireRow = True
		self._blobsfilters.selectEntireRow = True
		self._defaultflows.changed 		= self.__defaultflows_changed_evt
		self._player.processFrame 		= self.__process_frame

		self.filename = video


	@property
	def filename(self): return self._filename
	@filename.setter
	def filename(self, value): 
		self._filename 		= value
		self._player.value 	= value
	

	def __load_default_flows(self):
		self._defaultflows.addItem('Adaptative threshold', 1)
		self._defaultflows.addItem('Adaptative threshold & Mask', 2)

		self.__defaultflows_changed_evt()
		

	def __defaultflows_changed_evt(self):
		
		if   self._defaultflows.value==1:
			self._imgflow = self._imgfilters.value = [
				( 'Adaptative threshold', AdaptativeThreshold() ),
			]
			self._blobsflow = self._blobsfilters.value = [
				('Find blobs', FindBlobs() ),
				('Retrieve n blobs',BiggestsBlobs() ),
				('Order by position',OrderByPosition() )
			]
		
		elif self._defaultflows.value==2:
			self._imgflow = self._imgfilters.value = [
				('Adaptative threshold', AdaptativeThreshold() ),
				('Mask', PolygonsMask(video=self.filename)),
			]
			self._blobsflow = self._blobsfilters.value = [
				('Find blobs', FindBlobs() ),
				('Retrieve n blobs',BiggestsBlobs() ),
				('Order by position',OrderByPosition() )
			]

	def process(self, data):
		for name, f in self._imgflow: 	data = f.process(data)
		for name, f in self._blobsflow: data = f.process(data)
		return data

	def __process_frame(self, frame):
		data = frame
		for name, f in self._imgflow: data = f.process(data)
		filter_res = data

		for name, f in self._blobsflow: data = f.process(data)

		for i, blob in enumerate(data):
			if blob is not None:
				blob.draw(frame)
				cv2.putText(frame,str(i), blob._centroid, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255))

		return frame, filter_res
		



if __name__ == '__main__': 
	pyforms.startApp(SimpleImageFilterWorkflow)