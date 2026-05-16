import math
from core.canvas import paint_pixel, mouse_to_canvas
import numpy as np
from ui.COLORS import COR

def draw_line(x1, y1, x2, y2, color, thickness, canvas):
    pixels = line_bresenham(x1, y1, x2, y2)
    line_canva = canvas.deepcopy()

    for (px, py) in pixels:
        x, y,  = mouse_to_canvas(px, py)
        paint_pixel(x, y, color, thickness, line_canva)

def line_bresenham(x1, y1, x2, y2):
    pixels = [(x1, y1)]
    dx = x2 - x1
    dy = y2 - y1
    dy2 = 2*dy
    dydx2 = dy2 - 2*dx
    pant = dy2 - dx

    x = x1
    y = y1

    for i in range(dx):
        if pant < 0:
            pixels.append((x + 1, y))
            pant = pant + dy2
        else:
            pixels.append((x + 1, y+1))
            pant = pant + dydx2
            y += 1
        x += 1

    return pixels

def main():
    print(line_bresenham(2,2,12 ,8))

if __name__ == "__main__":
    main()


