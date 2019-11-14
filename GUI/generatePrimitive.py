import numpy as np
from OpenGL.GL import *

class GeneratePrimetive:
    def __init__(self):
        self._initiateQuad()
        self._initiateLine()
    def _initiateQuad(self):
        QuadVert = np.array([-1,  1,
                             -1, -1,
                              1,  1,
                              1, -1], dtype=np.float32)
        self._VAO_Quad = glGenVertexArrays(1)
        VBO_Quad = glGenBuffers(1)
        glBindVertexArray(self._VAO_Quad)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_Quad)
        glBufferData(GL_ARRAY_BUFFER, QuadVert.itemsize * len(QuadVert), QuadVert, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, QuadVert.itemsize * 2, ctypes.c_void_p(0))
    def _initiateLine(self):
        lineVert = np.array([0.0, -1.0,
                             0.0, 1.0], dtype=np.float32)
        self._VAO_Line = glGenVertexArrays(1)
        VBO_Line = glGenBuffers(1)
        glBindVertexArray(self._VAO_Line)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_Line)
        glBufferData(GL_ARRAY_BUFFER, 4 * 4, lineVert, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * 4, ctypes.c_void_p(0))

    def DrawQuad(self):
        glBindVertexArray(self._VAO_Quad)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindVertexArray(0)
    def DrawLine(self):
        glBindVertexArray(self._VAO_Line)
        glDrawArrays(GL_LINES, 0, 2)
        glBindVertexArray(0)
