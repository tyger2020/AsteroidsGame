# program template for Spaceship
# This is coded in chrome
# I added levels for fun :) Level 1 is required RiceRocks, level 2 you have to hit rocks twice
#for a point, level 3 you have a fixed number of missiles
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
velocity = 1
left = False
up = False
down = False
right = False
rocks = []
missiles = []
score = 0
lives = 4
collides = False
started = False
level = 0
missilenum = 200
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(0.99)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, angle_vel, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = angle_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        canvas.draw_image(ship_image,
                          ship_info.get_center(),
                          ship_info.get_size(),
                          self.pos,
                          (WIDTH/8, HEIGHT/8),self.angle)

    def update(self):
        global WIDTH
        global up
        
        # accelerate while up key is down
        if up == True:
            self.vel[0] += 0.1*math.cos(self.angle)
            self.vel[1] += 0.1*math.sin(self.angle)
        
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        self.pos = [self.pos[0]+self.vel[0],self.pos[1]+self.vel[1]]
        if (self.pos[0] > WIDTH):
            self.pos[0] = self.pos[0] - WIDTH
        if (self.pos[1] > HEIGHT):
            self.pos[1] = self.pos[1] - HEIGHT
        if (self.pos[0] < 0):
            self.pos[0] = self.pos[0] + WIDTH
        if (self.pos[1] < 0):
            self.pos[1] = self.pos[1] + HEIGHT
            
    def shoot(self):
        global missiles, missilenum, level, started
        x = my_ship.pos[0] + 45 * math.cos(my_ship.angle)
        y = my_ship.pos[1] + 45 * math.sin(my_ship.angle)
        missile = Sprite([x,y], [10, 0], my_ship.angle, 0,
                         missile_image, missile_info)
        missiles.append(missile)
        if (level == 3):
            missilenum -= 1
            print missilenum
            #canvas.draw_text("Remaining missiles: " + (str)(missilenum), (300, 50), 25, "Yellow")
            if missilenum == 0:
                started = False
    def collide(self, other_object):
        distance = dist(self.pos, other_object.pos)
        if (distance < other_object.radius + self.radius):
            return True
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.out = False
        self.hit = 0
        
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center,
                          self.image_size, self.pos,
                          self.image_size, self.angle)

    def update(self):
        #self.angle += self.angle_vel
        #self.pos[0] += self.vel[0]
        #self.pos[1] += self.vel[1]
        self.pos[0] += self.vel[0]*math.cos(self.angle)
        self.pos[1] += self.vel[0]*math.sin(self.angle)
        if (self.pos[0]<0 or self.pos[0]>WIDTH or
            self.pos[1]<0 or self.pos[1]>HEIGHT):
            self.out = True
        
    def collide(self, other_object):
        distance = dist(self.pos, other_object.pos)
        if (distance < other_object.radius + self.radius):
            return True
         
def draw(canvas):
    global time
    global rocks
    global missiles, missilenum
    global left, right, lives, score, collides, level, started
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(),
                      [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size,
                      (wtime - WIDTH / 2, HEIGHT / 2),
                      (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size,
                      (wtime + WIDTH / 2, HEIGHT / 2),
                      (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    
    for rock in rocks:    
        rock.draw(canvas)

    for missile in missiles:
        missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    
    for rock in rocks:
        rock.update()
        if (rock.out):
            rocks.remove(rock)
        
    for rock in rocks:
        if (rock.collide(my_ship)):
            rocks.remove(rock)
            if (lives > 0):
                lives -= 1
            if lives <= 0:
                started = False

    for missile in missiles:
        missile.update()
        if (missile.out):
            missiles.remove(missile)
            
    for missile in missiles:
        for rock in rocks:
            if (missile.collide(rock)):
                rock.hit += 1
                missiles.remove(missile)
                canvas.draw_image(explosion_image, explosion_info.get_center(),
                          explosion_info.get_size(),
                          rock.pos, [WIDTH, HEIGHT])
                explosion_sound.play()
                    
                print level
                if (level == 2 and rock.hit >= 2) or (level == 1) or (level == 3):
                    score += 1
                    rocks.remove(rock)    
    
    if started == False:
        canvas.draw_image(splash_image, splash_info.get_center(),
                      splash_info.get_size(),
                     [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
        lives = 3
        canvas.draw_text("You are starting Level " + (str)(level + 1), (250, 55), 25, "Yellow")
        
    #Rotate ship left or right    
    if left == True:
        my_ship.angle -= 0.05
    elif right == True:
        my_ship.angle += 0.05
    canvas.draw_text("Score:" + str(score), (600, 30), 25, "Yellow")
    canvas.draw_text("Lives:" + str(lives), (100, 45), 25, "Yellow")
    if level == 3:
        canvas.draw_text("Remaining missiles: " + (str)(missilenum), (300, 50), 25, "Yellow")
            
# timer handler that spawns a rock    
def rock_spawner():
    global rocks
    import random
    if started == True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        d1 = 2*random.random() - 1
        d2 = 2 * random.random() - 1
    
        if dist(my_ship.pos, [x,y]) < 50:
            x=x+150
            y=y+150
    
        rock = Sprite([x, y], [d1, d2], math.acos(d1), 0.1,
                  asteroid_image, asteroid_info)
        rocks.append(rock)
    
    
    
    
def keydown(key):
    global down, up, left, right
    if key == simplegui.KEY_MAP["down"]:
        down = True
        my_ship.vel[0] = 0 # math.cos(my_ship.angle)
        my_ship.vel[1] = 0 # math.sin(my_ship.angle)
        #if (my_ship.vel[0]!=0 or my_ship.vel[1]!=0):
        ship_thrust_sound.pause()
        #else:
         #   ship_thrust_sound.pause()
    elif key == simplegui.KEY_MAP["up"]:
        up = True
        my_ship.vel[0] += math.cos(my_ship.angle)
        my_ship.vel[1] += math.sin(my_ship.angle)
        if (my_ship.vel[0]!=0 or my_ship.vel[1]!=0):
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    elif key == simplegui.KEY_MAP["left"]:
        left = True
        #my_ship.vel[0] -= 1
        #if (my_ship.vel[0]!=0 or my_ship.vel[1]!=0):
        ship_thrust_sound.pause()
        
    elif key == simplegui.KEY_MAP["right"]:
        right = True
        
        #my_ship.vel[0] += 1
        #if (my_ship.vel[0]!=0 or my_ship.vel[1]!=0):
        ship_thrust_sound.pause()
        #else:
         #   ship_thrust_sound.pause()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        #ship_thrust_sound.play()
        #explosion_sound.play()
        missile_sound.play()
        
def keyup(key):
    global left, right, up
    if key == simplegui.KEY_MAP["left"]:
        left = False
    elif key == simplegui.KEY_MAP["right"]:
        right = False
    elif key == simplegui.KEY_MAP["up"]:
        up = False
        
def click(pos):
    global started,score,level,lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)

    started = True
        
    #print level
    if level == 0:
        level += 1
        
    else:
        if (score >= 10 * level):
            if level <= 3:
                level += 1
        print level
            
    if lives == 0:
        started = False
        
    if ((level == 1 and score >= 10 * level and lives == 0) or (level == 2 and score >= 10 * level and lives == 0)):
        started = False
        level += 1
        
               
        for rock in rocks:
            rocks.remove(rock)
            lives = 3
    if level == 4:
        level = 1
    print level
                      
    
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0,0], 0, 2,
               ship_image, ship_info)

a_rock = Sprite([400, 300], [0.3, 0.4], 0, 0.1,
                asteroid_image, asteroid_info)
rocks.append(a_rock)

# register handlers
frame.set_draw_handler(draw)

    
timer = simplegui.create_timer(1000.0, rock_spawner)
# get things rolling
timer.start()
frame.start()
