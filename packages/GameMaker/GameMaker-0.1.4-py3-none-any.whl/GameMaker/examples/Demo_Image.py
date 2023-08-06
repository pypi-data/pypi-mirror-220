import GameMaker as gm
from GameMaker.Assets import Image

window = gm.Window(screen_size=(800,450),title="This is a window")

image = Image("TEST_IMAGE.png",[5,5,100,100])

while window.RUNNING:
	window.draw(image)
	window.update()