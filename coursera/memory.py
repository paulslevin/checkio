# Implementation of card game Memory
# template: http://www.codeskulptor.org/#examples-memory_template.py
# play online: http://www.codeskulptor.org/#user40_cyNKn1PDQX_13.py

import simplegui
import random

# global constants/variables
card_list_1 = range(0, 8)
card_list_2 = range(0, 8)
cards = card_list_1 + card_list_2
exposed = [False for _ in range(16)]
state = 0
clicked_card_1 = -1
clicked_card_2 = -2
counter = 0


# helper function to initialize globals
def new_game():
    global counter, clicked_card_1, clicked_card_2, exposed, cards, exposed
    random.shuffle(cards)
    counter = 0
    clicked_card_1 = -1
    clicked_card_1 = -2
    exposed = [False for _ in range(16)]
    label.set_text("Turns = %d" % counter)


# define event handlers
def mouseclick(pos):
    global exposed, state, clicked_card_1, clicked_card_2, cards, counter
    if state == 0:
        for card_index in range(len(cards)):
            if card_index == pos[0] // 50:
                exposed[card_index] = True
                clicked_card_1 = card_index
                state = 1

    elif state == 1:
        counter += 1
        label.set_text("Turns = %d" % counter)
        if not (exposed[pos[0] // 50]):
            for card_index in range(len(cards)):
                if card_index == pos[0] // 50 and not (exposed[card_index]):
                    exposed[card_index] = True
                    clicked_card_2 = card_index
                    state = 2
    elif state == 2:
        if not (exposed[pos[0] // 50]):
            if not (cards[clicked_card_1] == cards[clicked_card_2]):
                exposed[clicked_card_1] = False
                exposed[clicked_card_2] = False
            for card_index in range(len(cards)):
                if card_index == pos[0] // 50 and not (exposed[card_index]):
                    exposed[card_index] = True
                    clicked_card_1 = card_index
                    state = 1


# cards are logically 50x100 pixels in size
def draw(canvas):
    for card_index in range(len(cards)):
        canvas.draw_text(str(cards[card_index]),
                         [50 * card_index + 15, 60], 40, "White")
    for card_index in range(len(cards)):
        if not exposed[card_index]:
            canvas.draw_polygon([[50 * card_index, 0],
                                 [50 * (card_index + 1), 0],
                                 [50 * (card_index + 1), 100],
                                 [50 * card_index, 100]], 5, "Grey", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
