from ui.header import *
from core.canvas import *
from tools import *

# -----------------------------
# DFINIÇÃO DE CONSTANTES E VARIÁVEIS IMPORTANTES
# -----------------------------
WIDTH, HEIGHT = 800, 600

CURRENT_COLOR = [0.0,0.0,0.0,0.0]
CURRENT_THICKNESS = 1 # grossura do traço

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

#  Criando o canva como uma matriz de 1's
canva = np.ones((CANVAS_HEIGHT, CANVAS_WIDTH, 4), dtype=np.float32)
BACKUP_CANVA = None  # Serve para guardar o canva anterior durante desenho de formas

def init(colorName):
    cor = COR[colorName]
    canva[:] = (cor[0], cor[1], cor[2], cor[3])
    glClearColor(*cor) # Define a nova cor de fundo

def render(canva, buttons):
    glClear(GL_COLOR_BUFFER_BIT) # Limpa (com a cor definida no init) os buffers antes de desenhar
    draw_canvas(canva)
    draw_header()

    for b in buttons:
        b.draw()

# --------------------------------
# Funções para lidar com as posições do mouse
# --------------------------------

def get_cursor_pos(window):
    '''
    Pega a posição do cursor na janela, retorna tupla de valores inteiros
    de (0,0) a WIDTH e HEIGHT
    '''
    
    mouse_x, mouse_y = glfw.get_cursor_pos(window)

    # Transformação para inteiros
    mouse_x = (mouse_x / WIDTH) * 2 - 1
    mouse_y = -((mouse_y / HEIGHT) * 2 - 1)

    return mouse_x, mouse_y

def get_mouse_on(window):
    global CURRENT_ROW_MOUSE_ON, CURRENT_COL_MOUSE_ON

    current_x, current_y = get_cursor_pos(window)
    pos = mouse_to_canvas(current_x, current_y)
    if pos:
        CURRENT_ROW_MOUSE_ON, CURRENT_COL_MOUSE_ON = pos

def set_current_button(action):
    ''' Define as ações que devem ser tomadas a partir do clique nos botões '''
    global CURRENT_COLOR
    global CURRENT_THICKNESS
    global CURRENT_TOOL

    #--- Main Buttons
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
    '''
    A cada frame verifica o estado do mouse e decide quais ações executar:
    - Clique em botões da interface
    - Uso das ferramentas sobre o canvas
    '''

    global LAST_MOUSE_STATE

    # Verifica o estado atual do botão esquerdo do mouse
    current_state = glfw.get_mouse_button(
        window,
        glfw.MOUSE_BUTTON_LEFT
    )

    # -----------------------------
    # EVENTOS DO MOUSE
    # -----------------------------

    # Mouse acabou de ser pressionado neste frame
    mouse_pressed = (
        current_state == glfw.PRESS and
        LAST_MOUSE_STATE == glfw.RELEASE
    )

    # Mouse continua pressionado (arrastando)
    mouse_holding = (
        current_state == glfw.PRESS and
        LAST_MOUSE_STATE == glfw.PRESS
    )

    # Mouse acabou de ser solto neste frame
    mouse_released = (
        current_state == glfw.RELEASE and
        LAST_MOUSE_STATE == glfw.PRESS
    )

    # Obtém posição atual do cursor
    x, y = get_cursor_pos(window)

    # Converte coordenadas da janela para coordenadas do canvas
    pos = mouse_to_canvas(x, y)

    # Se o cursor estiver dentro do canvas, obtém linha e coluna
    if pos:
        row, col = pos

    # Variáveis auxiliares para identificar qual tipo de botão foi clicad
    botao_clicado = None
    tool_clicado = None
    thickness_clicado = None
    color_clicado = None

    # -----------------------------
    # CLIQUE NOS BOTÕES
    # -----------------------------

    if mouse_pressed:

        for b in buttons: # Procura qual botão foi clicado

            if b.clicked(x, y):

                action = b.get_action()

                # Atualiza o botão/ferramenta atualmente selecionado
                set_current_button(action)

                # Identifica a categoria do botão clicado
                if action in MAIN_BUTTONS:
                    botao_clicado = action
                elif action in TOOLS:
                    tool_clicado = action
                elif action in THICKNESS:
                    thickness_clicado = action
                elif action in COR.keys():
                    color_clicado = action

        # -----------------------------
        # Atualização visual dos botões
        # -----------------------------

        # Botões da MAIN funcionam como ações únicas
        if botao_clicado:
            for b in buttons:
                if b.action in MAIN_BUTTONS:
                    b.set_not_clicked()

        # Ferramentas funcionam como seleção exclusiva também
        if tool_clicado:
            for b in buttons:
                if b.action == tool_clicado:
                    b.set_clicked()
                elif b.action in TOOLS:
                    b.set_not_clicked()

        # Espessuras funcionam como seleção exclusiva
        if thickness_clicado:
            for b in buttons:
                if b.action == thickness_clicado:
                    b.set_clicked()
                elif b.action in THICKNESS:
                    b.set_not_clicked()

        # Seleção exclusiva também
        if color_clicado:
            for b in buttons:
                if b.action == color_clicado:
                    b.set_clicked()
                elif b.action in COLOR_BUTTONS:
                    b.set_not_clicked()

    # -----------------------------
    # FERRAMENTAS
    # -----------------------------

    # Só executa ações de desenho se o cursor estiver dentro do canvas
    if pos:

        handle_button_click(
            canva,
            mouse_pressed, # clique inicial
            mouse_holding, # clique mantido
            mouse_released, # soltar o clique / forma finalizada
            row,
            col
        )

    # Armazena o estado atual para comparação no próximo frame
    LAST_MOUSE_STATE = current_state

def handle_button_click(
    canva,
    mouse_pressed,
    mouse_holding,
    mouse_released,
    row,
    col
):

    global SHAPE_START
    global BACKUP_CANVA

    # --------------------------------
    # HABILITA FERRAMENTAS DE DESENHO
    # --------------------------------

    # Essas ferramentas mudam o canva de modo automático, não há uso do BACKUP_CANVA
    if CURRENT_TOOL == 'pincel':

        if mouse_pressed or mouse_holding:

            habilitate_brush(
                row,
                col,
                CURRENT_COLOR,
                CURRENT_THICKNESS,
                canva
            )

    elif CURRENT_TOOL == 'borracha':

        if mouse_pressed or mouse_holding:

            habilitate_erase(
                row,
                col,
                COR[BACKGROUND_COLOR],
                CURRENT_THICKNESS,
                canva
            )

    elif CURRENT_TOOL == 'balde':
        paint_bucket(row, col, CURRENT_COLOR, mouse_pressed, canva)


    # As seguintes ferramentas retornam BACKUP_CANVA e ponto de inicio,
    # pois as formas são atualizadas conforme o movimento do mouse.

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

def main():
    glfw.init()                                                     # Inicializa a biblioteca GLFW
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)                    # Desabilita o redimensionamento manual da janela
    window = glfw.create_window(800, 600, "Mini Paint", None, None) # Cria a janela
    glfw.make_context_current(window)                               # Faz da janela criada o contexto atual

    buttons = set_buttons()                                         # Cria todos os tipos de botão do cabeçalho
    init(BACKGROUND_COLOR)                                          # Inicializa o canva com a cor de fundo especificada

    while not glfw.window_should_close(window):                     # Enquanto não clicar para fechar a janela
        glfw.poll_events()                                          # Armazena os eventos da janela

        get_mouse_on(window)                                        # Pega posição se estiver no canva
        handle_click(window, buttons)                               # Gerencia as ações realizadas no canva

        render(canva, buttons)                                      # Desenha a interface do Mini-Paint

        # draw_canvas(canva)
        # draw_header()
        #
        # for b in buttons:
        #     b.draw()

        glfw.swap_buffers(window)                                   # Troca o buffer atual pelo que foi atualizado

if __name__ == "__main__":
    main()
    glfw.terminate() # Finaliza a execução e a biblioteca GLFW
