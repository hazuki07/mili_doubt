from difflib import IS_CHARACTER_JUNK
from operator import is_
from re import A, X
import random
import cards
import daifugo

from collections import namedtuple

class Test():
    is_atk = bool
    # hands = [0, 1, 2, 3, 4, 5, 6]

    def __init__(self):
        # super().__init__()
        self.hands = cards.Deck(daifugo.Daifugo)

    def bool_t(self):
        self.is_atk = True

    def bool_f(self):
        self.is_atk = False

    def dec_atk(self, a:bool):
        if a == True:
            self.is_atk = True
        else:
            self.is_atk = False

    def prt_card(self):
        print("H_hand:" if self.is_atk == True else "V_hand:", end="")
        print(self.hands)
        # //TODO　print=> 9field

if __name__ == '__main__':
    a = Test()
    a.bool_f()
    a.is_atk = True
    a.prt_card()

    b = Test()
    b.dec_atk(False)
    b.prt_card()
    # a.full()
    # print(a)
    x = cards.Deck(daifugo.Daifugo)
    x.full()
    x.shuffle()
    for i in range(7):
        a.hands.get_card(x)
        b.hands.get_card(x)
    print(x)
    a.prt_card()
    b.prt_card()