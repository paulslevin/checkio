# Implementation of card game Blackjack
# template: http://www.codeskulptor.org/#examples-blackjack_template.py
# play online: http://www.codeskulptor.org/#user40_lYxRbmlEfL_0.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = "Hit or stand?"
score = 0
player_hand = []
dealer_hand = []
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
          '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        hand_string = "Hand contains"
        for card in self.hand:
            hand_string += " %s" % (str(card))

        return hand_string

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        ranks_list = []
        values_list = []
        for card in self.hand:
            ranks_list.append(card.rank)
            values_list.append(VALUES[card.rank])
        hand_value = sum(values_list)

        if not ('A' in ranks_list):
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value

    def draw(self, canvas, pos):
        count = 0
        for card in self.hand:
            card.draw(canvas, [pos[0] + (1.5 * count) * CARD_SIZE[0], pos[1]])
            count += 1


class Deck:
    def __init__(self):
        self.deck = [Card(x, y) for x in SUITS for y in RANKS]

    def shuffle(self):
        random.shuffle(self.deck)  # use random.shuffle()

    def deal_card(self):
        dealt_card = self.deck.pop()  # deal a card object from the deck
        return dealt_card

    def __str__(self):
        deck_string = "Deck contains"
        for card in self.deck:
            deck_string += " %s" % str(card)
        return deck_string


# define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, score
    deck = Deck()
    deck.shuffle()
    dealer_hand, player_hand = Hand(), Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    if in_play:
        outcome = "Why re-deal? Hit or stand?"
        score -= 1
    else:
        outcome = "Hit or stand?"
    in_play = True


def hit():
    global in_play, score, outcome, player_hand, deck
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            if player_hand.get_value() > 21:
                outcome = "You have busted. New deal?"
                score -= 1
                in_play = False


def stand():
    global in_play, score, outcome, player_hand, dealer_hand, deck
    if in_play and dealer_hand.get_value() < player_hand.get_value():
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if player_hand.get_value() <= dealer_hand.get_value() <= 21:
            outcome = "You have lost. New deal?"
            in_play = False
            score -= 1
        else:
            outcome = "You have won! New deal?"
            in_play = False
            score += 1

    elif in_play and dealer_hand.get_value() >= player_hand.get_value():
        outcome = "You have lost. New deal?"
        in_play = False
        score -= 1


def draw(canvas):
    global player_hand, dealer_hand
    canvas.draw_text("BLACKJACK", [30, 50], 40, "Red", "monospace")
    canvas.draw_text(outcome, [30, 100], 40, "White")
    canvas.draw_text("SCORE: %d" % score, [380, 50], 40, "Red", "monospace")
    canvas.draw_text("Dealer:", [30, 200], 40, "Pink", "sans-serif")
    canvas.draw_text("Player:", [30, 400], 40, "Pink", "sans-serif")
    player_hand.draw(canvas, [50, 450])
    dealer_hand.draw(canvas, [50, 250])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [50 + CARD_BACK_CENTER[0], 250 + CARD_BACK_CENTER[1]],
                          CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
