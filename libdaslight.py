#!/usr/bin/python
import usb.core, usb.util
import time
import threading

class DasLightInterface(threading.Thread):
	"""
	Handles all the interfacing with the hardware, including the USB interface.
	"""
	def __init__(self):
		self.values = [0] * 128
		self.values_lock = threading.Lock()
		self.setup_device()
		
	def _find_device(self):
		"""
		Looks for the first DVC128 device
		"""
		self.dev = usb.core.find(idVendor=0x6244)
	
	def setup_device(self):
		"""
		Sets up the device, configuration, interface and endpoint.
		We could also directly use device.write()
		"""
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
				return
			else:
				time.sleep(0.5)
				self.write_to_device(s)	
	
	def run(self):
		while True:
			self.values_lock.acquire(True) # blocking

			# validate, move to set_values
			if len(values) < 128:
				values = values+[0 for i in range(128-len(values))]
			assert len(values) == 128
			
			dmx_str = "".join(map(chr, values))
			self.write_to_device(dmx_str)
			self.values_lock.release()
			time.sleep(0.04)
	
class DasLightVC(object):
	"""
	Manages the thread and stuff.
	"""
	
	
	def __init__(self):
		self._thread = DasLightInterface()
		self._thread.start()
	
	def get_values(self):
		# This is probably not necessary, rather store it in this class
		# The thread doesn't change values
		self._thread.values_lock.acquire(True)
		ret = self._thread.values
		self._thread.values_lock.release()
		
	def set_values(self, vals):
		# TODO implement validating here
		
		self._thread.values_lock.acquire(True)
		self._thread.values = vals
		self._thread.values_lock.release()
	
	values = property(get_values, set_values)
	
	def send_dmx(self, values):
		"""
		Takes an array and sends
		"""
		
		dmx_str = "".join(map(chr, values))
		print values
		self.write_to_device(dmx_str)
		
		
if __name__ == "__main__":
	dl = DasLightVC()
	dl.values = [1,2,3]
	raw_input()
		
