import pygame
from pygame.locals import *






#get initial state of the puzzle
f = open("puzzle.in", "r")
first_line = [int(i) for i in f.readline().split()]
second_line = [int(i) for i in f.readline().split()]
third_line = [int(i) for i in f.readline().split()]

board= []
board.append(first_line)
board.append(second_line)
board.append(third_line)
test = first_line + second_line + third_line

f.close()

print(board)




# constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#colors
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
TILE =          (241, 149, 155)

# kung saan nakalagay yung boarad sa screen
YMARGIN = int((SCREEN_HEIGHT - (80 * 3 + (3 - 1))) / 2)
XMARGIN = int((SCREEN_WIDTH- (80 * 3+ (3 - 1))) / 2)





# Main loop
def main():
    global screen, BASICFONT
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    BASICFONT = pygame.font.Font('freesansbold.ttf', 15)
    FPS = pygame.time.Clock()
    while running:
        # Fill the background with white
        screen.fill((WHITE))
        createBoard(board)
        # Look at every event in the queue
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                # kunin kung may na click ba na tile or wala
                top, side = click(board, event.pos[0], event.pos[1])

                blankt, blanks = blank(board) #kunin kung saan blank
                # compare yung na click sa position ng blank
                print(blankt, blanks)
                # pag + 1 sa side nasa left
                if top == blankt and side == blanks + 1:
                    print('left')
                    move(board, 'left')
                # pag - 1 sa side nasa right
                elif top == blankt and side == blanks - 1:
                    print('right')
                    move(board, 'right')
                # pag +1 sa top nasa taas
                elif top == blankt + 1  and side == blanks:
                    print('uo')
                    move(board, 'up')
                #pag -1 sa top nasa baba
                elif top == blankt - 1 and side == blanks:
                    print('down')
                    move(board, 'down')
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        screen.fill((WHITE))
        createBoard(board)
        if solved() == 1:
            print('Solved')
            textSurf = BASICFONT.render('Nice one pare, tapos mo na', True, BLACK)
            textRect = textSurf.get_rect()
            textRect.center = SCREEN_WIDTH/2, 450
            screen.blit(textSurf, textRect)
        pygame.display.update()
        FPS.tick(30)

def createTile(ptop, pleft, number):
    #      border  + pos * size +  gap
    left = XMARGIN + (pleft * 80) + (pleft - 1)
    top = YMARGIN + (ptop * 80) + (ptop - 1)
    #borders niya yung left top
    #draw the tile
    pygame.draw.rect(screen, TILE, (left, top, 80, 80))
    #draw the number
    textSurf = BASICFONT.render(str(number), True, WHITE)
    textRect = textSurf.get_rect()
    textRect.center = left + int(80 / 2), top + int(80 / 2)
    screen.blit(textSurf, textRect)


def createBoard(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] != 0:
                createTile(x, y, board[x][y])
    if isSolvable() == 0:
        textSurf = BASICFONT.render('Not Solvable, Kahit anong gawin mo di mo ma solve yan', True, BLACK)
        textRect = textSurf.get_rect()
        textRect.center = SCREEN_WIDTH/2, 100
        screen.blit(textSurf, textRect)
    else: 
        textSurf = BASICFONT.render('Solvable, try ka lang ', True, BLACK)
        textRect = textSurf.get_rect()
        textRect.center = SCREEN_WIDTH/2, 100
        screen.blit(textSurf, textRect)



def isSolvable():
    #check if solvable yung puzzle
    inversion_count = 0
    for x in range(0,9):
        for y in range(x+1, 9):
            if test[y] != 0 and test[x] != 0 and test[x] > test[y]:
                inversion_count+=1
    if inversion_count%2 == 0: 
        return 1
    else:
        return 0

def blank(board):
    # hahanapin lang yung tile kung saan yung 0
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                return (x, y)

def move(board, move):
    blankx, blanky = blank(board)

    #kasi nalaman na kanina kung anong direction nung clinick yung blank
    #ito is exchange niya yung blank at yung clinick
    if move == 'up':
        board[blankx][blanky] = board[blankx+ 1][blanky]
        board[blankx+ 1][blanky] = 0
    elif move == 'down':
        board[blankx][blanky] = board[blankx- 1][blanky]
        board[blankx- 1][blanky] = 0
    elif move == 'left':
        board[blankx][blanky] = board[blankx][blanky+1]
        board[blankx][blanky+1] = 0
    elif move == 'right':
        board[blankx][blanky] = board[blankx][blanky-1]
        board[blankx][blanky-1] = 0
    print(board)
    


def click(board, x, y):
    # rerecompute yung bounds nung each tile tapus i check if yung click is within dun
    for tileX in range(3):
        for tileY in range(3):
            left = XMARGIN + (tileY * 80) 
            top = YMARGIN + (tileX * 80) 
            tileRect = pygame.Rect(left, top, 80, 80)
            if tileRect.collidepoint(x, y):
                print(tileX,tileY)
                return (tileX, tileY)
    return (None, None)

def solved():
    #pag ganyan oks na
    if board == [[1,2,3],[4,5,6],[7,8,0]]:
        return 1
    else: return 0


if __name__ == '__main__':
    main()
    pygame.quit()

