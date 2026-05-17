import numpy as np
from core.canvas import paint_pixel
from collections import deque
from ui.COLORS import COR

def paint_bucket(row, col, CURRENT_COLOR, mouse_pressed, canvas):

    if not mouse_pressed:
        return

    original_color = canvas[row][col].copy()
    print("atualizou")

    if tuple(original_color) == CURRENT_COLOR:
        return

    queue = deque()
    queue.append((row, col))

    while queue:
        r, c = queue.popleft()
        print(r, c)

        if r < 0 or r >= canvas.shape[0] or c < 0 or c >= canvas.shape[1]:
            print("entrou no if das bordas")
            continue

        if not np.array_equal(canvas[r, c], original_color):
            print(f"cores {canvas[r, c]} e {original_color} são diferentes!")
            print("entrou das cores")
            continue

        print("vai pintar: ", r, c)
        canvas[r, c] = CURRENT_COLOR
        #paint_pixel(r, c, CURRENT_COLOR, 0, canvas)
        print("pintou: ", r, c)

        queue.append((r-1, c))
        queue.append((r+1, c))
        queue.append((r, c-1))
        queue.append((r, c+1))

    return


import numpy as np
from collections import deque

def paint_bucket2(row, col, CURRENT_COLOR, mouse_pressed, canvas):

    if not mouse_pressed:
        return

    original_color = canvas[row, col].copy()
    new_color = np.array(CURRENT_COLOR, dtype=np.float32)

    # evita loop infinito
    if np.array_equal(original_color, new_color):
        return

    queue = deque()
    queue.append((row, col))

    while queue:

        r, c = queue.popleft()

        # verifica limites
        if r < 0 or r >= canvas.shape[0] or c < 0 or c >= canvas.shape[1]:
            continue

        # só pinta pixels da cor original
        if not np.array_equal(canvas[r, c], original_color):
            continue

        # pinta
        canvas[r, c] = new_color

        # vizinhos
        queue.append((r - 1, c))
        queue.append((r + 1, c))
        queue.append((r, c - 1))
        queue.append((r, c + 1))


def paint_bucket3(row, col, CURRENT_COLOR, mouse_pressed, canvas):

    if not mouse_pressed:
        return

    height, width = canvas.shape[:2]

    original_color = canvas[row, col].copy()
    new_color = np.array(CURRENT_COLOR, dtype=np.float32)

    if np.array_equal(original_color, new_color):
        return

    visited = np.zeros((height, width), dtype=bool)

    queue = deque()
    queue.append((row, col))
    visited[row, col] = True

    while queue:

        r, c = queue.popleft()

        pixel = canvas[r, c]

        if (
            pixel[0] != original_color[0] or
            pixel[1] != original_color[1] or
            pixel[2] != original_color[2] or
            pixel[3] != original_color[3]
        ):
            continue

        canvas[r, c] = new_color

        # cima
        if r > 0 and not visited[r - 1, c]:
            visited[r - 1, c] = True
            queue.append((r - 1, c))

        # baixo
        if r < height - 1 and not visited[r + 1, c]:
            visited[r + 1, c] = True
            queue.append((r + 1, c))

        # esquerda
        if c > 0 and not visited[r, c - 1]:
            visited[r, c - 1] = True
            queue.append((r, c - 1))

        # direita
        if c < width - 1 and not visited[r, c + 1]:
            visited[r, c + 1] = True
            queue.append((r, c + 1))