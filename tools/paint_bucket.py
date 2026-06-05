import numpy as np
from tools.utils import get_pixel
from collections import deque

def paint_bucket(row, col, CURRENT_COLOR, mouse_pressed, canvas):
    '''
        Balde de tinta utilizando Flood Fill:
        Quando o usuário clica em um pixel, todos os pixels 4-conectados
        que possuem a mesma cor inicial são substituídos pela cor atualmente selecionada.
    '''

    # Executa apenas no instante do clique do mouse evitando repetir o preenchimento em todos os frames
    if not mouse_pressed:
        return

    height, width = canvas.shape[:2]

    # Obtem a cor original do pixel clicado.
    original_color = get_pixel(row, col, canvas)

    # Converte a cor selecionada para o mesmo formato utilizado pelo canvas.
    new_color = np.array(CURRENT_COLOR, dtype=np.float32)

    # Se a região já possui a cor desejada não há nada para preencher.
    if np.array_equal(original_color, new_color):
        return

    # Matriz auxiliar utilizada para evitar que um mesmo pixel seja visitado várias vezes
    visited = np.zeros((height, width), dtype=bool)

    queue = deque()

    # Inicia a busca a partir do pixel clicado.
    queue.append((row, col))
    visited[row, col] = True

    # Continua enquanto existirem pixels pendentes na fila.
    while queue:

        r, c = queue.popleft() # Pega o próximo pixel

        pixel = canvas[r, c] # A cor atual do pixel

        # Caso o pixel não possua a cor original, ele não pertence à região a ser preenchida.
        if (
            pixel[0] != original_color[0] or
            pixel[1] != original_color[1] or
            pixel[2] != original_color[2] or
            pixel[3] != original_color[3]
        ):
            continue

        # Substitui a cor do pixel pela nova cor selecionada.
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