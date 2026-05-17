from OpenGL.GL import *

from tools import draw_rect
from ui.COLORS import *


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


        if self.isClicked:
            glColor4f(*COR['verde_oliva'])
        else:
            glColor4f(*COR['cinza_claro'])

        borda = 0.007
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
