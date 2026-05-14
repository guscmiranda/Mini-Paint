import glfw
from OpenGL.GL import *
from COLORS import *
from Button import *
import numpy as np
from header import *


def init(colorName):
    cor = COR[colorName]
    glClearColor(*cor)

def render():
    glClear(GL_COLOR_BUFFER_BIT)

def get_cursor_pos(window):
    mouse_x, mouse_y = glfw.get_cursor_pos(window)
    mouse_x = (mouse_x / 800) * 2 - 1
    mouse_y = -((mouse_y / 600) * 2 - 1)

    return mouse_x, mouse_y


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Mini Paint", None, None)
    glfw.make_context_current(window)
    buttons = set_buttons(8, .15, .1)

    init('fundo_claro')
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        draw_header()
        for b in buttons:
            b.draw()

        glfw.swap_buffers(window)

if __name__ == "__main__":
    main()
    glfw.terminate()
