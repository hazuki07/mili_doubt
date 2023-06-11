from enum import Enum
from importlib.util import set_loader
from multiprocessing.util import is_abstract_socket_namespace
from operator import truediv
import random
import turtle
from typing import Iterable, NamedTuple, Optional, Type

# from tkinter import MULTIPLE, N
import logging
import copy

# ***********************************************************
#  Suit & Number & Joker Enum
# ***********************************************************
class SuitProperty(NamedTuple):
    str: str
    value: int

class Suit(Enum):
    S = SuitProperty(str="♠", value=0)
    H = SuitProperty(str="♡", value=1)
    D = SuitProperty(str="♢", value=2)
    C = SuitProperty(str="♣", value=3)

    def __str__(self):
        return self.value.str

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

    def __int__(self):
        return self.value.value

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

class Number(Enum):
    _A = NumberProperty(str="A", value=1, is_pip=False, is_face=False)
    _2 = NumberProperty(str="2", value=2, is_pip=True, is_face=False)
    _3 = NumberProperty(str="3", value=3, is_pip=True, is_face=False)
    _4 = NumberProperty(str="4", value=4, is_pip=True, is_face=False)
    _5 = NumberProperty(str="5", value=5, is_pip=True, is_face=False)
    _6 = NumberProperty(str="6", value=6, is_pip=True, is_face=False)
    _7 = NumberProperty(str="7", value=7, is_pip=True, is_face=False)
    _8 = NumberProperty(str="8", value=8, is_pip=True, is_face=False)
    _9 = NumberProperty(str="9", value=9, is_pip=True, is_face=False)
    _10 = NumberProperty(str="10", value=10, is_pip=True, is_face=False)
    _J = NumberProperty(str="J", value=11, is_pip=False, is_face=True)
    _Q = NumberProperty(str="Q", value=12, is_pip=False, is_face=True)
    _K = NumberProperty(str="K", value=13, is_pip=False, is_face=True)

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

class Joker(Enum):
    B = JokerProperty(str="Joker")
    R = JokerProperty(str="Joker")

    def __str__(self):
        return self.value.str


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
    def number(self) -> Optional[Number]:
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

    def _face_up(self):
        self.__face_up = True

    # --- properties coming from Joker ---
    @property
    def is_joker(self):
        return self.joker is not None

    @property
    def face_up(self):
        return self.__face_up

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


# @property
INITIAL_HAND_SIZE = 7

class Milliondoubt(Card):
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


class Hands_sequence(Card):
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

class Player():
    is_dbt: bool
    play_burst: bool


    def __init__(self):
        self.field = Deck(Milliondoubt)
        self.hands = Deck(Hands_sequence)
        self.sel_opn = []
        self.sel_dbt = 0
        self.type = "Player"
        self.name = "Player"
        self.dict = Deck(Hands_sequence)
        self.dict.full()

        
    def __str__(self):
        return f"Player({self.name})"

    def bool_t(self):
        self.is_atk = True

    def bool_f(self):
        self.is_atk = False

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

    def return_cards(self):
        for i in reversed(range(len(self.field))):
            self.field[i]._face_up()
        for i in range(len(self.field)):
            self.hands.get_card(self.field)
        self.hands.sort()

    def dec_dbt(self):
        while True:
            self.is_dbt = False
            choice = input("ダウトの宣言フェーズです。 'doubt' or 'not' [d/N]: ").lower()
            if choice in ['d', 'do', 'dou', 'doub', 'doubt']:
                self.is_dbt = True
                return False
            elif choice in ['n', 'no', 'not']:
                self.is_dbt = False
                return False

    def sel_dbtcard(self, field: Deck):
        for i in range(len(field))[::-1]:
            field[i]._face_up()
        print(f"Field: {field}")
        while True:
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



    def opn_dbtcard(self, field: Deck):
        for i in sorted(self.sel_opn, reverse=True):
            card = field.pop(i)
            # print(f"pop: {i}")
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

    def sel_card(self, card_count: int):
        # 前回のカード枚数に合わせてカードを選択
        if card_count == 0:
            self.sel_opn = list(range(random.randint(1, 4)))
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
                self.field[i].flip()
            logging.info(self.field)
            return self.field
        else:
            return []  # パス


    def dec_dbt(self):
        doubt_probability = 0.2  # ダウトする確率
        self.is_dbt = random.random() < doubt_probability
        
    def sel_dbtcard(self, field: Deck):
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

        return input_list

class MLPlayer(CPUPlayer):
    def __init__(self, model=None):
        super().__init__()
        self.type = "ML"
        self.model = model  # 機械学習モデルをインスタンス変数として保存
        self.name = "MLPlayer"
        
    def __str__(self):
        return f"MLPlayer({self.name})"

    def sel_card(self, prev_card_count=None):
        # 機械学習モデルを使用したカード選択ロジック
        pass

    def dec_dbt(self):
        # 機械学習モデルを使用した疑いのロジック
        pass

class Game():
    def __init__(self):
        self.player0 = Player()
        self.player1 = CPUPlayer()
        self.round_start = True
        self.round = 1
        self.phase = 1
        self.turn = False
        self.play = True
        self.is_bluff = False
        self.deck = Deck(Milliondoubt)
        self.deck.full()
        self.dict = Deck(Milliondoubt)
        self.dict.full()
        self.field = Deck(Milliondoubt)
        self.Graveyard = Deck(Milliondoubt)
        self.log_storage = Deck(Milliondoubt)
        self.topcard = Deck(Milliondoubt)
        self.topcard_length = 0
        self.topcard_number = 0
        self.topcard_suits = []
        self.is_multiple_flag = False
        self.is_stairs_flag = False
        self.is_eleven_back = False
        self.before_suits = []
        self.restricted_suits = []
        self.skip = False
        self.winner = None
        
    def deal_cards(self):
        self.deck.shuffle()
        for i in range(INITIAL_HAND_SIZE):
            self.player0.hands.get_card(self.deck)
            self.player1.hands.get_card(self.deck)
        self.player0.hands.sort()
        self.player1.hands.sort()
        logging.info('Initial hands have been dealt.')
        logging.info(f'Player 0 initial hand: {self.player0.hands}')
        logging.info(f'Player 1 initial hand: {self.player1.hands}')

    def decide_attacker(self):
        atk = random.randint(0, 1)
        if atk == 0:
            print("your atk turn.")
            self.turn = True
        else:
            print("Villan's atk.")
            self.turn = False

    def switch_turn(self):
        self.turn = not self.turn
        logging.info(f'Switching turn to {"Hero" if self.turn else "Villain"}.')

    def get_topcard(self, cards: Deck):
        self.topcard = cards
        self.topcard_length = len(cards)
        for suit in cards:
            if suit.__face_up:
                self.topcard_suits.append(suit.suit)

    def play_card_effect(self, cards: Deck):
        self.restriction_suits()
        if self.contains_eight(cards):
            self.field_clear()
            self.switch_turn()
        self.contains_eleven(cards)
        self.revolution(cards)

    def contains_eight(self, cards: Deck):
        for card in cards:
            if card.number == self.dict[7].number and card.face_up:
                print("8切り！")
                return True
        return False

    def contains_eleven(self, cards: Deck):
        for card in cards:
            if card.number == self.dict[10].number and card.face_up:
                print("Jバック！")
                Milliondoubt.tgl_revolution()
                self.is_eleven_back = True
                return True
        return False

    def revolution(self, cards: Deck):
        if len(cards) >= 4:
            
            print("革命！")
            Milliondoubt.tgl_revolution()

# TODO
    def get_backcard_suit(self, cards):
        for card in cards:
            if card.__face_up:
                self.before_suits.append(card.suit)

    def restriction_suits(self):
        for suit in self.before_suits:
            for suit1 in self.topcard_suits:
                if suit1 == suit:
                    print(f"{suit}縛り")
                    self.restricted_suits.append(suit)

    def play_cards(self, player):
        if player.type == "Player":
            return self.play_cards_player(player)
        # BUG while loop: self.return_cards
        elif player.type == "CPU":
            return self.play_cards_CPU(player)
        elif player.type == "ML":
            return self.play_cards_ML(player)

    def play_cards_player(self, player):
        selected_indexes = player.sel_card()
        while selected_indexes:
            player.opn_card()
            player.sel_card_back()
            if self.is_validation(player.field, True):
                self.topcard = copy.deepcopy(player.field)
                self.topcard_number = self.get_topcard_number(player.field, True)
                self.topcard_length = len(player.field)
                self.is_bluff = self.is_bluff_cards(player.field, self.field)
                for i in range(len(player.field)):
                    self.field.get_card(player.field)
                logging.info(f'{"Hero" if self.turn else "Villain"} played cards: {player.field}')
                return True
            print("その手は出せません")
            player.return_cards()
            print(f"Field: {self.field}")
            print(player.hands)
            selected_indexes = player.sel_card()
        else:
            print("Passed.")
            self.skip = True
            self.field_clear()
            logging.info(f'{"Hero" if self.turn else "Villain"} passed.')
            return False

    def play_cards_CPU(self, player):
        selected_indexes = player.sel_card(self.topcard_length)
        while selected_indexes:
            player.sel_card_back()
            if self.is_validation(player.field, True):
                self.topcard = copy.deepcopy(player.field)
                self.topcard_number = self.get_topcard_number(player.field, True)
                self.topcard_length = len(player.field)
                self.is_bluff = self.is_bluff_cards(player.field, self.field)
                for i in range(len(player.field)):
                    self.field.get_card(player.field)
                logging.info(f'{"Hero" if self.turn else "Villain"} played cards: {player.field}')
                return True
            logging.warning("その手は出せません")
            player.return_cards()
            return False
        else:
            print("Passed.")
            self.skip = True
            self.field_clear()
            logging.info(f'{"Hero" if self.turn else "Villain"} passed.')
            return False

    def play_cards_ML(self, player):
        pass


    def get_topcard_number(self, player_field: Deck, visible_only: bool = False) -> int:
        max_number = 0
        stairs = self.is_stairs(player_field)
        pair = self.is_pair(player_field)
        visible_count = 0

        for i, card in enumerate(player_field):
            if visible_only and not card.face_up:
                continue
            if card.face_up:
                visible_count += 1

            if stairs and card.number == "Joker":
                if i > 0:
                    max_number = player_field[i - 1].number
                break
            elif card.number == "Joker":
                if not stairs and (len(player_field) == 1 or pair):
                    max_number = max(max_number, 14)
            elif card.number is not None and int(card.number) > max_number:
                max_number = int(card.number)

        if visible_only and visible_count == 0:
            return self.topcard_number

        return max_number
    
    def encode_hand(self, hand):
        encoded_hand = [card.encode() for card in hand]
        encoded_hand += [1] * (14 - len(hand))
        return encoded_hand
    
    def is_validation(self, cards: Deck, visible_only: bool = False):
        if not self.field:
            if len(cards) == 1:
                return True
            elif self.is_stairs(cards, visible_only) or self.is_pair(cards, visible_only) or self.is_multiple(cards, visible_only):
                return True
            else:
                return False
        
        if len(cards) != self.topcard_length:
            return False
        
        if len(cards) >= 2 and not(
            self.is_stairs(cards, visible_only)
            or self.is_pair(cards, visible_only)
            or self.is_multiple(cards, visible_only)
        ):
            return False
                
        if self.is_multiple_flag:
            logging.debug('Field has a multiple constraint')
        elif self.is_stairs_flag:
            logging.debug('Field has a stairs constraint')
        else:
            logging.debug('Field has a pair/single constraint')
            
        if not self.field:
            logging.debug("No cards on the field")
            if self.get_topcard_number(cards, visible_only) < self.topcard_number:
                logging.debug("Played cards have lower value than the top card")
                return False

            if not self.is_restriction_suits(cards, visible_only):
                logging.debug("Played cards do not meet the suit restriction")
                return False
        
        return True

    def is_restriction_suits(self, cards: Deck, visible_only: bool = False):
        if self.restricted_suits:  # suits が空でない場合のみ処理を実行
            for suit in self.restricted_suits:
                for card in cards:
                    if visible_only and not card.face_up:
                        continue
                    if card.suit == suit:
                        continue
                    else:
                        return False  # suits と一致しない場合、False を返す
        return True

    def is_pair(self, cards: Deck, visible_only: bool = False):
        if len(cards) == 2:
            if visible_only:
                if any(card.face_up == False for card in cards):
                    return True
                else:
                    if cards[0].is_joker or cards[1].is_joker:
                        return True
                    return cards[0].number == cards[1].number
            else:
                if cards[0].is_joker or cards[1].is_joker:
                    return True
                return cards[0].number == cards[1].number
        else:
            return False

    def is_multiple(self, cards: Deck, visible_only: bool = False):
        if len(cards) < 3:
            return False

        # face.up == True のカードから first_card_number を取得
        first_card_number = None
        for card in cards:
            if card.face_up and not card.is_joker:
                first_card_number = card.number
                break

        for card in cards:
            if visible_only and not card.face_up:
                continue
            if card.is_joker:
                continue
            if card.number != first_card_number:
                return False

        return True

    def is_stairs(self, cards: Deck, visible_only: bool = False):
        if len(cards) < 3:
            return False

        # カードを昇順にソート
        sorted_cards = sorted([card for card in cards if not card.is_joker], key=lambda card: (int(card.number), not card.face_up))
        joker_count = sum(1 for card in cards if card.is_joker)
        back_count = sum(1 for card in cards if not card.face_up)

        # すべてのカードが同じスートであることを確認
        first_card_suit = None
        for card in sorted_cards:
            if card.face_up and not card.is_joker:
                first_card_suit = card.suit
                break

        for card in sorted_cards[1:]:
            if visible_only and not card.face_up or card.is_joker:
                continue
            if card.suit != first_card_suit:
                return False

        # 階段出しの条件チェック
        needed_jokers = 0
        for i in range(len(sorted_cards) - 1 - back_count - joker_count):
            if visible_only and not sorted_cards[i].face_up:
                continue
            gap = int(sorted_cards[i + 1].number) - int(sorted_cards[i].number) - 1
            needed_jokers += gap
            if needed_jokers > joker_count + back_count:
                return False

        return True



    def is_bluff_cards(self, cards: Deck, field_cards: Deck):
        if field_cards is None:
            if len(cards) < 2:
                return False  # 場にカードがない場合は、出せるカードなのでFalseを返す
            else:
                if self.is_pair(cards, False) or self.is_multiple(cards, False) or self.is_stairs(cards, False):
                # ペア出し、複数枚出し、階段出しのいずれかである場合
                    return False  # 条件を満たすので、Falseを返す
                else:
                    return True
        # フィールドにカードが有る場合
        else:
            self.is_validation(cards, False)

    def field_clear(self):
        self.field.clear()
        self.topcard.clear()
        self.topcard_length = 0
        self.topcard_number = 0
        self.topcard_suits.clear()
        self.is_multiple_flag = False
        self.is_stairs_flag = False
        self.is_restriction = False
        self.restricted_suits.clear()
        self.before_suits.clear()
        self.round_start = True
        self.round += 1

        if self.is_eleven_back == True:
            Milliondoubt.tgl_revolution()
            self.is_eleven_back = False
    
    def should_doubt(self, player):
        player.dec_dbt()
        return player.is_dbt
    
    def handle_bluff_caught(self, bluffer, doubter):
        # ブラフがバレたため、フィールドのカードをブラフを行ったプレイヤーの手札に加える
        logging.info(f'{bluffer} was caught bluffing by {doubter}. Penalty applied.')
        print("ダウト成功")
        # print(self.field)
        # NOTE キャンセル処理
        doubter.sel_dbtcard(self.field)
        doubter.opn_dbtcard(self.field)

        for i in range(len(doubter.field)):
            bluffer.hands.get_card(doubter.field)
        self.field_clear()
        # ブラフがバレたプレイヤーにペナルティを与える（必要であれば）
        # 例: bluffer.penalty += 1

    def handle_false_doubt(self, player, doubter):
        # ダウトが失敗したため、フィールドのカードをダウトを行ったプレイヤーの手札に加える
        logging.info(f'{doubter} falsely doubted {player}. Penalty applied.')
        print("ダウト失敗")
        # print(self.field)
        # doubter.hand.extend(self.field)
        player.sel_dbtcard(self.field)
        player.opn_dbtcard(self.field)

        for i in range(len(player.field)):
            doubter.hands.get_card(player.field)
        self.field_clear()
        self.switch_turn()
        # ダウトが失敗したプレイヤーにペナルティを与える（必要であれば）
        # 例: doubter.penalty += 1

    def handle_no_doubt(self):
        pass

    def check_burst(self):
        # プレイヤーの手札が11枚以上になった場合、バーストとみなす
        if len(self.player0.hands) >= 11:
            self.player1.dec_burst()
            if self.player1.play_burst:
                self.winner = self.player0
                return self.winner
        elif len(self.player1.hands) >= 11:
            self.player0.dec_burst()
            if self.player0.play_burst:
                self.winner = self.player1
                return self.winner
        return False
    
        player.dec_burst()
        return player.is_burst

    def handle_burst(self):
        if self.winner:
            # toggle on/off
            self.show_winner(self.winner)
            # logging.info(f'{winner} burst with {loser_hands_size} cards in hand.')
            self.play = False

    def check_win(self):
        if len(self.player0.hands) == 0:
            print("Hero wins!")
            return self.player0
        elif len(self.player1.hands) == 0:
            print("Villain wins!")
            return self.player1

    def show_winner(self, player):
        winner = None
        loser_hands_size = None
        if player == self.player0:
            winner = "Hero"
            loser = "Villain"
            loser_hands_size = len(self.player1.hands)
        elif player == self.player1:
            winner = "Villain"
            loser = "Hero"
            loser_hands_size = len(self.player0.hands)

        print(f"{winner} の勝ち by {loser_hands_size} 枚")
        # logging.info(f'{winner} wins by {loser_hands_size} cards.')
        self.play = False

    def start_game(self):
        self.deal_cards()
        self.decide_attacker()

        while self.play:
            # ターンを表示
            logging.info(f'Phase {self.round}')
            logging.info("Hero's turn" if self.turn else "Villain's turn")
            print(f'Phase {self.phase}')
            print("Hero's turn" if self.turn else "Villain's turn")
            print(f"Field: {self.field}")

            # カードを表示
            print(f"相手札： {len(self.player1.hands)}枚")
            print("My hand:", end=" ")
            self.player0.prt_card()

            # カードを出す
            field = self.field
            if self.turn:
                cards_played = self.play_cards(self.player0)
            else:
                cards_played = self.play_cards(self.player1)

            # print(f"topcard: {self.topcard}")
            print(f"相手札： {len(self.player1.hands)}枚")
            # print(f"length: {self.topcard_length}")
            print(f"Play: {self.topcard}")
            print(" ")
            
            if not self.skip and not (self.round_start and len(self.topcard) == 1) and not all(card.face_up for card in self.topcard) and not self.topcard == []:
            # ダウトするかどうか判断
                if self.turn:
                    should_doubt = self.should_doubt(self.player1)
                else:
                    # print(f"Field: {self.field}")
                    # self.debug_func()
                    should_doubt = self.should_doubt(self.player0)
                # ダウト判断、ダウト実行処理
                if should_doubt:
                    print("ダウト")
                    print(" ")
                    # print("self.field")
                    if not self.is_bluff:
                        # !s 嘘がばれた場合
                        if self.turn:
                            # add kif "!s"
                            # handle_bluff_caught(self, bluffer, doubter)
                            self.handle_bluff_caught(self.player0, self.player1)
                            self.field_clear()
                        else:
                            # add kif "!s"
                            print(f"相手札： {len(self.player1.hands)}枚")
                            self.handle_bluff_caught(self.player1, self.player0)
                            self.field_clear()
                        # bst バースト判定
                        if self.check_burst():
                            print("Burst!")
                            if self.turn:
                                self.handle_burst()
                            else:
                                self.handle_burst()
                            break
                    else:
                        # !m 嘘じゃなかった場合
                        if self.turn:
                            # add kif "!m"
                            # handle_false_doubt(self, player, doubter)
                            self.handle_false_doubt(self.player1, self.player0)
                            self.field_clear()
                            self.phase -= 1
                            self.switch_turn()
                        else:
                            # add kif "!m"
                            print(f"相手札： {len(self.player1.hands)}枚")
                            self.handle_false_doubt(self.player0, self.player1)
                            self.field_clear()
                            self.phase -= 1
                            self.switch_turn()
                        # バースト判定
                        if self.check_burst():
                            print("Burst!")
                            if self.turn:
                                # バーストハンドリング
                                self.handle_burst()
                            else:
                                # バーストハンドリング
                                self.handle_burst()
                            break
                else:
                    # ダウトしない場合
                    self.handle_no_doubt()
                    
            self.round_start = False
            # パスの処理
            if not cards_played:
                print("パス")
                self.field_clear()
            # 勝利判定
            if self.check_win():
                print("Game Over")
                self.show_winner(self.check_win())
                break
            # カードの効果 not working
            self.play_card_effect(self.topcard)
            # ターン交代
            self.phase += 1
            self.switch_turn()
            self.skip = False
            self.is_bluff = False
            self.get_backcard_suit(self.topcard)
            print(" ")




if __name__ == '__main__':
    logging.basicConfig(filename='game.log', filemode='w', level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s')
    game = Game()
    game.start_game()