import pyforms, cv2
from pyforms import BaseWidget
from pyforms.Controls import ControlButton
from mcvapi.masks.polygons_mask import PolygonsMask as Class
from geometry_designer.modules.geometry_manual_designer.GeometryManualDesigner import GeometryManualDesigner

class PolygonsMask(Class, BaseWidget):
    
    def __init__(self, **kwargs):
        BaseWidget.__init__(self, 'Polygons Mask')
        Class.__init__(self, **kwargs)

        self._geo_window = GeometryManualDesigner('Geometry designer', parent=self)
        self._geo_window.apply_evt = self.__polys_ready
        self._geo_window._video.hide()

        self._geo_window._video.value = kwargs.get('video', None)

        self.layout().setContentsMargins(10, 5, 10, 5)
        self.setMinimumHeight(50)

        self._draw_btn = ControlButton('Draw a mask')

        self._draw_btn.value = self.__draw_btn_evt

    def __polys_ready(self):
        self._param_polygons_polys  = self._geo_window.polygons
        self._param_polygons_mask   = None
        self._geo_window.hide()

    def __draw_btn_evt(self):
        self._geo_window.show()


if __name__ == '__main__': 
    pyforms.startApp(PolygonsMask)