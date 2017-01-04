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
from mcvgui.masks.path_mask import PathMask
from pysettings import conf


class SimpleFilter(BaseWidget):


	def __init__(self, parent=None, video=None):
		BaseWidget.__init__(self, 'Simple workflow editor', parent_win=parent)
		self._parent = parent

		self._player   		= ControlPlayer('Player')
		self._imgfilters  	= ControlList('Image filters')
		self._imageflows 	= ControlCombo('Image workflows')
		self._blobsflows 	= ControlCombo('Blobs workflows')
		self._blobsfilters  = ControlList('Blobs filters')

		self._formset = [
			('_player',
			'||',
			['_imageflows',
			'_imgfilters',
			'_blobsflows',
			'_blobsfilters'])
		]

		self.__load_default_imageflows()
		self.__load_default_blobsflows()

		self.load_order = ['_imageflows', '_blobsflows']

		self._imgfilters.select_entire_row 		= True
		self._blobsfilters.select_entire_row 	= True
		self._imageflows.changed_event 			= self.__imageflows_changed_event
		self._blobsflows.changed_event 			= self.__blobsflows_changed_event
		self._player.process_frame_event		= self.__process_frame
		
		self.video_capture = video

		#self.video_capture = cv2.VideoCapture('/home/ricardo/Downloads/GOPR1871_single cortado.mp4')

	
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
	
	def clear(self):
		for name, f in self._imgfilters.value: 		data = f.clear()
		for name, f in self._blobsfilters.value: 	data = f.clear()
		

	def processflow(self, data):
		frame_index = self._player.video_index
		for name, f in self._imgfilters.value:
			f.frame_index = frame_index
			data = f.process(data)
		for name, f in self._blobsfilters.value: 	
			f.frame_index = frame_index
			data = f.process(data)
		return data

	###########################################################################
	### INTERFACE FUNCTIONS ###################################################
	###########################################################################

	def __load_default_imageflows(self):
		self._imageflows.add_item('Adaptative threshold', 1)
		self._imageflows.add_item('Adaptative threshold + Mask', 2)
		self._imageflows.add_item('Adaptative threshold + Mask the path', 3)
		self.__imageflows_changed_event()

	def __load_default_blobsflows(self):
		self._blobsflows.add_item('Find blobs + track path', 2)
		self.__blobsflows_changed_event()

	def __imageflows_changed_event(self):		
		if   self._imageflows.value==1:
		
			self._imgfilters.value = [
				( 'Adaptative threshold', 	AdaptativeThreshold() ),
			]
		
		elif self._imageflows.value==2:
			self._imgfilters.value = [
				('Adaptative threshold', 	AdaptativeThreshold() 				),
				('Mask', 					PolygonsMask(video=self.video_capture)	),
			]

		elif self._imageflows.value==3:
			paths  = self._parent.paths if hasattr(self,'_parent') and hasattr(self._parent, 'paths') else []
			radius = [30 for i in range(len(paths))]

			mask_path = PathMask()
			mask_path.mask_paths = paths
			
			self._imgfilters.value = [
				('Adaptative threshold', 	AdaptativeThreshold() ),
				('Mask the path', 			mask_path			  ),
			]
			
	def __blobsflows_changed_event(self):		
		if   self._blobsflows.value==2:
			
			self._blobsfilters.value = [
				('Find blobs', 			FindBlobs() 		),
				('Retrieve n blobs',	BiggestsBlobs() 	),
				('Order by position',	OrderByPosition() 	),
				('Track path',			TrackPath() 		)
			]



	def __process_frame(self, frame):
		frame_index = self._player.video_index
		
		data = frame
		for name, f in self._imgfilters.value: 
			f.frame_index = frame_index			
			data = f.process(data)
		filter_res = data
		for name, f in self._blobsfilters.value:
			f.frame_index = frame_index
			data = f.process(data)

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
	def video_capture(self): return self._player.value
	@video_capture.setter
	def video_capture(self, value): 
		self._player.value 	= value
		for name, f in self._imgfilters.value: 		f.video = value
		for name, f in self._blobsfilters.value: 	f.video = value

	def show(self):
		super(SimpleFilter, self).show()
		self._blobsfilters.show()
		self._blobsfilters.resizeRowsToContents()

if __name__ == '__main__': 
	pyforms.start_app(SimpleFilter)