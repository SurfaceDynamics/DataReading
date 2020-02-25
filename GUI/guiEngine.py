from PIL import Image
from OpenGL.GL import *
import pyrr
import numpy as np
import Shader
import fontRenderer
import keyboardCommands
import pathSplitter




class GuiEngine:
    def __init__(self, Scaler, WindowPointer, PrimetiveShapePointer, FontLoaderPointer, PosX, PosY, SizeX, SizeY, TexturePath=None):
        # Pointers
        self._Window = WindowPointer
        self._Primetive = PrimetiveShapePointer
        self._fontLoader = FontLoaderPointer
        self._PathSplitter = pathSplitter.PathSplitter()

        # Static values
        self._windowScaler = Scaler
        self._textSize = 0.25 * self._windowScaler
        self._baseAlpha = 0.88
        self._edge = 1.3
        self.TextBoxKeyEvent = False


        self._leftClickGuard = False
        self.ButtonState = False
        self._buttonHold = False
        self.SlidebarPercent = 0.5
        self._initiationFlag = True

        # DropDown Menu
        self._lastDropSize = False
        self._endPos = 0
        self._rangeText = 0
        self.DropDownIndex = 0
        self._spaceScale = self._textSize * 110
        self._dropDownName = ""
        self.dropDownHold = False







        self._sizeX = SizeX * self._windowScaler
        self._sizeY = SizeY * self._windowScaler
        self._positionX = PosX * self._windowScaler
        self._positionY = PosY * self._windowScaler
        self._RENDERTEXTURE = False
        if TexturePath is not None:
            self._loadImageData(TexturePath)
            self._RENDERTEXTURE = True

        self._lastWindowSizeX = self._Window.width
        self._lastWindowSizeY = self._Window.height
        self._shaderGUI = Shader.shader("../shaders/GUI.vs", "../shaders/GUI.fs")
        self._primaryFont = fontRenderer.FONTRENDERER(self._Window, self._fontLoader, 800)

        self._initiateGUI()

    def _windowSizeCheck(self):
        if self._lastWindowSizeX != self._Window.width or self._lastWindowSizeY != self._Window.height:
            self._lastWindowSizeX = self._Window.width
            self._lastWindowSizeY = self._Window.height
            return True
        else:
            return False
    def _loadImageData(self, Path):
        image = Image.open(str(Path))
        self._texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self._texture)
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(image.getdata()), np.uint8)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        try:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        except:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS, -0.0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
    def _draweQuad(self):
        glEnable(GL_BLEND)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ZERO)
        if self._RENDERTEXTURE:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self._texture)
        self._Primetive.DrawQuad()
        glDisable(GL_BLEND)
    def _initiateGUI(self):
        scaleX = self._sizeX / self._Window.width
        scaleY = self._sizeY / self._Window.height
        posX = scaleX - 1 + self._positionX / self._Window.width * 2.0
        posY = scaleY - 1 + self._positionY / self._Window.height * 2.0
        scaleMat = pyrr.matrix44.create_from_scale(np.array([scaleX, scaleY, 1.0]))
        transMat = pyrr.matrix44.create_from_translation(np.array([posX, -posY, 1.0]))
        modelMat = pyrr.matrix44.multiply(scaleMat, transMat)
        self._shaderGUI.use()
        self._shaderGUI.mat4("model", modelMat)

        aspectRatio = min(self._sizeY/self._sizeX, self._sizeX/self._sizeY)
        self._shaderGUI.float("aspectRatio", aspectRatio)
        self._shaderGUI.float("edge", self._edge / min(self._sizeX, self._sizeY))
        self._shaderGUI.float("baseAlpha", self._baseAlpha)
        if self._sizeX >= self._sizeY:
            self._shaderGUI.bool("edgeFlip", 0)
        else:
            self._shaderGUI.bool("edgeFlip", 1)
        self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.33)
        self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)
    def _mouseHoverButton(self, StartPosX=0, EndPosX=0, StartPosY=0, EndPosY=0):
        if (self._Window.MousePos[0] < (self._positionX + StartPosX) or self._Window.MousePos[0] > (self._positionX + self._sizeX + EndPosX)
        or (self._Window.MousePos[1] < (self._positionY + StartPosY) or self._Window.MousePos[1] >= (self._positionY + self._sizeY + EndPosY))):
            return False
        else:
            return True
    def _buttonClicked(self):
        if self._mouseHoverButton() is False:
            if self._Window.MouseButtons[0] == 0:
                self._leftClickGuard = False
            else:
                self._leftClickGuard = True
        else:
            if self._leftClickGuard is False and self._Window.MouseButtons[0] == 1:
                return True
            else:
                if self._Window.MouseButtons[0] == 0:
                    self._leftClickGuard = False
        return False
    def _slidebarCalc(self):
        if self._sizeX > self._sizeY:
            if self._Window.MousePos[0] >= self._positionX and self._Window.MousePos[0] <= (self._positionX + self._sizeX):
                currentDistance = self._Window.MousePos[0] - (self._positionX + self._edge)
                totalDistance = self._sizeX - self._edge * 2.0
                self.SlidebarPercent = currentDistance / totalDistance
        else:
            if self._Window.MousePos[1] >= self._positionY and self._Window.MousePos[1] <= (self._positionY + self._sizeY):
                currentDistance = self._Window.MousePos[1] - (self._positionY + self._edge)
                totalDistance = self._sizeY - self._edge * 2.0
                self.SlidebarPercent = 1.0 - currentDistance / totalDistance
        if self.SlidebarPercent > 1.0:
            self.SlidebarPercent = 1.0
        elif self.SlidebarPercent < 0.0:
            self.SlidebarPercent = 0.0
    def DrawSlidebar(self, Text, UpdateLogic=False, SlidebarPercent=False, Color=None, SlidebarScaler=1):
        if self._initiationFlag:
            self._initiationFlag = False
            self._secondaryFont = fontRenderer.FONTRENDERER(self._Window, self._fontLoader, 800)
        if self._windowSizeCheck():
            self._initiateGUI()
        self._shaderGUI.use()
        self._shaderGUI.int("type", 2)
        if self._sizeX >= self._sizeY:
            self._shaderGUI.bool("edgeFlip", 0)
        else:
            self._shaderGUI.bool("edgeFlip", 1)

        if UpdateLogic is False:
            self._shaderGUI.float("slidebarPercent", self.SlidebarPercent)
            if self._buttonClicked() is True:
                self._slidebarCalc()
                self._shaderGUI.vec3("mainColor", self._Window._mainColor)
                self._shaderGUI.vec3("edgeColor", self._Window._edgeColor)
            else:
                if self._mouseHoverButton() is True:
                    self._shaderGUI.vec3("mainColor", self._Window._mainColor*0.66)
                    self._shaderGUI.vec3("edgeColor", self._Window._edgeColor*0.75)
                else:
                    self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.33)
                    self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)
        else:
            self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.33)
            self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)
            if SlidebarPercent is not False:
                self.SlidebarPercent = SlidebarPercent/100
                self._shaderGUI.float("slidebarPercent", SlidebarPercent/100)

        self._draweQuad()
        if Color is None:
            colOne = self._Window._textColor
            colTwo = self._Window._edgeColor

        else:
            colOne = Color
            colTwo = Color
        self._primaryFont.DrawText(Text, self._positionX + self._sizeX / 2, self._positionY, self._textSize,
                                   colOne, True, True)
        self._secondaryFont.DrawText(str(int(self.SlidebarPercent * 100 * SlidebarScaler)) + "%", self._positionX + self._sizeX / 2,
                                     self._positionY + self._sizeY / 2, self._textSize, colTwo, True, False)


        return self.SlidebarPercent
    def DrawHoldButton(self, Text, UpdateLogic=False):
        if self._windowSizeCheck():
            self._initiateGUI()
        self._shaderGUI.use()
        self._shaderGUI.int("type", 1)
        if UpdateLogic is False:
            if self._buttonClicked() is True:
                if self.ButtonState is True and self._buttonHold is False:
                    self.ButtonState = False
                elif self.ButtonState is False and self._buttonHold is False:
                    self.ButtonState = True
                self._buttonHold = True
            else:
                self._buttonHold = False
            if self.ButtonState is True:
                self._shaderGUI.vec3("mainColor", self._Window._mainColor)
                self._shaderGUI.vec3("edgeColor", self._Window._edgeColor)
            else:
                if self._mouseHoverButton() is True:
                    self._shaderGUI.vec3("mainColor", self._Window._mainColor*0.66)
                    self._shaderGUI.vec3("edgeColor", self._Window._edgeColor*0.75)
                else:
                    self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.33)
                    self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)
        self._draweQuad()
        self._primaryFont.DrawText(Text, self._positionX + self._sizeX/2, self._positionY + self._sizeY/2, self._textSize, self._Window._edgeColor, True, False)
        return self.ButtonState
    def DrawDragNDrop(self):
        if self._initiationFlag:
            self.DragNDropFlag = False
            self._pathMSG = "Drag here!"
            self._initiationFlag = False
            self._shaderGUI.use()
            self._shaderGUI.int("type", 1)
            self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.33)
            self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)

        if self._windowSizeCheck():
            self._initiateGUI()
        self._shaderGUI.use()

        if self._Window.NewDragNDrop and self._mouseHoverButton():
            self._Window.NewDragNDrop = False
            self._pathMSG = self._PathSplitter.SplitPath(self._Window.CurrentDragNDropPath)
            sqlTest = str(self._pathMSG)
            sqlTest = sqlTest.split(".")
            try:
                if str(sqlTest[1]) == "sqlite":
                    self.DragNDropFlag = True
                    self._pathMSG = "File: " + str(sqlTest[0])
                    self._shaderGUI.vec3("mainColor", np.array([0.0, 0.7, 0.0]))
                else:
                    self.DragNDropFlag = False
                    self._pathMSG = "Cannot read fileformat: ." + str(sqlTest[1])
                    self._shaderGUI.vec3("mainColor", np.array([0.7, 0.1, 0.0]))
            except:
                self._shaderGUI.vec3("mainColor", np.array([0.7, 0.1, 0.0]))

        self._draweQuad()
        self._primaryFont.DrawText(self._pathMSG, self._positionX + self._sizeX/2, self._positionY + self._sizeY/2, self._textSize, self._Window._edgeColor, True, False)
        return self.ButtonState
    def DrawSnapButton(self, Text, UpdateLogic=False):
        if self._windowSizeCheck():
            self._initiateGUI()
        self._shaderGUI.use()
        self._shaderGUI.int("type", 1)
        if UpdateLogic is False:
            if self._buttonClicked() is True:
                self.ButtonState = True
            else:
                self.ButtonState = False
            if self.ButtonState is True:
                self._shaderGUI.vec3("mainColor", self._Window._mainColor)
                self._shaderGUI.vec3("edgeColor", self._Window._edgeColor)
            else:
                if self._mouseHoverButton() is True:
                    self._shaderGUI.vec3("mainColor", self._Window._mainColor*0.66)
                    self._shaderGUI.vec3("edgeColor", self._Window._edgeColor*0.75)
                else:
                    self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.33)
                    self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)
        self._draweQuad()
        self._primaryFont.DrawText(Text, self._positionX + self._sizeX/2, self._positionY + self._sizeY/2, self._textSize, self._Window._edgeColor, True, False)
        return self.ButtonState
    def DrawPlane(self, FullScreen=False, TopText=False):
        if self._windowSizeCheck():
            if FullScreen:
                self._sizeX = self._Window.width
                self._sizeY = self._Window.height
                self._positionX = 0
                self._positionY = 0
            self._initiateGUI()
        self._shaderGUI.use()
        self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.33)
        self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)
        if self._RENDERTEXTURE:
            self._shaderGUI.int("type", 0)
        else:
            self._shaderGUI.int("type", 1)
        self._draweQuad()
        if TopText is not False:
            self._primaryFont.DrawText(TopText, self._positionX + self._sizeX / 2, self._positionY,
                                 self._textSize*1.5, self._Window._textColor, True, True)
    def DrawDropDown(self, DrowDownText, TextArray, UpdateLogic=False):
        if self._initiationFlag:
            self._secondaryFont = fontRenderer.FONTRENDERER(self._Window, self._fontLoader, 800)
            self._dropDownName = TextArray[self.DropDownIndex]
            self._rangeText = int(len(TextArray))
            self._initiationFlag = False
            self._endPos = 0
            self._objectList = []
            for i in range(self._rangeText):
                self._endPos += self._spaceScale
                self._objectList.append(fontRenderer.FONTRENDERER(self._Window, self._fontLoader, 800))
            self._endPos = self._endPos + self._spaceScale*0.35 - self._sizeY
        if self._windowSizeCheck():
            self._initiateGUI()
        if DrowDownText is not False:
            self._secondaryFont.DrawText(DrowDownText, self._positionX + self._sizeX * 0.5, self._positionY,
                                 self._textSize, self._Window._textColor, True, True)
        self._shaderGUI.use()
        self._shaderGUI.int("type", 1)
        if self._sizeX >= self._sizeY:
            self._shaderGUI.bool("edgeFlip", 0)
        else:
            self._shaderGUI.bool("edgeFlip", 1)

        if self.dropDownHold and UpdateLogic is False:
            self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.66)
            self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.75)
            if self._mouseHoverButton() is False:
                self.dropDownHold = False
            else:
                if self._lastDropSize is False:
                    self._lastDropSize = True
                    self._sizeY += self._endPos
                    self._initiateGUI()
                self.DrawPlane()
                end = self._spaceScale
                start = 0
                for i in range(self._rangeText):
                    if self._mouseHoverButton(0, 0, start, end - self._sizeY):
                        textColor = self._Window._textColor
                        if self._Window.MouseButtons[0] == 1 and i != self.DropDownIndex:
                            self.DropDownIndex = i
                            self._dropDownName = TextArray[self.DropDownIndex]
                    else:
                        textColor = self._Window._textColor*0.6
                    if i == self.DropDownIndex:
                        textColor = self._Window._edgeColor

                    #self._primaryFont.DrawText(TextArray[i], self._positionX + self._sizeX*0.5, self._positionY + end,
                    #                    self._textSize, textColor, True, True)
                    self._objectList[i].DrawText(TextArray[i], self._positionX + self._sizeX*0.5, self._positionY + end,
                                        self._textSize, textColor, True, True)
                    end += self._spaceScale
                    start += self._spaceScale
        else:
            if self._mouseHoverButton():
                self.dropDownHold = True
            if self._lastDropSize is True:
                self._lastDropSize = False
                self._sizeY -= self._endPos
                self._initiateGUI()
            self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.33)
            self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)
            self._draweQuad()
            self._primaryFont.DrawText(self._dropDownName, self._positionX + self._sizeX / 2,
                                 self._positionY + self._sizeY / 2, self._textSize,
                                 self._Window._edgeColor, True, False)
        return self.DropDownIndex
    def DrawText(self, StringArray, RowSize, ColSize, ColLenght=2, Size=1, Color=None):
        if self._initiationFlag:
            self._initiationFlag = False
            self._objectList = []
            self._stringPositionsX = []
            self._stringPositionsY = []
            self._stringLen = int(len(StringArray))
            xPos = self._positionX
            yPos = self._positionY
            count = 0
            for i in range(self._stringLen):
                self._objectList.append(fontRenderer.FONTRENDERER(self._Window, self._fontLoader, 800))

                self._stringPositionsX.append(xPos)
                self._stringPositionsY.append(yPos)
                count += 1
                if count >= ColLenght:
                    xPos = self._positionX
                    yPos += RowSize * self._windowScaler
                    count = 0
                else:

                    xPos += ColSize * self._windowScaler
        if self._windowSizeCheck():
            self._initiateGUI()
        if Color is not None:
            color = Color
        else:
            color = self._Window._textColor
        for i in range(self._stringLen):
            if StringArray[i] != "":
                self._objectList[i].DrawText(StringArray[i], self._stringPositionsX[i], self._stringPositionsY[i], self._textSize*Size,
                                             color, False, False)
    def DrawTextBox(self, Text, UpdateLogic=False):

        if self._initiationFlag:
            self._secondaryFont = fontRenderer.FONTRENDERER(self._Window, self._fontLoader, 800)
            self._textBoxKeyCommand = keyboardCommands.KeyboardCommands(self._Window, self._secondaryFont,
                                                                        self._Primetive)
            self._textBoxKeyCommand.MainString = "None"
            self._textBoxKeyCommand.MousePickStartPos = self._positionX
            self._textBoxKeyCommand.MousePickEndPos = self._sizeX
            self._textBoxKeyCommand.MousePickHeightCenter = self._positionY + self._sizeY / 2

            self._initiationFlag = False
            self._shaderGUI.use()
            self._shaderGUI.int("type", 1)
            self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.33)
            self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)
        if self._windowSizeCheck():
            self._initiateGUI()
        self._shaderGUI.use()
        self._draweQuad()
        if UpdateLogic is False:
            if self._mouseHoverButton():
                if self._Window.MouseButtons[0] == 1:
                    self._buttonHold = True
                if self._Window.Keys[257]:
                    self._buttonHold = False
                if self._buttonHold:
                    self._shaderGUI.vec3("mainColor", self._Window._mainColor* 0.4)
                    self._shaderGUI.vec3("edgeColor", self._Window._edgeColor)
                    self._textBoxKeyCommand.KeyInput()
                    self.TextBoxKeyEvent = self._textBoxKeyCommand.KeyEvent
                else:
                    self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.20)
                    self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.75)
            else:
                self._buttonHold = False
                self._shaderGUI.vec3("mainColor", self._Window._mainColor * 0.0)
                self._shaderGUI.vec3("edgeColor", self._Window._edgeColor * 0.50)




        self._primaryFont.DrawText(Text, self._positionX + self._sizeX / 2, self._positionY, self._textSize,
                                   self._Window._textColor, True, True)
        self._secondaryFont.DrawText(self._textBoxKeyCommand.MainString, self._positionX + self._sizeX / 2,
                                     self._positionY + self._sizeY / 2, self._textSize*0.8, self._Window._edgeColor, True, False)
        return self._textBoxKeyCommand.MainString






