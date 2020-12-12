import pygame, sys
from pygame.locals import *
from pygame import mixer
import random
import time
 
'''install''' 
pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
'''Setting up FPS'''
FPS = 60
FramePerSec = pygame.time.Clock()

 


'''buat tampilan'''
panjang = 500
lebar = 650

tampilan = pygame.display.set_mode((panjang, lebar))

pygame.display.set_caption("Galaxy Shooter")



'''Text'''
text30 = pygame.font.SysFont('Constantia', 30)
text40 = pygame.font.SysFont('Constantia', 40)
text50 = pygame.font.SysFont('comicsans', 45)


'''Music'''
bom_music = pygame.mixer.Sound('img/bom.wav')
bom_music.set_volume(0.25) 

laser_music = pygame.mixer.Sound('img/laser2.wav')
laser_music.set_volume(0.25)



bom_hit_fx = pygame.mixer.Sound('img/bom.wav')
bom_hit_fx.set_volume(0.70) 

bom_hit_music = pygame.mixer.Sound('img/bom.wav')
bom_hit_music.set_volume(0.25) 

warning_fx = pygame.mixer.Sound('img/warning.wav')
warning_fx.set_volume(0.25) 

pygame.mixer.music.load("img/music.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.75)
'''Variabel'''

rows = 1
cols = 1
merah = (255,0,0)
hijau = (0,255,0)
putih = (255,255,255) 
alien_colldown = 1000
last_alien_shoot = pygame.time.get_ticks()
countdown = 14
last_count = pygame.time.get_ticks()

'''Text'''
def text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	tampilan.blit(img, (x, y))

def draw_text():
		level_label = text50.render("Level: 5", 1, (putih))
		tampilan.blit(level_label, (panjang - level_label.get_width() - 10, 10))
def text_bos():
	bos_label = text30.render("Bos Enemy", 1, (putih))
	tampilan.blit(bos_label, (10, 10))

'''Player Space Shoter'''
class Pesawat(pygame.sprite.Sprite):
	def __init__(self, x, y, darah):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('ship1.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
		self.health_start = darah
		self.health_remaining = darah
		self.last_shoot = pygame.time.get_ticks()


	def update(self):
		'''Kecepatan bergegerak'''
		kecepatan = 8

		'''Colldown'''
		colldown = 500
		COLLDOWN = 100
		game_over = 0

		speed = 5

		'''Keys/ Tombol untuk menjalankannya'''
		key = pygame.key.get_pressed()
		if key[pygame.K_a] and self.rect.left > 0:
			self.rect.x -= kecepatan
		if key[pygame.K_d] and self.rect.right < panjang:
			self.rect.x += kecepatan

		if key[pygame.K_w]:
			self.rect.y -= speed
		if key[pygame.K_s]:
			self.rect.y += speed
		'''catat waktu saat ini'''
		time_now = pygame.time.get_ticks()

		'''Tembak'''
		if key[pygame.K_SPACE] and time_now - self.last_shoot > colldown:
			laser_music.play()
			peluru = Peluru(self.rect.centerx, self.rect.top)
			peluru_group.add(peluru)
			self.last_shoot = time_now


		if key[pygame.K_b] and time_now - self.last_shoot > COLLDOWN:
			laser_music.play()
			peluru_laser = Peluru_laser(self.rect.centerx, self.rect.top-10)
			peluru_laser_group.add(peluru_laser)
			self.last_shoot = time_now
		'''mask'''
		self.mask = pygame.mask.from_surface(self.image)


		'''Menggambar darah'''
		pygame.draw.rect(tampilan, merah, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(tampilan, hijau, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)),15))
		elif self.health_remaining <= 0:
			bom_hit_music.play()
			bom = Bom(self.rect.centerx, self.rect.centery, 3)
			bom_group.add(bom)
			self.kill()
		


'''Musuh class'''
class Musuh(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('bos.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
		self.health_start = health
		self.health_remaining = 1000
		self.move_counter = 7
		self.move_direction = 1
		self.last_alien_shoot = pygame.time.get_ticks()
		self.alien_colldown = 250

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 180:
			self.move_direction *= -1
			self.move_counter *= self.move_direction
		
		time_now = pygame.time.get_ticks()

		if time_now - self.last_alien_shoot > self.alien_colldown:
			peluru_musuh = Peluru_Musuh(self.rect.centerx, self.rect.bottom)
			peluru_musuh_group.add(peluru_musuh)
			self.last_alien_shoot = time_now
		if self.health_remaining == 600:
			self.alien_colldown -= 150
			bom = Bom(self.rect.centerx, self.rect.centery, 3)
			bom_group.add(bom)
			bom_hit_music.play()
		elif self.health_remaining == 450:
			self.alien_colldown += 70
			bom = Bom(self.rect.centerx, self.rect.centery, 3)
			bom_group.add(bom)	
		elif self.health_remaining <= 0:			
			bom = Bom(self.rect.centerx, self.rect.centery, 3)
			bom_group.add(bom)
			self.kill()
			bom_hit_music.play()


'''Peluru player class'''
class Peluru(pygame.sprite.Sprite):
	def __init__(self, x, y,):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('peluru.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]

	def update(self):
		self.rect.y -= 9
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, musuh_group, False):
			self.kill()
			bom_music.play()
			musuh.health_remaining -=2
			bom = Bom(self.rect.centerx, self.rect.centery, 1)
			bom_group.add(bom)


'''laser player class'''
class Peluru_laser(pygame.sprite.Sprite):
	def __init__(self, x, y,):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('peluru_laser.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]


	def update(self):
		self.rect.y -= 9
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, musuh_group, False):
			self.kill()
			musuh.health_remaining -= 2
			bom = Bom(self.rect.centerx, self.rect.centery, 2)
			bom_group.add(bom)

				

'''Peluru musuh class'''
class Peluru_Musuh(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('peluru_musuh_1.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]

	def update(self):
		self.rect.y += 9
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, ship_group, False, pygame.sprite.collide_mask):
			self.kill()
			ship.health_remaining -= 15
			bom_music.play()
			bom = Bom(self.rect.centerx, self.rect.centery, 2)
			bom_group.add(bom)



'''bom class'''				
class Bom(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1,6):
			img = pygame.image.load(f'bom1.png')
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			if size == 4:
				img = pygame.transform.scale(img, (200, 200))
			self.images.append(img)

		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
		self.counter = 0

	def update(self):
		bom_speed = 3
		'''animasi bom'''
		self.counter += 1

		if self.counter >= bom_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		'''Delete bom animasi'''
		if self.index >= len(self.images) - 1 and self.counter >= bom_speed:
			self.kill()






'''	Buat spiret gruop'''
ship_group = pygame.sprite.Group()
peluru_group = pygame.sprite.Group()
musuh_group = pygame.sprite.Group()
peluru_musuh_group = pygame.sprite.Group()
bom_group = pygame.sprite.Group()
peluru_laser_group = pygame.sprite.Group()

			
'''buat player'''
ship = Pesawat(int(panjang / 2), lebar - 100, 100)
ship_group.add(ship)

'''Musuh'''
musuh = Musuh(int(panjang / 2), lebar - 500, 1000)
musuh_group.add(musuh)

'''Background bergerak'''                   
class Background():
      def __init__(self):
            self.bgimage = pygame.image.load('background3.png')
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = self.rectBGimg.height
            self.bgX2 = 0
 
            self.movingUpSpeed = 5
         
      def update1(self):
        self.bgY1 -= self.movingUpSpeed
        self.bgY2 -= self.movingUpSpeed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height
             
      def render(self):
         tampilan.blit(self.bgimage, (self.bgX1, self.bgY1))
         tampilan.blit(self.bgimage, (self.bgX2, self.bgY2))

'''Setting up Sprites'''
 
back_ground = Background()



'''Game Looping'''
run = True
while run:          

    
    back_ground.update1()
    back_ground.render()
    
    if countdown == 0:	
	    ship.update()
	    peluru_group.update()
	    musuh_group.update()
	    peluru_musuh_group.update()		
	   	


    bom_group.update()
    peluru_laser_group.update()
	
    '''menggambar spirite group'''
    ship_group.draw(tampilan)
    peluru_group.draw(tampilan)
    musuh_group.draw(tampilan) 
    peluru_musuh_group.draw(tampilan)
    bom_group.draw(tampilan)
    peluru_laser_group.draw(tampilan)
    draw_text()
    text_bos()
    '''Tombol atau keys '''   
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False	
    if countdown > 0:
    	text('WARNING!!', text40, putih, int(panjang / 2 - 110), int(lebar / 2 + 10))
    	count_timer = pygame.time.get_ticks()	
    	warning_fx.play()
    	if count_timer - last_count > 1000:
    	
    		countdown -= 1 
    		last_count = count_timer


    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()