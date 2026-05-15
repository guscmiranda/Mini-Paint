import glfw
from OpenGL.GL import *
from COLORS import *
from Button import *
import numpy as np
from header import *

WIDTH, HEIGHT = 800, 600
# MOUSE_X, MOUSE_Y = 0, 0
CURRENT_BUTTON = None

def init(colorName):
    cor = COR[colorName]
    glClearColor(*cor)

def render():
    glClear(GL_COLOR_BUFFER_BIT)

def get_cursor_pos(window):
    mouse_x, mouse_y = glfw.get_cursor_pos(window)
    mouse_x = (mouse_x / WIDTH) * 2 - 1
    mouse_y = -((mouse_y / HEIGHT) * 2 - 1)

    return mouse_x, mouse_y

def get_click(window, buttons):
    event = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT)

    if event == glfw.PRESS:
        x,y = get_cursor_pos(window)

        botao_clicado = None

        for b in buttons:
            if b.clicked(x,y):
                botao_clicado = b.key

        if botao_clicado:
            for b in buttons:

                if b.key == botao_clicado:
                    b.set_clicked()
                else:
                    b.set_not_clicked()

            '''if b.clicked(x,y):
                b.set_clicked()
            else:
                b.set_not_clicked()'''

        print(f"clicou em {x}, {y}")


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

        MOUSE_X, MOUSE_Y = get_cursor_pos(window)
        get_click(window, buttons)

        for b in buttons:
            b.draw()

        glfw.swap_buffers(window)

if __name__ == "__main__":
    main()
    glfw.terminate()
