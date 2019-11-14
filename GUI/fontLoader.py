import numpy as np
import guiWindow
import glfw
import numpy as np
import Shader
from OpenGL.GL import *
import pyrr
from PIL import Image
import time

class FontLoader:
    def __init__(self):
        self.asciiID = []
        self.xPos = []
        self.yPos = []
        self.widht = []
        self.height = []
        self.xOffset = []
        self.yOffset = []
        self.xAdvance = []

        self._fontTexture = self._loadFontTexture("../res/Font/Arial.png")
        self.imageSize = self._fontTexture.width
        self._loadFont("../res/Font/Arial.fnt")
        self.Texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.Texture)
        self._loadImageData(self._fontTexture)
        glBindTexture(GL_TEXTURE_2D, 0)

    def _initation(self, Size):
        if self._INITIATION:
            self._maxLineLenght *= 2.0 / Size
            self._INITIATION = False
            self._shaderFont.use()
            centerPos = np.array([-1.0, 1.0])
            self._shaderFont.vec2("centerPos", centerPos)

    def _loadFont(self, Path):
        def seperateList(File, SeperationString):
            sep = list(File.split(SeperationString))[1]
            sep = int(list(sep.split(" "))[0])
            return sep
        file = open(Path, "r")
        file = list(file.read().split("\n"))
        startIndex = 4
        numberOfChars = list(file[startIndex - 1].split("="))
        self.numberOfChars = int(numberOfChars[1])
        for i in range(self.numberOfChars):
            index = i + startIndex
            self.asciiID.append(seperateList(file[index], "id="))
            self.xPos.append(seperateList(file[index], "x="))
            self.yPos.append(seperateList(file[index], "y="))
            self.widht.append(seperateList(file[index], "width="))
            self.height.append(seperateList(file[index], "height="))
            self.xOffset.append(seperateList(file[index], "xoffset="))
            self.yOffset.append(seperateList(file[index], "yoffset="))
            self.xAdvance.append(seperateList(file[index], "xadvance="))
    def _loadFontTexture(self, Path):
        image = Image.open(str(Path))
        return image
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