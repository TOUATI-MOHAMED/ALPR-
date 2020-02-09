#!/usr/bin/python
# -*- coding: utf-8 *-*
"""
@author: López Ricardo Ezequiel
@license: GNU GENERAL PUBLIC LICENSE
@contact: mail@lopezezequiel.com
"""



########################################################################
#IMPORTS
########################################################################
import wx
import inspect


class ImagePanel(wx.Panel):


########################################################################
#CONSTANTS
########################################################################

    DEFAULT_CONFIG      = 0     #Set optimal size & pos, draggable=enabled, autorefresh=enabled, zoomwheel=enabled
    
    OPTIMAL_SIZE        = 0     #best size is chosen automatically
    NORMAL_SIZE         = 1     #original image size    
    TIGHT_SIZE          = 2     #max size that fits on the panel
    FULL_SIZE           = 3     #min size that fills entire panel
    ZOOM_SIZE           = 4     #it depends on the zoom
            
    
    OPTIMAL_X_POS       = 0     #best horizontal position is chosen automatically
    LEFT_POS            = 8     #align image to the left
    RIGHT_POS           = 16    #align image to the right
    SCROLLED_X_POS      = 24    #it depends on the scroll
    CENTERED_X_POS      = 32    #center the image on x axis
    
    OPTIMAL_Y_POS       = 0     #best vertical position is chosen automatically
    TOP_POS             = 64    #align image to the top
    BOTTOM_POS          = 128   #align image to the bottom
    SCROLLED_Y_POS      = 192   #it depends on the scroll
    CENTERED_Y_POS      = 256   #center the image on x axis
    
    #Move image with the mouse?
    DRAGGABLE           = 0
    NO_DRAGGABLE        = 512

    #Repaint automatically when calling methods shrink, enlarge, move, etc
    AUTO_REFRESH        = 0
    MANUAL_REFRESH      = 1024
    
    #Allow zooming with mouse wheel?
    ZOOM_WHEEL          = 0
    NO_ZOOM_WHEEL       = 2048
    



########################################################################
#INIT
########################################################################
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._SetUp()
        self._RecordEvents()


########################################################################
#PRIVATE METHODS
########################################################################        
    def _SetUp(self):   
        self.minZoom = 20.0;
        self.maxZoom = 120.0;   
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY)
        self.image = wx.EmptyImage(1, 1)

        self.SetConfig(self.DEFAULT_CONFIG)
        self.SetZoomStep(5.0)
        self.SetZoom(100.0)
        self.ScrollXY(0, 0)
    
    
    ####################################################################
    #EVENTS
    ####################################################################
    def _RecordEvents(self):
        self.Bind(wx.EVT_SIZE, self._OnSize)
        self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self._OnLeftDown)
        self.Bind(wx.EVT_MOUSEWHEEL, self._OnMouseWheel)    
        

    def _OnSize(self, e):
        """Resize image on resize event
        """
        self._RefreshImage()


    def _OnMouseWheel(self, e):
        """It allows zooming with mouse wheel
        """
        if self.ZoomWheel():
            Wimg, Himg = self.GetImageSize()
            
            X = e.GetX() - self.GetScrollX()
            Xr = X / Wimg
            
            Y = e.GetY() - self.GetScrollY()
            Yr = Y / Himg
            
            auto = self.AutoRefresh()
            self.SetManualRefresh()
            
            if e.GetWheelRotation() > 0:
                self.Enlarge()
            else:
                self.Shrink()
            
            if auto:
                self.SetAutoRefresh()
                
            Wimg, Himg = self.GetImageSize()
            scrollX = e.GetX() - Xr * Wimg
            scrollY = e.GetY() - Yr * Himg
            
            self.ScrollXY(scrollX, scrollY)


    def _OnLeftDown(self, e):
        """Init move of image
        """
        if self.IsDraggable():
            self.imageCtrl.Bind(wx.EVT_LEFT_UP, self._OnLeftUp)
            self.mouseX, self.mouseY = e.GetPosition()

    
    def _OnLeftUp(self, e):
        """Stop move of image
        """
        mouseX, mouseY = e.GetPosition()
        Xdiff = mouseX - self.mouseX
        Ydiff = mouseY - self.mouseY
        self.MoveXY(Xdiff, Ydiff)
        self.imageCtrl.Unbind(wx.EVT_LEFT_UP)
        

    ####################################################################
    #SIZES
    ####################################################################        
    def _GetTightSize(self):
        """Returns the max size of image that fits on panel
        @return: (width, height)
        @rtype: (float, float)
        """
        Wmax, Hmax = self.GetSize()
        Wimg, Himg = self.image.GetSize()
        
        if Wimg == 0 or Himg == 0:
            return (0, 0)
        
        Wr = Wmax / float(Wimg)
        Hr = Hmax / float(Himg)
        
        if Wr < Hr:
            W = Wmax
            H = Himg * W / float(Wimg)
        else:
            H = Hmax
            W = Wimg * H / float(Himg)
            
        return (W, H)

    
    def _GetFullSize(self):
        """Returns the min size of image that covers the entire panel
        @return: (width, height)
        @rtype: (float, float)
        """
        Wmax, Hmax = self.GetSize()
        Wimg, Himg = self.image.GetSize()
        
        if Wimg == 0 or Himg == 0:
            return (0, 0)
        
        Wr = Wmax / float(Wimg)
        Hr = Hmax / float(Himg)
        
        if Wr < Hr:
            H = Hmax
            W = Wimg * H / float(Himg)
        else:
            W = Wmax
            H = Himg * W / float(Wimg)
            
        return (W, H)
        
    
    def _GetOptimalSize(self):
        """Returns the best size for image according to the original size
        @return: (width, height)
        @rtype: (float, float)
        """
        Wmax, Hmax = self.GetSize()
        Wimg, Himg = self.image.GetSize()
        
        if Wmax >= Wimg and Hmax >= Himg:
            return self._GetNormalSize()

        return self._GetTightSize()
            
    
    def _GetNormalSize(self):
        """Returns original image size
        @return: (width, height)
        @rtype: (float, float)
        """
        originalSize = self.image.GetSize()
        width, height = originalSize
        return (float(width), float(height))


    def _GetZoomSize(self):
        """Returns image size based in zoom value
        @return: (width, height)
        @rtype: (float, float) 
        """
        zoom = self.GetZoom()
        Wimg, Himg = self.image.GetSize()
        
        W = zoom * Wimg / 100
        H = zoom * Himg / 100
        
        return (W, H)
        
        
    def _GetHeights(self):
        """Returns height values
        @return: (imageHeight, panelHeight, difference)
        @rtype: (float, float, float)
        """
        Himg = self.GetImageSize()[1]
        Hmax = self.GetSize()[1]
        Hdiff = Hmax - Himg
        return (Himg, Hmax, Hdiff)
        
    
    def _GetWidths(self):
        """Returns width values
        @return: (imageWidth, panelWidth, difference)
        @rtype: (float, float, float)
        """
        Wimg = self.GetImageSize()[0]
        Wmax = self.GetSize()[0]
        Wdiff = Wmax - Wimg
        return (Wimg, Wmax, Wdiff)


    ####################################################################
    #OTHERS
    ####################################################################        
    def _RefreshImage(self):
        """Refresh the image only if autorefresh is enable
        """
        if self.AutoRefresh():
            self.RefreshImage()


    def _GetBitmap(self):
        """Returns bitmap of image in the right size
        @return: bitmap of image
        @rtype: wx.Bitmap
        """
        image = self.image.Scale(*self.GetImageSize())
        return wx.BitmapFromImage(image)


    def _validate(self, value, value_type):
        if not isinstance(value, value_type):
            error = inspect.stack()[2]
            repl = (error[1], error[2], error[3], value_type)
            msg = 'File "%s", line %d, in %s. The type must be %s' % repl
            raise TypeError(msg)


########################################################################
#PUBLIC METHODS
########################################################################


    ####################################################################
    #CONFIG
    ####################################################################    
    def SetAutoRefresh(self):
        """Enable autorefresh
        """
        self.config &= ~self.MANUAL_REFRESH
        
    
    def SetManualRefresh(self):
        """Disable autorefresh
        """
        self.config |= self.MANUAL_REFRESH
        

    def AutoRefresh(self):
        """Returns true if autorefresh is enable
        @rtype: bool
        """
        return self.config & self.MANUAL_REFRESH == 0
        
        
    def ManualRefresh(self):
        """Returns true if autorefresh is disable
        @rtype: bool
        """
        return not self.AutoRefresh()
    

    def SetConfig(self, config):
        """It allow to configurate panel behaviour
        @param config: bit mask
        @type config: int
        """
        self._validate(config, int)
        self.config = config
        

    def GetConfig(self):
        """Returns panel configuration
        @return: bit mask
        @rtype: int
        """
        return self.config


    def GetSizeConfig(self):
        """Returns size configuration
        @rtype: int
        """
        return self.config & 7


    def GetXPositionConfig(self):
        """Returns horizontal position configuration
        @rtype: int
        """     
        return self.config & 56


    def GetYPositionConfig(self):
        """Returns vertical position configuration
        @rtype: int
        """
        return self.config & 448
    
    def IsDraggable(self):
        """Returns true if panel is configured as draggable
        @rtype: bool
        """
        return self.config & self.NO_DRAGGABLE == 0
        
    
    def ZoomWheel(self):
        """Returns true if panel is configured to allow zoom with mouse wheel
        @rtype: bool
        """
        return self.config & self.NO_ZOOM_WHEEL == 0
    
    
    ####################################################################
    #SETTERS & GETTERS FOR ZOOM & SIZE
    ####################################################################    
    def SetZoomStep(self, zoomStep):
        """Set percent of zoom step
        @param zoomStep: percent of step
        @type zoomStep: float
        """
        self._validate(zoomStep, (int, float))
        self.zoomStep = float(-zoomStep if zoomStep < 0 else zoomStep) 

    
    def SetMaxZoom(self, maxZoom):
        """Set percent of max zoom
        @param maxZoom: percent of max zoom
        @type maxZoom: float
        """
        self._validate(maxZoom, (int, float))
        self.maxZoom = float(self.minZoom if maxZoom < minZoom else self.maxZoom)
        
        
    def SetMinZoom(self, minZoom):
        """Set percent of min zoom
        @param minZoom: percent of min zoom 
        @type minZoom: float
        """
        self._validate(minZoom, (int, float))
        self.minZoom = float(0 if minZoom < 0 else (minZoom if minZoom < self.maxZoom else self.maxZoom))
                
    
    def SetZoom(self, zoom):
        """Set percent of zoom
        @param zoom: percent of zoom
        @type zoom: float
        """
        self._validate(zoom, (int, float))
        self.zoom = float(self.minZoom if zoom < self.minZoom else (self.maxZoom if zoom > self.maxZoom else zoom) )
        self._RefreshImage() 
    

    def AutoZoom(self):
        """Set best zoom for image
        """
        self.SetZoom(self.GetBestZoom())


    def Enlarge(self):
        """Increase de zoom and enlarge the image
        """
        self.SetZoom(self.zoom + self.zoomStep)
        self._RefreshImage()
                
                
    def Shrink(self):
        """Decreases de zoom and shrink the image
        """
        self.SetZoom(self.zoom - self.zoomStep)
        self._RefreshImage()
    

    def GetBestZoom(self):
        """Returns the best zoom for the image according to the size of the panel
        @return: best zoom
        @rtype: float
        """
        Wimg = self.image.GetSize()[0]
        if Wimg != 0:
            W = self._GetOptimalSize()[0]
            return W * 100.0 / Wimg
        return 0.0
        
        
    def GetMinZoom(self):
        """Returns minzoom
        @return: minzoom
        @rtype: float
        """
        return self.minZoom
        
        
    def GetMaxZoom(self):
        """Returns maxzoom
        @return: maxzoom
        @rtype: float
        """
        return self.maxZoom
        
    
    def GetZoom(self):
        """Returns current zoom
        @return: current zoom
        @rtype: float
        """
        return self.zoom


    def GetImageSize(self): 
        """Returns image size according to the size configuration 
        @return: image size
        @rtype: (float, float)
        """

        size_config = self.GetSizeConfig()
        
        return {
            self.TIGHT_SIZE:        self._GetTightSize,
            self.OPTIMAL_SIZE:      self._GetOptimalSize,
            self.NORMAL_SIZE:       self._GetNormalSize,
            self.FULL_SIZE:         self._GetFullSize,
            self.ZOOM_SIZE:         self._GetZoomSize
        }[size_config]()
        

    ####################################################################
    #SETTERS & GETTERS FOR POSITION
    ####################################################################
    def MoveX(self, x):
        """Move horizontaly the image
        @param x: relative distance
        @type x: int, float
        """
        self._validate(x, (int, float))
        self.ScrollX(self.x + x)


    def MoveY(self, y):
        """Move verticaly the image
        @param y: relative distance
        @type y: int, float
        """
        self._validate(y, (int, float))
        self.ScrollY(self.y + y)

        
    def MoveXY(self, x, y):
        """Move image
        @param x: relative distance in x
        @type x: int, float
        @param y: relative distance in y
        @type y: int, float
        """
        self._validate(x, (int, float))
        self._validate(y, (int, float))
        self.ScrollXY(self.x + x, self.y + y)
                
        
    def ScrollX(self, x):
        """It sets the horizontal absolute displacement
        @param x: x displacement
        @type x: int, float
        """
        self._validate(x, (int, float))
        self.ScrollXY(x, self.y)


    def ScrollY(self, y):
        """It sets the vertical absolute displacement
        @param y: y displacement
        @type y: int, float
        """
        self._validate(y, (int, float))
        self.ScrollXY(self.x, y)
                
        
    def ScrollXY(self, x, y):
        """It sets the absolute displacement
        @param x: x displacement
        @type x: int, float
        @param y: y displacement
        @type y: int, float
        """
        self._validate(x, (int, float))
        self._validate(y, (int, float))
        self.x = self.GetMinScrollX() if x < self.GetMinScrollX() else (self.GetMaxScrollX() if x > self.GetMaxScrollX() else x)
        self.y = self.GetMinScrollY() if y < self.GetMinScrollY() else (self.GetMaxScrollY() if y > self.GetMaxScrollY() else y)
        self._RefreshImage()
    

    def isOnLeft(self):
        """Returns true if horizontal scroll is 0
        @rtype: bool
        """
        return self.GetScrollX() == 0
    

    def isOnRight(self):
        """Returns true if horizontal scroll is max
        @rtype: bool
        """
        Wdiff = self._GetWidths()[2]
        return self.GetScrollX() == Wdiff
    

    def isOnTop(self):
        """Returns true if vertical scroll is 0
        @rtype: bool
        """
        return self.GetScrollY() == 0
    

    def isOnBottom(self):
        """Returns true if vertical scroll is max
        @rtype: bool
        """
        Hdiff = self._GetHeights()[2]
        return self.GetScrollY() == Hdiff
        

    def GetMinScrollX(self):
        """Returns minimum possible horizontal scroll
        @return: min scroll
        @rtype: float
        """
        Wdiff = self._GetWidths()[2]
        return Wdiff if Wdiff < 0 else 0.0
        
        
    def GetMinScrollY(self):
        """Returns minimum possible vertical scroll
        @return: min scroll
        @rtype: float
        """
        Hdiff = self._GetHeights()[2]
        return Hdiff if Hdiff < 0 else 0
            

    def GetMaxScrollX(self):
        """Returns maximum possible horizontal scroll
        @return: max scroll
        @rtype: float
        """
        Wdiff = self._GetWidths()[2]
        return Wdiff if Wdiff > 0 else 0
    
    
    def GetMaxScrollY(self):
        """Returns maximum possible vertical scroll
        @return: max scroll
        @rtype: float
        """
        Hdiff = self._GetHeights()[2]
        return Hdiff if Hdiff > 0 else 0
        
        
    def GetScrollX(self):
        """Returns horizontal scroll
        @return: horizontal scroll
        @rtype: float
        """
        x_config = self.GetXPositionConfig()
        Wdiff = self._GetWidths()[2]
        
        if x_config == self.OPTIMAL_X_POS:
            if Wdiff < 0:
                x_config = self.SCROLLED_X_POS
            else:
                x_config = self.CENTERED_X_POS

        if x_config == self.SCROLLED_X_POS:
            px = self.x
        elif x_config == self.CENTERED_X_POS:
            px =   Wdiff / 2.0
        elif x_config == self.LEFT_POS:
            px = 0.0
        else:
            px = Wdiff
        
        return px
    
    
    def GetScrollY(self):
        """Returns vertical scroll
        @return: vertical scroll
        @rtype: float
        """
        y_config = self.GetYPositionConfig()
        Hdiff = self._GetHeights()[2]
        
        if y_config == self.OPTIMAL_Y_POS:
            if Hdiff < 0:
                y_config = self.SCROLLED_Y_POS
            else:
                y_config = self.CENTERED_Y_POS
        
        if y_config == self.SCROLLED_Y_POS:
            py = self.y
        elif y_config == self.CENTERED_Y_POS:
            py =   Hdiff / 2.0
        elif y_config == self.TOP_POS:
            py = 0
        else:
            py = Hdiff
    
        return py


    def GetPosition(self):
        """Returns scroll position
        @return: (scroll x, scroll y)
        @rtype: (float, float)
        """
        return (self.GetScrollX(), self.GetScrollY())
    

    ####################################################################
    #OTHERS
    ####################################################################
    def SetImage(self, image):
        """Used to set an image
        @param image: an image
        @type image: wx.Image
        """
        self._validate(image, wx.Image)
        self.image = image
        self._RefreshImage()
        
        
    def RefreshImage(self):
        """Repaints the image
        """
        self.imageCtrl.SetBitmap(self._GetBitmap())
        self.imageCtrl.SetPosition(self.GetPosition())
