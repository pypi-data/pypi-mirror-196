import sys,io,types,threading
import os,sys
import numpy as np

import bokeh.io
import bokeh.events
import bokeh.models
import bokeh.plotting 

import OpenVisus as ov
from OpenVisus.pyquery import PyQuery
from OpenVisus.image_utils import SplitChannels, InterleaveChannels

import logging
logger = logging.getLogger(__name__)


if ov.cbool(os.environ.get("VISUS_DASHBOARDS_VERBOSE","0")) == True:
	ov.SetupLogger(logger)


# ////////////////////////////////////////////////////////////////////////////////////
class Canvas:
  
	# constructor
	def __init__(self, color_bar, color_mapper,sizing_mode='stretch_both'):
		self.sizing_mode=sizing_mode
		self.color_bar=color_bar
		self.color_mapper=color_mapper
		self.figure=bokeh.plotting.figure(active_scroll = "wheel_zoom") 
		self.figure.x_range = bokeh.models.Range1d(0,1024)   
		self.figure.y_range = bokeh.models.Range1d(0,768) 
		self.figure.toolbar_location="below"
		self.figure.sizing_mode = self.sizing_mode
		# self.figure.add_tools(bokeh.models.HoverTool(tooltips=[ ("(x, y)", "($x, $y)"),("RGB", "(@R, @G, @B)")])) # is it working?
  
		self.source_image = bokeh.models.ColumnDataSource(data={"image": [np.random.random((300,300))*255], "x":[0], "y":[0], "dw":[256], "dh":[256]})  
		self.figure.image("image", source=self.source_image, x="x", y="y", dw="dw", dh="dh", color_mapper=self.color_mapper)  
		self.figure.add_layout(self.color_bar, 'right')
 
		self.points     = None
		self.dtype      = None

	# getWidth
	def getWidth(self):
		return self.figure.inner_width

	# getHeight
	def getHeight(self):
		return self.figure.inner_height    

  	# getViewport
	def getViewport(self):
		x1,x2=self.figure.x_range.start, self.figure.x_range.end
		y1,y2=self.figure.y_range.start, self.figure.y_range.end 
		return (x1,y1,x2,y2)

  	# getViewport
	def setViewport(self,x1,y1,x2,y2):
		# fix aspect ratio
		W,H=self.getWidth(),self.getHeight()
		if W and H: 
			ratio=W/H
			w, h, cx, cy=(x2-x1),(y2-y1),0.5*(x1+x2),0.5*(y1+y2)
			w,h=(h*ratio,h) if W>H else (w,w/ratio) 
			x1,y1,x2,y2=cx-w/2,cy-h/2, cx+w/2, cy+h/2
		self.figure.x_range.start=x1
		self.figure.x_range.end  =x2
		self.figure.y_range.start=y1
		self.figure.y_range.end  =y2

	# renderPoints
	def renderPoints(self,points,size=20,color="red",marker="cross"):
		logger.info(f"Canvas::renderPoints {points}")
		if self.points is not None: 
			self.figure.renderers.remove(self.points)
		self.points = self.figure.scatter(x=[p[0] for p in points], y=[p[1] for p in points], size=size, color=color, marker=marker)   
		assert self.points in self.figure.renderers

	# getImage
	def getImage(self, data,normalize_float=True):

		height,width=data.shape[0],data.shape[1]

		# typycal case
		if data.dtype==np.uint8:

			# (height,width)::uint8... grayscale, I will apply the colormap
			if len(data.shape)==2:
				Gray=data
				return Gray 
	
			# (height,depth,channel)
			if len(data.shape)!=3:
				raise Exception(f"Wrong dtype={data.dtype} shape={data.shape}")

			channels=SplitChannels(data)

			if len(channels)==1:
				Gray=channels[0]
				return Gray

			if len(channels)==2:
				G,A=channels
				return  InterleaveChannels([G,G,G,A]).view(dtype=np.uint32).reshape([height,width]) 
	 
			elif len(channels)==3:
				R,G,B=channels
				A=np.full(channels[0].shape, 255, np.uint8)
				return  InterleaveChannels([R,G,B,A]).view(dtype=np.uint32).reshape([height,width]) 

			elif len(channels)==4:
				R,G,B,A=channels
				return InterleaveChannels([R,G,B,A]).view(dtype=np.uint32).reshape([height,width]) 
			
			
		else:

			# (height,depth) ... I will apply matplotlib colormap 
			if len(data.shape)==2:
				G=data.astype(np.float32)
				return G
			
			# (height,depth,channel)
			if len(data.shape)!=3:
				raise Exception(f"Wrong dtype={data.dtype} shape={data.shape}")  
		
			# convert all channels in float32
			channels=SplitChannels(data)
			channels=[channel.astype(np.float32) for channel in channels]

			if normalize_float:
				for C,channel in enumerate(channels):
					m,M=np.min(channel),np.max(channel)
					channels[C]=(channel-m)/(M-m)

			if len(channels)==1:
				G=channels[0]
				return G

			if len(channels)==2:
				G,A=channels
				return InterleaveChannels([G,G,G,A])
	 
			elif len(channels)==3:
				R,G,B=channels
				A=np.full(channels[0].shape, 1.0, np.float32)
				return InterleaveChannels([R,G,B,A])

			elif len(channels)==4:
				R,G,B,A=channels
				return InterleaveChannels([R,G,B,A])
		
		raise Exception(f"Wrong dtype={data.dtype} shape={data.shape}") 


	# renderImage
	def renderImage(self, data, x1, y1, x2, y2):
		img=self.getImage(data)
		dtype=img.dtype
 
		if self.dtype==dtype :
			# current dtype is 'compatible' with the new image dtype, just change the source _data
			self.source_image.data={"image":[img], "x":[x1], "y":[y1], "dw":[x2-x1], "dh":[y2-y1]}
		else:
			# need to create a new one from scratch
			self.figure.renderers=[]
			self.source_image = bokeh.models.ColumnDataSource(data={"image":[img], "x":[x1], "y":[y1], "dw":[x2-x1], "dh":[y2-y1]})
			if img.dtype==np.uint32:	
				self.image_rgba=self.figure.image_rgba("image", source=self.source_image, x="x", y="y", dw="dw", dh="dh") 
			else:
				self.img=self.figure.image("image", source=self.source_image, x="x", y="y", dw="dw", dh="dh", color_mapper=self.color_mapper) 
			self.dtype=img.dtype


# //////////////////////////////////////////////////////////////////////////////////////
class Widgets:

	# constructor
	def __init__(self):
   
		self.db=None

		self.widgets=types.SimpleNamespace()

		# palette
		self.m,self.M=0.0,1.0
		self.widgets.palette = bokeh.models.Select(title='Palette',  options=Widgets.GetPalettes(),value='Greys256',width=120,sizing_mode='fixed')
		self.widgets.palette.on_change ("value",lambda attr, old, new: self.setPalette(new, palette_range=self.getPaletteRange()))  
 
 		# color mapper
		self.color_mapper = bokeh.models.LinearColorMapper() # LogColorMapper
		self.color_mapper.palette=self.widgets.palette.value
		self.color_mapper.low=0
		self.color_mapper.high=1.0

		# colorbar
		self.color_bar = bokeh.models.ColorBar(color_mapper=self.color_mapper)
 
		# timestep
		self.widgets.timestep = bokeh.models.Slider(title='Time', value=0, start=0, end=1, sizing_mode='stretch_width')
		self.widgets.timestep.on_change ("value",lambda attr, old, new: self.setTimestep(int(new)))  
  
		# field
		self.widgets.field = bokeh.models.Select(title='Field',  options=["data"],value='data',width=120)
		self.widgets.field.on_change("value",lambda attr, old, new: self.setField(new))  
  
		# direction 
		self.widgets.direction = bokeh.models.Select(title='Direction', options=[('0','X'),('1','Y'),('2','Z')],value='2',width=80)
		self.widgets.direction.on_change ("value",lambda attr, old, new: self.setDirection(int(new)))  
  
		# offset 
		self.widgets.offset = bokeh.models.Slider(title='Offset', value=0, start=0, end=1024, sizing_mode='stretch_width')
		self.widgets.offset.on_change ("value",lambda attr, old, new: self.setOffset(int(new)))
  
		# num_refimements (0==guess)
		self.widgets.num_refinements=bokeh.models.Slider(title='Num Refinements', value=0, start=0, end=4, sizing_mode='stretch_width')
		self.widgets.num_refinements.on_change ("value",lambda attr, old, new: self.setNumberOfRefinements(int(new)))
  
		# quality (0==full quality, -1==decreased quality by half-pixels, +1==increase quality by doubling pixels etc)
		self.widgets.quality = bokeh.models.Slider(title='Quality', value=0, start=-12, end=+12, sizing_mode='stretch_width')
		self.widgets.quality.on_change("value",lambda attr, old, new: self.setQuality(int(new)))  
  
		# status_bar
		self.widgets.status_bar= {}
		self.widgets.status_bar["request" ]=bokeh.models.TextInput(title="Request" ,sizing_mode='stretch_width')
		self.widgets.status_bar["response"]=bokeh.models.TextInput(title="Response",sizing_mode='stretch_width')
  
	@staticmethod
	def GetPalettes():
		import colorcet 
		return [
	   	"Greys256", "Inferno256", "Magma256", "Plasma256", "Viridis256", "Cividis256", "Turbo256"
	  ] + [
		  it  for it in [
			'colorcet.blueternary', 
			'colorcet.coolwarm', 
			'colorcet.cyclicgrey', 
			'colorcet.depth', 
			'colorcet.divbjy', 
			'colorcet.fire', 
			'colorcet.geographic', 
			'colorcet.geographic2', 
			'colorcet.gouldian', 
			'colorcet.gray', 
			'colorcet.greenternary', 
			'colorcet.grey', 
			'colorcet.heat', 
			'colorcet.phase2', 
			'colorcet.phase4', 
			'colorcet.rainbow', 
			'colorcet.rainbow2', 
			'colorcet.rainbow3', 
			'colorcet.rainbow4', 
			'colorcet.redternary', 
			'colorcet.reducedgrey', 
			'colorcet.yellowheat']
		  if hasattr(colorcet,it[9:])
	]  

  # refresh (to override if needed)
	def refresh(self):
		pass

	# getPointDim
	def getPointDim(self):
		return self.db.getPointDim() if self.db else 2

	# getTimesteps
	def getTimesteps(self):
		return [int(value) for value in self.db.db.getTimesteps().asVector()]

	# getFields
	def getFields(self):
		return self.db.getFields()
  
	# setTimestep
	def setTimestep(self, value):
		self.widgets.timestep.value=value
		self.refresh()

	# getTimestep
	def getTimestep(self):	
		return int(self.widgets.timestep.value)

	# setField
	def setField(self,value):
		self.widgets.field.value=value
		self.refresh()
  
	# getField
	def getField(self):
		return str(self.widgets.field.value)

	# setDirection
	def setDirection(self,dir):
		pdim=self.getPointDim()
		if pdim==2: dir=2
		dims=[int(it) for it in self.db.getLogicSize()]
		self.widgets.direction.value = str(dir)

		# 2d there is no direction
		pdim=self.getPointDim()
		if pdim==2:
			assert dir==2
			self.widgets.offset.start, self.widgets.offset.end= 0,1
			self.widgets.offset.value = 0
		else:
			self.widgets.offset.start, self.widgets.offset.end = 0,int(dims[dir])
			self.widgets.offset.value = int(dims[dir]//2)
   
		self.refresh()

	# getDirection
	def getDirection(self):
		return int(self.widgets.direction.value)

	# setPalette
	def setPalette(self, value, palette_range=(0.0,1.0)):
		logger.info(f"Slice::setPalette direction={self.getDirection()} value={value} palette_range={palette_range}")
		self.widgets.palette.value=value
		if value.startswith("colorcet."):
			import colorcet
			value=getattr(colorcet,value[len("colorcet."):]) 
		self.color_mapper.palette=value
		self.color_mapper.low, self.color_mapper.high=palette_range
		self.refresh()

	# getPalette
	def getPalette(self):
		return self.widgets.palette.value

	# getPaletteRange
	def getPaletteRange(self):
		return self.color_mapper.low,self.color_mapper.high

	# setOffset (3d only)
	def setOffset(self,value):
		self.widgets.offset.value=value
		self.refresh()

	# getOffset
	def getOffset(self):
		return self.widgets.offset.value

	# setNumOfRefinements
	def setNumberOfRefinements(self,value):
		self.widgets.num_refinements.value=value
		self.refresh()

	# getNumberOfRefinements
	def getNumberOfRefinements(self):
		return self.widgets.num_refinements.value

	# setQuality
	def setQuality(self,value):
		self.widgets.quality.value=value
		self.refresh()

	# getQuality
	def getQuality(self):
		return self.widgets.quality.value


# ////////////////////////////////////////////////////////////////////////////////////
class Slice(Widgets):
    
    # constructor
    def __init__(self,doc=None, sizing_mode='stretch_both'):
        super().__init__()
        if doc is None: doc=bokeh.io.curdoc()
        self.doc=doc
        self.sizing_mode=sizing_mode
        self.access=None
        self.lock          = threading.Lock()
        self.aborted       = ov.Aborted()
        self.new_job       = False
        self.current_img   = None
        self.options={}
        self.render_id = 0
        self.canvas = Canvas(self.color_bar, self.color_mapper, sizing_mode=self.sizing_mode)
        self.status = {}
        self.layout=bokeh.layouts.column(children=[],sizing_mode=self.sizing_mode)
        self.show_options=["palette","timestep","field","direction","offset","quality","num_refinements","status_bar"]
        self.callback = doc.add_periodic_callback(self.onTimer, 100)  
        self.query=PyQuery()
        self.query.startThread()
        
    # setShowOptions
    def setShowOptions(self,value):
        self.show_options=value
  
	# getShowOptions
    def getShowOptions(self):
        return self.show_options

    # setDataset
    def setDataset(self,  db , direction=2):
        self.db=db
        self.access=self.db.createAccessForBlockQuery()
        while self.layout.children:
            self.layout.children.pop()
        first_row=[]
  
        if "palette" in self.show_options:  
            first_row.append(self.widgets.palette)

        timesteps=self.getTimesteps()
        self.widgets.timestep.end= max(1,len(timesteps)-1)
        if len(timesteps)>1 and "timestep" in self.show_options:  
            first_row.append(self.widgets.timestep)
  
        if len(self.getFields())>1 and "field" in self.show_options:
            first_row.append(self.widgets.field)
            
        if "num_refinements" in self.show_options:
            first_row.append(self.widgets.num_refinements)

        if "quality" in self.show_options:
            first_row.append(self.widgets.quality)            

        if self.getPointDim()==3 and "direction" in self.show_options:
            first_row.append(self.widgets.direction)
   
        if self.getPointDim()==3 and "offset" in self.show_options:
            first_row.append(self.widgets.offset)

        self.layout.children.append(bokeh.layouts.Row(*first_row, sizing_mode='stretch_width'))  
        self.layout.children.append(self.canvas.figure)
        
        if "status_bar" in self.show_options:
            self.layout.children.append(bokeh.layouts.Row(
                self.widgets.status_bar["request"],
                self.widgets.status_bar["response"], 
                sizing_mode='stretch_width'))
  
        self.setTimestep(timesteps[0])
        self.setField(self.getFields()[0])
        self.setDirection(direction)    

    # refresh
    def refresh(self):
        self.aborted.setTrue()
        self.new_job=True

    # enableDoubleTap
    def enableDoubleTap(self,fn):
        self.canvas.figure.on_event(bokeh.events.DoubleTap, lambda evt: fn(self.unproject((evt.x,evt.y))))
   
    # project
    def project(self,value):
        pdim=self.getPointDim()
        dir=self.getDirection()
        if hasattr(value[0],"__iter__"):
            p1,p2=(list(value[0]),list(value[1]))
            if pdim==3:
                del p1[dir]
                del p2[dir]
            return (p1,p2)
        # is a point
        else:
            p=list(value)
            if pdim==3:
                del p[dir]
            return p

    # unproject
    def unproject(self,value):

        pdim=self.getPointDim() 

        # no projection needed
        if pdim!=3: 
            return value

        dir=self.getDirection()
        # is a box?
        if hasattr(value[0],"__iter__"):
            p1,p2=(list(value[0]),list(value[1]))
            p1.insert(dir, self.widgets.offset.value+0)
            p2.insert(dir, self.widgets.offset.value+1)
            return (p1,p2)
        # is a point
        else:
            p=list(value)
            p .insert(dir, self.widgets.offset.value+0)
            return p
  
    # getLogicBox
    def getLogicBox(self):
        x1,y1,x2,y2=self.canvas.getViewport()
        return self.unproject(((x1,y1),(x2,y2)))

    # setLogicBox (NOTE: it ignores the coordinates on the direction)
    def setLogicBox(self,value):
        proj=self.project(value)
        self.canvas.setViewport(*(proj[0] + proj[1]))
        self.refresh()
  
    # getLogicCenter
    def getLogicCenter(self):
        pdim=self.getPointDim()  
        p1,p2=self.getLogicBox()
        assert(len(p1)==pdim and len(p2)==pdim)
        return [(p1[I]+p2[I])*0.5 for I in range(pdim)]

    # getLogicSize
    def getLogicSize(self):
        pdim=self.getPointDim()
        p1,p2=self.getLogicBox()
        assert(len(p1)==pdim and len(p2)==pdim)
        return [(p2[I]-p1[I]) for I in range(pdim)]

    # setAccess
    def setAccess(self, value):
        self.access=value
        self.refresh()

    # setDirection
    def setDirection(self,dir):
        super().setDirection(dir)
        dims=[int(it) for it in self.db.getLogicSize()]
        self.setLogicBox(([0]*self.getPointDim(),dims))
        self.refresh()
  

  # gotoPoint
    def gotoPoint(self,point):
        pdim=self.getPointDim()
        # go to the slice
        if pdim==3:
            dir=self.getDirection()
            self.setOffset(point[dir])
        # the point should be centered in p3d
        (p1,p2),dims=self.getLogicBox(),self.getLogicSize()
        p1,p2=list(p1),list(p2)
        for I in range(pdim):
            p1[I],p2[I]=point[I]-dims[I]/2,point[I]+dims[I]/2
        self.setLogicBox([p1,p2])
        self.canvas.renderPoints([self.project(point)])
  
    # renderImage
    def renderImage(self,I,N,timestep,field,query_box, data, msec):
        (x1,y1),(x2,y2)=self.project(query_box)
        self.canvas.renderImage(data,x1,y1,x2,y2)
        tot_pixels=data.shape[0]*data.shape[1]
        canvas_pixels=self.canvas.getWidth()*self.canvas.getHeight()
        self.widgets.status_bar["response"].value=f"{I}/{N} tms={timestep} fld={field} bx={query_box} pxl={tot_pixels:,}/{canvas_pixels:,} msc={msec}"  
        self.render_id+=1     

    # onTimer
    def onTimer(self):

        # ready for jobs?
        canvas_w,canvas_h=(self.canvas.getWidth(),self.canvas.getHeight())
        if canvas_w==0 or canvas_h==0 or not self.db:
            return

        # simulate fixAspectRatio (i cannot find a bokeh metod to watch for resize event)
        if self.status.get("w",0)!=canvas_w or self.status.get("h",0)!=canvas_h:
            self.canvas.setViewport(*self.canvas.getViewport())
            self.status["w"]=canvas_w
            self.status["h"]=canvas_h
            self.refresh()
   
        # a new image is available?
        result=self.query.popResult(last_only=True) 
        if result is not None:
            self.renderImage(*result)

        # push a new job if necesssary
        logic_box=self.getLogicBox()
        pdim=self.getPointDim()
        if self.new_job or str(self.status.get("logic_box",""))!=str(logic_box):
            # abort the last one
            self.aborted.setTrue()
            self.query.waitIdle()
            num_refinements = self.getNumberOfRefinements()
            if num_refinements==0:
                num_refinements=3 if pdim==2 else 4
            self.aborted=ov.Aborted()
            
            # compute max_pixels
            max_pixels=canvas_w*canvas_h
            quality=self.getQuality()
            if quality==0:
                pass
            elif quality<0:
                max_pixels=int(max_pixels/pow(1.3,abs(quality))) # decrease the quality
            else:
                max_pixels=int(max_pixels*pow(1.3,abs(quality))) # increase the quality
                
            timestep=self.getTimestep()
            field=self.getField()
            box_i=[[int(it) for it in jt] for jt in logic_box]
            self.widgets.status_bar["request"].value=f"tms={timestep} fdl={field} bx={box_i} nrf={num_refinements} qlt={quality} max_pxl={max_pixels:,}"
            self.query.pushJob(self.db, self.access, timestep, field, logic_box, max_pixels, num_refinements,self.aborted)
            self.status["logic_box"]=logic_box
            self.new_job=False


# //////////////////////////////////////////////////////////////////////////////////////
class Slices(Widgets):

	# constructor
	def __init__(self, doc=None,sizing_mode='stretch_both'):
		super().__init__()
		if doc is None: doc=bokeh.io.curdoc()
		self.doc=doc
		self.sizing_mode=sizing_mode
		self.slices=[]
		self.widgets.nviews=bokeh.models.Select(title='Layout',  options=["1","2","3","4"],value='3',width=50,sizing_mode='fixed')
		self.widgets.nviews.on_change("value",lambda attr, old, new: self.setDataset(self.db, layout=int(new)))
		self.layout=bokeh.layouts.column(children=[],sizing_mode=self.sizing_mode)
		self.show_options=[
      		"nviews","palette","timestep","field","quality","num_refinements",
        	"!direction","!offset" # this will be show on the single SLice
         ],

	# getHeaderLayout
	def getHeaderLayout(self):
   
		v=[]

		if "nviews" in self.show_options:
			v.append(self.widgets.nviews)
   
		if "palette" in self.show_options:
			v.append(self.widgets.palette)
  
		timesteps=self.getTimesteps()
		self.widgets.timestep.end= max(1,len(timesteps)-1)
		if len(timesteps)>1 and "timestep" in self.show_options:  
			v.append(self.widgets.timestep)
  
		if len(self.getFields())>1 and "field" in self.show_options:
			v.append(self.widgets.field)
   
		if "quality" in self.show_options:
			v.append(self.widgets.quality) 
  
		if "num_refinements" in self.show_options:
			v.append(self.widgets.num_refinements)  

		if self.getPointDim()==3 and "direction" in self.show_options:
			v.append(self.widgets.direction)
   
		if self.getPointDim()==3 and "offset" in self.show_options:
			v.append(self.widgets.offset)   

		return bokeh.layouts.Row(*v, sizing_mode='stretch_width')

	# getCells
	def getCells(self,value=None):
		if value is None or value==1: return [[2]] # just one 'Z' cell
		if value==2:                  return [[0,1]] # 'x' and 'y'
		if value==3:                  return [['r',0],[1,2]] # <empty> x,y,z
		if value==4:                  return [[2,0],[1,2]] # z,x,y,z
		return value

	# getCentralLayout
	def getCentralLayout(self, layout=None):
		cells=self.getCells(layout)
		nrows,ncols=len(cells),len(cells[0])
		children=[]
		for R in range(nrows):
			for C in range(ncols):
				cell=cells[R][C]
				if cell=="r":
						children.append(bokeh.layouts.Row())
				elif cell=="c":
						children.append(bokeh.layouts.Col())
				elif cell in [0,1,2]:
					slice=Slice(self.doc,sizing_mode=self.sizing_mode)	
					slice.show_options=["direction","offset"]
					slice.enableDoubleTap(self.gotoPoint)
					slice.setDataset(self.db, direction=cell)
					self.slices.append(slice)
					children.append(slice.layout)
				else:
					children.append(cell)
		ret=bokeh.layouts.grid(children=children, nrows=nrows, ncols=ncols, sizing_mode=self.sizing_mode) 
		return ret

	# clearSlices
	def clearSlices(self):
		
		for slice in self.slices:
			slice.aborted.setTrue()
			slice.query.stopThread()
  
		self.slices=[]  
		while self.layout.children:
			self.layout.children.pop()  
   
	# setDataset
	def setDataset(self, db, layout=None):
		self.clearSlices()
		self.db=db
		self.layout.children.append(self.getHeaderLayout())
		self.layout.children.append(self.getCentralLayout(layout))
		# in case I need to keep old stuff
		self.setTimestep(self.getTimestep())
		self.setField(self.getField()) 
		self.setPalette(self.getPalette(),palette_range=self.getPaletteRange()) 

	# setTimestep
	def setTimestep(self, value):
		super().setTimestep(value)
		for slice in self.slices:
			slice.setTimestep(value)
			
	# setField
	def setField(self, value):
		super().setField(value)
		for slice in self.slices:
			slice.setField(value)
  
	# setPalette
	def setPalette(self,value, palette_range=(0.0,1.0)):
		logger.info(f"Slices::setPalette value={value} palette_range={palette_range}")
		super().setPalette(value, palette_range)
		for slice in self.slices:
			slice.setPalette(value,palette_range=palette_range)

	# setQuality
	def setQuality(self,value):
		logger.info(f"Slices::setQuality value={value} ")    
		super().setQuality(value)
		for slice in self.slices:
			slice.setQuality(value)   
   
 	# setNumOfRefinements
	def setNumOfRefinements(self,value):
		logger.info(f"Slices::setNumOfRefinements value={value} ")    
		super().setNumOfRefinements(value)
		for slice in self.slices:
			slice.setNumOfRefinements(value)     

	# gotoPoint
	def gotoPoint(self, p):
		for slice in self.slices:
			slice.gotoPoint(p)
