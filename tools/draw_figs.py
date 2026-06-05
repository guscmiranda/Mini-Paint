import math
from core.canvas import paint_pixel, mouse_to_canvas, add_thickness
import numpy as np
from ui.COLORS import COR

def line_bresenham(x1, y1, x2, y2): # supor: x1=0, y1=0, x2=4, y2=2
    ''' Algoritmo demonstrado em sala para desenhar linhas retas'''

    pixels = [] # lista de pixels a serem pintados

    # Diferença entre o ponto final e o inicial, para saber qual varia mais
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Para saber a inclinação da reta
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:
        pixels.append((x1, y1))

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err # Evitar divisão por 2

        # Escolher qual dos pixels laterais será pintado
        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy

    return pixels

def call_bresenham(SHAPE_START, canva, row, col, color,thickness):
    ''' Pinta os pixels retornados pelo algoritmo do Bresenham'''
    x1, y1 = SHAPE_START

    # desenha reta final
    pixels = line_bresenham(x1, y1, row, col)
    for (px, py) in pixels:
        paint_pixel(px, py, color, thickness, canva)

def draw_reta(canva, col, mouse_holding, mouse_pressed, mouse_released, row, CURRENT_COLOR, CURRENT_THICKNESS, SHAPE_START, BACKUP_CANVA):
    # -------------------------
    # COMEÇOU A DESENHAR
    # -------------------------
    if mouse_pressed:

        SHAPE_START = (row, col)  # salva estado original

        BACKUP_CANVA = canva.copy() # Para guardar o quadro anterior e o movimento ficar flúido

    # -------------------------
    # ARRASTANDO
    # -------------------------
    elif mouse_holding and SHAPE_START: # Apenas se já houve um  clique inicial
        canva[:] = BACKUP_CANVA
        call_bresenham(SHAPE_START, canva, row, col, CURRENT_COLOR, CURRENT_THICKNESS)

    # -------------------------
    # TERMINOU
    # -------------------------
    elif mouse_released and SHAPE_START: # Quando o mouse for levantado e já tiver desenhado a reta

        SHAPE_START = None
        BACKUP_CANVA = None

    return BACKUP_CANVA, SHAPE_START

def draw_rect(canva, col, mouse_holding, mouse_pressed, mouse_released, row, CURRENT_COLOR, CURRENT_THICKNESS, SHAPE_START, BACKUP_CANVA):
    # -------------------------
    # COMEÇOU A DESENHAR
    # -------------------------
    if mouse_pressed:

        SHAPE_START = (row, col) # salva estado original

        BACKUP_CANVA = canva.copy()

    # -------------------------
    # ARRASTANDO
    # -------------------------
    elif mouse_holding and SHAPE_START:
        x, y = SHAPE_START
        canva[:] = BACKUP_CANVA
        call_bresenham(SHAPE_START, canva, x, col, CURRENT_COLOR, CURRENT_THICKNESS)
        call_bresenham(SHAPE_START, canva, row, y, CURRENT_COLOR, CURRENT_THICKNESS)
        call_bresenham((row,y), canva, row, col, CURRENT_COLOR, CURRENT_THICKNESS)
        call_bresenham((x, col), canva, row, col, CURRENT_COLOR, CURRENT_THICKNESS)

    # -------------------------
    # TERMINOU
    # -------------------------
    elif mouse_released and SHAPE_START:

        SHAPE_START = None
        BACKUP_CANVA = None

    return BACKUP_CANVA, SHAPE_START

def draw_filled_rect(canva, col, mouse_holding, mouse_pressed, mouse_released, row, CURRENT_COLOR, CURRENT_THICKNESS,
              SHAPE_START, BACKUP_CANVA):
    # -------------------------
    # COMEÇOU A DESENHAR
    # -------------------------
    if mouse_pressed:

        SHAPE_START = (row, col)

        # salva estado original

        BACKUP_CANVA = canva.copy()

    # -------------------------
    # ARRASTANDO
    # -------------------------
    elif mouse_holding and SHAPE_START:
        x, y = SHAPE_START
        canva[:] = BACKUP_CANVA
        call_bresenham(SHAPE_START, canva, x, col, CURRENT_COLOR, CURRENT_THICKNESS)
        call_bresenham(SHAPE_START, canva, row, y, CURRENT_COLOR, CURRENT_THICKNESS)
        call_bresenham((row, y), canva, row, col, CURRENT_COLOR, CURRENT_THICKNESS)
        call_bresenham((x, col), canva, row, col, CURRENT_COLOR, CURRENT_THICKNESS)

        x1, x2 = (x, row) if x < row else (row, x)
        y1, y2 = (y, col) if y < col else (col, y)

        # Preenche todos os pixels do retângulo com a cor selecionada
        for py in range(y1, y2 + 1):
            for px in range(x1, x2 + 1):
                paint_pixel(px, py, CURRENT_COLOR, 0, canva)

    # -------------------------
    # TERMINOU
    # -------------------------
    elif mouse_released and SHAPE_START:

        SHAPE_START = None
        BACKUP_CANVA = None

    return BACKUP_CANVA, SHAPE_START

def draw_circle(canva, col, mouse_holding, mouse_pressed, mouse_released, row, CURRENT_COLOR, CURRENT_THICKNESS,
              SHAPE_START, BACKUP_CANVA, border_only=True):
    # -------------------------
    # COMEÇOU A DESENHAR
    # -------------------------
    if mouse_pressed:

        SHAPE_START = (row, col) # salva estado original

        BACKUP_CANVA = canva.copy()

    # -------------------------
    # ARRASTANDO
    # -------------------------
    elif mouse_holding and SHAPE_START:
        x, y = SHAPE_START
        canva[:] = BACKUP_CANVA

        # Define o ponto central, é a média do ponto inicial com a posição atual do mouse
        cx = (x + row) // 2
        cy = (y + col) // 2

        r = int(math.hypot(row - cx, col - cy)/2) # Define raio

        midpointCircle(cx, cy, r, CURRENT_COLOR, CURRENT_THICKNESS, canva, border_only)

    # -------------------------
    # TERMINOU
    # -------------------------
    elif mouse_released and SHAPE_START:

        SHAPE_START = None
        BACKUP_CANVA = None

    return BACKUP_CANVA, SHAPE_START

def midpointCircle(cx, cy, r, color, thickness, canvas, border_only=True):
    '''
        Desenha o cículo usando um ponto dentral e seu raio
        Utiliza a pain_octantes para minimizar os cálculos
    '''

    x = 0
    y = r
    d = 1 - r

    paint_octants(cx, cy, x, y, color, thickness, canvas, border_only) # colore correspondentes por octante

    while y > x: # busca pontos até completar o octante (x == y)
        if d < 0:
            d += (2*x) + 3
        else:
            d += 2 * ( x - y ) + 5
            y-=1
        x+=1
        paint_octants(cx, cy, x, y, color, thickness, canvas, border_only) # colore correspondentes por octante


def paint_horizontal_line(x1, x2, y, color, thickness, canvas):

    if x1 > x2:
        x1, x2 = x2, x1

    for px in range(x1, x2 + 1):
        paint_pixel(px, y, color, thickness, canvas)

def paint_octants(cx, cy, x, y, color, thickness, canvas, border_only=True):

    if border_only:
        points = [
            (cx + x, cy + y),
            (cx - x, cy + y),

            (cx - y, cy + x),
            (cx - y, cy - x),

            (cx - x, cy - y),
            (cx + x, cy - y),

            (cx + y, cy - x),
            (cx + y, cy + x),
        ]

        for px, py in points:
            paint_pixel(px, py, color, thickness, canvas)
    else:# preencher o círculo
        # linhas horizontais principais
        paint_horizontal_line(cx - x, cx + x, cy + y, color, thickness, canvas)
        paint_horizontal_line(cx - x, cx + x, cy - y, color, thickness, canvas)

        # linhas horizontais secundárias
        paint_horizontal_line(cx - y,cx + y,cy + x, color,thickness,canvas)
        paint_horizontal_line(cx - y, cx + y, cy - x, color, thickness, canvas)




