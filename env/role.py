import random

from env import cards
from env import rule

import logging
import copy

from collections import namedtuple

class Player():
    is_play: bool
    reverse: bool
    declare_dbt: bool
    declare_burst: bool
    sel_card: bool
    play_burst: bool
    # 0...stairs, 2...pair, 3...stairs

    def __init__(self):
        self.field = cards.Deck(rule.Milliondoubt)
        self.hands = cards.Deck(rule.Hands_sequence)
        self.sel_opn = []
        self.sel_dbt = 0
        self.is_dbt = False
        self.type = "Player"
        self.name = "Player"
        self.dict = cards.Deck(rule.Hands_sequence)
        self.dict.full()

        
    def __str__(self):
        return f"Player({self.name})"

    def bool_t(self):
        self.is_atk = True

    def bool_f(self):
        self.is_atk = False

    def prt_card(self):
        # if self.is_turn == True:
        self.hands.sort()
        print(self.hands)

    def sel_card(self, action=None):
        while True:
            try:
                print('空白区切りでリスト番号を選択してください。パスは未選択。')
                user_input = input()
                if user_input == "":
                    return []  # パスの場合
                self.sel_opn = list(map(int, user_input.split()))
                # 入力されたインデックスが手札の範囲内にあるか確認
                if all(0 <= index < len(self.hands) for index in self.sel_opn):
                    return self.sel_opn
                else:
                    raise ValueError("選択されたインデックスが手札の範囲外です。")
            except ValueError as e:
                print(f"エラー: {e} 再度入力してください。")

    def opn_card(self):
        for i in self.sel_opn[::-1]:
            self.field.open_card(self.hands, i)
        self.field.sort()
        print(self.field)

    def sel_card_back(self, action=None):
        while True:
            try:
                print('裏出し：空白区切りでリスト番号を選択してください。空行で確定。')
                user_input = input()
                if user_input == "":
                    break
                user_input = list(map(int, user_input.split()))
                # 入力されたインデックスが手札の範囲内にあるか確認
                if all(0 <= index < len(self.field) for index in user_input):
                    for i in user_input[::1]:
                        self.field[i].flip()
                        self.field.sort()
                    print(self.field)
                    return self.field
                else:
                    raise ValueError("選択されたインデックスが手札の範囲外です。")
            except ValueError as e:
                print(f"エラー: {e} 再度入力してください。")

    def return_cards(self):
        for i in reversed(range(len(self.field))):
            self.field[i]._face_up()
        for i in range(len(self.field)):
            self.hands.get_card(self.field)
        self.hands.sort()

    def dec_dbt(self):
        while True:

            choice = input("ダウトの宣言フェーズです。 'doubt' or 'not' [d/N]: ").lower()
            if choice in ['d', 'do', 'dou', 'doub', 'doubt']:
                self.is_dbt = True
                return False
            elif choice in ['n', 'no', 'not']:
                self.is_dbt = False
                return False

    def sel_dbtcard(self, field: cards.Deck, action=None):
        for i in range(len(field))[::-1]:
            field[i]._face_up()
        print(f"Field: {field}")
        while True:
            # flag ==> env
            try:
                print('空白区切りでリスト番号を選択してください。スルーは未選択。')
                user_input = input()
                if user_input == "":
                    return []
                user_input = list(map(int, user_input.split()))
                # 入力されたインデックスが手札の範囲内にあるか確認し、すべてのインデックスが一意であることを確認
                if all(0 <= index < len(field) for index in user_input) and len(user_input) == len(set(user_input)):
                    print(user_input)
                    user_input.sort()
                    # print(field)
                    self.sel_opn = user_input
                    return self.sel_opn
                else:
                    raise ValueError("選択されたインデックスが手札の範囲外です。")
            except ValueError as e:
                print(f"エラー: {e} 再度入力してください。")



    def opn_dbtcard(self, field: cards.Deck):
        for i in sorted(self.sel_opn, reverse=True):
            print(f"pop: {i}")
            card = field.pop(i)
            self.field.append(card)
        self.field.sort()
        print(self.field)

    def dec_burst(self):
        while True:

            choice = input("バーストの宣言をしますか？ 'burst' or 'not' [b/N]: ").lower()
            if choice in ['b', 'bu', 'bur', 'burs', 'burst']:
                self.play_burst = True

                break
            elif choice in ['n', 'no', 'not']:
                self.play_burst = False

                break


class CPUPlayer(Player):
    def __init__(self):
        super().__init__()
        self.type = "CPU"
        self.name = "CPUPlayer"
        
    def __str__(self):
        return f"CPUPlayer({self.name})"

    def sel_card(self, card_count: int, action=None):
        # self.sel_opn = list(range(1))
        
        # 前回のカード枚数に合わせてカードを選択
        if card_count == 0:
            self.sel_opn = list(range(random.randint(1, min(4, len(self.hands)))))
        
        else:
            if card_count <= len(self.hands):
                self.sel_opn = list(range(card_count))
            else:
                return []

        for i in self.sel_opn[::-1]:
            self.field.open_card(self.hands, i)
            self.field.sort()
        return self.sel_opn


    def sel_card_back(self):
        if self.sel_opn:
            for i in self.sel_opn:
                #TODO
                pass
                # self.field[i].flip()
            logging.info(self.field)
            return self.field
        else:
            return []  # パス


    def dec_dbt(self, action=None):
        doubt_probability = 0.8  # ダウトする確率
        self.is_dbt = random.random() < doubt_probability
        
    def sel_dbtcard(self, field: cards.Deck, action=None):
        input_list = []
        for i in reversed(range(len(field))):
            field[i]._face_up()
        print(f"Field: {field}")
        if len(field) > 1:
            num_cards_to_select = random.randint(1, len(field) - 1)
        else:
            num_cards_to_select = 1
        input_list = random.sample(range(len(field)), num_cards_to_select)
        input_list.sort()
        
        self.sel_opn = input_list

        return self.sel_opn

    def dec_burst(self):
        self.play_burst = True


class MLPlayer(CPUPlayer):
    def __init__(self, model=None):
        super().__init__()
        self.type = "ML"
        # self.model = model  # 機械学習モデルをインスタンス変数として保存
        self.name = "MLPlayer"
        
    def __str__(self):
        return f"MLPlayer({self.name})"

    def sel_card(self, index):
        # flag ==> env
        # self.play = True

        if index == []:
            return []  # パスの場合
        
        # print(f"index1: {index}") # NOTE debug
        # 入力されたインデックスが手札の範囲内にあるか確認
        if all(0 <= idx < len(self.hands) for idx in index):
            # self.play = False
            self.sel_opn = index
            return self.sel_opn
        else:
            # raise ValueError("選択されたインデックスが手札の範囲外です。")
            print("index1 is out of range.")

    # def opn_card(self):
    #     # TODO fix BUG
    #     for i in self.sel_opn[::-1]:
    #         self.field.open_card(self.hands, i)
    #     self.field.sort()
    #     print(f"opn_card{self.field}")

    
    def sel_card_back(self, index):
        # flag ==> env
        # self.reverse = True
        # print(f"ind2{index}") # NOTE debug

        if index == []:
            return []
        
        # print(f"field:{self.field}")
        # print(f"index2: {index}") # NOTE debug
        # 入力されたインデックスが手札の範囲内にあるか確認
        if all(0 <= idx < len(self.field) for idx in index):
            for i in index[::1]:
                self.field[i].flip()
                self.field.sort()
            print(f"play_cards:{self.field}")
            # self.reverse = False
            return self.field
        else:
            # raise ValueError("選択されたインデックスが手札の範囲外です。")
            print("index2 is out of range.")


    def dec_dbt(self, bool):
        self.is_dbt = bool

# TODO update
    def sel_dbtcard(self, field: cards.Deck, index):
        print(f"index1: {index}")
        for i in range(len(field))[::-1]:
            field[i]._face_up()
        print(f"Field: {field}")

        if index == []:
            return []  # パスの場合

        # print(f"index1: {index}") # NOTE debug
        # 入力されたインデックスが手札の範囲内にあるか確認
        if all(0 <= idx < len(field)  for idx in index):
            # self.play = False
            self.sel_opn = index
            return self.sel_opn
        else:
            # raise ValueError("選択されたインデックスが手札の範囲外です。")
            print("index1 is out of range.")


    def dec_burst(self, bool):
        self.play_burst = bool #True

if __name__ == '__main__' :
    a = MLPlayer()
    # b = CPUPlayer()
    # A = cards.Deck()
    # A.full()
    # B = copy.deepcopy(A)
    # print(B)
    # print(type(B)=="cards.Deck")
    # c = Player()
    # d = Player()
    # print(A[7])
    # print(f"print A[7] = {A[7].face_up}")
    # c.field.append(copy.copy(A[7]))
    # d.field.append(copy.copy(A[10]))
    
    # __face_up = True
    # c.field[-1]._face_up()
    # d.field[-1]._face_up()
    
    # a.bool_f()
    # # a.is_atk = True
    # # a.is_turn = True
    # a.prt_card()

    # print("test")
    # b.dec_atk(False)
    # b.dec_turn(False)
    # b.prt_card()
    # a.full()
    # print(a)
    x = cards.Deck(rule.Milliondoubt)
    x.full()
    x.shuffle()
    for i in range(7):
        a.hands.get_card(x)
        # b.hands.get_card(x)
    print(x)
    a.hands.sort()
    # b.hands.sort()
    a.prt_card()
    # b.prt_card()

    # a.sel_card()
    # a.opn_card()
    # a.sel_card_back()
    # b.sel_card(0)
    # b.sel_card_back()
    # print(b.field)
    # print(b.hands)
    # print(c.field, d.field)
    # print(c.dict[46].number == c.field[0].number)
    # print(c.dict[20].number)
    # print(c.dict[7].number, c.dict[20].number, c.dict[33].number, c.dict[46].number)
    # print(int(c.dict[46].number) == 8)
    # print(c.dict[20].number == c.dict[33].number)