import GameMaker as gm
from GameMaker.Assets import Textbox

window = gm.Window(screen_size=(800,450),title="This is a window")

textbox = Textbox([50,50,300,30],default_text="username")

while window.RUNNING:
	window.update()