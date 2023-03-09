from difflib import IS_CHARACTER_JUNK
from operator import is_
from re import A, X
import random
import cards
import milliondoubt
import role

from collections import namedtuple

class Game:
    def __init__(self):
        # role.py
        self.player0 = role.Player()
        self.player1 = role.Player()
        # self.dealer = role.Dealer()

    def judge_win(self, player0, player1):

    def main(self):
        deck = cards.Deck()

if __name__ == '__main__' :
    game = Game()
    game.main