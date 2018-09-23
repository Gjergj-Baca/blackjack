from random import shuffle


class Table:

    def __init__(self, player, balance=100):
        self.dealer = Dealer()
        self.player = Player(player, balance)
        self.deck = Deck()
        self.rules = Rules()
        self.bet()
        self.player_hand = []
        self.dealer_hand = [self.deck.deal_card() for x in range(0, 1)]
        self.player_hand_init()
        self.setup()
        self.options()

    # handles options after first game has finished
    def options(self):
        choice = input('Write the numeric value for what you would like to do next:\n'
              '1 - Play another game\n'
              '2 - Show my current session stats\n'
              '3 - Add balance\n'
              '4 - Quit\n')
        try:
            if int(choice) == 1:
                self.restart()
            elif int(choice) == 2:
                self.total_session_stats()
            elif int(choice) == 3:
                self.player.balance += 100
                print('£100 has been deposited to your account\n')
                self.options()
            elif int(choice) == 4:
                exit()
            else:
                print('Command not recognised, please try again\n')
                self.options()
        except ValueError:
            print('Please choose a numeric number and try again\n')
            self.options()

    # handles starting new games
    def restart(self):
        self.deck = Deck()
        self.bet()
        self.player_hand = []
        self.dealer_hand = [self.deck.deal_card() for x in range(0, 1)]
        self.player_hand_init()
        self.setup()
        self.options()

    # handles statistics for games played
    def total_session_stats(self):
        print('\nTotal games played: {}\n'
              'Total games won: {}\n'
              'Total games draw: {}\n'
              'Total games lost: {}\n'
              'Total money won: £{}\n'
              'Total money lost: £{}\n'
              'You have won {}% of your games played\n'
              'You have lost {}% of your games played\n'.format(self.player.total_games_played,
                                                                 self.player.total_games_won,
                                                                 self.player.total_games_draw,
                                                                 self.player.total_games_lost,
                                                                 self.player.total_money_won,
                                                                 self.player.total_money_lost,
                                                                 int(self.player.total_games_won /
                                                                 self.player.total_games_played * 100),
                                                                 int(self.player.total_games_lost /
                                                                 self.player.total_games_played * 100)))
        self.options()

    # handles placing bets for the game
    def bet(self):
        bet_amount = input('Your current balance is: £{}\n'
                           'How much would you like to bet? Type number \n'.format(self.player.balance))

        try:
            if int(bet_amount) > self.player.balance:
                print('You have insufficient funds. Please try again. \n')
                self.bet()
            elif int(bet_amount) <= 0:
                print('You need to bet more than 0 to play. Please try again. \n')
                self.bet()
            else:
                print('You have a stake of £{} for this round'.format(bet_amount))
                self.bet_amount = int(bet_amount)
        except ValueError:
            print('Please choose a numeric number and try again\n')
            self.bet()

    # handles the setup of game
    def setup(self):
        print(self.stats())
        if self.rules.blackjack_rule(self.player.name, self.player_hand):
            print(self.rules.blackjack_rule(self.player.name, self.player_hand))
        elif self.rules.blackjack_rule('Dealer', self.dealer_hand):
            print(self.rules.blackjack_rule('Dealer', self.dealer_hand))
        else:
            self.hit_or_stick_player()
            if self.player_bust(self.player_score(self.player_hand)):
                self.player_bust(self.player_score(self.player_hand))
            else:
                self.hit_or_stick_dealer()

        self.find_winner(self.dealer_score(self.dealer_hand), self.player_score(self.player_hand))

    # handles the initial card distribution for player at the start of the game
    def player_hand_init(self):
        # distributes two cards to player
        for x in range(0, 2):
            card = self.deck.deal_card()
            self.player_hand.append(card)

        print(self.stats())

        # handles player cards if player gets Ace card at the start
        for el, x in enumerate(self.player_hand):
            self.player_hand_init_ace_handle(x, el)

    # handles how to treat an Ace card after providing the player the first two cards
    def player_hand_init_ace_handle(self, card, index):
        if card == {1: 'A'}:
            del self.player_hand[index]
            self.player_hand.append(self.ace_ten_or_one())

    # provides stats on the current game
    def stats(self):
        return str('\nPlayer hand: {}\n'
                   'Player total: {}\n\n'
                   'Dealer hand: {}\n'
                   'Dealer score: {}\n'.format(self.hand_cards(self.player_hand),
                                             self.player_score(self.player_hand),
                                             self.hand_cards(self.dealer_hand),
                                             self.dealer_score(self.dealer_hand)))

    # handles a players decision whether to hit more cards or to stick
    def hit_or_stick_player(self):
        while True:
            decision = input('\n{} - would you like to hit or stand? (h or hit / s or stand) \n'.format(self.player.name))

            if (decision == 'h' or decision=='hit'):
                self.hit_player()
                print(self.stats())
                if self.player_score(self.player_hand) > 21:
                    break
            elif (decision == 's' or decision == 's'):
                print(self.stats())
                break
            else:
                print('Command not understood, try again')
                continue

    # handles ruleset for dealers on whether to hit or stick with their cards
    def hit_or_stick_dealer(self):
        while True:
            print(self.stats())
            if self.dealer_score(self.dealer_hand) < 17:
                self.hit_dealer()
            else:
                break

    # add card to players deck
    def hit_player(self):
        card = self.deck.deal_card()
        if card == {1: 'A'}:
            card = self.ace_ten_or_one()
        return self.player_hand.append(card)

    # handles how to deal with an Ace card for the player, whether to treat it as 1 or 10
    def ace_ten_or_one(self):
        print(self.stats())
        choice = input('Would you like to treat Ace (A) as 1 or 10? Enter digit\n'
                       'Your new total score by choosing 1 will be {}\n'
                       'Your new total score by choosing 10 will be {}\n'.format(1 + self.player_score(self.player_hand),
                                                                                 10 + self.player_score(self.player_hand)))

        try:
            if int(choice) == 1:
                print(self.stats())
                return {1: 'A - 1'}
            elif int(choice) == 10:
                print(self.stats())
                return {10: 'A - 10'}
        except ValueError:
            print('Command not understood, try again\n')
            self.ace_ten_or_one()

    # add card to dealers deck
    def hit_dealer(self):
        self.stats()
        return self.dealer_hand.append(self.deck.deal_card())

    # returns the total score of a player based on what they have in their hand
    def player_score(self, hand):
        score = 0
        for x in hand:
            for i in x:
                score += int(i)
        return score

    # returns the cards of a dealers and players hand
    def hand_cards(self, hand):
        cards = str()
        for x in hand:
            for i in x.items():
                cards += '{}, '.format(str(i[1]))
        return cards

    # returns the total score of a dealer based on what they have in their hand
    def dealer_score(self, hand):
        score = 0
        for x in hand:
            for i in x:
                score += int(i)
        return score

    # gives cards to dealer
    def dealer_hand_cards(self, hand):
        return [x for x in hand]

    # handles finding a winner between player and dealer
    def find_winner(self, dealer_score, player_score):
        self.player.total_games_played += 1
        self.player_higher_than_dealer(player_score, dealer_score)

    # handles if a player goes bust (above 21 score)
    def player_bust(self, player_score):
        if player_score > 21:
            return True

    # handles player having a higher hands than a dealer
    def player_higher_than_dealer(self, player_score, dealer_score):
        if (player_score > dealer_score) and (player_score <= 21):
            self.add_player_balance(self.bet_amount)
            print(self.player_won())
            return True
        elif (dealer_score > 21) and (player_score <= 21):
            self.add_player_balance(self.bet_amount)
            print(self.player_won())
            return True
        self.dealer_higher_than_player(player_score, dealer_score)

    # handles player winning statement
    def player_won(self):
        self.player.total_games_won += 1
        self.player.total_money_won += self.bet_amount
        return '{} wins\n' \
               'You have won £{}\n' \
               'Your new balance is: £{}\n'.format(self.player.name, self.bet_amount,
                                                  self.player.balance)

    # handles dealer having a higher hands than a player
    def dealer_higher_than_player(self, player_score, dealer_score):
        if (dealer_score > player_score) and (dealer_score <= 21):
            self.remove_player_balance(self.bet_amount)
            print(self.dealer_won())
            return True
        elif (player_score > 21) and (dealer_score <= 21):
            self.remove_player_balance(self.bet_amount)
            print(self.dealer_won())
            return True
        self.dealer_player_draw(player_score, dealer_score)

    # both player and dealer goes above 21
    def dealer_player_draw(self, player_score, dealer_score):
        if (player_score > 21) and (dealer_score > 21):
            self.player.total_games_draw += 1
            print('It\'s a draw')
            return True
        elif player_score == dealer_score:
            self.player.total_games_draw += 1
            print('It\'s a draw')
            return True

    # handles if a dealer has won
    def dealer_won(self):
        self.player.total_games_lost += 1
        self.player.total_money_lost += self.bet_amount
        return 'Dealer wins\n' \
               'You have lost £{}\n' \
               'Your new balance is: £{}\n'.format(self.bet_amount, self.player.balance)

    # removes player balance
    def remove_player_balance(self, bet_amount):
        self.player.balance -= bet_amount
        return bet_amount

    # adds player balance
    def add_player_balance(self, bet_amount, multiplier=1):
        self.player.balance += (bet_amount * multiplier)
        return bet_amount


class Dealer(object):

    def __init__(self):
        self.name = "Dealer"
        self.score = 0
        self.hand = []


class Player(object):

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []
        self.deck = Deck
        self.total_games_played = 0
        self.total_games_won = 0
        self.total_games_draw = 0
        self.total_games_lost = 0
        self.total_money_won = 0
        self.total_money_lost = 0


class Deck(object):

    def __init__(self):
        self.stack = [{1: 'A'}, {2: '2'}, {3: '3'}, {4: '4'}, {5: '5'},
                      {6: '6'}, {7: '7'}, {8: '8'}, {9: '9'}, {10: '10'},
                      {10: 'J'}, {10: 'Q'}, {10: 'K'}] * 4
        self.shuffle()

    def shuffle(self):
        shuffle(self.stack)

    def deal_card(self):
        card = self.stack.pop()
        return card


class Rules(object):

    def __init__(self):
        self.blackjack = 21

    # handles evaluation for blackjack
    def blackjack_rule(self, name, cards):
        temp_value = list()

        for x in cards:
            for i in x.items():
                temp_value.append(i[1])

        first_card = temp_value[0]

        try:
            second_card = temp_value[1]
        except IndexError:
            pass

        if len(temp_value) == 2:
            for el, x in enumerate(temp_value):
                if (first_card == 'J'
                    or first_card == 'Q'
                    or first_card == 'K'
                    or first_card == 'A - 1'
                    or first_card == 'A - 10') and (second_card == 'J'
                                                    or second_card == 'Q'
                                                    or second_card == 'K'
                                                    or second_card == 'A - 1'
                                                    or second_card == 'A - 10'):
                    return '{} Blackjack!'.format(name)


def main():
    player_name = input("Welcome to Blackjack!\n"
                        "Created by Gjergj Baca\n"
                        "What's your name?\n")
    Table(player_name)


if __name__ == '__main__':
    main()

# Developed using Python 3.5

# Further development:
# 1 - integrate more rules that the user can decide, such as a split and insurances
# 2 - refactor some of the methods to better work together
# 3 - refactor some of the method names to make it clearer as to what they do specifically
# 4 - restructure and change some of the Table object methods to another object