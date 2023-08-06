import GameMaker as gm
from GameMaker.Assets import ProgressBar, Text

window = gm.Window(screen_size=(800,450),title="This is a window with a progress bar")

progress_bar = ProgressBar((10,30,100,20))

value = 0

while window.RUNNING:
	progress_bar.update(value)

	window.draw(progress_bar)

	window.draw(Text("Value: {}".format(round(value,1)),(10,0),font_size=20))

	window.update()

	if value < 1:
		value += 0.01
	else:
		value = 0