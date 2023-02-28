from difflib import IS_CHARACTER_JUNK
from operator import is_
from re import A, X
import random
import cards

from collections import namedtuple

class Daifugo(cards.Card):
    @property
    def _strength(self):
        if self.is_joker:
            return 13
        return (int(self.number) - 3) % 13

    @property
    def reverse(self):
        return 13 - self._strength if self._strength != 13 else 13

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self._strength < other._strength
        raise NotImplemented

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self._strength <= other._strength
        raise NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self._strength > other._strength
        raise NotImplemented

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self._strength >= other._strength
        raise NotImplemented


if '__name__' == '__main__':
    deck = cards.Deck(Daifugo)
    deck.full()
    print(deck)
    #[sA~,dA~,cA~,hA~,jo,jo]
    deck.shuffle()
    #print(deck)
    #print(card0, card1, card0 < card1)
    print(deck)

    hand0 = cards.Deck(Daifugo)
    hand1 = cards.Deck(Daifugo)
    #field = cards.Deck()

    # separate cards
    for i in range(7):
        hand0.get_card(deck)
        hand1.get_card(deck)
        # seiretsu

    #debug_hand
    print(hand0)
    print(hand1)
    #print(len(deck))
