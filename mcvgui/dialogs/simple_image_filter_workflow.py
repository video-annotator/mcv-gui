import pyforms
from pyforms import BaseWidget
from pyforms.Controls import ControlList
from pyforms.Controls import ControlPlayer
from pyforms.Controls import ControlText
from pyforms.Controls import ControlCombo

from mcvgui.filters.adaptative_threshold import AdaptativeThreshold
from mcvgui.masks.polygons_mask import PolygonsMask


class SimpleImageFilterWorkflow(BaseWidget):


	def __init__(self, parent=None):
		BaseWidget.__init__(self, 'Simple workflow editor', parentWindow=parent)

		self._player   		= ControlPlayer('Player')
		self._workflow  	= ControlList('Filters configuration')
		self._defaultflows 	= ControlCombo('Default workflows')

		self._formset = [
			'_defaultflows',
			'_player',
			'=',
			'_workflow',
		]

		self.__load_default_flows()

		self._workflow.selectEntireRow 	= True
		self._defaultflows.changed 		= self.__defaultflows_changed_evt
		self._player.processFrame 		= self.__process_frame

		self.filename = '/home/ricardo/Desktop/01Apollo201403210900/01Apollo201403210900MergedCascata.MP4'


	@property
	def filename(self): return self._filename
	@filename.setter
	def filename(self, value): 
		self._filename 		= value
		self._player.value 	= value
	

	def __load_default_flows(self):
		self._defaultflows.addItem('Adaptative threshold', 1)
		self._defaultflows.addItem('Adaptative threshold & Mask', 2)

		self._flow = self._workflow.value = [( 'Adaptative threshold', AdaptativeThreshold() )]
		

	def __defaultflows_changed_evt(self):
		
		if   self._defaultflows.value==1:
			self._flow = self._workflow.value = [( 'Adaptative threshold', AdaptativeThreshold() )]
		
		elif self._defaultflows.value==2:
			
			self._flow = self._workflow.value = [
				('Adaptative threshold', AdaptativeThreshold() ),
				('Mask', PolygonsMask(video=self.filename))
			]

	def process(self, data):
		for name, f in self._flow: data = f.process(data)
		return data

	def __process_frame(self, frame):
		return self.process(frame)



if __name__ == '__main__': 
	pyforms.startApp(SimpleImageFilterWorkflow)