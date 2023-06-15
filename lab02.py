import pygame
import tkinter
import tkinter.filedialog
import copy
from pygame.locals import *



def prompt_file():
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name




#get initial state of the puzzle
def parseFile(name):
    global board, sol , test, initial
    f = open(name, "r")
    first_line = [int(i) for i in f.readline().split()]
    second_line = [int(i) for i in f.readline().split()]
    third_line = [int(i) for i in f.readline().split()]

    board= []
    board.append(first_line)
    board.append(second_line)
    board.append(third_line)
    initial = copy.deepcopy(board)
    sol = copy.deepcopy(board)
    test = first_line + second_line + third_line
    f.close()

path = []
done = []
board = []
sol = []
test = []
pathcost = 0




# constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#colors
BLACK =         (  0,   0,   0)
GRAY =          (192, 192, 192)
WHITE =         (255, 255, 255)
TILE =          (241, 149, 155)

# kung saan nakalagay yung boarad sa screen
YMARGIN = int((SCREEN_HEIGHT - (80 * 3 + (3 - 1))) / 2)
XMARGIN = int((SCREEN_WIDTH- (80 * 3+ (3 - 1))) / 2)




# Main loop
def main():
    parseFile("puzzle.in")
    solution = None
    global screen,board, path, BASICFONT, sol, done, initial
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    BASICFONT = pygame.font.Font('freesansbold.ttf', 15)
    FPS = pygame.time.Clock()
    while running:
        # Fill the background with white
        screen.fill((WHITE))
        if solution == None:
            createBoard(board)
        else : 
            createBoard(sol)
        buttons(solution)
        # Look at every event in the queue
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                # kunin kung may na click ba na tile or wala
                top, side = click( event.pos[0], event.pos[1])

                blankt, blanks = blank(board) #kunin kung saan blank
                print("blank =" ,blankt, blanks)
                # compare yung na click sa position ng blank
                if top == 0 and side == 9 and solution == None:
                    print("BFS")
                    sol = copy.deepcopy(initial)
                    solution = 'BFS'
                    BFS()
                elif top == 0 and side == 9 and solution == 'BFS':
                    if len(path) > 0:
                        next()
                    else : 
                        board = sol
                        solution = None
                        path = []
                        done = []
                elif top ==1 and side ==9 and solution == None:
                    solution = 'DFS'
                    sol = copy.deepcopy(initial)
                    print("DFS")
                    DFS()
                elif top ==1 and side ==9 and solution == 'DFS':
                    if len(path) > 0:
                        next()
                    else : 
                        board = sol
                        solution = None
                        path = []
                        done = []
                elif solution!='BFS' and solution!='DFS' and solution!='A STAR': 
                    solution = None

                # pag + 1 sa side nasa left
                if top == blankt and side == blanks + 1 and solution == None:
                    print('right')
                    move(board, 'right')
                    print(board)
                # pag - 1 sa side nasa right
                elif top == blankt and side == blanks - 1 and solution == None:
                    print('left')
                    move(board, 'left')
                    print(board)
                # pag +1 sa top nasa taas
                elif top == blankt + 1  and side == blanks and solution == None:
                    print('down')
                    move(board, 'down')
                    print(board)
                #pag -1 sa top nasa baba
                elif top == blankt - 1 and side == blanks and solution == None:
                    print('up')
                    move(board, 'up')
                    print(board)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    f = prompt_file()
                    print(f)
                    parseFile(f)

            elif event.type == QUIT:
                running = False

        if solved() == 1:
            textSurf = BASICFONT.render('Nice one pare, Panalo ka na', True, BLACK)
            textRect = textSurf.get_rect()
            textRect.center = SCREEN_WIDTH/2, 440
            screen.blit(textSurf, textRect)
            if pathcost >0:
                pathSurf = BASICFONT.render('Path cost : ' + str(pathcost) , True, BLACK)
                pathRect = pathSurf.get_rect()
                pathRect.center = SCREEN_WIDTH/2, 465
                screen.blit(pathSurf, pathRect)
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

def buttons(text):
    for x in range(2):
        i = 2 + x 
        pygame.draw.rect(screen, TILE, (600, (SCREEN_HEIGHT/6) * i - 10, 60, 40))
        if x == 0:
            if text == 'BFS':
                textSurf = BASICFONT.render('NEXT', True, BLACK)
            else: 
                textSurf = BASICFONT.render('BFS', True, BLACK)
            textRect = textSurf.get_rect()
            textRect.center = 600 + 30 , (SCREEN_HEIGHT/6) * i - 10 + 20,
            screen.blit(textSurf, textRect)
        if x == 1:
            if text == 'DFS':
                textSurf = BASICFONT.render('NEXT', True, BLACK)
            else: 
                textSurf = BASICFONT.render('DFS', True, BLACK)
            textRect = textSurf.get_rect()
            textRect.center = 600 + 30 , (SCREEN_HEIGHT/6) * i - 10 + 20,
            screen.blit(textSurf, textRect)
    


def createBoard(b):
    for x in range(len(b)):
        for y in range(len(b[0])):
            if b[x][y] != 0:
                createTile(x, y, b[x][y])

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

    showSolution()



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

def blank(b):
    # hahanapin lang yung tile kung saan yung 0
    for x in range(3):
        for y in range(3):
            if b[x][y] == 0:
                return (x, y)

def move(b, move):
    blankx, blanky = blank(b)

    #kasi nalaman na kanina kung anong direction nung clinick yung blank
    #ito is exchange niya yung blank at yung clinick
    if move == 'down':
        b[blankx][blanky] = b[blankx+ 1][blanky]
        b[blankx+ 1][blanky] = 0
    elif move == 'up':
        b[blankx][blanky] = b[blankx- 1][blanky]
        b[blankx- 1][blanky] = 0
    elif move == 'right':
        b[blankx][blanky] = b[blankx][blanky+1]
        b[blankx][blanky+1] = 0
    elif move == 'left':
        b[blankx][blanky] = b[blankx][blanky-1]
        b[blankx][blanky-1] = 0
    


def click(x, y):
    # rerecompute yung bounds nung each tile tapus i check if yung click is within dun
    for tileX in range(3):
        for tileY in range(3):
            left = XMARGIN + (tileY * 80) 
            top = YMARGIN + (tileX * 80) 
            tileRect = pygame.Rect(left, top, 80, 80)
            if tileRect.collidepoint(x, y):
                print("tile =",tileX,tileY)
                return (tileX, tileY)
    
    for j in range(2):
        i = 2 + j 
        tileRect = pygame.Rect(600, (SCREEN_HEIGHT/6) * i - 10, 60, 40)
        if tileRect.collidepoint(x, y):
                return(j, 9)
    return (None, None)

def BFS():
    blankx, blanky = blank(initial)
    frontier = []
    explored = []
    # na explore na syempre yung initial
    current = copy.deepcopy(initial)
    current.append('')
    frontier.append(copy.deepcopy(current))
    # set up yung initial frontier
    # gagawin kasing loop is while frontier is not empty
    # so i populate muna frontier gamit initial values galing dun
    
    while len(frontier) > 0: 
        current = frontier.pop(0)
        b = current[:-1]
        direction = current[3]
        if b== [[1,2,3],[4,5,6],[7,8,0]]:
            explored.append(copy.deepcopy(current))
            p = direction
            break
        elif b in explored:
            continue
        else :
            explored.append(copy.deepcopy(b))
            blankx, blanky = blank(b)
            if blankx-1 >= 0: 
                temp = copy.deepcopy(b)
                move(b,'up')
                temp1 = direction
                direction = direction + ' U'
                b.append(direction)
                frontier.append(b)
                b = copy.deepcopy(temp)
                direction = temp1
            if blanky+1 <= 2: 
                temp = copy.deepcopy(b)
                move(b, 'right')
                temp1 = direction
                direction = direction + ' R'
                b.append(direction)
                frontier.append(b)
                b = copy.deepcopy(temp)
                direction = temp1
            if blankx+1 <= 2: 
                temp = copy.deepcopy(b)
                move(b, 'down')
                temp1 = direction
                direction = direction + ' D'
                b.append(direction)
                frontier.append(b)
                b = copy.deepcopy(temp)
                direction = temp1
            if blanky-1 >= 0:
                temp = copy.deepcopy(b)
                move(b, 'left')
                temp1 = direction
                direction = direction + ' L'
                b.append(direction)
                frontier.append(b)
                b = copy.deepcopy(temp)
                direction = temp1
    f = open("puzzle.out", "w")
    f.write(p)
    f.close()
    global path, pathcost
    path = p.split()
    pathcost = len(path)
    print(p)
    print(len(path))
    print(len(explored))

    # eto plano
    # bawat append sa frontier is may kasama path taken (string siya) kunwari ' U R D L'
    # bale magiging [[[[1,2,3],[4,5,6],[7,8,0]],' U R D L']] siya
    # yan is per state
    # ang i checheck lang is yung yung state para check if okay na
    # para kahit di na siguro node
    # yung string is mag + na lang kung anong klase yung ginawa bale 'U' + 'R'
    # python naman eh
    # tapus kada press na lang ng next  is kukunin niya solution den move base dun
    # lagay na lang siguro ng isa pang variable solved  para di na to i call ulit pag i next
    # gawa so bago function na next
    # lagyan ng explored list
    # sheeeeeeeesh gumana naman 
    # kaso napakabagal lol

def DFS():
    blankx, blanky = blank(initial)
    frontier = []
    explored = []
    current = copy.deepcopy(initial)
    current.append('')
    frontier.append(copy.deepcopy(current))
    while len(frontier) > 0: 
        current = frontier.pop()
        b = current[:-1]
        direction = current[3]
        if b== [[1,2,3],[4,5,6],[7,8,0]]:
            explored.append(copy.deepcopy(current))
            p = direction
            break
        elif b in explored:
            continue
        if b not in explored: 
            explored.append(copy.deepcopy(b))
            blankx, blanky = blank(b)
            if blankx-1 >= 0: 
                temp = copy.deepcopy(b)
                move(b,'up')
                temp1 = direction
                direction = direction + ' U'
                b.append(direction)
                frontier.append(b)
                b = copy.deepcopy(temp)
                direction = temp1
            if blanky+1 <= 2: 
                temp = copy.deepcopy(b)
                move(b, 'right')
                temp1 = direction
                direction = direction + ' R'
                b.append(direction)
                frontier.append(b)
                b = copy.deepcopy(temp)
                direction = temp1
            if blankx+1 <= 2: 
                temp = copy.deepcopy(b)
                move(b, 'down')
                temp1 = direction
                direction = direction + ' D'
                b.append(direction)
                frontier.append(b)
                b = copy.deepcopy(temp)
                direction = temp1
            if blanky-1 >= 0:
                temp = copy.deepcopy(b)
                move(b, 'left')
                temp1 = direction
                direction = direction + ' L'
                b.append(direction)
                frontier.append(b)
                b = copy.deepcopy(temp)
                direction = temp1
            
        # binaliktad kasi di ba order checking is U R D L 
        # so ang alam ko first depth na i explore is sa U 
        # so dapat yung U ang nasa taas ng stack lagi 
        # bale siya last na i check dito 
    f = open("puzzle.out", "w")
    f.write(p)
    f.close()
    global path, pathcost
    path = p.split()
    pathcost = len(path)
    print(p)
    print(len(path))
    print(len(explored))


def next():
    cur = path.pop(0)
    print(cur)
    if cur == 'U':
        move(sol,'up')
    elif cur == 'R': 
        move(sol,'right')
    elif cur == 'D':
        move(sol, 'down')
    elif cur == 'L':
        move(sol,'left')
    global done
    done.append(copy.deepcopy(cur))
    print(done)
    print(path)

def solved():
    #pag ganyan oks na
    if board == [[1,2,3],[4,5,6],[7,8,0]]:
        return 1
    else: return 0

def showSolution():
    for d in range(len(done)):
        textSurf = BASICFONT.render(done[d], True, BLACK)
        textRect = textSurf.get_rect()
        textRect.center = 10 + d*10 , 500
        screen.blit(textSurf, textRect)

    last = len(done)*10 + 10
    for r in range(len(path)):
        textSurf = BASICFONT.render(path[r], True, GRAY)
        textRect = textSurf.get_rect()
        textRect.center = last + r*10 , 500
        screen.blit(textSurf, textRect)





if __name__ == '__main__':
    main()
    pygame.quit()

