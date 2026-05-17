import math
from core.canvas import paint_pixel, mouse_to_canvas
import numpy as np
from ui.COLORS import COR

# def line_bresenham(x1, y1, x2, y2):
#     pixels = [(x1, y1)]
#     dx = x2 - x1
#     dy = y2 - y1
#     dy2 = 2*dy
#     dydx2 = dy2 - 2*dx
#     pant = dy2 - dx
#
#     x = x1
#     y = y1
#
#     for i in range(dx):
#         if pant < 0:
#             pixels.append((x + 1, y))
#             pant = pant + dy2
#         else:
#             pixels.append((x + 1, y+1))
#             pant = pant + dydx2
#             y += 1
#         x += 1
#
#     return pixels

def line_bresenham(x1, y1, x2, y2): # supor: x1=0, y1=0, x2=4, y2=2
    pixels = []

    dx = abs(x2 - x1) #dx=4
    dy = abs(y2 - y1) #dy=2

    sx = 1 if x1 < x2 else -1 #sx=1
    sy = 1 if y1 < y2 else -1 #sy=1

    err = dx - dy #err=2

    while True:
        pixels.append((x1, y1)) # [(0,0), (1, 0)]

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err #e2=4

        if e2 > -dy: #4>-2 true
            err -= dy #2-2=0
            x1 += sx #x1=0+1=1

        if e2 < dx: # 4 < 2 false
            err += dx
            y1 += sy

    return pixels

def call_bresenham(SHAPE_START, canva, row, col, color,thickness):
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

        SHAPE_START = (row, col)

        # salva estado original

        BACKUP_CANVA = canva.copy()


    # -------------------------
    # ARRASTANDO
    # -------------------------

    elif mouse_holding and SHAPE_START:
        canva[:] = BACKUP_CANVA
        call_bresenham(SHAPE_START, canva, row, col, CURRENT_COLOR, CURRENT_THICKNESS)


    # -------------------------
    # TERMINOU
    # -------------------------

    elif mouse_released and SHAPE_START:
        # canva[:] = BACKUP_CANVA
        # call_bresenham(SHAPE_START, canva, row, col, CURRENT_COLOR, CURRENT_THICKNESS)

        SHAPE_START = None

        BACKUP_CANVA = None

    return BACKUP_CANVA, SHAPE_START


def draw_rect(canva, col, mouse_holding, mouse_pressed, mouse_released, row, CURRENT_COLOR, CURRENT_THICKNESS, SHAPE_START, BACKUP_CANVA):
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
        call_bresenham((row,y), canva, row, col, CURRENT_COLOR, CURRENT_THICKNESS)
        call_bresenham((x, col), canva, row, col, CURRENT_COLOR, CURRENT_THICKNESS)


    # -------------------------
    # TERMINOU
    # -------------------------

    elif mouse_released and SHAPE_START:
    #     x, y = SHAPE_START
    #     canva[:] = BACKUP_CANVA
    #     call_bresenham(SHAPE_START, canva, col, x, CURRENT_COLOR, CURRENT_THICKNESS)
    #     call_bresenham(SHAPE_START, canva, y, row, CURRENT_COLOR, CURRENT_THICKNESS)
    #     call_bresenham((row, y), canva, col, row, CURRENT_COLOR, CURRENT_THICKNESS)
    #     call_bresenham((x, col), canva, col, row, CURRENT_COLOR, CURRENT_THICKNESS)
    #
        SHAPE_START = None

        BACKUP_CANVA = None

    return BACKUP_CANVA, SHAPE_START
