from core.canvas import paint_pixel

def habilitate_erase(row, col, CURRENT_COLOR, CURRENT_THICKNESS, canva):
    paint_pixel(row, col, CURRENT_COLOR, int(CURRENT_THICKNESS) + 5, canva)
