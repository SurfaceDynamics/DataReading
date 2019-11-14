import Shader
from OpenGL.GL import *
import OpenGL.GL.shaders
import pyrr
from PIL import Image

import glfw
from OpenGL.GL import *
import numpy as np
import guiEngine
import guiWindow
import generatePrimitive
import fontLoader
import fontRenderer
import mainDatabase
import time
class MainGUI:
    def __init__(self):
        self.DragNDrop = False
        self._size = np.array([1200, 800])
        self._dropSize = np.array([500, 250])
        self._space = 20
        self._database = mainDatabase.MainDatabase()
        self._generatePlot = None
        self.QUIT = False
    def Initiation(self):
        self._Window = guiWindow.GUIWindow("Database Reader", self._size[0], self._size[1], np.array([1.0, 1.0, 1.0]), np.array([0.5, 0.5, 0.5]))
        self._PrimetiveShape = generatePrimitive.GeneratePrimetive()
        self._FontLoader = fontLoader.FontLoader()

        self._background = guiEngine.GuiEngine(1, self._Window, self._PrimetiveShape, self._FontLoader,
                                              0, 0, self._size[0], self._size[1],
                                              "../res/sdb_s.png")
        self._dragNdrop = guiEngine.GuiEngine(1, self._Window, self._PrimetiveShape, self._FontLoader,
                                              (self._size[0] - self._dropSize[0])/2,
                                              (self._size[1] - self._dropSize[1])/2,
                                              self._dropSize[0],
                                              self._dropSize[1])
        self._generateExcel = guiEngine.GuiEngine(1, self._Window, self._PrimetiveShape, self._FontLoader,
                                              self._space,
                                              self._space,
                                              self._space*8,
                                              self._space * 4)
        self._generatePlot = guiEngine.GuiEngine(1, self._Window, self._PrimetiveShape, self._FontLoader,
                                                  self._size[0] - self._space * 9,
                                                  self._space,
                                                  self._space * 8,
                                                  self._space * 4)
        self._feedback = fontRenderer.FONTRENDERER(self._Window, self._FontLoader, 800)
        self._feedbackMSG = ""
        self.Path = ""

    def Render(self):
        fpsLimit = 20
        endTime = 0
        while not glfw.window_should_close(self._Window.Window):
            startTime = time.clock()
            deltaTime = startTime - endTime
            if deltaTime > 0:
                if int(1 / deltaTime) >= fpsLimit:
                    time.sleep(abs(deltaTime - 1 / fpsLimit))
            endTime = time.clock()

            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self._background.DrawPlane()
            self.DragNDrop = self._dragNdrop.DrawDragNDrop()
            self._generateExcel.DrawHoldButton("Push Excel")
            self._generatePlot.DrawHoldButton("Plot Data")
            if self._generateExcel.ButtonState:
                if self._dragNdrop.DragNDropFlag:
                    self.Path = self._dragNdrop._PathSplitter.Path
                    if self._database.PushExcellSheet(self.Path) is False:
                        self._feedbackMSG = "Corrupt database"
                    else:
                        self._feedbackMSG = "Push successful"
                else:
                    self._feedbackMSG = "Cannot read file"
                self._generateExcel.ButtonState = False
            self._feedback.DrawText(self._feedbackMSG, self._size[0] / 2, self._space * 4, 0.5, (1, 1, 1), True)

            glfw.swap_buffers(self._Window.Window)
            glfw.poll_events()
        self.QUIT = True