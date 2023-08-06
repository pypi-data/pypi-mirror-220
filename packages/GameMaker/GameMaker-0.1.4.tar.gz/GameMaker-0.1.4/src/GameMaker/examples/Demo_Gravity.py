import GameMaker as gm
from GameMaker.Assets import Rectangle, CheckCollision
from GameMaker.Physics import Gravity

import pygame as pg

gravity = Gravity(
	gravity_scaling = 1.0, 
	reduction = 10, 
	jump_increase = 5, 
	max_gravity = 10
)

window = gm.Window(screen_size=(800,450), title="Demo Gravity", background_color = (100,220,255))
ground = Rectangle([0,440,800,10],outline=0,foreground_color=(100,20,20))

position = 0
velocity = 0

size = 20

while window.RUNNING:
	player = Rectangle([window.H_WIDTH - size, position, size, size])

	collisions = CheckCollision(player,ground)

	if collisions['Bottom']:
		velocity = 0
		position = window.HEIGHT - (ground.h * 3)

		if window.get_key(pg.K_SPACE) or window.get_key(pg.K_UP):
			velocity = gravity.jump()
	else:
		velocity = gravity.tick()

	position -= velocity

	window.draw([ground,player])
	window.update()
