from ui.header import *
from canvas import *
from tools import *
from core.constants import *


WIDTH, HEIGHT = 800, 600

CURRENT_BUTTON = None
CURRENT_COLOR = [0.0,0.0,0.0,0.0]
CURRENT_THICKNESS = 1 # 1=fino, 2=médio, 3=GROSSO

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 510
CURRENT_ROW_MOUSE_ON = 0
CURRENT_COL_MOUSE_ON = 0

SHAPE_START = None
LAST_MOUSE_STATE = glfw.RELEASE

BACKGROUND_COLOR = 'fundo_claro'

MAIN_BUTTONS = ['salvar', 'novo']
TOOLS = [ 'pincel', 'borracha', 'reta', 'retangulo', 'retangulo_preenchido','circulo', 'circulo_preenchido', 'balde']
THICKNESS = ['thickness-0', 'thickness-1', 'thickness-2', 'thickness-4']

CURRENT_TOOL = 'pincel'

canva = np.ones((CANVAS_HEIGHT, CANVAS_WIDTH, 4), dtype=np.float32)
BACKUP_CANVA = None

def init(colorName):
    cor = COR[colorName]
    canva[:] = (cor[0], cor[1], cor[2], cor[3])
    glClearColor(*cor)

def render():
    glClear(GL_COLOR_BUFFER_BIT)

def get_cursor_pos(window):
    mouse_x, mouse_y = glfw.get_cursor_pos(window)
    mouse_x = (mouse_x / WIDTH) * 2 - 1
    mouse_y = -((mouse_y / HEIGHT) * 2 - 1)

    return mouse_x, mouse_y

def set_current_button(action):
    global CURRENT_BUTTON
    global CURRENT_COLOR
    global CURRENT_THICKNESS
    global CURRENT_TOOL

    #--- Main Buttons
    #if action in MAIN_BUTTONS:
        #CURRENT_BUTTON = action

    if action == 'novo':
        clean_canva(canva)

    elif action == 'salvar':
        save_canva(canva)

    #--- Tools Buttons
    if action in TOOLS:
        CURRENT_TOOL = action

    #--- Thickness
    if action in THICKNESS:
        CURRENT_THICKNESS = action.split('-')[1]

    #--- Color
    if action in COR.keys() :
        CURRENT_COLOR = COR[action]


def handle_click(window, buttons):

    global LAST_MOUSE_STATE

    current_state = glfw.get_mouse_button(
        window,
        glfw.MOUSE_BUTTON_LEFT
    )

    # -----------------------------
    # EVENTOS DO MOUSE
    # -----------------------------

    mouse_pressed = (
        current_state == glfw.PRESS and
        LAST_MOUSE_STATE == glfw.RELEASE
    )

    mouse_holding = (
        current_state == glfw.PRESS and
        LAST_MOUSE_STATE == glfw.PRESS
    )

    mouse_released = (
        current_state == glfw.RELEASE and
        LAST_MOUSE_STATE == glfw.PRESS
    )

    x, y = get_cursor_pos(window)

    pos = mouse_to_canvas(x, y)

    if pos:
        row, col = pos

    botao_clicado = None
    tool_clicado = None
    thickness_clicado = None
    color_clicado = None

    # -----------------------------
    # CLIQUE NOS BOTÕES
    # -----------------------------

    if mouse_pressed:

        for b in buttons:

            if b.clicked(x, y):

                action = b.get_action()

                set_current_button(action)

                if action in MAIN_BUTTONS:
                    botao_clicado = action
                elif action in TOOLS:
                    tool_clicado = action
                elif action in THICKNESS:
                    thickness_clicado = action
                elif action in COR.keys():
                    color_clicado = action

        if botao_clicado:
            for b in buttons:
                if b.action in MAIN_BUTTONS:
                    b.set_not_clicked()

        if tool_clicado:
            for b in buttons:
                if b.action == tool_clicado:
                    b.set_clicked()
                elif b.action in TOOLS:
                    b.set_not_clicked()

        if thickness_clicado:
            for b in buttons:
                if b.action == thickness_clicado:
                    b.set_clicked()
                elif b.action in THICKNESS:
                    b.set_not_clicked()

        if color_clicado:
            for b in buttons:
                if b.action == color_clicado:
                    b.set_clicked()
                elif b.action in COLOR_BUTTONS:
                    b.set_not_clicked()

    # -----------------------------
    # FERRAMENTAS
    # -----------------------------

    if pos:

        handle_button_click(
            canva,
            mouse_pressed,
            mouse_holding,
            mouse_released,
            row,
            col
        )

    LAST_MOUSE_STATE = current_state

def handle_button_click(
    canva,
    mouse_pressed,
    mouse_holding,
    mouse_released,
    row,
    col
):

    global CURRENT_BUTTON
    global SHAPE_START
    global BACKUP_CANVA

    # -------------------------
    # BOTÕES
    # -------------------------

    if CURRENT_BUTTON == 'novo':

        clean_canva(canva)

        CURRENT_BUTTON = None

    elif CURRENT_BUTTON == 'salvar':

        save_canva(canva)

        CURRENT_BUTTON = None

    # -------------------------
    # PINCEL
    # -------------------------

    if CURRENT_TOOL == 'pincel':

        if mouse_pressed or mouse_holding:

            habilitate_brush(
                row,
                col,
                CURRENT_COLOR,
                CURRENT_THICKNESS,
                canva
            )

    # -------------------------
    # BORRACHA
    # -------------------------

    elif CURRENT_TOOL == 'borracha':

        if mouse_pressed or mouse_holding:

            habilitate_erase(
                row,
                col,
                COR[BACKGROUND_COLOR],
                CURRENT_THICKNESS,
                canva
            )

    # -------------------------
    # RETA
    # -------------------------

    elif CURRENT_TOOL == 'reta':

        BACKUP_CANVA, SHAPE_START = draw_reta(canva, col, mouse_holding, mouse_pressed, mouse_released,
                  row, CURRENT_COLOR, CURRENT_THICKNESS, SHAPE_START, BACKUP_CANVA)

    elif CURRENT_TOOL == 'retangulo':

        BACKUP_CANVA, SHAPE_START = draw_rect(canva, col, mouse_holding, mouse_pressed, mouse_released,
                                              row, CURRENT_COLOR, CURRENT_THICKNESS, SHAPE_START, BACKUP_CANVA)

    elif CURRENT_TOOL == 'retangulo_preenchido':
        BACKUP_CANVA, SHAPE_START = draw_filled_rect(canva, col, mouse_holding, mouse_pressed, mouse_released,
                                              row, CURRENT_COLOR, CURRENT_THICKNESS, SHAPE_START, BACKUP_CANVA)

    elif CURRENT_TOOL == 'circulo':
        BACKUP_CANVA, SHAPE_START = draw_circle(canva, col, mouse_holding, mouse_pressed, mouse_released,
                                                     row, CURRENT_COLOR, CURRENT_THICKNESS, SHAPE_START, BACKUP_CANVA)

    elif CURRENT_TOOL == 'circulo_preenchido':
        BACKUP_CANVA, SHAPE_START = draw_circle(canva, col, mouse_holding, mouse_pressed, mouse_released,
                                                row, CURRENT_COLOR, CURRENT_THICKNESS, SHAPE_START, BACKUP_CANVA, False)


    elif CURRENT_TOOL == 'balde':
        paint_bucket3(row, col, CURRENT_COLOR, mouse_pressed, canva)


def get_mouse_on(window):
    global CURRENT_ROW_MOUSE_ON, CURRENT_COL_MOUSE_ON

    current_x, current_y = get_cursor_pos(window)
    pos = mouse_to_canvas(current_x, current_y)
    if pos:
        CURRENT_ROW_MOUSE_ON, CURRENT_COL_MOUSE_ON = pos

def main():
    glfw.init()
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    window = glfw.create_window(800, 600, "Mini Paint", None, None)
    glfw.make_context_current(window)

    buttons = set_buttons()
    init(BACKGROUND_COLOR)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        get_mouse_on(window)
        handle_click(window, buttons)

        render()

        draw_canvas(canva)
        draw_header()

        for b in buttons:
            b.draw()

        glfw.swap_buffers(window)

if __name__ == "__main__":
    main()
    glfw.terminate()
