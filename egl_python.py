"""
**Usage**

  .. code:: python

     from glumpy import app

     app.use("egl")
     window = app.Window()
"""
import os
import sys
import ctypes
from ctypes import pointer
from ctypes.util import find_library

# call this _before_ any OpenGL things
os.environ['PYOPENGL_PLATFORM'] = 'egl'

import OpenGL
from OpenGL.GL import (GL_RENDERER, GL_SHADING_LANGUAGE_VERSION,
    GL_STATIC_DRAW, GL_TRIANGLES, GL_TRUE, GL_VENDOR, GL_VERSION,
    GL_VERTEX_SHADER,  glGetString)




# Backend version (if available)
__version__ = ""

# Backend availability
__availability__ = False

# Whether the framework has been initialized
__initialized__ = False

# Active windows
__windows__ = []


# ------------------------------------------------------------ availability ---

os.environ['PYOPENGL_PLATFORM'] = 'egl'
_find_library_old = find_library
try:

    def _find_library_new(name):
        return {
            'GL': 'libOpenGL.so',
            'EGL': 'libEGL.so',
        }.get(name, _find_library_old(name))
    find_library = _find_library_new
    import OpenGL.EGL as egl
    __availability__ = True
    print("imported EGL")

except ImportError:
    __availability__ = False
    __version__ = None
except:
  print('Unable to load OpenGL libraries. '
        'Make sure you use GPU-enabled backend.')
  print('Press "Runtime->Change runtime type" and set '
        '"Hardware accelerator" to GPU.')
  raise

finally:
    find_library = _find_library_old




# -------------------------------------------------------------- capability ---
capability = {
    "Window position get/set" : False,
    "Window size get/set"     : False,
    "Multiple windows"        : False,
    "Mouse scroll events"     : False,
    "Non-decorated window"    : False,
    "Non-sizeable window"     : False,
    "Fullscreen mode"         : False,
    "Unicode processing"      : False,
    "Set GL version"          : False,
    "Set GL profile"          : False,
    "Share GL context"        : False,
}


def main():    
    _width = 256
    _height = 256
    # Whether hidpi is active
    
    #def on_error(error, message):
    #    log.warning(message)
    #glfw.glfwSetErrorCallback(on_error)

    egl_display = egl.eglGetDisplay(egl.EGL_DEFAULT_DISPLAY)

    major, minor = egl.EGLint(), egl.EGLint()
    egl.eglInitialize(egl_display, pointer(major), pointer(minor))

    config_attribs = [
        egl.EGL_SURFACE_TYPE, egl.EGL_PBUFFER_BIT, egl.EGL_BLUE_SIZE, 8,
        egl.EGL_GREEN_SIZE, 8, egl.EGL_RED_SIZE, 8, egl.EGL_DEPTH_SIZE, 24,
        egl.EGL_RENDERABLE_TYPE, egl.EGL_OPENGL_BIT, egl.EGL_NONE
    ]
    config_attribs = (egl.EGLint * len(config_attribs))(*config_attribs)

    num_configs = egl.EGLint()
    egl_cfg = egl.EGLConfig()
    egl.eglChooseConfig(egl_display, config_attribs, pointer(egl_cfg), 1,
                        pointer(num_configs))

    pbuffer_attribs = [
        egl.EGL_WIDTH,
        _width,
        egl.EGL_HEIGHT,
        _height,
        egl.EGL_NONE,
    ]
    pbuffer_attribs = (egl.EGLint * len(pbuffer_attribs))(*pbuffer_attribs)
    egl_surf = egl.eglCreatePbufferSurface(egl_display, egl_cfg, pbuffer_attribs)

    egl.eglBindAPI(egl.EGL_OPENGL_API)

    egl_context = egl.eglCreateContext(egl_display, egl_cfg, egl.EGL_NO_CONTEXT,
                                        None)

    egl.eglMakeCurrent(egl_display, egl_surf, egl_surf, egl_context)
    #print("context made current")

    print('Vendor: {}'.format(glGetString(GL_VENDOR).decode('utf-8')))
    print('Opengl version: {}'.format(glGetString(GL_VERSION).decode('utf-8')))
    print('GLSL Version: {}'.format(glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')))
    print('Renderer: {}'.format(glGetString(GL_RENDERER).decode('utf-8')))

if __name__ == "__main__":
    main()
    print("done.")
