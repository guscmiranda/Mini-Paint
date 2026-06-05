from OpenGL.GL import *
from ui.Button import Botao
from ui.COLORS import *
from core.run import MAIN_BUTTONS, TOOLS, THICKNESS


# =======================
# CONFIGURAÇÕES GERAIS
# =======================

HEADER_TOP = 1.0
HEADER_BOTTOM = 0.7

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

# ======================
# DESENHAR HEADER
# ======================

def draw_header():
    ''' Desenha o cabeçalho com fundo cinza e uma borda para dividir do canva '''

    glColor3f(*COR['cinza_claro'][:3]) # Define a cor do fundo

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

# ====================
# CRIA BOTÕES
# ====================

def create_buttons(x, y, width, height, spacing, color, buttons_type, rows=1, add_height=False, shape_path=None):
    ''' Cria cada tipo de botão distribuído na quantidade de linhas específicada '''
    buttons = []
    length = len(buttons_type)
    b_per_line = length / rows # Para saber quantos botões terá por linha
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
            shape_path[i] if shape_path else None,
            nome,
            color if color is not None else nome,
        )

        buttons.append(button)

        x += width + spacing
        if add_height:
            height *= 1.5

    return buttons

# ==========================
# INSTANCIA TODOS OS BOTÕES
# ==========================

def set_buttons():

    buttons = []

    # main buttons
    buttons.extend(create_buttons(x = -0.95, y = 0.96, width = 0.18, height = 0.10, spacing = 0.05, color = 'cinza', buttons_type = MAIN_BUTTONS, shape_path=['icons/salvar.png', 'icons/novo.png']))
    # tool buttons
    buttons.extend(create_buttons(x = -0.95, y = 0.82, width = 0.10, height = 0.10, spacing = 0.02, color = 'cinza', buttons_type = TOOLS, shape_path=['icons/lapis.png', 'icons/borracha.png', 'icons/reta.png', 'icons/retangulo.png', 'icons/retangulo_preenchido.png', 'icons/circulo.png', 'icons/circulo_preenchido.png', 'icons/balde.png']))
    # thickness buttons
    buttons.extend(create_buttons(x = 0.10, y = 0.75, width = 0.26, height = 0.02, spacing = 0.02, color = 'preto', buttons_type = THICKNESS, rows = 4, add_height = True))
    # color buttons
    buttons.extend(create_buttons(x = 0.47, y = 0.82, width = 0.08, height = 0.08, spacing = 0.02, color = None, buttons_type = COLOR_BUTTONS, rows = 2))

    return buttons