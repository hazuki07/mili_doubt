import random
import cards

from collections import namedtuple
from typing import Iterable, NamedTuple, Optional, Type

# @property
INITIAL_HAND_SIZE = 7

class Milliondoubt(cards.Card):
    revolution_flag = False

    @property
    def _strength(self):
        if self.is_joker:
            return 13
        return ((int(self.number) - 3) % 13)

    @classmethod
    def tgl_revolution(cls):
        cls.revolution_flag = not cls.revolution_flag

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            if self.__class__.revolution_flag:
                return self._strength < other._strength
            else:
                return self._strength > other._strength
        raise NotImplementedError

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            if self.__class__.revolution_flag:
                return self._strength <= other._strength
            else:
                return self._strength >= other._strength
        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            if self.__class__.revolution_flag:
                return self._strength > other._strength
            else:
                return self._strength < other._strength
        raise NotImplementedError

    def __le__(self, other):
        if isinstance(other, self.__class__):
            if self.__class__.revolution_flag:
                return self._strength >= other._strength
            else:
                return self._strength <= other._strength
        raise NotImplementedError


class Hands_sequence(cards.Card):
        @property
        def _strength(self):
            if self.is_joker:
                return 13
            return (int(self.number) - 3) % 13

        def __gt__(self, other):
            if isinstance(other, self.__class__):
                return self._strength > other._strength
            raise NotImplementedError

        def __ge__(self, other):
            if isinstance(other, self.__class__):
                return self._strength >= other._strength
            raise NotImplementedError

        def __lt__(self, other):
            if isinstance(other, self.__class__):
                return self._strength < other._strength
            raise NotImplementedError

        def __le__(self, other):
            if isinstance(other, self.__class__):
                return self._strength <= other._strength
            raise NotImplementedError
    

if __name__ == '__main__':
    deck = cards.Deck(Milliondoubt)
    # deck = PreField()
    deck.full()
    # print(deck)
    deck.shuffle()
    card0 = deck.draw()
    card1 = deck.draw()
    # print(card0.suit)
    # print(card0.number)
    print(card0.suit)
    print(str(card0) + " > " + str(card1))
    print(card0 > card1)
    print(str(card0) + " > " + str(card1))
    deck.toggle_revolution()
    # print(deck.reverse_flag)
    print(card0 > card1)
    # deck.reverse()
    # print(card0 > card1)
    # print(card0.reverse > card1.reverse)
    print(len(deck))

    # # deck[0].flip()
    # print(deck)
    # deck.shuffle()
    deck.sort()
    print(deck)
    # deck.reverse()
    # deck.sort()
    # # deck[0].flip()
    # print(deck)
    # deck[0].test()
