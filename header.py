'''
    Para criar o cabeçalho de ferramentas
'''
import numpy as np

from Button import Botao
from OpenGL.GL import *
from COLORS import *

def draw_header():
    glColor4f(*COR['cinza_claro'])
    glBegin(GL_QUADS)
    glVertex2f(-1, 0.7)
    glVertex2f(-1, 1)
    glVertex2f(1, 1)
    glVertex2f(1, 0.7)
    glEnd()

def set_buttons(quant, width, height):
    gaps = np.linspace(-.9, .75, quant)
    buttons = []
    for g in gaps:
        button = Botao(g, 0.9, g+width, 0.9 - height, None, None, 'laranja')
        buttons.append(button)

    return buttons

#ateste = Botao(-0.90, 0.90, -0.75, 0.80, None, None, 'laranja')
#bteste = Botao(-0.65, 0.90, -0.50, 0.80, None, None, 'verde_oliva')

