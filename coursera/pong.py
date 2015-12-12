# Implementation of classic arcade game Pong
# use W, S, UP, DOWN to play
# template: http://www.codeskulptor.org/#examples-pong_template.py
# play online: http://www.codeskulptor.org/#user40_oAVn2yjs7G_0.py

import simplegui
import random

# constants
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
MIDPOINT = [WIDTH / 2, HEIGHT / 2]
PAD_SPEED = 3
SCORE_SIZE = 50
SCORE1_POS = [MIDPOINT[0] - 85, 60]
SCORE2_POS = [MIDPOINT[0] + 60, 60]
LEFT = False
RIGHT = True

# initialize globals

ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_pos_x = HALF_PAD_WIDTH
paddle1_pos_y = (HEIGHT - PAD_HEIGHT) / 2
paddle2_pos_x = WIDTH - HALF_PAD_WIDTH
paddle2_pos_y = (HEIGHT - PAD_HEIGHT) / 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0


# if direction is RIGHT, the ball's velocity is upper right, else upper left


def spawn_ball(direction):
    """Sets the initial position and velocity of the ball"""

    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel[0] = random.randrange(120, 240) / 60
    ball_vel[1] = -random.randrange(60, 180) / 60
    if direction == "LEFT":
        ball_vel[0] = -ball_vel[0]


# define event handlers

def new_game():
    global paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1, score2 = 0, 0
    spawn_ball("RIGHT")


def draw(canvas):
    global score1, score2
    global paddle1_pos_x, paddle1_pos_y, paddle2_pos_x, paddle2_pos_y
    global ball_pos, ball_vel, paddle1_vel, paddle2_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1,
                     "White")

    # update ball

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if ball_pos[0] <= PAD_WIDTH and not (
                    paddle1_pos_y <= ball_pos[1] <= paddle1_pos_y + PAD_HEIGHT):
        score2 += 1
        spawn_ball("RIGHT")
    elif ball_pos[0] <= PAD_WIDTH and paddle1_pos_y <= ball_pos[1] \
            <= paddle1_pos_y + PAD_HEIGHT:
        ball_vel[0] *= - 1.1
    elif ball_pos[0] >= WIDTH - PAD_WIDTH and not (
                    paddle2_pos_y <= ball_pos[1] <= paddle2_pos_y + PAD_HEIGHT):
        score1 += 1
        spawn_ball("LEFT")
    elif ball_pos[0] >= WIDTH - PAD_WIDTH and paddle2_pos_y <= \
            ball_pos[1] <= paddle2_pos_y + PAD_HEIGHT:
        ball_vel[0] *= - 1.1
    else:
        if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT:
            ball_vel[1] *= -1

    # draw ball

    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")

    # update paddle's vertical position, keep paddle on the screen

    if paddle1_pos_y <= 0 and paddle1_vel == -PAD_SPEED:
        pass
    elif paddle1_pos_y >= HEIGHT - PAD_HEIGHT and paddle1_vel == PAD_SPEED:
        pass
    else:
        paddle1_pos_y += paddle1_vel
    if paddle2_pos_y <= 0 and paddle2_vel == -PAD_SPEED:
        pass
    elif paddle2_pos_y >= HEIGHT - PAD_HEIGHT and paddle2_vel == PAD_SPEED:
        pass
    else:
        paddle2_pos_y += paddle2_vel

    # draw paddles

    canvas.draw_line([paddle1_pos_x, paddle1_pos_y],
                     [paddle1_pos_x, paddle1_pos_y + PAD_HEIGHT], PAD_WIDTH,
                     "White")

    canvas.draw_line([paddle2_pos_x, paddle2_pos_y],
                     [paddle2_pos_x, paddle2_pos_y + PAD_HEIGHT], PAD_WIDTH,
                     "White")

    # draw scores

    canvas.draw_text(str(score1), SCORE1_POS, SCORE_SIZE, "White")
    canvas.draw_text(str(score2), SCORE2_POS, SCORE_SIZE, "White")


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["W"] or key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel = -PAD_SPEED
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel = PAD_SPEED
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PAD_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_SPEED


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
