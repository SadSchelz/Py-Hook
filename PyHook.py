__author__: str = "Schelz"
__version__: str = "0.3"

import os, sys
import glfw
import time
import numpy
import pyrr
try:
    import pyautogui
except ImportError:
    os.system("pip install pyautogui")
try:
    import psutil
except ImportError:
    os.system("pip install psutil")
try:
    import freetype
except ImportError:
    os.system("pip install freetype-py")
import threading
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from OpenGL.GLUT import *
if sys.platform == "win32":
    import win32api
    import win32gui

vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
out vec3 v_color;
void main()
{
    gl_Position = vec4(a_position, 1.0);
    v_color = a_color;
}
"""

fragment_src = """
# version 330
in vec3 v_color;
out vec4 out_color;
void main()
{
    out_color = vec4(v_color, 1.0);
}
"""

def _shader(vertex_src: str, fragments_src: str, vertices: list, indices: list or None, EBO_buffer: bool):
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    if EBO_buffer == False: pass
    else:
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glUseProgram(shader)

class mem_proc:
    def __init__(self, proc_name: str):
        super().__init__()
        """"No need to put .exe"""
        self.local_pid = os.getpid()
        self.proc_name = proc_name

    def GetProcPID(self):
        pid = None
        for proc in psutil.process_iter():
            if self.proc_name in proc.name():
                pid = proc.pid
        return pid

    def GetProcName(self, pid):
        process = psutil.Process(pid)
        process_name = str(process.name())
        return process_name

    def GetCurrentPID(self):
        while True:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            lpdw_process_id = ctypes.c_ulong()
            result = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw_process_id))
            process_id = lpdw_process_id.value
            return process_id  

class Draw:
    def __init__(self):
        pass

    def vertex_array(self, array: list):
        return numpy.array(array, dtype=numpy.float32)
    
    def indices(self, array: list):
        return numpy.array(self.indices, dtype=numpy.uint32)

    

    def _Text(self, window, message: str, pos_x: int, pos_y: int, color: tuple, font: str):
        pass


    def _Image(self, width: int, height: int, alpha: bool):
        pass

    def _Line(self):
        vertices = [
            -0.5, -0.5, 0.0, 
            0.5, -0.5, 0.0, 
            0.0, 0.5, 0.0
        ]

        color = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ]
        self.vertex_array(vertices)
        self.vertex_array(color)

        glEnable(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vertices)

    def _3D_Object(self, vertices, color):
        pass


def window_resize(window, width: int, height: int):
    glViewport(0, 0, width, height)

class VirtualWindow:
    def __init__(self, width: int, height: int, title: str, fullscreen: bool):
        super().__init__()
        if not glfw.init():
            raise Exception("glfw not created!")

        ctypes.windll.shcore.SetProcessDpiAwareness(2) # windows 10
        glfw.window_hint(glfw.DECORATED, glfw.FALSE)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
        glfw.window_hint(glfw.FOCUS_ON_SHOW, glfw.TRUE)
        glfw.window_hint(glfw.REFRESH_RATE, 10)
        glfw.window_hint(glfw.FOCUSED, glfw.TRUE)

        self.monitor = glfw.get_primary_monitor() if fullscreen else None  # ??
        self._windll = glfw.create_window(width, height, title, None, None)
        self.pos = glfw.get_monitor_pos(self.monitor)
        self.size = glfw.get_window_size(self._windll)
        self.mode = glfw.get_video_mode(self.monitor)

        if not self._windll:
            glfw.terminate()
            raise Exception("glfw not created!")

        glfw.set_window_pos(self._windll,
            int(self.pos[0] + (self.mode.size.width - self.size[0]) / 2),
            int(self.pos[1] + (self.mode.size.height - self.size[1]) / 2))
        
        glfw.set_window_size_callback(self._windll, window_resize)

        glfw.make_context_current(self._windll)

        vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                    0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                    -0.5,  0.5, 0.0, 0.0, 0.0, 1.0,
                    0.5,  0.5, 0.0, 1.0, 1.0, 1.0]

        vertices = Draw().vertex_array(vertices)
        _shader(vertex_src, fragment_src, vertices, None, False)
        #self.rotation_loc = glGetUniformLocation(shader, "rotation")

    def DoWork(self):
        while not glfw.window_should_close(self._windll):
            time.sleep(0.01)
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            #rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
            #rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
            glfw.swap_buffers(self._windll)
            #if mem_proc("csgo.exe").GetProcPID() != mem_proc("csgo.exe").GetCurrentPID(): pass
        glfw.terminate()

width = pyautogui.size()[0]
height = pyautogui.size()[1]

if __name__ == "__main__":
    threading.Thread(target=mem_proc("csgo.exe").GetCurrentPID, daemon=True).start()
    VirtualWindow(400, 300, "Overlay", True).DoWork()
