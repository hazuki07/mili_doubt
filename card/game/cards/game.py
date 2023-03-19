import random
import cards
import rule
import role

from collections import namedtuple

class Game():
    def __init__(self):
        # role.py
        self.player0 = role.Player()
        self.player1 = role.Player()
        self.atk = False
        self.turn = False
        self.play = True
        self.deck = cards.Deck(rule.Milliondoubt)
        self.deck.full()

    # hero's atk if x=0 else villan's atk
    def dec_atk(self):
        atk = random.randint(0, 1)
        if atk == 0:
            print("your atk turn.")
            self.atk = True
        else:
            print("Villan's atk.")
            self.atk = False

# rev
    def judge_win(self, player0, player1):
        # self.field.len() + self.loser.len()
        pass

    def main(self):
        deck = cards.Deck()

        """checking role
        def update_
        """

    # TODO test_
    def contains_eight(self, cards: cards.Deck) -> bool:
        for card in cards:
            if card.number == 8:
                return True
        return False

    # TODO test
    def jack_back(self, cards: cards.Deck):
        for card in cards:
            if card.number == "J":
                return True
        return False
    
    # TODO test
    def revolution(self, cards: cards.Deck):
        if len(Deck) >= 4:
            if self.revolution == False:
                use_reverse()
            else:
                use_milliondoubt()

    # TODO test
    def is_pair(self, cards: cards.Deck) -> bool:
        if len(cards) != 2:
            return False
        return cards[0].number == cards[1].number

    def is_multiple(self, cards: cards.Deck) -> bool:
        if len(cards) < 3:
            return False
        first_card_number = cards[0].number
        for card in cards[1:]:
            if card.number != first_card_number:
                return False
        return True

    def is_stairs(self, cards: cards.Deck):
        if len(cards) < 3:
            return False

        # カードを昇順にソート
        sorted_cards = sorted(cards, key=lambda card: card.number)

        # 階段出しの条件チェック
        for i in range(len(sorted_cards) - 1):
            if sorted_cards[i].number + 1 != sorted_cards[i + 1].number:
                return False
        return True

    def is_fake(self, cards: cards.Deck):
    # NOTE not pair stairs mul cards
        while not self.is_pair() or self.is_multiple() or self.is_stairs():
            return True
    

if __name__ == '__main__' :
    game = Game()
    # game.player0.prt_card()
"""
    while play:
        
        if self.turn == True:
            # my atk.
            # mysel()
            # bluff
            # sel dbt()

        else:
            # vi atk.
            # vi sel()
            # bluff
            # sel dbt()
        
        if self.dbt == True:
            if self.sucess == True:
                # mysel()
                self.turn == True
            else:
                # visel()
                self.turn == False
        else:
            self.turn_switch()
        
        if self.burst == True:
            # sel dbt()"""