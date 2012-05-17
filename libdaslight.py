#!/usr/bin/python
import usb.core, usb.util
import time
class DasLightVC(object):
	def __init__(self):
		pass
		
	def _find_device(self):
		"""
		Looks for the first DVC128 device
		"""
		self.dev = usb.core.find(idVendor=0x6244)
	
	def setup_device(self):
		self._find_device()
		self.dev.set_configuration()
		self.cfg = self.dev.get_active_configuration()
		self.interface_number = self.cfg[(0,0)].bInterfaceNumber
		self.intf = usb.util.find_descriptor(self.cfg, bInterfaceNumber = self.interface_number)
		self.endpoint = self.intf[1]
	
	def write_to_device(self, s):
		"""
		Sends the string s to the device.
		"""
		try:
			self.endpoint.write(s)
		except Exception as e:
			print "Error while writing to device"
			print e
			print "Reconnecting..."
			try:
				self.setup_device()
			except Exception as e2:
				print "Fatal error"
				print e
				print "Terminating..."
				return
			else:
				time.sleep(0.5)
				self.write_to_device(s)
		
		
	def send_dmx(self, values):
		if len(values) < 512:
			values = values+[0 for i in range(512-len(values))]
		assert len(values) == 512
		dmx_str = "".join(map(chr, values))
		print values
		self.write_to_device(dmx_str)
		
		
if __name__ == "__main__":
	dl = DasLightVC()
	dl.setup_device()
	while True:
		dl.send_dmx([65,88,10,33])
		time.sleep(0.04)
		
