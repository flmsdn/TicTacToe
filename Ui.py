from abc import ABC, abstractmethod
from Game import Game, GameError
from tkinter import *
from itertools import product

class Ui(ABC):
    '''Class to contain the UI'''
    @abstractmethod
    def run(self):
        raise NotImplementedError


class Gui(Ui):
    def __init__(self):
        root = Tk()
        #root.geometry("1080x720")
        root.title("Tic Tac Toe")
        frame = Frame(root)
        frame.pack()
        self.__root = root
        Button(
            frame,
            text="Help",
            command=self.__showHelp
        ).pack(fill=X)

        Button(
            frame,
            text="Play",
            command=self.__playGame
        ).pack(fill=X)

        Button(
            frame,
            text="Quit",
            command=self.__root.quit
        ).pack(fill=X)

        scroll = Scrollbar(frame)
        console = Text(frame, height=4, width=50)
        scroll.pack(side=RIGHT, fill=Y)
        console.pack(side=LEFT, fill=Y)
        scroll.config(command=console.yview)
        console.config(yscrollcommand=scroll.set)

        self.__root = root
        self.__console = console
        self.__gameWin=None

    def run(self):
        self.__root.mainloop()
    
    def __showHelp(self):
        pass

    def __playGame(self):
        if self.__gameWin: return
        self.__game = Game(True)

        gameWin = Toplevel(self.__root)
        gameWin.title("Game")
        frame = Frame(gameWin)
        frame.grid(row=0,column=0)

        Grid.columnconfigure(gameWin, 0, weight=1)
        Grid.rowconfigure(gameWin, 0, weight=1)
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        self.__buttons = [[None for _ in range(3)] for _ in range(3)]
        for row,col in product(range(3),range(3)):
            b=StringVar()
            b.set(self.__game.at(row+1,col+1))
            self.__buttons[row][col]=b

            cmd = lambda r=row, c=col: self.__play(r,c)
            Button(
                frame,
                textvariable=b,
                command=cmd
            ).grid(row=row,column=col,sticky=N + S + W + E)
        for i in range(3):
            Grid.columnconfigure(frame, i, weight=1)
            Grid.rowconfigure(frame, i, weight=1)
        self.__gameWin= gameWin
        Button (gameWin, text="Dismiss",command=self.__dismiss).grid(row=1,column=0)
    
    def __dismiss(self):
        self.__gameWin.destroy()
        self.__gameWin = None

    def __play(self,r,c):
        if self.__finished: return
        try:
            self.__game.play(r+1,c+1)
        except GameError as e:
            self.__console.insert(END,f"{e}\n")
        self.__buttons[r][c].set(self.__game.at(r+1,c+1))
        if self.__game.winner == Game.DRAW:
            self.__console.insert(END,f"Game was drawn\n")
            self.__finished=True
        elif self.__game.winner:
            self.__console.insert(END,f"Game was won by {self.__game.winner}\n")
            self.__finished=True

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
