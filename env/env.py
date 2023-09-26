import gym
import random
import numpy as np
# from cards import Card, Deck

from env import cards
from env import game

# actionの設計

class MillionDoubtEnv(gym.Env):
    def __init__(self):
        # self.is_playing = False
        # self.is_declaring_doubt = False
        # self.is_selecting = False
        # self.is_declaring_burst = False
        # self.decode_option = False
        self.game = game.Game()
        self.obs_dict = {
            'player_hand': [],
            'opponent_hand_len': [],
            'field': [],
            'topcard': [],
            'turn': 0,
            'phase_type': 0,
            'is_revolution': 0,
            'restricted_suits': 0,
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
            'restricted_suits': gym.spaces.MultiBinary(4),
        })


        # 行動空間の定義
        self.action_space = gym.spaces.Dict({
            'play_card': gym.spaces.MultiBinary(11),
            'play_card_back': gym.spaces.MultiBinary(11),
            'doubt': gym.spaces.Discrete(2),
            'select_card': gym.spaces.MultiBinary(11),
            # 'burst': gym.spaces.Discrete(2),
        })

    def play(self, action):
        index1, index2 = self.decode_index(action['play_card'], action['play_card_back'])
        return index1, index2

    def declare_doubt(self, action):
        if action['doubt'] == 0:
            return False
        else:
            return True

    def select_dbtcard(self, action):
        index = self.decode_index(action['select_card'])
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
        
        # TODO fix
        # ゲームが終了した場合、報酬を計算
        player_hand_size = len(self.game.player0.hands)
        
        opponent_hand_size = len(self.game.player1.hands)

        # 勝者の勝ち点、敗者の敗北点を報酬として返す
        if player_hand_size < opponent_hand_size:
            return opponent_hand_size
        else:
            return - player_hand_size

    def get_action(self, obs):
        action = {
            'play_card': np.empty([0]),
            'play_card_back': np.empty([0]),
            'doubt': np.empty([0]),
            'select_card': np.empty([0]),
            # 'burst': np.empty([0]),
        }
        
        legal_moves = []
        
        if obs['phase_type'] == 0:
            return action
        
        elif obs['phase_type'] == 1:
            if self.game.turn:
                # self.obs_dict['phase_type'] = 1
                legal_moves = self.game.searching_legal_move(self.game.player0)
                print(len(legal_moves)) # NOTE debug
                rand_int = random.randint(0, len(legal_moves)-1)
                print(len(legal_moves[rand_int])) #　NOTE debug
                # print(legal_moves)
                action['play_card'] = legal_moves[rand_int][0]
                action['play_card_back'] = legal_moves[rand_int][1]
                # self.decode_option = True
            return action

    # ダウト(sample())
        elif obs['phase_type'] == 2:
            if not self.game.turn:
                action['doubt'] = self.action_space['doubt'].sample()
            return action

    # select card(sample())
        elif obs['phase_type'] == 3:
            if self.game.player0_dbtcard_right:
                # self.obs_dict['phase_type'] = 3
                # action['select_card'] = self.action_space['select_card'].sample()
                sample = np.random.randint(2, size=len(self.game.field), dtype=int)
                zeros = np.zeros(14 - len(self.game.field))
                
                # action['select_card'] = self.decode_index(np.concatenate([sample, zeros], 0))
                action['select_card'] = np.concatenate([sample, zeros], 0)
                
            return action

    # バースト(sample())
        elif obs['phase_type'] == 4:
            return action
        #     action['burst'] = 1 # True
        #     # self.decode_option = False
        #     return action

        else:
            print("NotImplementedError_get_action")

    def step(self, action):
        done = False
        reward = 0
        info = {}
        play_card = []
        play_card_back = []
        doubt = []
        dbtcard = []
        burst = []

    # TODO act =>
        # 'NoneType' object is not subscriptable
        # print("Action:", action)
        # if action is not None:
        #     print("play_card:", action.get('play_card'))
        #     print("play_card_back:", action.get('play_card_back'))
        
        # カードをプレイするフェーズの処理
        # if action['play_card'].size > 0 and action['play_card_back'].size > 0:
        if len(action['play_card']) > 0 and len(action['play_card_back']) > 0:
            # play_card, play_card_back = self.play(action)
            play_card = action['play_card']
            play_card_back = action['play_card_back']
            
        elif action['doubt']:
        # ダウトをするフェーズの処理
            doubt = self.declare_doubt(action)
        elif len(action['select_card']) > 0:
        # ダウトカードを選択するフェーズの処理
            dbtcard = self.select_dbtcard(action)
        # elif action['burst']:
        # # バーストを宣言するフェーズの処理
        #     burst = self.declare_burst(action)
        
        # print no action
        else:
            if self.game.my_phase == "play":
                if not self.game.turn:
                    pass
            elif self.game.my_phase == "dec_doubt":
                if self.game.turn:
                    pass
            elif self.game.my_phase == "sel_dbtcard":
                if not self.game.is_should_doubt:
                    pass
            elif self.game.my_phase == "dec_burst":
                pass
            else:
                print("no_action")

        if self.game.my_phase == "play":
            if self.game.turn:
                print(f"action1:{play_card}") # NOTE debug
                print(f"action2:{play_card_back}") # NOTE debug
                self.game.phase_play(play_card, play_card_back) # act
            else:
                self.game.phase_play()
            
        elif self.game.my_phase == "dec_doubt":
            if self.game.check_is_doubt():
                if self.game.turn:
                    self.game.phase_dec_doubt()
                else:
                    self.game.phase_dec_doubt(doubt) # act
                    print(doubt) # NOTE debug

        elif self.game.my_phase == "sel_dbtcard":
            print(dbtcard)
            # ダウト判断、ダウト実行処理
            if self.game.is_should_doubt:
                # print("ダウト\n")
                if self.game.player0_dbtcard_right:
                    self.game.phase_sel_dbtcard(dbtcard) #act
                else:
                    self.game.phase_sel_dbtcard() #act
                self.game.field_clear()
            else:
                # ダウトしない場合
                # print("スルー\n")
                self.game.handle_no_doubt()
            
        elif self.game.my_phase == "dec_burst":
            print(burst)
            # バースト判定
            if self.game.check_burst():
                self.game.call_burst() # act
                self.game.handle_burst()
            
        if self.game.is_turn_end:
            self.game.end_phase()


    # dec_burst or 敗北のlog表記
        # Check if game is over
    # TODO 報酬枚数の記憶
        done = self.game_over()
        if done: # This function needs to be defined.
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
            self.game.decide_attacker()

            self.update_obs()

            # self.clear_field() => dictの指定部分のみを更新

        return self.obs_dict

    def game_over(self):
        if not self.game.play:
            return True
        return False

    def encode_card(self, card, option: bool=True):
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


    def encode_cards(self, cards, max_cards_len, option: bool=True):
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
        
# TODO バイナリからindexに変換
    def decode_index(self, bin1, bin2=None):
        index1 = [i for i, value in enumerate(bin1) if value == 1]

# TODO 選択されたカードのうちからindex
        if bin2 is not None:
            index2 = [i for i, value in enumerate(bin2) if value == 1]
            # self.decode_option = False
            return index1, index2
        else:
            return index1


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

        # Phase_type
        phase = 0
        if self.game.my_phase == "None":
            phase = 0
        elif self.game.my_phase == "play":
            phase = 1
        elif self.game.my_phase == "dec_doubt":
            phase = 2
        elif self.game.my_phase == "sel_dbtcard":
            phase = 3
        elif self.game.my_phase == "dec_burst":
            phase = 4
        else:
            print("NotImplementedError_#383_env.py")

        self.obs_dict['phase_type'] = phase

        # 革命状態かどうか
        is_revolution = 1 if self.game.is_revolution else 0
        self.obs_dict['is_revolution'] = is_revolution

        # 制限スートのエンコード
        restricted_suits_from_game = self.game.restricted_suits
        if restricted_suits_from_game is not None:
            # 0で初期化された4要素のリストを作成
            restricted_suits = [0 for _ in range(4)]
            # restricted_suits_from_gameの各要素が対応するスートである場合、その位置を1に設定

            # NOTE　TypeError: list indices must be integers or slices, not Suit
            for suit in restricted_suits_from_game:
                restricted_suits[int(suit)] = 1
        else:
            restricted_suits = [0 for _ in range(4)]

        self.obs_dict['restricted_suits'] = np.array(restricted_suits)


        return self.obs_dict

# # MLPlayer vs human, CPUPlayer
env = MillionDoubtEnv()
log_episode_reward = []
log = []
obs = env.reset()

# MLPlayer vs CPUPlayer
while True:
    # print(env.game.player0.hands)
    obs = env.update_obs()
    act = env.get_action(obs)
    print(f"phase: {env.obs_dict['phase_type']}")
    print(act)
    next_obs, reward, done, info = env.step(act)

    log.append((obs, act, next_obs, reward, done))
    log_episode_reward.append(reward)

    if done:
        break

    obs = next_obs

episode_rewrd = sum(log_episode_reward)