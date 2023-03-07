from difflib import IS_CHARACTER_JUNK
from operator import is_
from re import A, X
import random
from tkinter import N
import cards
import daifugo

from collections import namedtuple

class Field(cards.Deck):
    is_field: bool
    # //NOTE 場のカードを管理するオブジェクト、ディーラーが流れを管理する(is_field)
    # 一度fieldに移されてから

class Player():
    is_atk: bool
    is_turn: bool
    is_dbt: bool

    def __init__(self):
        self.field = cards.Deck(daifugo.Daifugo)
        self.hands = cards.Deck(daifugo.Daifugo)
        self.sel_opn = 0
        self.sel_dbt = 0

    def bool_t(self):
        self.is_atk = True

    def bool_f(self):
        self.is_atk = False

    def dec_atk(self, atk : bool):
        if atk == True:
            self.is_atk = True
        else:
            self.is_atk = False

    def dec_turn(self, turn : bool):
        if turn == True:
            self.is_turn = True
        else:
            self.is_turn = False

    # //TODO 毎ターン表示
    def prt_card(self):
        if self.is_turn == True:
            print("MyTurn.")
        print("H_hand:" if self.is_atk == True else "V_hand:", end="")
        print(self.hands)

    def sel_card(self):
        print('空白区切りでリスト番号を選択してください。')
        self.sel_opn = list(map(int, input().split()))
        return self.sel_opn
        #print(self.inp1)
        # try, ...except "no index"

    def opn_card(self):
        for i in self.sel_opn[::-1]:
            self.field.open_card(self.hands, i)
        print(self.field)

    def dec_dbt(self, dbt : bool):
        if dbt == True:
            self.is_dbt = True
        else:
            self.is_dbt = False

    def sel_dbtcard(self):
        print('空白区切りでリスト番号を選択してください。')
        self.sel_dbt = list(map(int, input().split()))
        return self.sel_dbt
        #print(self.sel_dbt)
        # try, ...except "no index"
        # list = [0, 1, 2, ..., 6, ..., 13]

    def opn_dbtcard(self):
        for i in self.sel_opn[::-1]:
            self.field.open_card(self.hands, i)
        print(self.field)

# //TODO ディーラーでクラスで手配をプリントするか
class Dealer(Player):
    is_turn: bool
    # atk: int

    def __init__(self):
        super().__init__()
        self.deck = bool
        self.atk = bool
        self.turn = bool

    # hero's atk if x=0 else villan's atk
    def dec_atk(self):
        atk = random.randint(0, 1)
        if atk == 0:
            print("your atk turn.")
            self.atk = True
        else:
            print("Villan's atk.")
            self.atk = False

    #   NOTE mada jissou suruka wakaran
    # def get_card(self, cards: Iterable[Card]):
    #     return self.append(cards.pop())

a = Player()
a.bool_f()
a.is_atk = True
a.is_turn = True
a.prt_card()

print("test")
b = Player()
b.dec_atk(False)
b.dec_turn(False)
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

a.sel_card()
a.opn_card()