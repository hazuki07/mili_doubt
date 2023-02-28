from difflib import IS_CHARACTER_JUNK
from operator import is_
from re import A, X
import random
import cards
import daifugo

from collections import namedtuple

"""
class Field(Deck):
    is_field: bool
    # //NOTE 場のカードを管理するオブジェクト、ディーラーが流れを管理する(is_field)
    # 一度fieldに移されてから

class Player(self):
    is_atk: bool
    is_turn: bool
    
    def __init__():
        self.hands = card.Deck(daifugo.Daifugo)
        # self.field =

    def bool_t(self):
        self.is_atk = True

    def bool_f(self):
        self.is_atk = False

    def dec_atk(self, atk : bool):
        if atk == True:
            self.is_atk = True
        else:
            self.is_atk = False

    def dec_atk(self, turn : bool):
        if turn == True:
            self.is_turn = True
        else:
            self.is_turn = False

    def prt_card(self):
        print("H:" if self.is_atk == True else "V:", end="")
        print(self.hands)

    # //TODO 毎ターン表示
    def prt_card();
        print("H_hand:" if is_atk=True else "V_hand:", end="")
        print(self.hands)

    def sel_card(self):
    # //TODO 
    # list = [0, 1, 2, ..., 6, ..., 10]
    # try, ...except "no index"
    return sel_opn: list

    def opn_card(self, sel_opn):
    # //TODO 
    # for i in sel_opn[::-1]:
        # open_card(~~, i)
    print Field
    
    def dec_dbt(self, detect):
    # //TODO　
    # detect is bool
    
    def sel_dbtcard(self, sel_dbt):
    # //TODO 
    # list = [0, 1, 2, ..., 6, ..., 13]
    # try, ...except "no index"
    return sel_dbt: list
    
    def opn_dbtcard():
    # todo  open_card()

# //TODO ディーラーでクラスで手配をプリントするか
class Dealer(Player):
    is_turn: bool

    def __init__(self):
        super().__init__()
        self.deck = 
        self.atk = 
        self.turn = 

    # hero's atk if x=0 else villan's atk
    def dec_atk(x):
    x = random.randint(0, 1)
    return x 

    # //NOTE mada jissou suruka wakaran
    def get_card(self, cards: Iterable[Card]):
        return self.append(cards.pop())

    
"""
