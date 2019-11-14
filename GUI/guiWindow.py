import glfw
import numpy as np
from OpenGL.GL import *

class GUIWindow:
    def __init__(self, Name, SizeX, SizeY, MainColor, EdgeColor):
        if not glfw.init():
            return
        self._mainColor = MainColor
        self._edgeColor = EdgeColor
        self.width, self.height = SizeX, SizeY
        '''
        monitors = glfw.get_monitors()
        if len(monitors) > 1:
            monitor = monitors[1]
        else:
            monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(monitor)

        print(mode)
        glfw.window_hint(glfw.RED_BITS, mode[1][0])
        glfw.window_hint(glfw.GREEN_BITS, mode[1][1])
        glfw.window_hint(glfw.BLUE_BITS, mode[1][2])
        glfw.window_hint(glfw.REFRESH_RATE, mode[2])
        glfw.window_hint(glfw.AUTO_ICONIFY, False)
        #glfw.window_hint(glfw.DECORATED, False)
        #GLFW_DECORATED


        self.Window = glfw.create_window(mode[0][0], mode[0][1], Name, monitor, None)
        glfw.set_window_monitor(self.Window, monitor, 0, 0, mode[0][0], mode[0][1], mode[2])
        #print(mode[0][0], mode[0][1], mode[2])
        '''
        glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
        self.Window = glfw.create_window(self.width, self.height, Name, None, None)
        glfw.make_context_current(self.Window)




        #print(monitors, len(monitors))
        if not self.Window:
            glfw.terminate()
            return

        self.Keys = [False] * 1024
        self.KeyPressed = False
        self.MousePos = np.zeros([2])
        self.MouseButtons = np.zeros([5])
        self.MouseScroll = 0
        self.LeftArrow = False
        self.RightArrow = False
        self.MouseEventFlag = False
        self._lastColor = None
        self.NewDragNDrop = False
        self.CurrentDragNDropPath = "Drag here"



        glfw.set_drop_callback(self.Window, self.drop_callback)
        glfw.set_window_size_callback(self.Window, self.window_resize)
        glfw.set_key_callback(self.Window, self.key_callback)
        glfw.set_mouse_button_callback(self.Window, self.mouse_button_callback)
        glfw.set_cursor_pos_callback(self.Window, self.cursor_pos_callback)
        glfw.set_scroll_callback(self.Window, self.mouse_scroll_callback)
        glClearColor(0.3, 0.1, 0.1, 1.0)
    def minimumSize_guard(self, Width, Height):
        lowerLim = 100
        if Width < lowerLim or Height < lowerLim:
            return False
        else:
            return True
    def set_window_size(self, widht, hight):
        if self.minimumSize_guard(widht, hight):
            glfw.set_window_size(self.Window, widht, hight)
    def window_resize(self, window, width, height):
        if self.minimumSize_guard(width, height):
            self.width = width
            self.height = height
            glViewport(0, 0, self.width, self.height)
    def drop_callback(self, window, Path):
        self.NewDragNDrop = True
        self.CurrentDragNDropPath = str(Path)
    def key_callback(self, window, key, scancode, action, mode):
        #if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        #    glfw.set_window_should_close(window, True)
        if key >= 0 and key < 1024:
            if action == glfw.PRESS:
                #print(key)
                self.KeyPressed = True
                self.Keys[key] = True
                if key == glfw.KEY_LEFT:
                    self.LeftArrow = True
                if key == glfw.KEY_RIGHT:
                    self.RightArrow = True
            if action == glfw.RELEASE:
                self.Keys[key] = False
    def mouse_scroll_callback(self, window, mods, scroll):
        self.MouseScroll -= scroll
        self.MouseEventFlag = True

    def mouse_button_callback(self, window, button, action, mods):
        self.MouseEventFlag = True
        for i in range(5):
            if action == glfw.PRESS:
                if int(button) == i:
                    self.MouseButtons[i] = 1
            if action == glfw.RELEASE:
                if int(button) == i:
                    self.MouseButtons[i] = 0
    def cursor_pos_callback(self, window, xpos, ypos):
        self.MousePos = (xpos, ypos)
        self.MouseEventFlag = True