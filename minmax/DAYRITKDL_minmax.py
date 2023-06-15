import tkinter as tk
from tkinter import *
import random

import copy

boardState = [['-','-','-'],
              ['-','-','-'],
              ['-','-','-']]

def main():
    # TODO: ASK user if ai will go first
    root = Tk()
    root.geometry("300x400")
    root.title("Min Max Algorithm")
    root.configure(bg="lightgray")

    label = tk.Label(root, text='What do you want to play?')
    label.place(x=75,y=50)

    x_player = tk.Button(root, text="X", command=lambda:createBoard('X', root, True), width= 10, height=3)
    x_player.pack()
    x_player.place(x=60,y=90)
    
    o_player = tk.Button(root, text="O", command=lambda:createBoard('O', root, True), width=10, height=3)
    o_player.pack()
    o_player.place(x=160,y=90)

    root.mainloop()


def createBoard(player, screen, first):
    for widgets in screen.winfo_children():
        widgets.destroy()
    

    bot = 'O'
    global boardState
    if player == 'O':
        bot = 'X'
        if first == True:
            place = [0,2]
            boardState[random.choice(place)][random.choice(place)] = bot
    
    if stateCheck(player, boardState) == True:
        endScreen("CONGRATS", screen, player)
    elif stateCheck(bot, boardState) == True:
        endScreen("YOU LOSE", screen, player)
    elif  stateCheck(bot, boardState) == "DRAW" or stateCheck(player, boardState) == "DRAW":
       endScreen("DRAW", screen, player)
    else:
        possible = []
        
        for x in range(3):
            possible.append(x)
            possible[x] = []
            for y in range(3):
                if boardState[x][y] == '-':
                    possible[x].append(y)
                elif boardState[x][y] == player:
                    tk.Label(screen, text=boardState[x][y], width=12, height=6, background="lightblue").place(x=5+y*100,y=5+x*100)
                elif boardState[x][y] == bot:
                    tk.Label(screen, text=boardState[x][y], width=12, height=6, background="pink").place(x=5+y*100,y=5+x*100)
        

        button = {}
        count = 0
        #https://stackoverflow.com/questions/27198287/tkinter-create-multiple-buttons-with-different-command-function
        for rows in possible:
            for cols in rows:
                name = str(count) + str(cols)
                button[name] = tk.Button(screen, text=boardState[count][cols],command=lambda count=count,cols=cols :clicked(player,screen, count,cols), width=12, height=6)
                button[name].pack()
                button[name].place(x=5+(cols*100),y=5+(count*100))
            count+=1


def endScreen(status,screen, player):
    bot = 'O'
    global boardState
    if player == 'O':
        bot = 'X'
    for x in range(3):
            for y in range(3):
                if boardState[x][y] == '-':
                    tk.Label(screen, text=boardState[x][y], width=12, height=6).place(x=5+y*100,y=5+x*100)
                elif boardState[x][y] == player:
                    tk.Label(screen, text=boardState[x][y], width=12, height=6, background="lightblue").place(x=5+y*100,y=5+x*100)
                elif boardState[x][y] == bot:
                    tk.Label(screen, text=boardState[x][y], width=12, height=6, background="pink").place(x=5+y*100,y=5+x*100)
    tk.Label(screen, text= status, width=12, height=6, background="gray").place(x=100,y=300)

def clicked(player,screen, row, col):
    move(player, row, col)
    createBoard(player, screen, False)

#==========================================================================================================================================
# function that will print current board state
def printBoard(boardState):
    print("    0   1   2")
    for i in range(3):
        print("  -------------")
        print("{0} |".format(i),end='')
        for j in range(3):
            print(" {0} |".format(boardState[i][j]),end='')
        print()
    print("  -------------")

# replaces a coordinate in the board with a piece
def move(player, row, col):
    bot = 'O'
    if player == 'O':
        bot = 'X'
    global boardState
    if boardState[row][col] == '-':
        boardState[row][col] = player
        botMove(bot)

# check if board has finished state
# finished state is when 3 of the same symbol appeared in a line
def stateCheck(player, boardState):
    # 11 finished states
    for x in range(3):
        if x == 0 :
            #0th row horizontal
            if boardState[x][0] == player and boardState[x][1] == player and boardState[x][2]== player :
                return True
            #0th column vertical
            if boardState[x][0] == player and boardState[x+1][0]== player  and boardState[x+2][0]== player :
                return True
        if x == 1 :
            #1st row horizontal
            if boardState[x][0] == player and boardState[x][1] == player and boardState[x][2]== player :
                return True
            #1st column vertical
            x -=1
            if boardState[x][1] == player and boardState[x+1][1] == player and boardState[x+2][1]== player :
                return True
        if x == 2 :
            #2nd row horizontal
            if boardState[x][0] == player and boardState[x][1]== player  and boardState[x][2]== player :
                return True
            #2nd column vertical
            x -=2
            if boardState[x][2] == player and boardState[x+1][2]== player  and boardState[x+2][2]== player :
                return True
    # check for diagonals
    if boardState[1][1] == player:
        # check for backward diagonal \
        if boardState[0][0] == player and boardState[2][2] == player :
            return True
        # check for forward diagonal /
        if boardState[0][2] == player and boardState[2][0] == player :
            return True
    # check for draws
    # if all tiles are field but there are no winners it is a draw
    filled = True
    for i in range(3):
        for j in range(3):
            if boardState[i][j] == '-':
                filled = False
    if filled == True:
        return "DRAW"
    # if nothing then false
    return False

#generates the moves of the bot
# maximize the bot
# minimuze the player
# TODO: natatalo yung bot, di dapat
# TODO: lagyan ng counter kung ilang state para malaman ang fastest
# TODO: lagyan ng comparison sa loob mismo ng min max function (comparison is yung pipili kung ano yung best sa moveset)
def botMove(bot):
    global boardState
    board = copy.deepcopy(boardState)
    maxMove(bot,board)


def maxMove(player, board):
    global boardState
    next = 'O'
    if player == 'O':
        next = 'X'
    # bale panalo yung previous player
    if stateCheck(next, board) == True:
        return -1 
    elif stateCheck(next, board) == "DRAW":
        return 0

    #generate moves
    m = -1000000000
    moveset = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                moveset.append([i,j])
    #dictionary of actions that has a score of 1 
    choice = []
    for action in moveset:
        x,y = action
        next_board = copy.deepcopy(board)
        next_board[x][y] = player
        v = minMove(next, next_board)
        if v > m:
            m = v
            choice = [x,y]
    next_board = copy.deepcopy(board)
    next_board[choice[0]][choice[1]] = player
    boardState = copy.deepcopy(next_board)
    return m



def minMove(player, board):
    global boardState
    next = 'O'
    if player == 'O':
        next = 'X'
    # bale panalo yung previous player
    if stateCheck(next, board) == True:
        return 1
    elif stateCheck(next, board) == "DRAW":
        return 0

    #generate moves
    m = 1000000000
    moveset = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                moveset.append([i,j])

    #dictionary of actions that has a score of 1 
    choice = []
    for action in moveset:
        x,y = action
        next_board = copy.deepcopy(board)
        next_board[x][y] = player
        v= maxMove(next, next_board)
        if v < m:
            m = v
            choice = [x,y]
    next_board = copy.deepcopy(board)
    next_board[choice[0]][choice[1]] = player
    boardState = copy.deepcopy(next_board)
    return m




if __name__ == '__main__':
    main()
