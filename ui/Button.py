from OpenGL.GL import *

from core.texture import load_texture
from tools import draw_rect
from ui.COLORS import *


class Botao:
    def __init__(self,x_up, y_up, x_down, y_down, shade_path, action, main_color):
        self.x_up = x_up
        self.y_up = y_up
        self.x_down = x_down
        self.y_down = y_down

        self.texture = None

        if shade_path:
            self.texture = load_texture(shade_path) # Carrega as imagens dos botões
        self.action = action # reta ou fullfill ou quadrado

        self.main_color = COR[main_color]
        self.isClicked = False

    def set_clicked(self):
        self.isClicked = True

    def set_not_clicked(self):
        self.isClicked = False

    def clicked(self, mousex, mousey):
        if (self.x_up <= mousex <= self.x_down and
                self.y_up >= mousey >= self.y_down):
            self.isClicked = True
            return True

        return False

    def get_action(self):
        return self.action

    def draw(self):
        '''Pinta a borda do botão e aplica a textura nos botões'''

        if self.isClicked:
            glColor4f(*COR['preto'])
        else:
            glColor4f(*COR['cinza_claro'])

        borda = 0.008
        glBegin(GL_QUADS)
        # Expandimos os limites para fora somando/subtraindo a borda
        glVertex2f(self.x_up - borda, self.y_up + borda)
        glVertex2f(self.x_up - borda, self.y_down - borda)
        glVertex2f(self.x_down + borda, self.y_down - borda)
        glVertex2f(self.x_down + borda, self.y_up + borda)
        glEnd()

        glColor4f(*self.main_color)
        glBegin(GL_QUADS)
        glVertex2f(self.x_up, self.y_up)
        glVertex2f(self.x_up, self.y_down)
        glVertex2f(self.x_down, self.y_down)
        glVertex2f(self.x_down, self.y_up)
        glEnd()

        # Para colar a imagem dos botões
        if self.texture:
            glEnable(GL_TEXTURE_2D)

            glBindTexture(GL_TEXTURE_2D, self.texture)

            glColor3f(1, 1, 1)

            glBegin(GL_QUADS)

            glTexCoord2f(0, 0)
            glVertex2f(self.x_up, self.y_down)

            glTexCoord2f(1, 0)
            glVertex2f(self.x_down, self.y_down)

            glTexCoord2f(1, 1)
            glVertex2f(self.x_down, self.y_up)

            glTexCoord2f(0, 1)
            glVertex2f(self.x_up, self.y_up)

            glEnd()

            glDisable(GL_TEXTURE_2D)
