"""
Executive function: texas_referee
Input: a community hand in Texas Hold 'Em
Output: the best 5-card hand
Example: "Kh,Qh,Ah,9s,2c,Th,Jh" --> "Ah,Kh,Qh,Jh,Th"
Link: http://www.checkio.org/mission/texas-referee/
"""
from itertools import product, combinations
from string import digits


class Card(object):

    def __init__(self, card, suit_order=("s", "c", "d", "h")):
        self.card_dict = {}
        for i, (rank, suit) in enumerate(product(digits[2:] + "TJQKA",
                                                 suit_order)):
            self.card_dict["{}{}".format(rank, suit)] = i + 1
        self.card = card
        self.suit = card[1]
        self.rank = card[0]
        self.value = self.card_dict[card]

    def __eq__(self, other):
        return self.value == other.value

    def __le__(self, other):
        return self.value < other.value

    def __repr__(self):
        return self.card


class Hand(object):

    def __init__(self, *args):
        cards = list(args)
        cards.sort(key=lambda c: c.value, reverse=True)
        self.cards = tuple(cards)
        self.values = tuple(card.value for card in self.cards)
        self.ranks = tuple(card.rank for card in self.cards)
        self.suits = tuple(card.suit for card in self.cards)

    def __repr__(self):
        return str(self.cards)

    def score(self):
        return sum(self.values)

    def is_high_card(self):
        return self, self.score(), 1

    def is_straight(self):
        for i in range(1, 50, 4):
            ranges = [range(i + j, i + j + 4) for j in range(0, 18, 4)]
            iterator = product(*ranges)
            if self.values[::-1] in iterator:
                return self, self.score(), 5

    def is_flush(self):
        modulo = set(value % 4 for value in self.values)
        if len(modulo) == 1:
            return self, self.score(), 6

    def is_straight_flush(self):
        if self.is_straight() and self.is_flush():
            return self, self.score(), 9

    def is_4_kind(self):
        for i in range(1, 50, 4):
            if set(range(i, i + 4)).issubset(self.values):
                return self, self.score(), 8

    def is_3_kind(self):
        for i in range(1, 50, 4):
            for combination in combinations(range(i, i + 4), 3):
                if set(combination).issubset(self.values):
                    return self, self.score(), 4

    def is_pair(self):
        for i in range(1, 50, 4):
            for combination in combinations(range(i, i + 4), 2):
                if set(combination).issubset(self.values):
                    return self, self.score(), 2

    def is_2_pair_or_full_house(self, a, b, score):
        copy = list(self.values)
        ranging = range(1, 50, 4)
        for i in ranging:
            for combination in set(combinations(range(i, i + 4), a)):
                if set(combination).issubset(copy):
                    copy = [value for value in copy if value not in combination]
                    ranging.remove(i)
                    break
            else:
                return None
            break
        for i in ranging:
            for combination in set(combinations(range(i, i + 4), b)):
                if set(combination).issubset(copy):
                    return self, self.score(), score

    def is_2_pair(self):
        return self.is_2_pair_or_full_house(2, 2, 3)

    def is_full_house(self):
        return self.is_2_pair_or_full_house(3, 2, 7)

    def triples(self):
        return [self.is_straight_flush(), self.is_4_kind(),
                self.is_full_house(), self.is_flush(), self.is_straight(),
                self.is_3_kind(), self.is_2_pair(),
                self.is_pair(), self.is_high_card()]

    def get_best_triple(self):
        for triple in self.triples():
            if triple:
                return triple

    def get_card_string(self):
        return ",".join(str(card) for card in self.cards)


class Community(object):

    def __init__(self, card_str):
        self.cards = [Card(card) for card in card_str.split(",")]

    def get_hands(self):
        hand_list = []
        for combination in combinations(self.cards, 5):
            hand_list.append(Hand(*combination))
        return hand_list

    def get_best_hand(self):
        triple_list = [hand.get_best_triple() for hand in self.get_hands()]
        winning_hand_value = max(triple[2] for triple in triple_list)
        possible_winning_hands = [triple[:2] for triple in triple_list
                                  if triple[2] == winning_hand_value]
        winner = max(possible_winning_hands, key=lambda h: h[1])
        return winner[0].get_card_string()


def texas_referee(cards_str):
    x = Community(cards_str)
    return x.get_best_hand()
