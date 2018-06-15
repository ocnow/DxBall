import os,pygame
from pygame.locals import *
from pygame.compat import geterror
from load_data import *

#classes for game objects
class Block(pygame.sprite.Sprite):
	def __init__(self,posx,posy):
		# call the parent class constructor
		pygame.sprite.Sprite.__init__(self)
		
		# create an image of the block and fill it with color.
		self.image = pygame.Surface([10,10])
		self.image.fill((0,255,0))
	
		#fetching the rectangle which has dimensions of the image
		self.rect = self.image.get_rect()
	
		self.rect.topleft = posx,posy


class Plate(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
		#initializing the image and rect		
		self.image = pygame.Surface([120,24])
		self.image.fill((255,0,0))
		self.rect = self.image.get_rect()
		
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		
		#positioning the plate		
		self.rect.left = 100
		self.rect.bottom = 540
		
		#maintaining the co-ordinates
		self.LeX = self.rect.left
		self.RiX = self.rect.right


	def moveLeft(self):
		if not self.rect.left - 20 < 0:
			newpos = self.rect.move((-20,0))
			self.rect = newpos


	def moveRight(self):
		if not self.rect.right + 20 > self.area.right:
			newpos = self.rect.move((20,0))
			self.rect = newpos


class Ball(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		#initializing the image and rect
		self.image,self.rect = load_image('football.png',-1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		
		#assigning the speeds
		self.spX,self.spY = 12,-12

		#positioning the ball
		self.rect.left = 100 + 60
		self.rect.bottom = self.area.bottom - 24

		#boolean variable if ball is on plate
		self.onPlate = 0
	def update(self):
		#changing the horizantal speed if going out of bounds
		if self.rect.left + self.spX < 0  or self.rect.right + self.spY > self.area.right:
			self.spX *= -1

		#changing vertical speed for upper bounds
		if self.rect.top + self.spY <0 :
			self.spY *= -1

		#changing the vertical speed for lower bounds
		if self.rect.bottom + self.spY > self.area.bottom - 24:
			if self.onPlate:
				self.spY *= -1
				self.onPlate = 0
			else:
				print("Game Over")
				pygame.quit()

		#updating the position
		newpos = self.rect.move((self.spX,self.spY))
		self.rect = newpos
	
	def isOnPlate(self,target):
		if self.rect.right < target.rect.left or self.rect.left > target.rect.right:
			self.onPlate = 0
			return
		print("on plate the ball")
		self.onPlate = 1


def positionBlocks():
	#sprite group for blocks
	blocks = pygame.sprite.RenderPlain()

	x=30
	while x<=700:
		y=20
		while y<=400:
			blck = Block(x,y)
			blocks.add(blck)
			y+=20
			#print((x,y))
		x+=20
	return blocks

def main():
	pygame.init()
	screen = pygame.display.set_mode((720,540))
	pygame.display.set_caption("Monkey Fever")	

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250,250,250))

	ball = Ball()
	plate = Plate()

	allsprites = pygame.sprite.RenderPlain((ball,plate))
	blocks = positionBlocks()

	clock = pygame.time.Clock()

	pygame.key.set_repeat(100,100)
	while True:
		clock.tick(20)
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					plate.moveLeft()
				elif event.key == pygame.K_RIGHT:
					plate.moveRight()		
		#deleting the hit blocks
		blocks_hit_list = pygame.sprite.spritecollide(ball,blocks,True)

		ball.isOnPlate(plate)
		screen.blit(background,(0,0))

	
		allsprites.update()
		allsprites.draw(screen)
		blocks.draw(screen)
		pygame.display.flip()

if __name__ == '__main__':
	main()
