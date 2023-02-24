from re import X
import cards

from collections import namedtuple

class strength(cards.Card):
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

deck = cards.Deck(strength)
deck.full()
print(deck)
#[sA~,dA~,cA~,hA~,jo,jo]
deck.shuffle()
print(deck)
deck.sort(key=lambda x: (x.suit, x.number))
print(deck)
card0 = deck.draw()
card1 = deck.draw()
print(card0.suit)
print(card0.number)
print(str(card0) + " > " + str(card1))
print(card0 > card1)
print(str(card1) + " < " + str(card0))
print(card0.reverse > card1.reverse)
#print(card0)
"""
class cards_role(strength):
    def 
"""

H_hand = cards.Deck()
V_hand = cards.Deck()
field = cards.Deck()