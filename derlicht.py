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
		self.main_panel = wx.Panel( self, -1 )
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.scroll = wx.ScrolledWindow( self.main_panel, -1 )
		self.scroll.SetScrollbars(1, 1, 1, 1)
		self.sliders_sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.sliders = []
		for i in range(128):
			s = wx.Slider(self.scroll,-1, maxValue=255,style=wx.SL_VERTICAL|wx.SL_INVERSE)
			self.sliders.append(s)
			self.sliders_sizer.Add(s, 1, wx.EXPAND)
		
		self.main_sizer.Add(self.scroll, proportion=1, flag=wx.ALL|wx.EXPAND)

		self.main_panel.SetSizer(self.main_sizer)
		self.main_panel.SetAutoLayout( True )
		self.main_panel.Layout()
		self.main_panel.Fit()

		self.scroll.SetSizer(self.sliders_sizer)
		self.scroll.SetAutoLayout(True)
		self.scroll.Layout()
		self.scroll.Fit()
		
		self.Bind(wx.EVT_CLOSE, self.OnQuit)
	def OnQuit(self, *args):
		sys.exit()
		
app = wx.App(False)
frame = MainWindow(None, 'Der Licht Virtual Controller')
app.MainLoop()
