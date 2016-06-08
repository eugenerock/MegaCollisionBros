import math, os, pygame, random, vector, objs
from pygame.locals import *
from const import *



class Arena:
    def __init__(self):
        self.rect = SCREENRECT
        self.background = pygame.Surface(SCREENRECT.size).convert()        

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREENRECT.size)#, pygame.FULLSCREEN)
        self.arena = Arena()
        self.screen.blit(self.arena.background, (0, 0))        
        pygame.display.flip()
        self.all = pygame.sprite.RenderUpdates()
        self.particles = pygame.sprite.RenderUpdates()
        objs.Player.containers = self.all
        objs.Enemy.containers = self.all       
        objs.Bullet.containers = self.particles
        objs.Explosion.containers = self.particles
        objs.Particle.containers = self.particles
        clock = pygame.time.Clock()
        self.player = objs.Player()
        self.enemy = objs.Enemy()  
       
        while 1:
            # self.all
            #check quit events
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return

            #check what keys pressed and respond
            keyPressed = pygame.key.get_pressed()            
            #FIX THIS
            if not self.player.stunned:
                if keyPressed[K_LEFT]:
                    self.player.vel.x  = -self.player.walkSpeed
                if keyPressed[K_RIGHT]:
                    self.player.vel.x = self.player.walkSpeed
                if keyPressed[K_x]:
                    if not (self.player.jump or self.player.fall):
                        self.player.vel.y = -self.player.jumpSpeed
                        self.player.jump = True
                if keyPressed[K_DOWN]:
                    self.player.action = 'crouch'
                if keyPressed[K_SPACE]:
                    self.enemy.direction = -self.enemy.direction
                if keyPressed[K_b]:
                    self.spawnParticles()
                if keyPressed[K_z]:
                    self.spawnBullet(self.player)
            
            self.all.clear(self.screen, self.arena.background)
            self.all.update(pygame.time.get_ticks())
           # print self.getCollisions()
            self.particles.clear(self.screen, self.arena.background)
            self.doCollisions(self.getCollisions())
            self.particles.update(pygame.time.get_ticks())
            self.Collide()
            dirty = self.all.draw(self.screen)
            dirty.extend(self.particles.draw(self.screen))
            pygame.display.update(dirty)
            clock.tick(FPS)
        pygame.display.quit() 

    def spawnBullet(self, owner):
        direction = owner.direction
        pos = vector.Vect2D(owner.pos.x + (owner.rect.width / 2 + 1) * owner.direction, owner.pos.y)
        bullet = objs.Bullet(pos, direction)        
        self.all.add(bullet)
        
    def spawnParticles(self):
        for i in range(0, 5):
            vx = random.randint(-50, 50)/float(20)
            vy = random.randint(-5, 0)
            vel = vector.Vect2D(vx, vy)
            self.particles.add(objs.Particle(vel))     
        
    def getCollisions(self):
        sprites = [sprite for sprite in self.all]
        collisions = []
        for sprite in self.all:
            sprites.remove(sprite)
            collision = sprite.rect.collidelist([i.rect for i in sprites])
            if collision != -1:
                collisions.append([sprite, sprites[collision]])
        return collisions

    def Displace(self, rect1, rect2):
        overlap = rect1.clip(rect2)
        if overlap.size != 0:
            if overlap.height > overlap.width:
                v_dp = vector.Vect2D(overlap.width / float(2), 0)
                if rect1.centerx < rect2.centerx:
                    return vector.Vect2D(rect1.centerx, rect1.centery) - v_dp, vector.Vect2D(rect2.centerx, rect2.centery) + v_dp
                else:
                    return vector.Vect2D(rect1.centerx, rect1.centery) + v_dp, vector.Vect2D(rect2.centerx, rect2.centery) - v_dp
            else:
                v_dp = vector.Vect2D(0, overlap.height / float(2))
                if rect1.centery < rect2.centery:
                    return vector.Vect2D(rect1.centerx, rect1.centery) - v_dp, vector.Vect2D(rect2.centerx, rect2.centery) + v_dp
                else:
                    return vector.Vect2D(rect1.centerx, rect1.centery) + v_dp, vector.Vect2D(rect2.centerx, rect2.centery) - v_dp
            

    def doCollisions(self, collisions):
        for sprites in collisions:      
            #find new x and y displacement values for each pos so sprites dont get 'entangeld"           
            try:                    
                sprites[0].vel, sprites[1].vel = vector.vectorCollision(sprites[0].vel, sprites[1].vel, sprites[0].pos, sprites[1].pos)
                sprites[0].pos, sprites[1].pos = self.Displace(sprites[0].rect, sprites[1].rect)
            except: pass
            sprites[0].stunned = True
            sprites[1].stunned = True
        
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
    objs.init()
    pygame.display.set_caption("Test")   
    game = Game()
    pygame.display.quit()
    
        
if __name__ == '__main__': main()


