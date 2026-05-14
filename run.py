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


def main():
    glfw.init()
    window = glfw.create_window(800, 600, "Mini Paint", None, None)
    glfw.make_context_current(window)

    # teste ok
    buttons = set_buttons(8, .15, .1)

    ateste = Botao(-0.90, 0.90, -0.75, 0.80, None, None, 'laranja')
    bteste = Botao(-0.65, 0.90, -0.50, 0.80, None, None, 'verde_oliva')

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
