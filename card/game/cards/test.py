from re import X
import cards

from collections import namedtuple

deck = cards.Deck(cards.DaifugoCard)
deck.full()
print(deck)
#[sA~,dA~,cA~,hA~,jo,jo]
deck.shuffle()
print(deck)
card0 = deck.draw()
card1 = deck.draw()
print(card0, card1, card0 > card1)
#print(card0)

H_hand = cards.Deck()
V_hand = cards.Deck()
field = cards.Deck()

"""
# separate cards
for i in range(7):
    H_hand.get_card(deck)
    V_hand.get_card(deck)
    # seiretsu
"""

"""field_open
hands = [H_hand, V_hand]
rep = []
for i in rep:
    field.open_card(hands(0), rep(i))
"""

"""debug_hand
print(H_hand)
print(V_hand)
print(len(deck))
print(field)
"""
