import GameMaker as gm
from GameMaker.Assets import Button, Text

window = gm.Window(screen_size=(800,450),title="This is a window")

button1 = Button([50,50,50,50],"-",outline=0,font_size=32)
button2 = Button([110,50,50,50],"+",outline=0,font_size=32)
button3 = Button([170,50,200,50],"HOLD ME",outline=0,font_size=32)

value = 0

while window.RUNNING:

	window.draw([button1,button2,button3,Text(value,[5,5])],gm.GUI)
	window.update()

	if button1.status == gm.PRESSED:
		value -= 1 
	if button2.status == gm.PRESSED:
		value += 1

	if button3.status in [gm.PRESSED,gm.HELD]:
		value += 1