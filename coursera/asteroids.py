# Implementation of card game Blackjack
# template: http://www.codeskulptor.org/#examples-spaceship_template.py
# play online: http://www.codeskulptor.org/#user40_nhF4vjfYZI_0.py

import simplegui
import math
import random

# globals for user interface
ANG_VEL = 0.075
ACC = 0.2
FRIC = 0.99
KEY_DICT = {"left": -ANG_VEL, "right": ANG_VEL}
WIDTH = 800
HEIGHT = 600
SCREEN_SIZE = [WIDTH, HEIGHT]
score = 0
lives = 0
time = 0
rock_group = set()
missile_group = set()
started = False
rock_modifier = 0


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
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


# art assets created by Kim Lathrop, may be freely re-used in non-commercial
# projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png,
# debris4_brown.png, debris1_blue.png, debris2_blue.png, debris3_blue.png,
# debris4_blue.png, debris_blend.png

debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        sprite.update()
        if sprite.update():
            group.remove(sprite)


def group_collide(group, other_object):
    for sprite in set(group):
        if sprite.collide(other_object):
            group.remove(sprite)
            return True
    else:
        return False


def group_group_collide(group_1, group_2):
    count = 0
    for element in set(group_1):
        if group_collide(group_2, element):
            group_1.discard(element)
            count += 1
    return count


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = pos
        self.vel = vel
        self.thrusters = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def thrust(self):
        self.thrusters = not self.thrusters
        if self.thrusters:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()

    def draw(self, canvas):
        if self.thrusters:
            canvas.draw_image(self.image, [
                ship_info.get_center()[0] + ship_info.get_size()[0],
                ship_info.get_center()[1]], ship_info.get_size(), self.pos,
                              [3 * ship_info.get_radius()] * 2, self.angle)
        else:
            canvas.draw_image(self.image, ship_info.get_center(),
                              ship_info.get_size(), self.pos,
                              [3 * ship_info.get_radius()] * 2, self.angle)

    def update(self):
        self.angle += self.angle_vel
        if self.thrusters:
            forward_vector = angle_to_vector(self.angle)
        else:
            forward_vector = [0, 0]
        for i in range(2):
            self.vel[i] = FRIC * self.vel[i] + ACC * forward_vector[i]
            self.pos[i] = (self.pos[i] + self.vel[i]) % SCREEN_SIZE[i]

    def inc_angle_vel(self, amount):
        self.angle_vel += amount

    def dec_angle_vel(self, amount):
        self.angle_vel -= amount

    def shoot(self):
        global missile_group
        a_missile = Sprite([self.pos[0] + 50 * angle_to_vector(self.angle)[0],
                            self.pos[1] + 50 * angle_to_vector(self.angle)[1]],
                           [self.vel[0] + 5 * angle_to_vector(self.angle)[0],
                            self.vel[1] + 5 * angle_to_vector(self.angle)[1]],
                           0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = pos
        self.vel = vel
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_object):
        if dist(self.get_position(),
                other_object.get_position()) < self.get_radius() + \
                other_object.get_radius():
            return True
        else:
            return False

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, [2 * self.radius] * 2, self.angle)

    def update(self):
        self.angle += self.angle_vel
        for i in range(2):
            self.pos[i] = (self.pos[i] + self.vel[i]) % SCREEN_SIZE[i]
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True


def mouseclick_handler(pos):
    global started, lives
    if not started:
        started = True
        lives = 3
        timer.start()
        soundtrack.rewind()
        soundtrack.play()


def keydown_handler(key):
    for i in KEY_DICT:
        if key == simplegui.KEY_MAP[i]:
            my_ship.inc_angle_vel(KEY_DICT[i])
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust()
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()


def keyup_handler(key):
    for i in KEY_DICT:
        if key == simplegui.KEY_MAP[i]:
            my_ship.dec_angle_vel(KEY_DICT[i])
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust()


def draw(canvas):
    global time, score, lives, started, rock_group, rock_modifier
    if lives == 0:
        started = False
        rock_group = set()
        timer.stop()
        rock_modifier = 0
        score = 0
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size,
                      (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size,
                      (wtime + WIDTH / 2, HEIGHT / 2),
                      (WIDTH / 10, HEIGHT / 10))

    # draw ship
    my_ship.draw(canvas)

    # update ship and sprites
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    if group_collide(rock_group, my_ship):
        lives -= 1
    score += group_group_collide(rock_group, missile_group)

    # lives and score
    canvas.draw_text("Lives: %d" % lives, [10, 40], 40, "Magenta", "sans-serif")
    canvas.draw_text("Score: %d" % score, [625, 40], 40, "Magenta",
                     "sans-serif")

    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          [WIDTH / 2, HEIGHT / 2])


# timer handler that spawns a rock
def rock_spawner():
    global rock_group, rock_modifier
    if len(rock_group) < 12:
        a_rock = Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)],
                        [(1 + 0.01 * rock_modifier) *
                         random.randrange(1, 100) / 100.0,
                         (1 + 0.01 * rock_modifier) *
                         random.randrange(1, 100) / 100.0],
                        random.randrange(365) / 12.56,
                        random.randrange(100) / 1000.0, asteroid_image,
                        asteroid_info)
        if dist(a_rock.get_position(), my_ship.get_position()) > 2 * (
                    a_rock.get_radius() + my_ship.get_radius()):
            rock_group.add(a_rock)
            rock_modifier += 1


# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(mouseclick_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
