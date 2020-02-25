import numpy as np
import guiWindow
import glfw
import numpy as np
import Shader
from OpenGL.GL import *
import pyrr
from PIL import Image
import time


class FONTRENDERER:
    def __init__(self, WINDOW, FONTLOADER, MaxLineLenght):

        self._maxLineLenght = MaxLineLenght
        ## Initialize Current Window
        # Pointers
        self._Window = WINDOW
        self._FontLoader = FONTLOADER
        self.StringLenght = np.zeros([2])
        self._fixedWindowSize = False
        self._INITIATION = True
        self._fullUpdate = True
        self._stringLenght = 0
        self._fontColor = np.ones([3])
        self._screenWidth, self._screenHeight = 0, 0
        self._stringList = ""
        self._maxStringHeight = 0
        self._maxStringWidth = 0
        self._maxHeightOffset = 0
        self._maxLetterLength = int(1000)
        self._bufferItemSize = int(4 * (2 * 4))
        self._UPDATETEXTPOS = True
        self._lastPositionX = 0
        self._lastPositionY = 0
        self._shaderFont = Shader.shader("../shaders/font.vs", "../shaders/font.fs")
        self._shaderFont.use()    
        # self._shaderFont.Int("bitMap", 1)
        self._initiateQuad()

    def FixWindowSize(self, Width, Height, Size):
        self._fixedWindowSize = True
        self._shaderFont.use()
        self._screenSizeChange(Width, Height)
        self._shaderFont.vec2("screenSize", np.array([Width, Height]) / Size)

    def _initation(self, Size):
        if self._INITIATION:
            self._maxLineLenght *= 2.0 / Size
            self._INITIATION = False
            self._shaderFont.use()
            centerPos = np.array([-1.0, 1.0])
            self._shaderFont.vec2("centerPos", centerPos)
            self._shaderFont.vec3("color", self._fontColor)

    def _loadFontTexture(self, Path):
        image = Image.open(str(Path))
        return image

    def _currentStringData(self, String):
        self._stringLenght = int(len(String))
        if len(self._stringList) != self._stringLenght:
            self._UPDATETEXTPOS = True
            self._maxStringHeight = 0
            self._maxStringWidth = 0
            self._maxHeightOffset = 0
            self._stringList = ["" for x in range(self._stringLenght)]
            self.StringLenght = np.zeros([self._stringLenght])
            self._fullUpdate = True

        for i in range(self._stringLenght):
            if self._stringList[i] != String[i]:
                self._fullUpdate = True
                break
        if self._fullUpdate:
            # print("Full Update")
            self._fullUpdate = False
            xAdvance = 0
            for i in range(self._stringLenght):
                Index = self._indexCheck(String[i])
                texPos = np.array([self._FontLoader.xPos[Index],
                                   -self._FontLoader.yPos[Index] - self._FontLoader.height[
                                       Index]]) / self._FontLoader.imageSize
                texScale = np.array(
                    [self._FontLoader.widht[Index], self._FontLoader.height[Index]]) / self._FontLoader.imageSize
                pos = np.array([self._FontLoader.xOffset[Index] * 2.0 + xAdvance * 2.0 + self._FontLoader.widht[Index],
                                -self._FontLoader.yOffset[Index] * 2.0 - self._FontLoader.height[Index]])
                scale = np.array([self._FontLoader.widht[Index], self._FontLoader.height[Index]])
                if self._stringLenght > 1:
                    self._stringList[i] = String[i]
                else:
                    self._stringList = String
                self._maxStringWidth = max(self._maxStringWidth, abs(pos[0] + self._FontLoader.xAdvance[Index]))
                self._maxStringHeight = max(self._maxStringHeight, abs(
                    -self._FontLoader.yOffset[Index] * 2.0 - self._FontLoader.height[Index] * 2.0))
                self._maxHeightOffset = max(self._maxHeightOffset, abs(self._FontLoader.height[Index] * 2.0))
                self.StringLenght[i] = self._FontLoader.xAdvance[Index] * self._Size

                if (pos[0] > self._maxLineLenght):
                    power = int(pos[0] / self._maxLineLenght)
                    pos[0] -= self._maxLineLenght * power
                    pos[1] -= self._maxHeightOffset * 1.5 * power
                self._updateStringData(texPos, texScale, pos, scale, i)
                xAdvance += self._FontLoader.xAdvance[Index]
        self._fullUpdate = False

    def _indexCheck(self, CurrentChar):
        for i in range(self._FontLoader.numberOfChars):
            if ord(CurrentChar) == self._FontLoader.asciiID[i]:
                return i

    def _loadImageData(self, image):
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(flipped_image.getdata()), np.uint8)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS, -0.0)
        glEnable(GL_TEXTURE_2D)

    def _initiateQuad(self):
        QuadVert = np.array([-1, 1, 0, 1,
                             -1, -1, 0, 0,
                             1, 1, 1, 1,
                             1, -1, 1, 0], dtype=np.float32)
        self._VAO = glGenVertexArrays(1)
        VBO_Quad = glGenBuffers(1)
        glBindVertexArray(self._VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_Quad)
        glBufferData(GL_ARRAY_BUFFER, 4 * 4 * 4, QuadVert, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(4 * 2))

        self.VBO_Instanced = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_Instanced)
        glBufferData(GL_ARRAY_BUFFER, self._maxLetterLength * self._bufferItemSize, None, GL_DYNAMIC_DRAW)

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, self._bufferItemSize, ctypes.c_void_p(int(0)))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, self._bufferItemSize, ctypes.c_void_p(int(2 * 4)))
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4, 2, GL_FLOAT, GL_FALSE, self._bufferItemSize, ctypes.c_void_p(int(2 * 4 * 2)))
        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5, 2, GL_FLOAT, GL_FALSE, self._bufferItemSize, ctypes.c_void_p(int(2 * 4 * 3)))
        glVertexAttribDivisor(2, 1)
        glVertexAttribDivisor(3, 1)
        glVertexAttribDivisor(4, 1)
        glVertexAttribDivisor(5, 1)

        '''
        self._textPos_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._textPos_VBO)
        glBufferData(GL_ARRAY_BUFFER, int((self._maxLetterLength + 2) * 2 * 4), None, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 4 * 2, ctypes.c_void_p(0))
        glVertexAttribDivisor(2, 1)

        self._textScale_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._textScale_VBO)
        glBufferData(GL_ARRAY_BUFFER, int((self._maxLetterLength + 2) * 2 * 4), None, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, 4 * 2, ctypes.c_void_p(0))
        glVertexAttribDivisor(3, 1)

        self._pos_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._pos_VBO)
        glBufferData(GL_ARRAY_BUFFER, int((self._maxLetterLength + 2) * 2 * 4), None, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4, 2, GL_FLOAT, GL_FALSE, 4 * 2, ctypes.c_void_p(0))
        glVertexAttribDivisor(4, 1)

        self._scale_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._scale_VBO)
        glBufferData(GL_ARRAY_BUFFER, int((self._maxLetterLength + 2) * 2 * 4), None, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5, 2, GL_FLOAT, GL_FALSE, 4 * 2, ctypes.c_void_p(0))
        glVertexAttribDivisor(5, 1)
        '''

    def _textPosChange(self, PositionX, PositionY, Size, Center, Top):
        if self._UPDATETEXTPOS or PositionX != self._lastPositionX or PositionY != self._lastPositionY:
            self._lastPositionX = PositionX
            self._lastPositionY = PositionY
            self._UPDATETEXTPOS = False
            position = np.array(
                [PositionX * 2.0 / Size, -PositionY * 2.0 / Size + self._maxStringHeight - self._maxHeightOffset])
            if Center:
                position += np.array([-self._maxStringWidth * 0.5, self._maxHeightOffset * 0.5])
                if Top:
                    position += np.array([0, self._maxHeightOffset * 0.5])
            elif Center is None:
                position += np.array([-self._maxStringWidth, self._maxHeightOffset * 0.5])
                if Top:
                    position += np.array([0, self._maxHeightOffset * 0.5])
            else:
                if Top:
                    position += np.array([0, self._maxHeightOffset])

            self._shaderFont.vec2("position", position)

    def _textColorChange(self, Color):
        if Color[0] != self._fontColor[0] or Color[1] != self._fontColor[1] or Color[2] != self._fontColor[2]:
            self._fontColor = np.array(Color)
            return True
        else:
            return False

    def _screenSizeChange(self, Width, Height):
        if Width != self._screenWidth or Height != self._screenHeight:
            self._screenWidth, self._screenHeight = Width, Height
            return True
        else:
            return False

    def _updateStringData(self, TextPos, TextScale, Pos, Scale, Index):
        leng = int(2)
        data = []
        for tp in range(leng):
            data.append(TextPos[tp])
        for ts in range(leng):
            data.append(TextScale[ts])
        for p in range(leng):
            data.append(Pos[p])
        for s in range(leng):
            data.append(Scale[s])
        NewData = np.array(data, np.float32).flatten()

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_Instanced)
        glBufferSubData(GL_ARRAY_BUFFER, int(Index * self._bufferItemSize), int(self._bufferItemSize), NewData)

    def DrawText(self, String, PositionX, PositionY, Size, Color, Center=False, Top=False):
        self._Size = Size
        self._initation(Size)
        self._currentStringData(String)
        self._shaderFont.use()
        self._textPosChange(PositionX, PositionY, Size, Center, Top)
        if self._textColorChange(Color):
            self._shaderFont.vec3("color", Color)
        if self._fixedWindowSize is False:
            if self._screenSizeChange(self._Window.width, self._Window.height):
                self._shaderFont.vec2("screenSize", np.array([self._Window.width, self._Window.height]) / Size)
        # Draw
        glEnable(GL_BLEND)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ZERO)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self._FontLoader.Texture)
        glBindVertexArray(self._VAO)
        glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 4, self._stringLenght)
        glBindVertexArray(0)
        glDisable(GL_BLEND)

    def MarkString(self, Mark):
        self._shaderFont.use()
        self._shaderFont.bool("markString", Mark)
