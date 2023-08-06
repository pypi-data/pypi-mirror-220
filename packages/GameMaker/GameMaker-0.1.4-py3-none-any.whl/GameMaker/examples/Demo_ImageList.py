import GameMaker as gm
from GameMaker.Assets import ImageList

images = ImageList(
	image = "YOUR_IMAGE.jpg",
	size = [100,100], # Width, Height
	x_copies = 10,
	y_copies = 5,
	x_offset = 25,
	y_offset = 20,
)

window = gm.Window(screen_size=(800,450),title="This is a window")


while window.RUNNING:
	window.draw(images)
	window.update()