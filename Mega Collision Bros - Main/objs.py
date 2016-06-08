import anim, gfx, pygame, vector
from const import *

class Player(gfx.AnimatedSprite):    
    action = 'stand'
    #anims = anim.player_anims
    walkSpeed = 5
    jumpSpeed = 15
    stunned = False
    jump = False
    fall = True
    direction = 1
    maxJump = 150
    
    def __init__(self): 
        #init base class
        gfx.AnimatedSprite.__init__(self, self.anims)

        # set player start point
        # TODO: Random.choice(Arena.spawnpoints)
        self.rect.bottom = SCREENRECT.bottom - 300 
        self.rect.left = SCREENRECT.left + 100

        self.pos = vector.Vect2D(self.rect.centerx, self.rect.centery)
        self.vel = vector.Vect2D(0,0)  

    def update(self, t):     
        #change action depending on velocity
        if self.vel.x > 0:
            self.action = 'walk_right'
            self.direction = 1
        elif self.vel.x < 0:
            self.action = 'walk_left'
            self.direction = -1
        else:
            self.action = 'stand'            

        if self.jump or self.fall:
            if self.vel.y <= TERM_VEL: self.vel.y += GRAVITY
            if self.rect.bottom + self.vel.y >= SCREENRECT.bottom:
                self.vel.y = SCREENRECT.bottom - self.rect.bottom

        if self.vel.y == 0:
            if self.jump:
                self.fall = True
                self.jump = False
            elif self.fall:
                self.fall = False
        else:
            if not self.fall:
                self.jump = True

        if 1 > self.vel.x > -1 and self.stunned:
            self.stunned = False
            self.vel.x = 0              

        # apply velocity
        self.pos += self.vel 
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        if not(self.jump or self.fall or self.vel.x == 0):
            self.vel.x += FRICTION * -self.direction

        self.Animate(t, self.action)    

class Particle(pygame.sprite.Sprite):
    lifeTime = 500
    def __init__(self, pos, vel):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(pos.x, pos.y, pos.x + 1, pos.y + 1)
        self.image = pygame.Surface((1,1))
        self.image.fill([255,0,0])
        self.vel = vel
        self.t = pygame.time.get_ticks()

    def update(self, t):
        if t - self.t > self.lifeTime:
            self.kill()
        self.rect.centerx += self.vel.x
        self.rect.centery += self.vel.y
        self.vel.y += GRAVITY 

class Enemy(Player):
    action = 'walk_right'
    #anims = anim.enemy_anims
    walkSpeed = 1
    stunned = False   

    def __init__(self):
        Player.__init__(self)
        self.rect.bottom = SCREENRECT.bottom
        self.rect.right = 512
        self.pos = vector.Vect2D(self.rect.centerx, self.rect.centery)
        self.direction = 1
        self.vel = vector.Vect2D(self.walkSpeed,0)
    def update(self, t):        

        if not self.stunned:
            self.vel.x = self.walkSpeed * self.direction

        Player.update(self, t)    

class Explosion(gfx.AnimatedSprite):
    action = 'explode'
    #anims = anim.explosion_anims
    speed = 0    
    
    def __init__(self, pos):
        gfx.AnimatedSprite.__init__(self, self.anims)        
        self.pos = pos
        self.t = pygame.time.get_ticks()        
        self.rect = self.image.get_rect()
        self.rect.centerx = pos.x
        self.rect.centery = pos.y
        self.lifeTime = len(self.anims[self.action]) * (1000 / FPS)
    def update(self, t):
        if t - self.t > self.lifeTime:
            self.kill()
        self.Animate(t, self.action)

class Bullet(gfx.AnimatedSprite):
    action = 'bullet'
    #anims = anim.bullet_anims
    speed = 5
    lifeTime = 1000

    def __init__(self, pos, direction):
        gfx.AnimatedSprite.__init__(self, self.anims)        

        self.rect.centerx = pos.x
        self.rect.centery = pos.y
        self.pos = pos
        self.t = pygame.time.get_ticks()
        
        self.direction = direction
        self.vel = vector.Vect2D(self.speed, 0) * direction        
        self.rect = self.image.get_rect()

    def update(self, t):       
        self.pos += self.vel
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y       
        
        self.Animate(t, self.action)

        if t - self.t > self.lifeTime:            
            self.kill()
            self = Explosion(self.pos)
            
def init():
    Bullet.anims = anim.loadImages(anim.bullet_anims)
    Player.anims = anim.loadImages(anim.player_anims)
    Enemy.anims = anim.loadImages(anim.enemy_anims)
    Explosion.anims = anim.loadImages(anim.explosion_anims)
