class Gravity():
	def __init__(self,gravity_scaling = 0.995, reduction = 5, jump_increase = 5, max_gravity = 10):
		self.y_velocity = 0

		self.gravity_scaling = gravity_scaling
		self.reduction = reduction
		self.jump_increase = jump_increase
		self.max_gravity = max_gravity

	def tick(self) -> float:
		self.y_velocity -= self.gravity_scaling / self.reduction
		self.y_velocity *= self.gravity_scaling

		if self.y_velocity > self.max_gravity: self.y_velocity = self.y_velocity

		return self.y_velocity

	def jump(self,true=True) -> float:
		if true: self.y_velocity = self.jump_increase

		return self.y_velocity

class Movement2D():
	def __init__(self,min_speed = 0.1, max_speed = 4, speed = 0.8, scaling = 0.92):
		self.velocity = 0

		self.min_speed = min_speed
		self.max_speed = max_speed
		self.speed = speed
		self.scaling = scaling

	def tick(self) -> float:
		self.velocity *= self.scaling

		if -self.min_speed < self.velocity < self.min_speed: self.velocity = 0
		if self.velocity > self.max_speed: self.velocity = self.max_speed
		if self.velocity < -self.max_speed: self.velocity = -self.max_speed

		return self.velocity

	def move_left(self,true=True) -> float:
		if true: self.velocity -= self.speed

		return self.velocity

	def move_right(self,true=True) -> float:
		if true: self.velocity += self.speed

		return self.velocity

class Bounce():
	def __init__(self,value: float = 0.8,min_gravity: float = 0.1):
		self.value = value
		self.min_gravity = min_gravity

	def tick(self,velocity: float) -> float:
		if velocity > self.min_gravity:
			return velocity * self.value * -1
		else:
			return 0