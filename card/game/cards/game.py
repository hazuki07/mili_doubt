import random
from site import check_enableusersite
from turtle import Turtle
import cards
import rule
import role

from collections import namedtuple

class Game():
    def __init__(self):
        # role.py
        self.player0 = role.Player()
        self.player1 = role.Player()
        self.phase = 1
        self.turn = False
        self.play = True
        self.is_bulff = False
        self.deck = cards.Deck(rule.Milliondoubt)
        self.deck.full()
        self.field = cards.Deck(rule.Milliondoubt)
        self.Graveyard = cards.Deck(rule.Milliondoubt)
        self.topcards_length = 0
        self.topcard_number = 0
        self.is_stair = False
        self.is_restriction = False
        self.skip = False

    def deal_cards(self):
        self.deck.shuffle()
        for i in range(rule.INITIAL_HAND_SIZE):
            self.player0.hands.get_card(self.deck)
            self.player1.hands.get_card(self.deck)
        self.player0.hands.sort()
        self.player1.hands.sort()

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

    def play_cards(self, player):
        selected_indexes = player.sel_card()
        if selected_indexes:
            # while self.contradiction:
            player.opn_card()
            player.sel_card_back()
            # if self_is_bluff:
            self.topcard_number = self.get_topcard_number(player.field)

        else:
            print("Passed.")
            self.skip = True

    # TODO test undo
    def get_topcard_number(self, player_field: cards.Deck) -> int:
        max_number = 0
        stairs = self.is_stairs(player_field)

        for i, card in enumerate(player_field):
            # if card._Card__face_up:
            if stairs and card.number == "Joker":
                if i > 0:
                    max_number = player_field[i - 1].number
                break
            elif card.number > max_number:
                max_number = card.number
        return max_number


    # TODO test undo
    def contains_eight(self, cards: cards.Deck) -> bool:
        for card in cards:
            if card.number == 8:
                return True
        return False

    # TODO test undo
    def jack_back(self, cards: cards.Deck):
        for card in cards:
            if card.number == 11:
                return True
        return False

    # TODO test undo
    def revolution(self, cards: cards.Deck):
        if len(cards) >= 4:
            # TODO
            rule.Milliondoubt.tgl_revolution()

    # TODO test
    def is_pair(self, cards: cards.Deck) -> bool:
        if len(cards) != 2:
            return False
        self.is_restriction = True
        return cards[0].number == cards[1].number

    def is_multiple(self, cards: cards.Deck) -> bool:
        if len(cards) < 3:
            return False
        first_card_number = cards[0].number
        for card in cards[1:]:
            if card.number != first_card_number:
                return False
        self.is_restriction = True
        return True

    def is_stairs(self, cards: cards.Deck):
        if len(cards) < 3:
            return False

        # カードを昇順にソート
        sorted_cards = sorted(cards, key=lambda card: int(card.number))

        # 階段出しの条件チェック
        for i in range(len(sorted_cards) - 1):
            if int(sorted_cards[i].number) + 1 != int(sorted_cards[i + 1].number):
                return False
        self.is_restriction = True
        return True

    def is_bluff(self, cards: cards.Deck, field_cards: cards.Deck) -> bool:
        # TODO param self.is_bluff
        if field_cards is None:
            return False  # 場にカードがない場合は、出せるカードなのでFalseを返す

        if self.is_pair(cards) or self.is_multiple(cards) or self.is_stairs(cards):
            # ペア出し、複数枚出し、階段出しのいずれかである場合
            if cards[-1] > field_cards:
                # 場のカードより大きい場合
                return False  # 条件を満たすので、Falseを返す
        return True  # それ以外の場合は、Trueを返す
    
    def should_doubt(self, player):
        player.dec_dbt()
        return player.is_dbt
    
    def handle_bluff_caught(self, bluffer, doubter):
        # ブラフがバレたため、フィールドのカードをブラフを行ったプレイヤーの手札に加える
        print(self.field)
        # NOTE キャンセル処理
        doubter.sel_dbtcard()
        doubter.opn_dbtcard(self.field)
        bluffer.hands.get_card(doubter.field)
        self.field.clear()

        # ブラフがバレたプレイヤーにペナルティを与える（必要であれば）
        # 例: bluffer.penalty += 1

        # ターンを維持または変更する（必要に応じて）
        # 例: self.turn = doubter

    # TODO rev
    def handle_false_doubt(self, player, doubter):
        # ダウトが失敗したため、フィールドのカードをダウトを行ったプレイヤーの手札に加える
        print(self.field)
        # doubter.hand.extend(self.field)
        player.sel_dbtcard()
        player.opn_dbtcard(self.field)
        doubter.hands.get_card(player.field)
        self.field.clear()

        # ダウトが失敗したプレイヤーにペナルティを与える（必要であれば）
        # 例: doubter.penalty += 1

        # ターンを維持または変更する（必要に応じて）
        # 例: self.turn = doubter

    def handle_no_doubt(self):
        # ダウトが行われなかったため、フィールドのカードをクリアする
        # self.field.clear()
        pass

    def check_burst(self):
        # プレイヤーの手札が11枚以上になった場合、バーストとみなす
        if len(self.player0.hands) >= 11:
            return self.player0
        elif len(self.player1.hands) >= 11:
            return self.player1
        return False

    def handle_burst(self):
        if self.check_burst():
            # toggle on/off
            self.show_winner(self.check_burst())
            self.play = False

    def check_win(self):
        if len(self.player0.hands) == 0:
            print("Hero wins!")
            return self.player0
        elif len(self.player1.hands) == 0:
            print("Villan wins!")
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
        self.play = False

    def start_game(self):
        # カードを配る
        self.deal_cards()

        # 先行後攻を決める
        self.decide_attacker()

        while self.play:
            # ターンを表示
            print("Phase", end=" ")
            print(self.phase)
            print("Hero's turn" if self.turn else "Villain's turn")
            print("Field:", end=" ")
            print(self.field)

            # カードを表示
            print("My hand:", end=" ")
            self.player0.prt_card()

            # カードを出す
            if self.turn:
                cards_played = self.play_cards(self.player0)

                # TODO bluff play_cardsに組込
                # ブラフフラグ
                # is_bluff = self.is_bluff(self.player0.field)
                """for cards in self.player0.field:
                    self.field.get_card(cards)"""
            else:
                """cards_played = self.play_cards(self.player1)
                """
                
                pass

            # skip しない
            if not self.skip:
    #  ~~~devlopping now
                
                                # ダウトするかどうか判断
                if self.turn:
                    should_doubt = self.should_doubt(self.player1)
                else:
                    should_doubt = self.should_doubt(self.player0)

                # ダウト判断、処理
                if should_doubt:
                    # BUG
                    if self.is_bluff:
                        # 嘘がばれた場合
                        if self.turn:
                            self.handle_bluff_caught(self.player0,self.player1)
                        else:
                            self.handle_bluff_caught(self.player1,self.player0)

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
                        # 嘘じゃなかった場合
                        if self.turn:
                            self.handle_false_doubt(self.player1, self.player0)
                        else:
                            self.handle_false_doubt(self.player0, self.player1)

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

            # パスの処理
            else:
                self.field.clear()
            
                # 勝利判定
            if self.check_win():
                print("Game Over")
                self.show_winner(self.check_win())
                break

            # ターン交代
            self.phase += 1
            self.switch_turn()
            self.skip = False
            self.is_restriction = False


if __name__ == '__main__':
    game = Game()
    game.start_game()
