from enum import Enum
from importlib.util import set_loader
from multiprocessing.util import is_abstract_socket_namespace
from operator import truediv
import random
import turtle
from typing import Iterable, NamedTuple, Optional, Type


# ***********************************************************
#  Suit & Number & Joker Enum
# ***********************************************************
class SuitProperty(NamedTuple):
    str: str
    value: int
    is_black: bool


class Suit(Enum):
    S = SuitProperty(str="♠", value=0, is_black=True)
    H = SuitProperty(str="♡", value=1, is_black=False)
    D = SuitProperty(str="♢", value=2, is_black=False)
    C = SuitProperty(str="♣", value=3, is_black=True)

    def __str__(self):
        return self.value.str

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

    def __int__(self):
        return self.value.value

    @property
    def is_black(self):
        return self.value.is_black

    @property
    def is_red(self):
        return not self.value.is_black

    def __gt__(self, other):
        """Override it at a sub-class if needed"""
        if isinstance(other, self.__class__):
            return int(self) < int(other)
        raise NotImplemented

    def __ge__(self, other):
        """Override it at a sub-class if needed"""
        if isinstance(other, self.__class__):
            return int(self) <= int(other)
        raise NotImplemented

    def __lt__(self, other):
        """Override it at a sub-class if needed"""
        if isinstance(other, self.__class__):
            return int(self) > int(other)
        raise NotImplemented

    def __le__(self, other):
        """Override it at a sub-class if needed"""
        if isinstance(other, self.__class__):
            return int(self) >= int(other)
        raise NotImplemented

class NumberProperty(NamedTuple):
    str: str
    value: int
    is_pip: bool
    is_face: bool
    is_card: bool

class Number(Enum):
    _A = NumberProperty(str="A", value=1, is_pip=False, is_face=False, is_card=False)
    _2 = NumberProperty(str="2", value=2, is_pip=True, is_face=False, is_card=False)
    _3 = NumberProperty(str="3", value=3, is_pip=True, is_face=False, is_card=False)
    _4 = NumberProperty(str="4", value=4, is_pip=True, is_face=False, is_card=False)
    _5 = NumberProperty(str="5", value=5, is_pip=True, is_face=False, is_card=False)
    _6 = NumberProperty(str="6", value=6, is_pip=True, is_face=False, is_card=False)
    _7 = NumberProperty(str="7", value=7, is_pip=True, is_face=False, is_card=False)
    _8 = NumberProperty(str="8", value=8, is_pip=True, is_face=False, is_card=True)
    _9 = NumberProperty(str="9", value=9, is_pip=True, is_face=False, is_card=False)
    _10 = NumberProperty(str="10", value=10, is_pip=True, is_face=False, is_card=False)
    _J = NumberProperty(str="J", value=11, is_pip=False, is_face=True, is_card=True,)
    _Q = NumberProperty(str="Q", value=12, is_pip=False, is_face=True, is_card=False)
    _K = NumberProperty(str="K", value=13, is_pip=False, is_face=True, is_card=False)

    def __str__(self):
        return self.value.str

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

    def __int__(self):
        return self.value.value

    @property
    def is_pip(self):
        return self.value.is_pip

    @property
    def is_face(self):
        return self.value.is_face

    @property
    def is_ace(self):
        return self is self.__class__._A

# sort実装の余地
    def __gt__(self, other):
        """Override it at a sub-class if needed"""
        if isinstance(other, self.__class__):
            return int(self) > int(other)
        raise NotImplementedError

    def __ge__(self, other):
        """Override it at a sub-class if needed"""
        if isinstance(other, self.__class__):
            return int(self) >= int(other)
        raise NotImplementedError

    def __lt__(self, other):
        """Override it at a sub-class if needed"""
        if isinstance(other, self.__class__):
            return int(self) < int(other)
        raise NotImplementedError

    def __le__(self, other):
        """Override it at a sub-class if needed"""
        if isinstance(other, self.__class__):
            return int(self) <= int(other)
        raise NotImplementedError


class JokerProperty(NamedTuple):
    str: str
    is_black: bool


class Joker(Enum):
    B = JokerProperty(str="Joker", is_black=True)
    R = JokerProperty(str="Joker", is_black=False)

    def __str__(self):
        return self.value.str

    # @property
    # def is_black(self):
    #     return self.value.is_black

    # @property
    # def is_red(self):
    #     return not self.value.is_black


# ***********************************************************
#  Card class
# ***********************************************************
class Card:
    def __init__(
            self,
            *,
            suit: Optional[Suit] = None,
            number: Optional[Number] = None,
            joker: Optional[Joker] = None,
            face_up: bool = True,
    ):
        if not ((suit is number is None and joker is not None)
                or (suit is not None and number is not None and joker is None)):
            raise ValueError("designate one and only one of (suit, number) or joker")
        self.__suit = suit
        self.__number = number
        self.__joker = joker
        self.__face_up = face_up

    @property
    def suit(self):
        return self.__suit

    @property
    def number(self):
        return self.__number

    @property
    def joker(self):
        return self.__joker

    def __str__(self):
        if self.__face_up:
            if self.is_joker:
                return str(self.joker)
            else:
                return str(self.suit) + str(self.number)
        else:
            return "B"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.suit)}, {repr(self.number)})"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.suit, self.number, self.joker) == (other.suit, other.number, other.joker)
        raise NotImplemented

    def flip(self):
        self.__face_up = not self.__face_up

    # --- properties coming from Joker ---
    @property
    def is_joker(self):
        return self.joker is not None

    @property
    def face_up(self):
        return self.__face_up

    # --- properties coming from Suit (and Joker) ---
    # @property
    # def is_black(self):
    #     if self.is_joker:
    #         return self.joker.is_black
    #     else:
    #         return self.suit.is_black

    # @property
    # def is_red(self):
    #     if self.is_joker:
    #         return self.joker.is_red
    #     else:
    #         return self.suit.is_red

    # --- properties coming from Number ---
    @property
    def is_pip(self):
        return not self.is_joker and self.number.is_pip

    @property
    def is_face(self):
        return not self.is_joker and self.number.is_face

    @property
    def is_ace(self):
        return not self.is_joker and self.number.is_ace


# ***********************************************************
#  Deck class
# ***********************************************************
class Deck(list):
    revolution_flag = False

    def __init__(self, cls_card: Type[Card] = Card):
        super().__init__()
        self.__cls_card = cls_card

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"

    def __repr__(self):
        def __str__(self):
            return "[" + ", ".join(repr(x) for x in self) + "]"

    def toggle_revolution(self):
        self.__class__.revolution_flag = not self.__class__.revolution_flag
        self.__cls_card.tgl_revolution()

    def full(self):
        super().__init__(
            self.__cls_card(suit=suit, number=number)
            for suit in Suit
            for number in Number
        )
        self.add_cards(self.__cls_card(joker=joker) for joker in Joker)

    def add_cards(self, cards: Iterable[Card]):
        self.extend(cards)

    def shuffle(self):
        random.shuffle(self)

    def draw(self):
        return self.pop()

    # draw in deck
    def get_card(self, cards: Iterable[Card]):
        return self.append(cards.pop())

    # raise card
    def open_card(self, cards: Iterable[Card], num: int):
        return self.append(cards.pop(num))
    
    # def reverse(self):
    #     self.reverse_flag = not self.reverse_flag  


if __name__ == '__main__':
    class DaifugoCard(Card):
        @property
        def _strength(self):
            if self.is_joker:
                return 13
            return (int(self.number) - 3) % 13

        def __gt__(self, other):
            if isinstance(other, self.__class__):
                return self._strength > other._strength
            raise NotImplemented

        def __ge__(self, other):
            if isinstance(other, self.__class__):
                return self._strength >= other._strength
            raise NotImplemented

        def __lt__(self, other):
            if isinstance(other, self.__class__):
                return self._strength < other._strength
            raise NotImplemented

        def __le__(self, other):
            if isinstance(other, self.__class__):
                return self._strength <= other._strength
            raise NotImplemented

    deck = Deck(DaifugoCard)
    deck.full()
    deck[0].flip()
    print(deck)
    deck.shuffle()
    deck.sort()
    print(deck)
    deck[0].flip()
    print(deck)