from pyforms import BaseWidget
from mcvapi.blobs.order_by_position import OrderByPosition as Class


class OrderByPosition(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Order by position')
		Class.__init__(self, **kwargs)
