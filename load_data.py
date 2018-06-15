import os,pygame
from pygame.locals import *
from pygame.compat import geterror


if not pygame.font:print("warning,fonts disabled")

if not pygame.mixer:print("warning,sounds disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]

data_dir = os.path.join(main_dir,'data')

#functions to create our resources
def load_image(name,colorkey = None):
	fullname = os.path.join(data_dir,name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error:
		print("cannot load image:",fullname)
		raise SystemExit(str(geterror()))

	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey,RLEACCEL)
	return image,image.get_rect()

def load_sound(name):
	class NoneSound:
		def play(self):pass
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound()
	fullname = os.path.join(data_dir,name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error:
		print("cannot load sound: %s"%wav)
		raise SystemExit(str(geterror()))
	return sound

