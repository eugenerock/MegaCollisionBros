import pygame
from PIL import Image

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
    def __init__(self, anims):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.anims = anims        
        self.image = anims[self.action][0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.facing = 0
        self.lastAnimUpdate = 0
        self.animDelay = 60
        self.Animate(pygame.time.get_ticks(), self.action)    
    def Animate(self, t, action):
        self.images = self.anims[action]
        if t - self.lastAnimUpdate > self.animDelay:
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0
            self.image = self.images[self.frame]
            self.lastAnimUpdate = t
