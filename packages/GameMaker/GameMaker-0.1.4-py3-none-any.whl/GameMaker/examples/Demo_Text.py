import GameMaker as gm
from GameMaker.Assets import Text

window = gm.Window(screen_size=(800,450),title="This is a window with text")

text1 = Text("This is some text",(10,0))
text2 = Text("This is some colored text",(10,45),font_size=22,color=(200,0,0))
text3 = Text("This is some small text",(10,80),font_size=14)

x_pos = -1 * text3.w

while window.RUNNING:
	window.draw([text1,text2,text3])

	window.draw(Text("This is moving text",(x_pos,120),font_size=22))

	window.update()

	if x_pos < window.WIDTH:
		x_pos += 3
	else:
		x_pos = -1 * text3.w
