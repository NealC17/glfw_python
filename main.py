import pygame as pg
import numpy as np
import math
import os
import taichi as ti 
res = width, height = 800, 450 
offset = np.array([1.3 * width, height])//2
max_iter = 30
zoom = 2.2/height
texture = pg.image.load('images/texture.jpg')
texture_size = min(texture.get_size()) - 1
texture_array = pg.surfarray.array3d(texture).astype(dtype=np.uint32)



@ti.data_oriented
class Fractal:
	def __init__(self, app):
		self.app = app
		self.screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint8)
		ti.init(arch=ti.opengl)
		self.screen_field = ti.Vector.field(3, ti.uint32, (width, height))
		self.texture_field=ti.Vector.field(3, ti.uint32, texture.get_size())
		self.texture_field.from_numpy(texture_array)	
	
	@ti.kernel
	def render(self):
		for x, y in self.screen_field: 
			c = ti.Vector([(x - offset[0]) * zoom, (y - offset[1]) * zoom])
			z = ti.Vector([0.0, 0.0])
			num_iter =0 
			
			for i in range(max_iter):
				z = ti.Vector([(z.x ** 2 - z.y **2 + c.x), (2 * z.x * z.y + c.y)])
				if z.dot(z)> 4:
					break
				num_iter +=1 
			col = int(texture_size* num_iter/max_iter)
			self.screen_field[x, y] = self.texture_field[col, col]
	
	def update(self):
		self.render()
		self.screen_array = self.screen_field.to_numpy()	
	
	def draw(self):
		pg.surfarray.blit_array(self.app.screen, self.screen_array)
		
	def run(self):
		self.update()
		self.draw()


class App:
	def __init__(self):
		self.screen = pg.display.set_mode(res, pg.SCALED)
		self.clock = pg.time.Clock()
		self.fractal = Fractal(self)
		
	def run(self):
		while True:
			self.screen.fill('black')
			
			self.fractal.run()			
			[exit() for i in pg.event.get() if i.type == pg.QUIT]
			self.clock.tick()
			pg.display.set_caption(f'FPS: {self.clock.get_fps()}')

			pg.display.flip()
app = App()
app.run()
				
