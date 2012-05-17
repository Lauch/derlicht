#!/usr/bin/python
# encoding: utf8
from collections import OrderedDict

MAX_DMX = 128 # maximum DMX channels

class DMXDevice(object):
	"""
	A DMXDevice consists of a mapping from names/variables to multiple channels.
	These channels are always contiguous.
	For example, RGB lights:
	These would have an R, G and B attribute.
	"""
	channels = 0 # Number of channels this device takes up
	
	attributes = [] # Attributes in order	
	
	values = [] # Initial values, same order as attributes
	
	def __init__(self, start_channel):
		self.start_channel = start_channel
		pass # override this
	
	@property
	def end_channel(self):
		return self.start_channel + self.channels - 1 # 3 Channels, occupies the start channel, +1 and +2
	
# TODO: read profiles from files

class RGBDimmer(DMXDevice):
	"""
	A simple RGB dimmer.
	"""
	
	channels = 3
	
	attributes = ["Red", "Green", "Blue"]

	values = [0,0,0]
	
class Mapping(object):
	"""
	This class provides sort of "patching", a mapping for channel to devices.
	This class should perform the conversion of Device states to DMX channel values,
	so if you change the mapping, it automatically changes the order and so on.
	The actual mapping is stored in the device instance itself.
	Note that DMX Numbering starts from 1, not 0, but we still start from 0. The DMX interface should take
	care of that.
	"""
	
	devices = [] # just an indexed list with instantiated devices. to remove a device, save its index, remove it here and then remove the index in all scenes.
	# Advantage is that you can change the device -> channels mapping without having to change anything else.
	# Got any other ideas?
	
	_scenes = []
	
	def generate_dmx_values(self, scene):
		if not scene.mapping == self:
			raise Exception("Wrong mapping.")
		l = [0] * MAX_DMX
		for index, dev in enumerate(self.devices):
			for k, i in enumerate(range(dev.start_channel, dev.end_channel+1)):
				l[i] = scene.values[index][k]
		return l

	def add_device(self, dev):
		self.devices.append(dev)
		for i in self._scenes:
			i.add_device(dev)
			

class Scene(object):
	"""

	"""
	values = []
	
	def __init__(self, mapping):
		self.mapping = mapping
		mapping._scenes.append(self)
		for i in mapping.devices:
			self.add_device(i)
		
	def remove_device(self, index):
		del self.values[index]
		
	def add_device(self, dev):
		self.values.append(dev.values[:])
		
if __name__ == "__main__":
	m = Mapping()
	dev1 = RGBDimmer(0)
	dev2 = RGBDimmer(3)
	m.add_device(dev1)
	m.add_device(dev2)
	s1 = Scene(m)
	s1.values[0] = [91,90,128]
	s1.values[1] = [90,90,128]
	print m.generate_dmx_values(s1)
