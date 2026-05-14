from OpenGL.GL import *
from COLORS import *


class Botao:
    def __init__(self,x_up, y_up, x_down, y_down, shade_path, action, main_color):
        self.x_up = x_up
        self.y_up = y_up
        self.x_down = x_down
        self.y_down = y_down

        self.shade_path = shade_path
        self.action = action # reta ou fullfill ou quadrado

        self.main_color = COR[main_color]
        self.isClicked = False

    def update(self):
        pass

    def update_position(self, x_up, y_up, x_down, y_down):
        pass

    def click(self):
        self.isClicked = True
        # depois de terminar o desenho voltar a ser False

    def draw(self):
        if self.isClicked:
            glColor4f(*COR['azul_escuro'])
        else:
            glColor4f(*self.main_color)

        glBegin(GL_QUADS)
        glVertex2f(self.x_up, self.y_up)
        glVertex2f(self.x_up, self.y_down)
        glVertex2f(self.x_down, self.y_down)
        glVertex2f(self.x_down, self.y_up)
        glEnd()
