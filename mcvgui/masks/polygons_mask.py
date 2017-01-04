import pyforms, cv2, base64, numpy as np
from pyforms import BaseWidget
from pyforms.Controls import ControlButton
from mcvapi.masks.polygons_mask import PolygonsMask as Class
from geometry_designer.modules.geometry_manual_designer.GeometryManualDesigner import GeometryManualDesigner

class PolygonsMask(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Polygons Mask')
		Class.__init__(self, **kwargs)

		self._geo_window = GeometryManualDesigner('Geometry designer', parent=self)
		self._geo_window.apply_event = self.__polys_ready
		self._geo_window._video.hide()

		self._geo_window.video_capture = kwargs.get('video', '') if kwargs.get('video', '') is not None else ''

		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(50)

		self._draw_btn = ControlButton('Draw a mask')

		self._draw_btn.value = self.__draw_btn_event

	def __polys_ready(self):
		self._param_polygons_polys  = self._geo_window.polygons
		self._param_polygons_mask   = None
		self._geo_window._player.stop()
		self._geo_window.hide()

	def __draw_btn_event(self):
		self._geo_window.show()

	def save(self, data):
		super(PolygonsMask, self).save(data)
		if self._param_polygons_polys is not None:
			polys = self._param_polygons_polys
			data['polygons'] = [str(polys.dtype), base64.b64encode(polys), polys.shape]
		return data

	def load(self, data):
		super(PolygonsMask, self).load(data)
		polys = data.get('polygons', None)
		if polys:
			
			dataType  = np.dtype(polys[0])
			dataArray = np.frombuffer(base64.decodestring(polys[1]), dataType)
			dataArray = dataArray.reshape(polys[2])
			self._param_polygons_polys = dataArray


	@property	
	def video(self): return self._geo_window.video_capture
	@video.setter
	def video(self, value):  self._geo_window.video_capture = value



if __name__ == '__main__': 
	pyforms.start_app(PolygonsMask)