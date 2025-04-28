import random
import json


class Deck:
    def __init__(self, cards_file):
        with open(cards_file, "r") as file:
            self.cards = json.load(file)
        self.discarded = []
        self.hand = []

    def draw_hand(self):
        self.hand = random.sample(self.cards, 4)

    def discard_card(self, card):
        self.hand.remove(card)
        self.discarded.append(card)

    def reshuffle(self):
        self.cards.extend(self.discarded)
        self.discarded = []
        random.shuffle(self.cards)
