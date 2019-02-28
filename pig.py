from random import *

class Game:
    def __init__(self, human, number_of_computers):
        self.human = human
        self.computers = {}
        for i in range(number_of_computers):
            self.computers[i + 1] = Computer(i + 1)
        self.turn_order = []
        self.number_of_players = number_of_computers + 1
        self.running = True

    def determine_turn_order(self):
        self.human.turn_placement = randint(1, self.number_of_players)
        i = 1
        while i < self.number_of_players or (i == self.number_of_players and self.human not in self.turn_order):
            if i == self.human.turn_placement and self.human not in self.turn_order:
                self.turn_order.append(self.human)
            else:
                self.turn_order.append(self.computers[i])
                i += 1
        self.current_player = self.turn_order[0]
        self.current_player.my_turn = True
        return self

    def switch_turns(self):
        current_player_index = self.turn_order.index(self.current_player)
        current_player_index += 1
        current_player_index = current_player_index % (self.number_of_players)
        self.current_player = self.turn_order[current_player_index]
        self.current_player.my_turn = True
        return self

    def display_scores(self):
        print()
        for i in range(self.number_of_players - 1):
            print(f"{self.computers[i + 1]}'s score: {self.computers[i+1].score}")
        print(f"Your score: {self.human.score}")
        print()
        
    def check_win(self):
        if self.current_player.score >= 100:
            print(f"{self.current_player} wins!")
            self.running = False
        return self  

def hold_till_20(computer, game):
    if computer.turn_total >= 20:
        return False
    return True

def roll_six(computer, game):
    if computer.roll_count < 6:
        return True

def nervous(computer, game):
    scores = []
    for i in range(game.number_of_players - 1):
        scores.append(game.computers[i+1].score)
    distance_till_win = 100 - max(scores)
    turn_total_objective = 100 // (distance_till_win / 2)
    if computer.turn_total >= turn_total_objective:
        return False
    return True

def greedy_rolls(computer, game):
    if computer.roll_count < 10:
        return True
    return False

def greedy_points(computer, game):
    if computer.turn_total < 30:
        return True
    return False

def ranking(computer, game):
    scores = []
    for i in range(game.number_of_players - 1):
        scores.append(game.computers[i+1].score)
    scores = sorted(scores, reverse=True)
    ranking = scores.index(computer.score) + 1
    if computer.roll_count < 2 * ranking:
        return True
    return False

def super_safe(computer, game):
    if computer.turn_total < 10:
        return True
    return False

def wild_card(computer, game):
    if randint(0, 1):
        return True
    return False

def cheating(computer, game):
    computer.score += 2
    if computer.turn_total >= 20:
        return False
    return True

computer_strategies = [nervous, roll_six, hold_till_20, ranking, greedy_points, greedy_rolls, super_safe, wild_card, cheating]

class Computer:
    def __init__(self, number):
        self.number = number
        self.score = 0
        self.turn_total = 0
        self.my_turn = False
        self.strategy = choice(computer_strategies)
        self.roll_count = 0

    def __str__(self):
        return f"Computer {self.number}"

    def take_turn(self):
        print(f"{self} is taking its turn.")
        while self.strategy(self, game):
            roll = randint(1, 6)
            print(f"{self} rolled: {roll}")
            if roll > 1:
                self.turn_total += roll
                self.roll_count += 1
            else:
                self.turn_total = 0
                self.roll_count = 0
                break
        self.score += self.turn_total
        print(f"Turn total: {self.turn_total}")
        self.turn_total = 0
        self.roll_count = 0
        self.my_turn = False
        return self

class Human:
    def __init__(self):
        self.turn_placement = 0
        self.score = 0
        self.turn_total = 0
        self.my_turn = False

    def __str__(self):
        return "You"

    def take_turn(self):
        print("Your turn.")
        while self.my_turn:
            decision = input(f"Turn total: {self.turn_total}. Roll or hold? ").lower()
            if decision == 'roll':
                roll = randint(1,6)
                print()
                print(f"You rolled: {roll}")
                print()
                if roll > 1:
                    self.turn_total += roll
                else:
                    self.turn_total = 0
                    self.my_turn = False
            elif decision == 'hold':
                self.score += self.turn_total
                print(f"Turn total: {self.turn_total}")
                self.turn_total = 0               
                self.my_turn = False
            else:
                print('That was not a valid input')
        return self

number_of_opponents = int(input("How many players do you want to play against? "))
game = Game(Human(), number_of_opponents)
game.determine_turn_order()

while game.running:
    game.current_player.take_turn()
    game.display_scores()
    game.check_win()
    game.switch_turns()
    if not game.running:
        play_again = input("Would you like to play again? (Y / N) ").lower()
        if play_again == "y":
            number_of_opponents = int(input("How many players do you want to play against? "))
            game = Game(Human(), number_of_opponents)
            game.determine_turn_order()
        else:
            print("Bye!")
