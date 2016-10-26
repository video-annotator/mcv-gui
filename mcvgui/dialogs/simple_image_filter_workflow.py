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
from mcvgui.blobs.track_path import TrackPath

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

		self.load_order = ['_defaultflows', ]

		self._imgfilters.selectEntireRow 	= True
		self._blobsfilters.selectEntireRow 	= True
		self._defaultflows.changed 			= self.__defaultflows_changed_evt
		self._player.processFrame 			= self.__process_frame
		self.filename 						= video

	def initForm(self):
		super(SimpleImageFilterWorkflow,self).initForm()

	###########################################################################
	### IO FUNCTIONS ##########################################################
	###########################################################################
	def save(self, data={}):
		data = super(SimpleImageFilterWorkflow,self).save(data)
		data['image-filters'] = {}
		for label, widget in self._imgfilters.value:
			data['image-filters'][label] = widget.save({})
		data['blobs-filters'] = {}
		for label, widget in self._blobsfilters.value:
			data['blobs-filters'][label] = widget.save({})
		return data

	def load(self, data):
		super(SimpleImageFilterWorkflow,self).load(data)

		if data.get('blobs-filters', None):
			for label, widget in self._blobsfilters.value:
				if label in data['blobs-filters']: widget.load(data['blobs-filters'][label])
		if data.get('image-filters', None):
			for label, widget in self._imgfilters.value:
				if label in data['image-filters']: widget.load(data['image-filters'][label])
		
	###########################################################################
	### FUNCTIONS #############################################################
	###########################################################################


	def processflow(self, data):
		for name, f in self._imgflow: 	data = f.process(data)
		for name, f in self._blobsflow: data = f.process(data)
		return data

	###########################################################################
	### INTERFACE FUNCTIONS ###################################################
	###########################################################################

	def __load_default_flows(self):
		self._defaultflows.addItem('Adaptative threshold', 1)
		self._defaultflows.addItem('Adaptative threshold & Mask', 2)
		self.__defaultflows_changed_evt()

	def __defaultflows_changed_evt(self):		
		if   self._defaultflows.value==1:
			self._blobsflow = self._blobsfilters.value = [
				('Find blobs', FindBlobs() ),
				('Retrieve n blobs',BiggestsBlobs() ),
			]
			self._imgflow = self._imgfilters.value = [
				( 'Adaptative threshold', AdaptativeThreshold() ),
			]
		
		elif self._defaultflows.value==2:
			self._blobsflow = self._blobsfilters.value = [
				('Find blobs', FindBlobs() ),
				('Retrieve n blobs',BiggestsBlobs() ),
				('Order by position',OrderByPosition() ),
				('Track path',TrackPath() )
			]
			self._imgflow = self._imgfilters.value = [
				('Adaptative threshold', AdaptativeThreshold() ),
				('Mask', PolygonsMask(video=self.filename)),
			]
			


	def __process_frame(self, frame):
		
		data = frame
		for name, f in self._imgflow: data = f.process(data)
		filter_res = data
		for name, f in self._blobsflow: data = f.process(data)

		step = 16581375 / (len(data)+1)

		for i, blob in enumerate(data):
			if blob is not None:
				rgb_int = step*(i+1)
				blue 	=  rgb_int & 255
				green 	= (rgb_int >> 8) & 255
				red 	= (rgb_int >> 16) & 255
				c = (blue, green, red)

				blob.draw(frame, color=c)
				if blob.centroid:
					cv2.putText(frame,str(i), blob.centroid, cv2.FONT_HERSHEY_SIMPLEX, 1, c)

		return frame, filter_res
		


	###########################################################################
	### PROPERTIES ############################################################
	###########################################################################

	@property
	def filename(self): return self._filename
	@filename.setter
	def filename(self, value): 
		self._filename 		= value
		self._player.value 	= value

	def show(self):
		super(SimpleImageFilterWorkflow, self).show()
		self._blobsfilters.show()
		self._blobsfilters.resizeRowsToContents()

if __name__ == '__main__': 
	pyforms.startApp(SimpleImageFilterWorkflow)