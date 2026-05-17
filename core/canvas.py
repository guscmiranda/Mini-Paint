import numpy as np
import glfw
from OpenGL.GL import *
# from run import canva


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 510

# print("FORMATO do canva ", canva.shape)

def draw_canvas(canvas):

    glRasterPos2f(-1, -1)

    flipped = np.flipud(canvas)

    glDrawPixels(
        CANVAS_WIDTH,
        CANVAS_HEIGHT,
        GL_RGBA,
        GL_FLOAT,
        flipped
    )

def mouse_to_canvas(mx, my):

    # ignora header
    if my > 0.7:
        return None

    col = int((mx + 1) / 2 * CANVAS_WIDTH)

    normalized_y = (my + 1) / 1.7

    row = int((1 - normalized_y) * CANVAS_HEIGHT)

    return row, col

def paint_pixel(row, col, color, thickness, canvas):

    points = add_thickness(row, col, thickness)

    for row, col in points:
        if 0 <= row < CANVAS_HEIGHT and 0 <= col < CANVAS_WIDTH:
            canvas[row, col] = color

def add_thickness(row, col, thickness):

    points = []

    radius = int(thickness)
    for dr in range(-radius, radius+1):
        for dc in range(-radius, radius+1):
            if abs(dr) + abs(dc) <= radius:
                points.append((row + dr, col + dc))

    return points



