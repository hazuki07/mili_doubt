import gym
import numpy as np
from cards import Card, Deck
import game

# actionの設計

class MillionDoubtEnv(gym.Env):
    def __init__(self):
        # self.is_playing = False
        # self.is_declaring_doubt = False
        # self.is_selecting = False
        # self.is_declaring_burst = False
        self.game = game.Game()
        self.obs_dict = {
            'player_hand': [],
            'opponent_hand_len': [],
            'field': [],
            'topcard': [],
            'turn': 0,
            'phase_type': 0,
            'is_revolution': 0,
            'restriction_suits': 0,
        }
        
        # 観測空間の定義
        # [0. 0. 0] = NONE, [0, 0, 1] = BACK
        self.observation_space = gym.spaces.Dict({
            # 手札 (A-13: カードの数字, 14: ジョーカー, 0: 空欄) (最大14枚) + スート (0: ジョーカー, 1: スペード, 2: ハート, 3: ダイヤ, 4: クラブ) (最大14枚)
            'player_hand': gym.spaces.MultiDiscrete(([15] * 14) + ([5] * 14)),
            # 相手手札の大きさ
            'opponent_hand_len': gym.spaces.Discrete(14),
            # フィールド (A-13: カードの数字, 14: ジョーカー, 0: 空欄) (最大13枚) + スート (0: ジョーカー, 1: スペード, 2: ハート, 3: ダイヤ, 4: クラブ) (最大13枚) + 表裏状態 (表: 0, 裏: 1) (最大13枚)
            'field': gym.spaces.MultiDiscrete(([15] * 13) + ([5] * 13) + ([2] * 13)),
            # トップカード (A-13: カードの数字, 14: ジョーカー, 0: 空欄) (最大11枚) + スート (0: ジョーカー, 1: スペード, 2: ハート, 3: ダイヤ, 4: クラブ) (最大11枚) + 表裏状態 (表: 0, 裏: 1) (最大11枚)
            'topcard': gym.spaces.MultiDiscrete(([15] * 11) + ([5] * 11) + ([2] * 11)),
            'turn': gym.spaces.Discrete(2),
            # カード選択(sel_playcard, sel_dbtcard) or 宣言フェーズ(dec_dbt, dec_burst)
            'phase_type': gym.spaces.Discrete(4),
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

# TODO Check Row.226
    def play(self, action):
        # 選択されたカードをプレイヤーの手札から削除
        index1, index2 = self.decode_index(action['play_card'], 14, True)
        return index1, index2

    def declare_doubt(self, action):
        if action['doubt'] == 0:
            return False
        else:
            return True

# TODO Check Row.226
    def select_dbtcard(self, action):
        index = []
        index = self.decode_index(action['play_card'], 11, False)        
        return index
        
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

# TODO コーディング
    def get_action(self, obs):
        action = None
        # 全部裏出し
        if self.obs['phase_type'] == 1:
            return action
        # Call doubt
        elif self.obs['phase_type'] == 2:
            return action
        # All cards return
        elif self.obs['phase_type'] == 3:
            return action
        # Call Burst
        elif self.obs['phase_type'] == 4:
            return action
        
        else:
            print("NotImplementedError")

    def step(self, action):
        done = False
        reward = 0
        info = {}
        
        # アクションのラベル判定
        
        # 現在のフェーズに基づいて処理を行う
        # phaseはネットワークに認識させる
        
        if self.game.my_phase == "play":
            # カードをプレイするフェーズの処理
            index1, index2 = self.play(action)
            # >>role.py selcard,selcard_back input
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
            
        
# TODO check game.py status
        # Check if game is over
        if self.game_over(): # This function needs to be defined.
            done = True
            reward = self.compute_reward(done=True)
        else:
            reward = self.compute_reward(done=False)

        self.obs_dict = self.update_obs() # This function needs to be defined.

        return self.obs_dict, reward, done, info


    def reset(self, kif=None):
        # 棋譜を読み込みます。
        if kif:
            pass
        # 環境を初期状態にリセットします。
        else:
            self.game.deal_cards()
            # print(self.game.player0.hands)
            # self.game.decide_attacker()
            
            self.update_obs()
            
            # self.clear_field() => dictの指定部分のみを更新

        return self.obs_dict
    
    # def render(self, mode="human"):
	# 	if mode == 'line':
	# 		print(self.game.to_kif())
	# 	else:
	# 		return self.game
        

#　TODO player_hand
    def game_over(self):
        return len(self.obs_dict['player_hand']) == 0 or self.obs_dict['opponent_hand_len'] == 0
    
    def encode_card(self, card: Card, option: bool=True):
        if card.joker:
            number = 14
            suit = 0
        else:
            number = int(card.number)
            suit = int(card.suit) + 1

        if option and not card.face_up:
            number = 0
            suit = 0

        face = 0 if card.face_up else 1

        if option:
            return [number, suit, face]
        else:
            return [number, suit]
        

    def encode_cards(self, cards: Deck, max_cards_len, option: bool=True):
        encoded_cards = [self.encode_card(card, option) for card in cards]

        # Noneを出力するカウンタ
        default_values_count = max_cards_len - len(cards)
        
        # Noneの値
        default_values = [[0, 0, 0]] if option else [[0, 0]]
        
        # デフォルト値[0,0]の代入
        encoded_cards.extend(default_values * default_values_count)
                
        encoded_cards = [item for sublist in encoded_cards for item in sublist]
        if option:
            encoded_cards = [encoded_cards[i::3] for i in range(3)]
        else:
            encoded_cards = [encoded_cards[i::2] for i in range(2)]
        encoded_cards = [item for sublist in encoded_cards for item in sublist]
        
        # converted array
        return np.array(encoded_cards)

# TODO Deck() to index
    def decode_cards(self, cards_state, option=True):
        cards = []
        converted_number = ""
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
        
# TODO Check
    def decode_index(self, cards_state, cards_len, option=True):
        index1 = []
        index2 = []
        for i in range(cards_len):
            if not (cards_state[i] == 0 and cards_state[cards_len + i - 1] == 0):
                index1.append(i) 

        if option:
            for i in range(cards_len):
                if not (cards_state[i] == 0 and cards_state[cards_len + i - 1] == 0):
                    # 0 or 1カードうらおもて
                    if cards_state[2*cards_len + i - 1] == 1:
                        index2.append(i) 
                else:
                    continue
            return index1, index2
        else:
            return index1
        
    #TODO Check
    def update_obs(self):
        # 手札のエンコード
        player_hand = self.encode_cards(self.game.player0.hands, 14, False)
        self.obs_dict['player_hand'] = player_hand

        # 相手の手札の長さ
        opponent_hand_len = len(self.game.player1.hands)
        self.obs_dict['opponent_hand_len'] = opponent_hand_len

        # フィールドのエンコード
        field = self.encode_cards(self.game.field, 13)
        self.obs_dict['field'] = field

        # トップカードのエンコード
        topcard = self.encode_cards(self.game.topcard, 11)
        self.obs_dict['topcard'] = topcard

        my_turn = 1 if self.game.turn else 0
        self.obs_dict['turn'] = my_turn

# TODO Phase_type
        phase = 0
        # if self.game.my_phase == "None":
        #     phase = 0
        if self.game.my_phase == "play":
            phase = 1
        elif self.game.my_phase == "dec_doubt":
            phase = 2
        elif self.game.my_phase == "sel_card":
            phase = 3
        elif self.game.my_phase == "dec_burst":
            phase = 4
        else:
            print("NotImplementedError")

        self.obs_dict['phase'] = phase

        # 革命状態かどうか
        is_revolution = 1 if self.game.is_revolution else 0
        self.obs_dict['is_revolution'] = is_revolution

        # 制限スートのエンコード
        restriction_suits = self.game.restriction_suits()
        if restriction_suits is not None:
            restriction_suits = [1 if restriction_suits[suit] else 0 for suit in range(4)]
        else:
            restriction_suits = [0 for _ in range(4)]
        self.obs_dict['restriction_suits'] = np.array(restriction_suits)

        return self.obs_dict

env = MillionDoubtEnv()

# print(env.observation_space)
obs = env.reset()
# print(obs)