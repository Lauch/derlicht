#!/usr/bin/env python
import wx
class MainWindow(wx.Frame):
	"""Main Window for the application. """
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(800,600))
		self.create_components()
		self.Show(True)

	def create_components(self):
		#self.scenes_panel = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
		
		
		self.scroll = wx.ScrolledWindow( self, -1 )
		self.slider_panel = wx.Panel( self.scroll, -1 )
		self.sizer_slider = wx.BoxSizer(wx.HORIZONTAL)
		
		sizer_main = wx.BoxSizer(wx.VERTICAL)
		self.sizer_sliders = wx.BoxSizer(wx.HORIZONTAL)
		
		self.sliders = []
		for i in range(128):
			s = wx.Slider(self.slider_panel,-1, maxValue=255,style=wx.SL_VERTICAL)
			self.sliders.append(s)
			self.sizer_sliders.Add(s, 1, wx.EXPAND)
		
		self.panel_sizer = wx.BoxSizer( wx.VERTICAL )
		self.panel_sizer.Add(self.sizer_sliders, proportion=1, flag=wx.ALL)
		
		self.slider_panel.SetSizer(self.panel_sizer)
		self.slider_panel.SetAutoLayout( True )
		self.slider_panel.Layout()
		self.slider_panel.Fit()
		
		#sizer_main.Add(self.scenes_panel, 1, wx.EXPAND)
		sizer_main.Add(self.slider_panel, 1, wx.EXPAND)
		
		
		
		
			
		self.SetSizer(sizer_main)
		self.SetAutoLayout(1)
		#sizer_main.Fit(self)
		
app = wx.App(False)
frame = MainWindow(None, 'Der Licht Virtual Controller')
app.MainLoop()
