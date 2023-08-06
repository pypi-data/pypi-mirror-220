from GameMaker.Globals import *

import pygame as pg

def CheckCollision(obj1, obj2, x_tolerance: int = 0, y_tolerance: int = 0):
	sides = [
		(obj2.collision_mask[1] + obj2.collision_mask[3] - y_tolerance) >= (obj1.collision_mask[1]) >= (obj2.collision_mask[1] + y_tolerance),
		(obj2.collision_mask[1] + obj2.collision_mask[3] - y_tolerance) >= (obj1.collision_mask[1] + obj1.collision_mask[3]) >= (obj2.collision_mask[1] + y_tolerance),
		(obj2.collision_mask[0] + obj2.collision_mask[2] - x_tolerance) >= (obj1.collision_mask[0]) >= (obj2.collision_mask[0] + x_tolerance),
		(obj2.collision_mask[0] + obj2.collision_mask[2] - x_tolerance) >= (obj1.collision_mask[0] + obj1.collision_mask[2]) >= (obj2.collision_mask[0] + x_tolerance),
	]

	x,y = (sides[2] or sides[3]), (sides[0] or sides[1])

	return { 
		"Top": obj2 if sides[0] and x else None,
		"Bottom": obj2 if sides[1] and x else None,
		"Left": obj2 if sides[2] and y else None,
		"Right": obj2 if sides[3] and y else None,
	}

def CheckAllCollisions(obj1, window, layer: int = FOREGROUND, x_tolerance: int = 0, y_tolerance: int = 0):
	all_collisions = {"Top": None,"Bottom": None,"Left": None,"Right": None}
	
	for obj2 in window.drawlist[layer]:
		if obj1 == obj2: continue

		temp_collisions = CheckCollision(obj1,obj2,x_tolerance=x_tolerance,y_tolerance=y_tolerance)
		for i in temp_collisions:
			if temp_collisions[i] != None:
				all_collisions[i] = obj2

	return all_collisions

def ImageList(
		image: str,
		size: tuple[int,int],
		x_copies: int,
		y_copies: int,
		x_offset: int = 0,
		y_offset: int = 0
	):

	return [Image(image,[x * (x_offset + size[0]), y * (y_offset + size[1]),size[0],size[1]]) for x in range(x_copies) for y in range(y_copies)]

class Text():
	def __init__(
			self,
			text: str,
			position: [int,int],
			font_name: str = 'freesansbold.ttf',
			color: tuple[int,int,int] = (0,0,0),
			font_size: int = 32,
			antialias: bool = True,
			center: list[int] = [TOP,LEFT],
			background = None
		):

		self.text = str(text)
		self.color = color
		self.antialias = antialias
		self.background = background
		self.center = center

		self.font_name = str(font_name)
		self.font_size = font_size

		self.x, self.y = position

		self.render()

		self.collision_mask = self.x,self.y,self.w,self.h

	def render(self):
		self.font = pg.font.Font(self.font_name, self.font_size)
		self.rendered_text = self.font.render(self.text, self.antialias, self.color, self.background)

		self.rect = self.rendered_text.get_rect()

		self.w, self.h = self.rect.w, self.rect.h

		self.rect.center = self.x + ((self.w // 2) * self.center[1]), self. y + ((self.h // 2) * self.center[0])

	def update(self,text):
		self.text = str(text)

		self.rendered_text = self.font.render(self.text, self.antialias, self.color, self.background)
		self.rect = self.rendered_text.get_rect()

		self.w, self.h = self.rect.w, self.rect.h

	def draw(self,window):
		self.rect.center = self.x + ((self.w // 2) * self.center[1]), self. y + ((self.h // 2) * self.center[0])
		window.blit(self.rendered_text,self.rect)

class Rectangle():
	def __init__(
			self,
			position: list[int,int,int,int],
			background_color: tuple[int,int,int] = (50,50,50),
			foreground_color: tuple[int,int,int] = (200,200,200),
			outline: int = 2,
			health=0,
		):

		self.background_color = background_color
		self.foreground_color = foreground_color

		self.outline = outline

		self.collision_mask = self.x,self.y,self.w,self.h = position

	def draw(self,window):
		if self.outline > 0: pg.draw.rect(window, self.background_color, [self.x,self.y,self.w,self.h])
		pg.draw.rect(window, self.foreground_color, [self.x+self.outline,self.y+self.outline,self.w-self.outline*2,self.h-self.outline*2])

class Line():
	def __init__(
			self,
			position: list[int,int,int,int],
			color: tuple[int,int,int] = (50,50,50),
			width : int = 2,
			health=0,
		):

		self.color = color
		self.width = width

		self.collision_mask = self.x,self.y,self.w,self.h = position

	def draw(self,window):
		pg.draw.line(window, self.color, [self.x,self.y],[self.w,self.h], width=self.width)

class ProgressBar():
	def __init__(
			self,
			position: list[int,int,int,int],
			percent: float = 1.0,
			background_color: tuple[int,int,int] = (50,50,50),
			foreground_color: tuple[int,int,int] = (0,200,20),
			outline: int = 2,
			health=0,
		):

		self.background_color = background_color
		self.foreground_color = foreground_color

		self.outline = outline

		self.collision_mask = self.x,self.y,self.w,self.h = position

		self.percent = percent

	def update(self,percent: float):
		self.percent = percent
		return self

	def get_width(self) -> float:
		return self.w * self.percent

	def draw(self,window):
		pg.draw.rect(window, self.background_color, [self.x,self.y,self.w,self.h])
		pg.draw.rect(window, self.foreground_color, [self.x + self.outline,self.y + self.outline,self.get_width() - self.outline * 2,self.h - self.outline * 2])

class RotatedRectangle():
	def __init__(
			self,
			position: list[int,int,int,int],
			rotation: float = 0.0,
			background_color: tuple[int,int,int] = (50,50,50),
			foreground_color: tuple[int,int,int] = (200,200,200),
			outline: int = 2,
			health=0,
		):

		self.background_color = background_color
		self.foreground_color = foreground_color

		self.outline = outline

		self.x,self.y,self.w,self.h = position

		self.rotation = rotation

		self.surface = pg.Surface((self.w,self.h))
		self.surface.set_colorkey((0, 0, 0))
		self.surface.fill(self.foreground_color)
		self.rect = self.surface.get_rect()

		self.collision_mask = self.rect

	def draw(self,window):
		self.surface.fill(self.foreground_color)

		self.rect.center = (self.x + self.w/2, self.y + self.h/2)

		old_center = self.rect.center
		new = pg.transform.rotate(self.surface, self.rotation)
		self.rect = new.get_rect()
		self.rect.center = old_center
		window.blit(new, self.rect)
		
		self.collision_mask = self.rect

class Button():
	def __init__(
			self,
			position: list[int,int,int,int],
			text: str = "",
			font_name: str = 'freesansbold.ttf',
			font_size: int = 20,
			antialias: bool = True,
			text_pos: list[int] = [TOP,LEFT],
			text_color: tuple[int,int,int] = (10,10,10),
			background_color: tuple[int,int,int] = (50,50,50),
			foreground_color: tuple[int,int,int] = (200,200,200),
			hovered_color: tuple[int,int,int] = (170,170,170),
			pressed_color: tuple[int,int,int] = (120,120,120),
			outline: int = 2,
			held = False,
			background = None
		):

		self.text = str(text)
		self.antialias = antialias
		self.text_pos = text_pos
		self.background = background

		self.font_name = str(font_name)
		self.font_size = font_size

		self.background_color = background_color
		self.foreground_color = foreground_color
		self.hovered_color = hovered_color
		self.pressed_color = pressed_color
		self.text_color = text_color

		self.outline = outline

		self.collision_mask = self.x,self.y,self.w,self.h = position

		self.render()

		self.status = NONE

	def render(self):
		self.font = pg.font.Font(self.font_name, self.font_size)
		self.rendered_text = self.font.render(self.text, self.antialias, self.text_color, self.background)

		self.rect = self.rendered_text.get_rect()

		self.rect.center = self.x + ((self.w // 2) * self.text_pos[1]), self. y + ((self.h // 2) * self.text_pos[0])

	def draw(self,window):
		x,y = pg.mouse.get_pos()
		click = pg.mouse.get_pressed(num_buttons=3)[0]

		w = (x >= self.x) and (x <= self.x + self.w)
		h = (y >= self.y) and (y <= self.y + self.h)

		self.status = HELD if w and h and click and self.status in [PRESSED,HELD] else PRESSED if w and h and click else RELEASED if not click and self.status in [PRESSED,HELD] else HOVERED if w and h else NONE

		if self.outline > 0: pg.draw.rect(window, self.background_color, [self.x,self.y,self.w,self.h])
		pg.draw.rect(window, self.pressed_color if self.status in [HELD,PRESSED] else self.hovered_color if self.status == HOVERED else self.foreground_color, [self.x+self.outline,self.y+self.outline,self.w-self.outline*2,self.h-self.outline*2])

		if self.text != "":
			window.blit(self.rendered_text,self.rect)

class Image():
	def __init__(
			self,
			path: str,
			position: [int,int,int,int],
		):
		
		self.path = path

		self.collision_mask = self.x, self.y, self.w, self.h = position

		self.image = pg.image.load(path).convert_alpha()

		self.image = pg.transform.scale(self.image, (self.w, self.h))

		self.rect = self.image.get_rect()

		self.rect.x = self.x
		self.rect.y = self.y
		
	def draw(self,window):
		window.blit(self.image,self.rect)

class RotatedImage():
	def __init__(
			self,
			path: str,
			position: [int,int,int,int],
			rotation: float = 0.0,
		):
		
		self.path = path

		self.collision_mask = self.x, self.y, self.w, self.h = position

		self.image = pg.image.load(path).convert_alpha()

		self.image = pg.transform.scale(self.image, (self.w, self.h))

		self.rect = self.image.get_rect()

		self.rect.x = self.x
		self.rect.y = self.y

		self.rotation = rotation
		
	def draw(self,window):
		rotated = pg.transform.rotate(self.image, self.rotation)

		self.rect = rotated.get_rect()

		self.rect.center = (self.x + self.w/2, self.y + self.h/2)

		window.blit(rotated,self.rect)

		self.collision_mask = self.rect

class ScriptedObject():
	def __init__(self,sprite: str, script: type(lambda x: None)):
		pass

class AlphaRectangle():
	def __init__(
			self,
			position: list[int,int,int,int],
			color: tuple[int,int,int] = (200,200,200,255),
			rotation: float = 0.0,
		):

		self.collision_mask = self.x, self.y, self.w, self.h = position
		self.rotation = rotation
		self.color = color

		self.surface = pg.Surface((self.w,self.h))
		self.surface.set_alpha(self.color[3])
		self.surface.fill(self.color[0:3])
		self.rect = self.surface.get_rect()

	def draw(self,window):
		self.surface.set_alpha(self.color[3])

		rotated = pg.transform.rotate(self.surface, self.rotation)

		self.rect.center = (self.x + self.w/2, self.y + self.h/2)
		
		window.blit(rotated,self.rect)

class Slider():
	def __init__(
			self,
			position: list[int,int,int,int],
			button_width: int = 10,
			vertical: bool = False,
		):
			
		self.collision_mask = self.x, self.y, self.w, self.h = position

		self.button_width = button_width

		self.vertical = vertical

		if self.vertical:
			self.button = Button([self.x,self.y,self.w,self.button_width])
		else:
			self.button = Button([self.x,self.y,self.button_width,self.h])

		self.background = Rectangle([self.x,self.y,self.w,self.h],foreground_color=(100,100,100))

		self.value = 0

	def draw(self,window):
		if self.button.status in [PRESSED,HELD]:
			if self.vertical:
				self.button.y = pg.mouse.get_pos()[1] - self.button.h / 2

				if self.button.y < self.y: self.button.y = self.y

				if self.button.y + self.button.h > self.y + self.h: self.button.y = self.y + self.h - self.button.h
			else:
				self.button.x = pg.mouse.get_pos()[0] - self.button.w / 2

				if self.button.x < self.x: self.button.x = self.x

				if self.button.x + self.button.w > self.x + self.w: self.button.x = self.x + self.w - self.button.w

		if self.vertical:
			self.value = (self.button.y - self.y) / (self.h - self.button.h)
		else:
			self.value = (self.button.x - self.x) / (self.w - self.button.w)

		self.value = round(self.value,2)

		self.background.draw(window)
		self.button.draw(window)

class Ellipse():
	def __init__(
			self,
			position: list[int,int,int,int],
			color: tuple[int,int,int] = (200,200,200),
			width: int = 2,
		):

		self.color = color

		self.width = width

		self.collision_mask = self.x,self.y,self.w,self.h = position

	def draw(self,window):
		pg.draw.ellipse(window, self.color, [self.x,self.y,self.w,self.h], self.width)

class Arc():
	def __init__(
			self,
			position: list[int,int,int,int],
			start_angle: int,
			stop_angle: int,
			color: tuple[int,int,int] = (200,200,200),
			width: int = 2,
		):

		self.color = color

		self.start_angle = start_angle
		self.stop_angle = stop_angle

		self.width = width

		self.collision_mask = self.x,self.y,self.w,self.h = position

	def draw(self,window):
		pg.draw.arc(window, self.color, [self.x,self.y,self.w,self.h], self.start_angle, self.stop_angle, self.width)

class Textbox():
	def __init__(
			self,
			position: list[int,int,int,int],
			default_text: str = "",
			text_color: tuple[int,int,int] = (0,0,0),
			background_color: tuple[int,int,int] = (50,50,50),
			foreground_color: tuple[int,int,int] = (200,200,200),
			outline: int = 2,
			max_length: int = 999,
		):

		self.background_color = background_color
		self.foreground_color = foreground_color

		self.text = default_text
		self.draw_text = Text(self.text,[position[0] + 5, position[1] + position[3] / 2],color=text_color,font_size=position[3]//2,center=[CENTER,LEFT])

		self.outline = outline
		self.max_length = max_length

		self.collision_mask = self.x,self.y,self.w,self.h = position

	def update(self,window):
		for e in window.keys_down:
			if e.key == pg.K_BACKSPACE:
				self.text = self.text[:-1]
			else:
				if len(self.text) <= self.max_length:
					self.text += e.unicode

		if len(window.keys_down) > 0: self.draw_text.update(self.text)

	def draw(self,window):
		if self.outline > 0: pg.draw.rect(window, self.background_color, [self.x,self.y,self.w,self.h])
		pg.draw.rect(window, self.foreground_color, [self.x+self.outline,self.y+self.outline,self.w-self.outline*2,self.h-self.outline*2])

		self.draw_text.x, self.draw_text.y = self.x + 5, self.y + self.h / 2

		self.draw_text.draw(window)