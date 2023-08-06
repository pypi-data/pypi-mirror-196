from os.path import dirname, join
from PIL import ImageTk, Image


images = {
    name: Image.open(join(dirname(__file__), f"{name}.png"))
    for name in ["add", "delete", "edit"]
}


def icon(name):
    return ImageTk.PhotoImage(images[name])
