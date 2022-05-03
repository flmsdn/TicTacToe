from Colours import Colour
class GameError(Exception):
    pass

class Game:

    EMPTY = "."
    P1 = Colour.BLUE + Colour.BOLD + "0" + Colour.ENDC
    P2 = Colour.RED + Colour.BOLD + "X" + Colour.ENDC
    DRAW = "draw"

    def __init__(self,GUI=False):
        if GUI: Game.P1,Game.P2 = "0", "X"
        self.__board = [[Game.EMPTY for _ in range(3)] for _ in range(3)]
        self.__player = Game.P1

    def __repr__(self):
        s="  | " + Colour.BOLD + Colour.YELLOW + "1 2 3" + Colour.ENDC + "\n---------\n"
        for c in range(3):
            s+=Colour.BOLD + Colour.YELLOW + f"{c+1}" + Colour.ENDC + " | " + " ".join(self.__board[c]) +"\n"
        return s

    def play(self,row,col):
        row -= 1
        col -= 1
        if self.__board[row][col] != Game.EMPTY:
            raise GameError("Cannot play here!")
        self.__board[row][col] = self.__player
        self.__player = Game.P2 if self.__player == Game.P1 else Game.P1
    
    def at(self,row, col):
        row-=1
        col-=1
        return self.__board[row][col]
    
    @property
    def winner(self):
        #check if a player has won
        rs = [list(set(r)) for r in self.__board]
        cs = [list(set(self.__board[row][col] for row in range(3))) for col in range(3)]
        d1 = list( set(self.__board[i][i] for i in range(3) ))
        d2 = list(set(self.__board[2-i][i] for i in range(3)))
        ptot = rs+cs+[d1]+[d2]
        stTot = "".join(["".join(x) for x in ptot])
        for a in ptot:
            if len(a)==1 and a[0]!=Game.EMPTY: return a[0]
        if Game.EMPTY not in stTot: return Game.DRAW
        return None

if __name__ == "__main__":
    #print(Game.winner)
    pass
