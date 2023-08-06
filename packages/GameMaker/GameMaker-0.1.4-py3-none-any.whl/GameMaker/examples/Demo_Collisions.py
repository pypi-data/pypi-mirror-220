import GameMaker as gm
from GameMaker.Assets import Rectangle, CheckCollision, Text

window = gm.Window(screen_size=(800,450),title="This is a collision test")

target = Rectangle((window.H_WIDTH - 100, window.H_HEIGHT - 50, 200, 100))
target_text = Text("Hover over me",(window.H_WIDTH - 90, window.H_HEIGHT - 15),font_size=25)

mouse = gm.Mouse

while window.RUNNING:
	x,y = mouse.get_pos()

	cursor = Rectangle((x-3,y-3,6,6))

	collisions = CheckCollision(cursor,target)

	target.foreground_color = (200,200,200)

	for i,c in enumerate(collisions):
		if collisions[c] != None:
			target.foreground_color = (200,0,0)

		window.draw(Text("{}: {}".format(c,collisions[c] != None),(10,20*i+5),font_size=20))

	window.draw([target,target_text,cursor])
	window.update()