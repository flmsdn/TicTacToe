from abc import ABC, abstractmethod
from Game import Game, GameError

class Ui(ABC):
    '''Class to contain the UI'''
    @abstractmethod
    def run(self):
        raise NotImplementedError


class Gui(Ui):
    def __init__(self):
        pass

    def run(self):
        pass

class Terminal(Ui):
    def __init__(self):
        self.__game = Game()

    def __getInput(self):
        while True:
            try:
                row, col = int(input("Enter Row: ")), int(input("Enter Column: "))
                if row in range(1,4) and col in range(1,4):
                    break
                else:
                    print("Invalid Input, please try again")
            except ValueError:
                print("Invalid Input, please try again")
        return row,col

    def run(self):
        while self.__game.winner == None:
            print(self.__game)
            row, col = self.__getInput()
            try:
                self.__game.play(row, col)
            except GameError as e:
                print(e)
        print(self.__game)
        if self.__game.winner == Game.DRAW:
            print("The game was drawn")
        else:
            print(f"The winner is {self.__game.winner}")
