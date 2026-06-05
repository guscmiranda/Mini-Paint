from ui.COLORS import COR
from core.run import BACKGROUND_COLOR

def clean_canva(canva):
    canva[:] = COR[BACKGROUND_COLOR]
