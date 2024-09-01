import pygame as pg
import numpy as np
import math
import numba 

res = width, height = 800, 450 
offset = np.array([1.3 * width, height])//2
max_iter = 30
zoom = 2.2/height
texture = pg.image.load('images/texture.jpg')
texture_size = min(texture.get_size()) - 1
texture_array = pg.surfarray.array3d(texture)




class Fractal:
	def __init__(self, app):
		self.app = app
		self.screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint8)
		self.x = np.linspace(0, width, num=width, dtype=np.float32)	
		self.y = np.linspace(0, height, num=height, dtype=np.float32)	
	def render(self):
		x = (self.x - offset[0]) * zoom
		y = (self.y - offset[1]) * zoom
		c = x + 1j * y[:, None]
		
		num_iter = np.full(c.shape, max_iter)
		z = np.zeros(c.shape, np.complex128)
		for i in range(max_iter):
			mask = (num_iter == max_iter)
			z[mask] = z[mask] ** 2 + c[mask]
			z[mask] = np.where(np.abs(z[mask]) > 10, 10 + 0j, z[mask])
			num_iter[mask & (z.real **2 + z.imag ** 2 > 4.0)] = i+1
		
		col = (num_iter.T * texture_size/max_iter).astype(np.uint8)
		self.screen_array = texture_array[col, col]
	def update(self):
		self.render()
		
	
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
				
