from ui.header import *
from canvas import *
from tools import *


WIDTH, HEIGHT = 800, 600

CURRENT_BUTTON = None
CURRENT_COLOR = [0,0,0,0]
CURRENT_THICKNESS = 1 # 1=fino, 2=médio, 3=GROSSO

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 510
CURRENT_ROW_MOUSE_ON = 0
CURRENT_COL_MOUSE_ON = 0

LIKE_STARTED = None

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
    event = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT)

    if event == glfw.PRESS:
        x,y = get_cursor_pos(window)

        # TODO: se clique no header chama handle_click_header() senão, handler_click_canvas()
        #--- Lidando com botões
        botao_clicado = None

        for b in buttons:
            if b.clicked(x,y):
                action = b.get_action()
                set_current_button(action)
                botao_clicado = action

        if botao_clicado:
            for b in buttons:

                if b.action == botao_clicado:
                    b.set_clicked()
                    print(b.action)
                else:
                    b.set_not_clicked()

        LAST_MOUSE_CLICK_X = x
        LAST_MOUSE_CLICK_Y = y

        #--- Lidando com o canva
        pos = mouse_to_canvas(x, y)
        if pos:
            handle_button_click(canva)

        # print(f"clicou em {x}, {y}")

def handle_button_click(canva):
    global CURRENT_BUTTON

    if CURRENT_BUTTON == 'novo':
        clean_canva(canva)
        CURRENT_BUTTON = None

    elif CURRENT_BUTTON == 'salvar':
        save_canva(canva)
        CURRENT_BUTTON = None

    elif CURRENT_TOOL == 'pincel':
        habilitate_brush(CURRENT_ROW_MOUSE_ON, CURRENT_COL_MOUSE_ON, CURRENT_COLOR, CURRENT_THICKNESS, canva)
    elif CURRENT_TOOL == 'borracha':
        habilitate_erase(CURRENT_ROW_MOUSE_ON, CURRENT_COL_MOUSE_ON, COR[BACKGROUND_COLOR], CURRENT_THICKNESS, canva)
    elif CURRENT_TOOL == 'reta':
        draw_line(x1, y1, CURRENT_ROW_MOUSE_ON, CURRENT_COL_MOUSE_ON, CURRENT_COLOR, CURRENT_THICKNESS, canva )



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
