__author__: str = "Schelz"
__version__: str = "0.3"

import os, sys
import glfw
import time
import pyautogui
import psutil
import threading
import freetype
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *

class CharacterSlot:
    def __init__(self, texture, glyph):
        self.texture = texture
        self.textureSize = (glyph.bitmap.width, glyph.bitmap.rows)

        if isinstance(glyph, freetype.GlyphSlot):
            self.bearing = (glyph.bitmap_left, glyph.bitmap_top)
            self.advance = glyph.advance.x
        elif isinstance(glyph, freetype.BitmapGlyph):
            self.bearing = (glyph.left, glyph.top)
            self.advance = None
        else:
            raise RuntimeError('unknown glyph type')

def win_resolution():
    return pyautogui.size()

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

    def _Text(self, window, message: str, pos_x: int, pos_y: int, color: tuple, font: str):
        pass


    def _Image(self, width: int, height: int, alpha: bool):
        pass

    def _Shapes(self):
        pass

class VirtualWindow:
    def __init__(self, width: int, height: int, title: str, fullscreen: bool):
        super().__init__()
        if not glfw.init():
            raise Exception("glfw not created!")

        ctypes.windll.shcore.SetProcessDpiAwareness(2) # windows 10
        glfw.window_hint(glfw.DECORATED, glfw.FALSE)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
        glfw.window_hint(glfw.FOCUS_ON_SHOW, glfw.FALSE)
        #glfw.window_hint(glfw.GLFW_MOUSE_PASSTHROUGH, glfw.TRUE)

        self.monitor = glfw.get_primary_monitor() if fullscreen else None  # ??
        self._windll = glfw.create_window(width, height, title, None, None)
        self.pos = glfw.get_monitor_pos(self.monitor)
        self.size = glfw.get_window_size(self._windll)
        self.mode = glfw.get_video_mode(self.monitor)

        glfw.set_window_pos(self._windll,
            int(self.pos[0] + (self.mode.size.width - self.size[0]) / 2),
            int(self.pos[1] + (self.mode.size.height - self.size[1]) / 2))

        if not self._windll:
            glfw.terminate()
            raise Exception("glfw not created!")

        glfw.make_context_current(self._windll)
        glDrawBuffer(GL_BACK);
        glClearColor(0.0, 0.0, 0.0, 0.0)

        glBegin(GL_QUADS);
        glColor4f(1.0, 0.0, 0.0, 0.3)
        glVertex3f(-0.5, -0.5, 0)
        glVertex3f(+0.5, -0.5, 0)
        glVertex3f(+0.5, +0.5, 0)
        glVertex3f(-0.5, +0.5, 0)
        glEnd()

    def DoWork(self):
        while not glfw.window_should_close(self._windll):
            time.sleep(0.05)
            #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glfw.poll_events()
            glfw.swap_buffers(self._windll)
            #if mem_proc("csgo.exe").GetProcPID() != mem_proc("csgo.exe").GetCurrentPID(): pass
        glfw.terminate()

width = pyautogui.size()[0]
height = pyautogui.size()[1]

if __name__ == "__main__":
    threading.Thread(target=mem_proc("csgo.exe").GetCurrentPID, daemon=True).start()
    VirtualWindow(400, 300, "Caca", True).DoWork()
