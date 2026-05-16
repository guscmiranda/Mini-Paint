from datetime import datetime
import numpy as np
from PIL import Image

def save_canva(canva):

    img = canva[:, :, :3]
    img = (img * 255).astype(np.uint8)

    name = datetime.now().strftime("desenho_%Y%m%d_%H%M%S.png")

    Image.fromarray(img, "RGB").save(name)

    print(f"Salvo como {name}")