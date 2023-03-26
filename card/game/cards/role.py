import random
from tkinter import N
import cards
import rule

from collections import namedtuple

class Player():
    # is_atk: bool
    # is_turn: bool
    is_dbt: bool

    def __init__(self):
        self.field = cards.Deck(rule.Milliondoubt)
        self.hands = cards.Deck(rule.Hands_sequence)
        self.sel_opn = []
        self.sel_dbt = 0

    def bool_t(self):
        self.is_atk = True

    def bool_f(self):
        self.is_atk = False

    # def dec_atk(self, atk : bool):
    #     if atk == True:
    #         self.is_atk = True
    #     else:
    #         self.is_atk = False

    # def dec_turn(self, turn : bool):
    #     if turn == True:
    #         self.is_turn = True
    #     else:
    #         self.is_turn = False

    # //TODO 毎ターン表示
    def prt_card(self):
        # if self.is_turn == True:
        #     print("MyTurn.")
        # print("H_hand:" if self.is_atk == True else "V_hand:", end="")
        print(self.hands)

    def sel_card(self, prev_card_count=None):
        while True:
            try:
                print('空白区切りでリスト番号を選択してください。パスは未選択。')
                user_input = input()
                if user_input == "":
                    return []  # パスの場合
                self.sel_opn = list(map(int, user_input.split()))
                # 入力されたインデックスが手札の範囲内にあるか確認
                if all(0 <= index < len(self.hands) for index in self.sel_opn):
                    if prev_card_count is not None and len(self.sel_opn) != prev_card_count:
                        raise ValueError("出すカードの枚数が前回と同じでなければなりません。")
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

    def sel_card_back(self):
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

    def ret_card(self):
        for i in self.field:
            self.hands.get_card(self.field)
        self.hands.sort()

    def dec_dbt(self):
        while True:
            self.is_dbt = False
            choice = input("Please doubt's respond with 'doubt' or 'not' [d/N]: ").lower()
            if choice in ['d', 'do', 'dou', 'doub', 'doubt']:
                self.is_dbt = True
                return False
            elif choice in ['n', 'no', 'not']:
                self.is_dbt = False
                return False

    def sel_dbtcard(self):
        print('空白区切りでリスト番号を選択してください。skipは未選択。')
        self.sel_dbt = list(map(int, input().split()))
        return self.sel_dbt
        #print(self.sel_dbt)
        # try, ...except "no index"
        # list = [0, 1, 2, ..., 6, ..., 13]

    def opn_dbtcard(self,field: cards.Deck):
        for i in self.sel_opn[::-1]:
            self.field.open_card(field, i)
        self.field.sort()
        print(self.field)

# TODO update
class CPUPlayer(Player):
    def sel_card(self, prev_card_count=None, field_top_card=None):
        self.hands.sort()
        if prev_card_count is not None:
            # 前回のカード枚数に合わせてカードを選択
            if prev_card_count <= len(self.hands):
                selected_indices = list(range(prev_card_count))
            else:
                return []  # パス
        else:
            # 自分の手番であれば、複数枚出しにくい手を選択
            selected_indices = [0]  # 最も小さいカードを選択

        # フィールドのカードより小さいカードは出せないルールの適用
        if field_top_card is not None:
            while self.hands[selected_indices[0]] <= field_top_card:
                if len(selected_indices) < len(self.hands):
                    selected_indices[0] += 1
                else:
                    return []  # パス

        self.sel_opn = selected_indices
        return selected_indices

    def dec_dbt(self):
        doubt_probability = 0.2  # ダウトする確率
        self.is_dbt = random.random() < doubt_probability

class MLPlayer(CPUPlayer):
    def __init__(self, model):
        super().__init__()
        self.model = model  # 機械学習モデルをインスタンス変数として保存

    def sel_card(self, prev_card_count=None):
        # 機械学習モデルを使用したカード選択ロジック
        pass

    def dec_dbt(self):
        # 機械学習モデルを使用した疑いのロジック
        pass
    

if __name__ == '__main__' :
    a = Player()
    # a.dec_atk(False)

    a = Player()
    a.bool_f()
    # a.is_atk = True
    # a.is_turn = True
    a.prt_card()

    print("test")
    b = Player()
    # b.dec_atk(False)
    # b.dec_turn(False)
    b.prt_card()
    # a.full()
    # print(a)
    x = cards.Deck(rule.Milliondoubt)
    x.full()
    x.shuffle()
    for i in range(7):
        a.hands.get_card(x)
        b.hands.get_card(x)
    print(x)
    a.hands.sort()
    b.hands.sort()
    a.prt_card()
    b.prt_card()

    a.sel_card()
    a.opn_card()
    a.sel_card_back()