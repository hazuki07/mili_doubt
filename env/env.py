from xmlrpc.client import _DateTimeComparable
import tensorflow as tf
import gym
import numpy as np
import torch
import random
import itertools
import game.game


class MillionDoubtEnv(gym.Env):
    def __init__(self):
        self.through = False
        self.doubt_success = False
        self.my_turn = False
        self.call_pass = False
        self.is_playing = False
        self.is_declaring_doubt = False
        self.is_selecting = False
        self.is_declaring_burst = False
        #TODO
        self.game = game.Game()
        # self.my_round = False
        # 観測空間の定義
        # [0. 0. 0] = NONE, [0, 0, 1] = BACK
        self.observation_space = gym.spaces.Dict({
            # 手札 (A-13: カードの数字, 14: ジョーカー, 0: 空欄) (最大14枚) + スート (0: ジョーカー, 1: スペード, 2: ハート, 3: ダイヤ, 4: クラブ) (最大14枚)
            'player_hand': gym.spaces.MultiDiscrete(([15] * 14) + ([5] * 14)),
            # 手札
            'opponent_hand_len': gym.spaces.Discrete(14),
            # フィールド (A-13: カードの数字, 14: ジョーカー, 0: 空欄) (最大13枚) + スート (0: ジョーカー, 1: スペード, 2: ハート, 3: ダイヤ, 4: クラブ) (最大13枚) + 表裏状態 (表: 0, 裏: 1) (最大13枚)
            'field': gym.spaces.MultiDiscrete(([15] * 13) + ([5] * 13) + ([2] * 11)),
            # トップカード (A-13: カードの数字, 14: ジョーカー, 0: 空欄) (最大11枚) + スート (0: ジョーカー, 1: スペード, 2: ハート, 3: ダイヤ, 4: クラブ) (最大11枚) + 表裏状態 (表: 0, 裏: 1) (最大11枚)
            'top_card': gym.spaces.MultiDiscrete(([15] * 11) + ([5] * 11) + ([2] * 11)),
            'my_round': gym.spaces.Discrete(2),
            'is_revolution': gym.spaces.Discrete(2),
            'restriction_suits': gym.spaces.MultiBinary(4),
        })


        # 行動空間の定義
        self.action_space = gym.spaces.Dict({
            # プレイカード (A-13: カードの数字, 14: ジョーカー, 0: 空欄) (最大11枚) + スート (0: ジョーカー, 1: スペード, 2: ハート, 3: ダイヤ, 4: クラブ)  (最大11枚) + 表裏状態 (表: 0, 裏: 1) (最大11枚)
            'play_card': gym.spaces.MultiDiscrete(([15] * 11) + ([5] * 11) + ([2] * 11)),
            'doubt': gym.spaces.Discrete(2),
            'select_card': gym.spaces.MultiDiscrete(([15] * 11) + ([5] * 11)),
            'burst': gym.spaces.Discrete(2),
        })

    def play(self, action):
        # 選択されたカードをプレイヤーの手札から削除
        cards = []
        cards = self.decode_cards(action['play_card'])
        for card in cards:
            # TODO 合っているか確認
            self.state['player_hand'].remove(card)

        # 選択されたカードをフィールドに追加
        self.state['field'] += cards

        # 選択されたカードをトップカードに設定
        self.state['top_card'] = cards
        
        return cards

    def declare_doubt(self, action):
        if action['doubt'] == 0:
            return False
        else:
            return True

    # when he successes doubt
    def select_dbtcard(self, action):
        cards = []
        cards = self.decode_cards(action['play_card'])               
        for card in cards:
            # TODO 合っているか確認
            self.state['field'].remove(card)
        self.clear_field()
        
        return cards
        
    def declare_burst(self, action):
        if action['burst'] == 0:
            return False
        else:
            return True

    def compute_reward(self, done):
        # ゲームが終了していない場合、報酬は0
        if not done:
            return 0
        # ゲームが終了した場合、報酬を計算
        player_hand_size = len(self.observation_space['player_hand'].nvec) / 2
        # opponent_hand_size = len(self.observation_space['opponent_hand'].nvec) / 2
        opponent_hand_size = self.observation_space['opponent_hand_len']

        # 勝者の勝ち点、敗者の敗北点を報酬として返す
        if player_hand_size < opponent_hand_size:
            return opponent_hand_size
        else:
            return - player_hand_size

    def step(self, action):
        done = False
        reward = 0
        info = {}
        
        # アクションのラベル判定
        
        # 現在のフェーズに基づいて処理を行う
        if self.game.my_phase == "play":
            # カードをプレイするフェーズの処理
            index1, index2 = self.play(action)
            self.game.player0.sel_card(index1)
            self.game.player0.sel_card_back(index2)
            
        if self.game.my_phase == "dec_doubt":
            # ダウトをするフェーズの処理
            self.game.player0.dec_dbt(self.declare_doubt(action))
            
        if self.game.my_phase == "sel_card":
            # ダウトカードを選択するフェーズの処理
            self.game.player0.sel_dbtcard(self.select_dbtcard(action))
            
        if self.game.my_phase == "dec_burst":
            # バーストを宣言するフェーズの処理
            self.game.player0.dec_burst(self.declare_burst(action))
            
        

        # Check if game is over
        if self.game_over(): # This function needs to be defined.
            done = True
            reward = self.compute_reward(done=True)
        else:
            reward = self.compute_reward(done=False)

        self.state = self.update_state() # This function needs to be defined.

        return self.state, reward, done, info


    def reset(self, kif=None):
        # 棋譜を読み込みます。
        if kif:
            pass
        # 環境を初期状態にリセットします。
        else:
            self.game.deal_cards()
            self.game.decide_attacker()
            
            self.doubt_success = False
            self.my_round = False
            player_hand = encode_cards(self.game.player0.hand)
            opponent_hand = len(self.game.player1.hand)
            self.state = {
                'player_hand': player_hand,
                'opponent_hand_len': opponent_hand,
            }
            self.clear_field()
        return self.state
    
    def render(self, mode="human"):
		if mode == 'line':
			print(self.game.to_kif())
		else:
			return self.game


    def clear_field(self):
        self.state = {
            'field': [],
            'top_card': [],
            'is_revolution': 0,
            'restriction_suits': [0, 0, 0, 0],
        }


    def game_over(self):
        return len(self.state['player_hand']) == 0 or self.state['opponent_hand_len'] == 0
    
    def encode_card(self, card, option: bool=True):
        if card.joker:
            number = -1
            suit = -1
        else:
            number = int(card.number)
            suit = int(card.suit)

        if option and not card.face_up:
            number = 1
            suit = -1

        face = 1 if card.face_up else 0

        return [number, suit, face]

    def encode_cards(self, cards, max_cards_len, option: bool=True):
        encoded_cards = [self.encode_card(card, option) for card in cards]
        while len(encoded_cards) < max_cards_len:
            encoded_cards.append([-1, -1, 0])  # 空欄を表すデフォルト値 None,jo,face [0, 0, 0] back [0 ,0 , 1]
        return [value for card in encoded_cards for value in card]

    # def encode_binary(self, value):
    #     return [0 if not value else 1]
    

    def decode_cards(self, cards_state, option=True):
        cards = []
        converted_numbers = ""
        converted_suit = ""
        
        if option:
            for i in range(11):
                number = cards_state[3*i]
                suit = cards_state[3*i + 1]
                face_up = cards_state[3*i + 2]

                if face_up == 0:
                    if number == 14 and suit == 0:
                        # ジョーカーの場合
                        cards.append("Jo")
                    elif number == 0:
                        # 空欄の場合
                        continue
                    else:
                        if number >= 2 and number <= 10:
                            converted_number = number
                        else:
                            converted_number = {11: 'J', 12: 'Q', 13: 'K', 1: 'A'}.get(number, number)
                        
                        converted_suit = {1: '♠', 2: '♡', 3: '♣', 4: '♢'}.get(suit, suit)
                        cards.append(converted_suit + converted_number)

                else:
                    cards.append("B")

            return cards
        
        else:
            for i in range(11):
                number = cards_state[2*i]
                suit = cards_state[2*i + 1]
                
                if number == 14 and suit == 0:
                    # ジョーカーの場合
                    cards.append("Jo")
                elif number == 0:
                    # 空欄の場合
                    continue
                else:
                    if number >= 2 and number <= 10:
                        converted_number = number
                    else:
                        converted_number = {11: 'J', 12: 'Q', 13: 'K', 1: 'A'}.get(number, number)
                    
                    converted_suit = {1: '♠', 2: '♡', 3: '♣', 4: '♢'}.get(suit, suit)
                    cards.append(converted_suit + converted_number)

            return cards