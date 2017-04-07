import pyforms, cv2
from pyforms import BaseWidget
from pyforms.Controls import ControlList
from pyforms.Controls import ControlPlayer
from pyforms.Controls import ControlText
from pyforms.Controls import ControlCombo
from mcvapi.mcvbase import MCVBase

from pysettings import conf


class SimpleFilter(BaseWidget, MCVBase):
	"""
	It implements a dialog that allow the user to choose several combinations of
	filters and apply them to a video.
	The player allow the user to pre visualize the result.
	"""


	def __init__(self, parent=None, video=None):
		BaseWidget.__init__(self, 'Simple workflow editor', parent_win=parent)
		self._parent = parent

		self._player   		= ControlPlayer('Player')
		self._imgfilters  	= ControlList('Image filters')
		self._imageflows 	= ControlCombo('Image workflows')
		self._blobsflows 	= ControlCombo('Blobs workflows')
		self._blobsfilters  = ControlList('Blobs filters')

		self.formset = [
			('_player',
			'||',
			['_imageflows',
			'_imgfilters',
			'_blobsflows',
			'_blobsfilters'])
		]

		self.formset = [
			'_imageflows',
			'_imgfilters',
			'=',
			('_player','||',['_blobsflows','_blobsfilters'])
		]


		self.load_order = ['_imageflows', '_blobsflows']

		self._imgfilters.select_entire_row 		= True
		self._blobsfilters.select_entire_row 	= True
		self._imageflows.changed_event 			= self.__imageflows_changed_event
		self._blobsflows.changed_event 			= self.__blobsflows_changed_event
		self._player.process_frame_event		= self.__process_frame
		
		self.video_capture = video

		self._pipelines = {}
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
		"""
		Reinit all the filters
		"""
		for name, f in self._imgfilters.value: 		data = f.clear()
		for name, f in self._blobsfilters.value: 	data = f.clear()
		

	def processflow(self, data):
		"""
		Apply the selected workflow of filters.
		"""
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

	
	def __load_default_blobsflows(self):
		self._blobsflows.add_item('Find blobs + track path', 2)
		self.__blobsflows_changed_event()


	def __imageflows_changed_event(self):
		workflow = []
		for title, flow_filter in self._pipelines.get(self._imageflows.value, []):
			workflow.append( (title, flow_filter() ) )
		self.image_filters = workflow

		
	def __blobsflows_changed_event(self):
		workflow = []
		for title, flow_filter in self._pipelines.get(self._blobsflows.value, []):
			workflow.append( (title, flow_filter() ) )
		self.blobs_filters = workflow

	def __process_frame(self, frame):
		frame_index = self._player.video_index-1
		
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
				rgb_int = int(step*(i+1))
				blue 	=  rgb_int & 255
				green 	= (rgb_int >> 8) & 255
				red 	= (rgb_int >> 16) & 255
				c = (blue, green, red)

				blob.draw(frame, color=c)
				if blob.centroid:
					cv2.putText(frame,str(i), blob.centroid, cv2.FONT_HERSHEY_SIMPLEX, 1, c)

		return frame, filter_res
		

	def add_image_filters(self, filtername, pipeline):
		"""
		Add an image filter
		"""
		first_filters = self._imageflows.value==None
		self._imageflows.add_item(filtername)
		self._pipelines[filtername] = pipeline
		if first_filters: self.__imageflows_changed_event()

	def add_blobs_filters(self, filtername, pipeline):
		"""
		Add a blob filter
		"""
		first_filters = self._blobsflows.value==None
		self._blobsflows.add_item(filtername)
		self._pipelines[filtername] = pipeline
		if first_filters: self.__blobsflows_changed_event()


	###########################################################################
	### PROPERTIES ############################################################
	###########################################################################

	@property
	def image_filters(self):
		"""
		Set and retrieve the selected list of image filters
		"""
		for name, f in self._imgfilters.value: yield f
	@image_filters.setter
	def image_filters(self, value): self._imgfilters.value = value


	@property
	def blobs_filters(self):
		"""
		Set and retrieve the selected list of blobs filters
		"""
		for name, f in self._blobsfilters.value: yield f
	@blobs_filters.setter
	def blobs_filters(self, value): self._blobsfilters.value = value
	
	
	@property
	def video_capture(self): 
		"""
		Set and retrieve the video for previsualization.
		The value should be from type cv2.VideoCapture or a path to a video file.
		"""
		return self._player.value
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