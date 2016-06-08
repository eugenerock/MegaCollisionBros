import math, os, pygame, random
from pygame.locals import *
from PIL import Image

SCREENRECT = Rect(0, 0, 1024, 768)
GRAVITY = 9.8

def load_image(filename, colorkey = None):
    filename = os.path.join('data', filename)
    image = pygame.image.load(filename).convert()
    return image

def imgcolorkey(image, colorkey):
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

class SpriteSheet:
    def __init__(self, filename, columns, rows):
        self.sheet = load_image(filename)
        self.rows = rows
        self.columns = columns
        self.tileOffsetX = self.sheet.get_size()[0] / self.columns
        self.tileOffsetY = self.sheet.get_size()[1] / self.rows
    def imgat(self, rect, colorkey = None):
        rect = Rect(rect)
        image = pygame.Surface(rect.size,SRCALPHA, 32)
        image.blit(self.sheet, (0, 0), rect)
        return image    
    def imgsat(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs
    def getTile(self, x, y, colorkey = None):
        rect = Rect(x * self.tileOffsetX, y * self.tileOffsetY, self.tileOffsetX, self.tileOffsetY)
        image = pygame.Surface(rect.size, SRCALPHA, 32)
        image.blit(self.sheet, (0, 0), rect)
        return image 
    

class AnimatedGif(object):
    def __init__(self, gif):
        self.gif = gif
        self.gif_image = Image.open(self.gif)
    def getImgs(self, flip=None):
        self.images = []
        palette = self.to_triplets(self.gif_image.getpalette())
        try:
            while 1:
                if flip:
                    image = pygame.image.fromstring(self.gif_image.transpose(Image.FLIP_LEFT_RIGHT).tostring(), self.gif_image.size, 'P')
                else:
                    image = pygame.image.fromstring(self.gif_image.tostring(), self.gif_image.size, 'P')
                image.set_palette(palette)
                image.set_colorkey(self.gif_image.info['transparency'])
                self.images.append(image)
                self.gif_image.seek(self.gif_image.tell() + 1)
        except: pass
        return self.images
    def to_triplets(self, pil_palette):
        return [pil_palette[i:i+3] for i in range(0, len(pil_palette), 3)]
    def listImgs(self, name, count):
        return[pygame.image.fromstring(Image.open(name+str(i)+'.gif').tostring(), Image.open(name+str(i)+'.gif').size, 'P') for i in range(1,count)]
         
         
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, actions):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.actions = actions        
        self.image = actions['stand'][0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.facing = 0
        self.lastUpdate = 0
        self.delay = 60
        self.Animate(pygame.time.get_ticks(), self.action)
    def Animate(self, t, action):
        self.images = self.actions[action]
        if t - self.lastUpdate > self.delay:
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0
            self.image = self.images[self.frame]
            self.lastUpdate = t

    
class Player(AnimatedSprite):
    #default action for this game object
    action = 'stand'
    
    
    def __init__(self, actions): 
        #init base class
        AnimatedSprite.__init__(self, actions)

        self.rect.bottom = SCREENRECT.bottom - 300
        self.rect.left = SCREENRECT.left + 100

        self.vel = Vector(0,0)        

        #put this somewhere else
        self.bullet_actions = {}
        self.bullet_actions['stand'] = AnimatedGif('EnergyBall_small.gif').getImgs()
        self.bullet_actions['bullet'] = AnimatedGif('EnergyBall_small.gif').getImgs() 

    def Shoot(self):
        self.bullet = Bullet(self.bullet_actions, self.facing, self.rect.right)        

    def Locate(self, x, y):
        self.rect.centerx += x
        self.rect.bottom += y

    def update(self, t):
        self.x = 0
        self.keys = pygame.key.get_pressed()
        self.rect.size = self.image.get_rect().size
        if self.keys[K_LEFT]:
            self.delay = 60
            self.direction = 'walk_left'
            self.Animate(t, self.direction)
            self.rect.centerx -= self.speed
            self.facing  = 1
        if self.keys[K_RIGHT]:
            self.delay = 60
            self.direction = 'walk_right'
            self.Animate(t, self.direction)
            self.rect.centerx += self.speed
            self.facing = 0
        if self.keys[K_DOWN] and self.facing == 0:
            self.delay = 120
            self.Animate(t, 'crouch')
            self.rect.bottom = SCREENRECT.bottom
        if self.keys[K_DOWN] and self.facing == 1:
            self.delay = 120
            self.Animate(t, 'crouch_left')
            self.rect.bottom = SCREENRECT.bottom
        if self.keys[K_SPACE]:
            self.delay = 70
            self.Shoot()
            self.Animate(t, 'shoot_right')
        else:
            self.delay = 120
            if self.facing == 0:
                self.Animate(t, 'stand')
            elif self.facing == 1:
                self.Animate(t, 'stand_left')


class Enemy(AnimatedSprite):
    action = 'stand'

    def __init__(self, actions):
        AnimatedSprite.__init__(self, actions)
        self.rect.bottom = SCREENRECT.bottom
        self.rect.right = SCREENRECT.right - 100
        self.direction = ''
        self.speed = 1
        self.delay = 120
    def update(self, t):
        self.Animate(t, 'stand')

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def X(self):
        return self.x
    def Y(self):
        return self.y


#class Gun(pygame.sprite.Sptite):
#    def __init__(self):
#        pygame.sprite.Sprite.__init__(self)






#class Bullet(pygame.sprite.Sprite):
#    def __init__(self, image):
#        pygame.sprite.Sprite.__init__(self)
#        self.image = image
#        self.speed = 3
#        sel.rect = self.image.get_rect()
#    def update(self):
#        self.rect.centerx += self.speed
    
                        
class Arena:
    def __init__(self):
        self.rect = SCREENRECT
        self.background = pygame.Surface(SCREENRECT.size).convert()
        

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREENRECT.size)
        self.arena = Arena()
        self.screen.blit(self.arena.background, (0, 0))
        pygame.display.flip()
        all = pygame.sprite.RenderUpdates()
        Player.containers = all
        Enemy.containers = all
        Bullet.containers = all
        clock = pygame.time.Clock()
        self.getPlayers()
        #player.containers = sprites
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            all.clear(self.screen, self.arena.background)
            all.update(pygame.time.get_ticks())
            self.Collide()
            dirty = all.draw(self.screen)
            pygame.display.update(dirty)
            clock.tick(100)
        pygame.display.quit()
        

    def getPlayers(self):
        player_actions = {}
        player_actions['stand'] = AnimatedGif('Fio_stand.gif').getImgs()
        player_actions['stand_right'] = AnimatedGif('Fio_stand.gif').getImgs()
  #      player_actions['stand_left'] = AnimatedGif('Fio_stand.gif').getImgs(flip='y')
        player_actions['crouch'] = AnimatedGif('Fio_crouch_rifle.gif').getImgs()
        player_actions['walk_right'] = AnimatedGif('Fio_run.gif').getImgs()
        player_actions['walk_left'] = AnimatedGif('Fio_run.gif').getImgs(flip='y')
        player_actions['stand_left'] = AnimatedGif('Fio_stand.gif').getImgs(flip='y')
        player_actions['crouch_left'] = AnimatedGif('Fio_crouch_rifle.gif').getImgs(flip='y')
        player_actions['shoot_right'] = AnimatedGif('Fio_shoot2.gif').getImgs()
        player_actions['shoot_left'] = AnimatedGif('Fio_shoot2.gif').getImgs(flip='y')
        enemy_actions = {}
        enemy_actions['stand'] = AnimatedGif('Eri_stand.gif').getImgs(flip='y')
        enemy_actions['walk_right'] = AnimatedGif('Eri_run.gif').getImgs()
        enemy_actions['walk_left'] = AnimatedGif('Eri_run.gif').getImgs(flip='y')
        self.player = Player(player_actions)
        self.enemy = Enemy(enemy_actions)
    

    def Collide(self):
        if not self.arena.rect.contains(self.player.rect):
            if self.player.rect.left < self.arena.rect.left:
                self.player.rect.left = self.arena.rect.left
            elif self.player.rect.right > self.arena.rect.right:
                self.player.rect.right = self.arena.rect.right
        if self.player.rect.top < self.arena.rect.top:
            self.player.rect.top = self.arena.rect.top
        if self.player.rect.bottom > self.arena.rect.bottom:
            self.player.rect.bottom = self.arena.rect.bottom
        

def main():
    pygame.init()
    pygame.display.set_caption("Test")   
    game = Game()
    
        
if __name__ == '__main__': main()



#velocity = [10, 10]
