#!/usr/bin/env python
import wx
import sys
class MainWindow(wx.Frame):
	"""Main Window for the application. """
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(800,600))
		self.create_components()
		self.Show(True)

	def create_components(self):
		#self.scenes_panel = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
		
		self.scroll = wx.ScrolledWindow( self, -1 )
		self.panel = wx.Panel( self, -1 )
		
		self.sizer_main = wx.BoxSizer(wx.VERTICAL)
		self.sizer_sliders = wx.BoxSizer(wx.HORIZONTAL)
		
		self.sliders = []
		for i in range(128):
			s = wx.Slider(self.panel,-1, maxValue=255,style=wx.SL_VERTICAL)
			self.sliders.append(s)
			self.sizer_sliders.Add(s, 1, wx.EXPAND)
		
		self.sizer_main.Add(self.sizer_sliders, proportion=1, flag=wx.ALL|wx.EXPAND)
		
		self.panel.SetSizer(self.sizer_main)
		self.panel.SetAutoLayout( True )
		self.panel.Layout()
		self.panel.Fit()
		
		self.SetSizer(self.sizer_main)
		self.SetAutoLayout(1)
		
		self.Bind(wx.EVT_CLOSE, self.OnQuit)
	def OnQuit(self, *args):
		sys.exit()
		
app = wx.App(False)
frame = MainWindow(None, 'Der Licht Virtual Controller')
app.MainLoop()
