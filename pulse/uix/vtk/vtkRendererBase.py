from abc import ABC, abstractmethod 
import vtk

class vtkRendererBase(ABC):
    def __init__(self, style):
        super().__init__()
        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground(0.2,0.2,0.2)
        self._style = style
        self._style.SetDefaultRenderer(self._renderer)
        self._textActor = vtk.vtkTextActor()
        self.actors = {}
        self._inUse = False
        self._usePicker = True
        self.textProperty = vtk.vtkTextProperty()
        self.textProperty.SetFontSize(16)
        # self.textProperty.SetItalic(1)

    def resetCamera(self):
        self._renderer.ResetCamera()

    def getRenderer(self):
        return self._renderer

    def getStyle(self):
        return self._style

    def getSize(self):
        return self._renderer.GetSize()

    def getInUse(self):
        return self._inUse

    def getUsePicker(self):
        return self._usePicker

    def setUsePicker(self, value):
        self._usePicker = value

    def setInUse(self, value):
        self._style.releaseButtons()
        self._inUse = value

    def createInfoText(self, text):
        #Remove the actor if it already exists
        self._renderer.RemoveActor2D(self._textActor)

        height = self._renderer.GetSize()[1] - 30
        width = 20
        
        self.textProperty.SetVerticalJustificationToTop()
        self.textProperty.SetJustificationToLeft()
        self._textActor.SetInput(text)
        self._textActor.SetTextProperty(self.textProperty)
        self._textActor.SetDisplayPosition(width, height)
        self._renderer.AddActor2D(self._textActor)

    @abstractmethod
    def updateInfoText(self):
        #It's necessary to call createInfoText with the text to plot.
        pass

    @abstractmethod
    def plot(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def update(self):
        pass