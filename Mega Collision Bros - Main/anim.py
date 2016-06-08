import gfx, pygame

player_anims = {
        'stand'         : ('.\\gfx\\Fio_stand.gif', False),
        'stand_right'   : ('.\\gfx\\Fio_stand.gif', False),
        'stand_left'    : ('.\\gfx\\Fio_stand.gif', True),
        'crouch'        : ('.\\gfx\\Fio_crouch_rifle.gif', False),
        'walk_right'    : ('.\\gfx\\Fio_run.gif', False),
        'walk_left'     : ('.\\gfx\\Fio_run.gif', True),
        'crouch_left'   : ('.\\gfx\\Fio_crouch_rifle.gif', True),
        'shoot_right'   : ('.\\gfx\\Fio_shoot2.gif', False),
        'shoot_left'    : ('.\\gfx\\Fio_shoot2.gif', True)
}

enemy_anims = {
        'walk_right'    : ('.\\gfx\\Monkey_walk.gif', False),
        'walk_left'     : ('.\\gfx\\Monkey_walk.gif', True),
        'stand'         : ('.\\gfx\\Monkey_walk.gif', False)
}

bullet_anims = {
        'bullet'        : ('.\\gfx\\EnergyBall_small.gif', False)
}

explosion_anims = {
        'explode'       : ('.\\gfx\\Explosion_grenade.gif', False)
}  

def init():
    """Initialises animation lists. Must be called AFTER pygame.init()"""
    global player_anims, enemy_anims, bullet_anims, explosion_anims    
    
    player_anims = loadImages(player_anims)
    enemy_anims = loadImages(enemy_anims)
    bullet_anims = loadImages(bullet_anims)
    explosion_anims = loadImages(explosion_anims)
    
def loadImages(images):    
    imageDict = {}
    for key in images.keys(): 
        imageDict[key]= gfx.AnimatedGif(images[key][0]).getImgs(flip = images[key][1])
    return imageDict



