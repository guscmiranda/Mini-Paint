# '''
#     Para criar o cabeçalho de ferramentas
# '''
# import numpy as np
#
# from Button import Botao
# from OpenGL.GL import *
# from COLORS import *
#
# BUTTON_WIDTH = 0.12
# BUTTON_HEIGHT = 0.12
#
# MAIN_BUTTON_WIDTH = 0.18
# MAIN_BUTTON_HEIGHT = 0.12
#
# MAIN_BUTTONS = ['salvar', 'novo']
#
# def draw_header():
#     glColor4f(*COR['cinza_claro'])
#     glBegin(GL_QUADS)
#     glVertex2f(-1, 0.7)
#     glVertex2f(-1, 1)
#     glVertex2f(1, 1)
#     glVertex2f(1, 0.7)
#     glEnd()
#
# def set_buttons(quant, width, height):
#     gaps = np.linspace(-BUTTON_HEIGHT, .75, quant)
#     buttons = []
#     for g, (nome, config) in zip(gaps, botoes_dict.items()):
#         cor = config.get('main_color')
#         shade_path = config.get('shade_path')
#         pos_x = config.get('pos_x')
#         pos_y = config.get('pos_y')
#
#         if nome in MAIN_BUTTONS:
#             height = MAIN_BUTTON_HEIGHT
#             width = MAIN_BUTTON_WIDTH
#         else:
#             height = BUTTON_HEIGHT
#             width = BUTTON_WIDTH
#
#         button = Botao(pos_x, pos_y, pos_x + width, pos_y - height, shade_path, nome, cor, nome)
#         buttons.append(button)
#
#     return buttons
#
# botoes_dict = {
#     'novo':{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': -0.9,
#         'pos_y': 0.9,
#     },
#     "salvar":{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': 1,
#         'pos_y': 1
#     },
#     'pincel':{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': 1,
#         'pos_y': 1
#     },
#     'borracha':{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': 1,
#         'pos_y': 1
#     },
#     'linha_reta':{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': 1,
#         'pos_y': 1
#     },
#     'retangulo_vazado':{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': 1,
#         'pos_y': 1
#     },
#     'retangulo_preenchido':{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': 1,
#         'pos_y': 1
#     },
#     'circulo_vazado':{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': 1,
#         'pos_y': 1
#     },
#     'circulo_preenchido':{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': 1,
#         'pos_y': 1
#     },
#     'balde':{
#         'shade_path': None,
#         'main_color':'cinza',
#         'pos_x': 1,
#         'pos_y': 1
#     }
#
# }
#
'''
    HEADER / UI DO MINI PAINT
'''

from OpenGL.GL import *
from ui.Button import Botao
from ui.COLORS import *
from core.run import MAIN_BUTTONS, TOOLS, THICKNESS


# =========================================================
# CONFIGURAÇÕES GERAIS
# =========================================================

HEADER_TOP = 1.0
HEADER_BOTTOM = 0.7

#MAIN_BUTTONS = ['salvar', 'novo']

#TOOLS = [ 'pincel', 'borracha', 'linha', 'retangulo', 'circulo', 'balde']


#THICKNESS = ['thickness-1', 'thickness-2', 'thickness-3']

# COLOR_BUTTONS = [
#     ('preto', 'preto'),
#     ('vermelho', 'vermelho'),
#     ('verde', 'verde'),
#     ('azul', 'azul'),
#     ('areia', 'areia')
# ]

COLOR_BUTTONS = [
    'branco',
    'preto',
    'red',
    'green',
    'blue',
    'cyan',
    'magenta',
    'yellow',
    'vinho',
    'laranja'
]


# =========================================================
# DESENHAR HEADER
# =========================================================

def draw_header():

    # fundo
    glColor3f(*COR['cinza_claro'][:3])

    glBegin(GL_QUADS)

    glVertex2f(-1, HEADER_BOTTOM)
    glVertex2f(-1, HEADER_TOP)
    glVertex2f(1, HEADER_TOP)
    glVertex2f(1, HEADER_BOTTOM)

    glEnd()

    # linha divisória
    glColor3f(0.5, 0.5, 0.5)

    glBegin(GL_LINES)

    glVertex2f(-1, HEADER_BOTTOM)
    glVertex2f(1, HEADER_BOTTOM)

    glEnd()


# =========================================================
# BOTÕES PRINCIPAIS
# =========================================================

def create_main_buttons():

    buttons = []

    x = -0.95
    y = 0.96

    width = 0.18
    height = 0.10

    spacing = 0.05

    for nome in MAIN_BUTTONS:

        button = Botao(
            x,
            y,
            x + width,
            y - height,
            None,
            nome,
            'cinza'
        )

        buttons.append(button)

        x += width + spacing

    return buttons


# =========================================================
# BOTÕES DE FERRAMENTAS
# =========================================================

def create_tool_buttons():

    buttons = []

    x = -0.95
    y = 0.82

    width = 0.10
    height = 0.10

    spacing = 0.02

    for nome in TOOLS:

        button = Botao(
            x,
            y,
            x + width,
            y - height,
            None,
            nome,
            'cinza',
        )

        buttons.append(button)

        x += width + spacing

    return buttons


# =========================================================
# ESPESSURA
# =========================================================

def create_thickness_buttons():

    buttons = []

    x = -0.10
    y = 0.82

    width = 0.08
    height = 0.08

    spacing = 0.02

    for nome in THICKNESS:

        button = Botao(
            x,
            y,
            x + width,
            y - height,
            None,
            nome,
            'preto',
        )

        buttons.append(button)

        x += width + spacing

    return buttons


# =========================================================
# CORES
# =========================================================

def create_color_buttons():

    buttons = []

    x = 0.30
    y = 0.82

    width = 0.08
    height = 0.08

    spacing = 0.02

    for nome, cor in COLOR_BUTTONS:

        button = Botao(
            x,
            y,
            x + width,
            y - height,
            None,
            nome,
            cor,
        )

        buttons.append(button)

        x += width + spacing

    return buttons


def create_buttons(x, y, width, height, spacing, color, buttons_type, rows=1, add_height=False):

    buttons = []
    length = len(buttons_type)
    b_per_line = length / rows
    base_x = x
    for i, nome in enumerate(buttons_type):
        if i > 0 and i % b_per_line == 0:
            y += (height + 0.02)
            x = base_x
        button = Botao(
            x,
            y,
            x + width,
            y - height,
            None,
            nome,
            color if color is not None else nome,
        )

        buttons.append(button)

        x += width + spacing
        if add_height:
            height *= 1.5

    return buttons

# =========================================================
# CRIAR TODOS BOTÕES
# =========================================================

def set_buttons():

    buttons = []

    # main buttons
    buttons.extend(create_buttons(x = -0.95, y = 0.96, width = 0.18, height = 0.10, spacing = 0.05, color = 'cinza', buttons_type = MAIN_BUTTONS))
    # tool buttons
    buttons.extend(create_buttons(x = -0.95, y = 0.82, width = 0.10, height = 0.10, spacing = 0.02, color = 'cinza', buttons_type = TOOLS))
    # thickness buttons
    buttons.extend(create_buttons(x = 0.10, y = 0.75, width = 0.26, height = 0.02, spacing = 0.02, color = 'preto', buttons_type = THICKNESS, rows = 4, add_height = True))
    # color buttons
    buttons.extend(create_buttons(x = 0.47, y = 0.82, width = 0.08, height = 0.08, spacing = 0.02, color = None, buttons_type = COLOR_BUTTONS, rows = 2))

    # buttons.extend(create_main_buttons())
    #
    # buttons.extend(create_tool_buttons())
    #
    # buttons.extend(create_thickness_buttons())
    #
    # buttons.extend(create_color_buttons())

    return buttons