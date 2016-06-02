__author__ = 'Alastair'
import random, pygame, sys, time
from pygame.locals import *#

BOARDWIDTH = 100
BOARDHEIGHT = 100
SQUARESIZE = 20
MINES = 1000
WINDOWWIDTH = (BOARDWIDTH * SQUARESIZE) + 1
WINDOWHEIGHT = (BOARDHEIGHT * SQUARESIZE) + 1
FPS = 30
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
BGCOLOUR = GRAY
Square = pygame.image.load('MinesweaperSquare20px.jpg')  # Loads in icons
PressedSquare = pygame.image.load('MinesweaperPressedSquare.jpg')
MouseSquare = pygame.image.load('MinesweaperMouseSquare.jpg')
Mine = pygame.image.load('MinesweaperMine.jpg')
Flag = pygame.image.load('MinesweaperFlag.jpg')
num = [0] * 8
num[0] = pygame.image.load('Minesweeper_1.png')  # Loads in number pictures
num[1] = pygame.image.load('Minesweeper_2.png')
num[2] = pygame.image.load('Minesweeper_3.png')
num[3] = pygame.image.load('Minesweeper_4.png')
num[4] = pygame.image.load('Minesweeper_5.png')
num[5] = pygame.image.load('Minesweeper_6.png')
num[6] = pygame.image.load('Minesweeper_7.png')
num[7] = pygame.image.load('Minesweeper_8.png')


def main():

    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    mousex = 0
    mousey = 0
    currentSquare = [0, 0]
    pygame.display.set_caption('Minesweaper')
    DISPLAYSURF.fill(BGCOLOUR)
    MINELOCATION = generateBoard(MINES)  # Generates mine locations and numbers
    GAMEBOARD = [[3 for j in range(BOARDHEIGHT)] for i in range(BOARDWIDTH)]  # Sets all squares to blank (3 is blank 0 is uncovered)

    while True:
        mouseClicked = False
        checkwin(GAMEBOARD, MINELOCATION, currentSquare)
        DISPLAYSURF.fill(BGCOLOUR)
        drawBoard(GAMEBOARD, MINELOCATION, currentSquare)
        MouseDown = False
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                boxx, boxy = getBoxAtPixle(mousex, mousey)
                currentSquare = [boxx, boxy]
            elif event.type == MOUSEBUTTONDOWN:
                MouseDown = True
            elif event.type == MOUSEBUTTONUP:
                buttonPressed = event.button
                mousex, mousey = event.pos
                boxx, boxy = getBoxAtPixle(mousex, mousey)
                mouseClicked = True
        if mouseClicked:

            if buttonPressed == 1:
                if GAMEBOARD[boxx][boxy] != 0:
                    if MINELOCATION[boxx][boxy] == "mine":
                        gameOver()
                    else:
                        if MINELOCATION[boxx][boxy] == 0:
                            GAMEBOARD = uncoverSquares(GAMEBOARD, MINELOCATION, boxx, boxy)
                        else:
                            GAMEBOARD[boxx][boxy] = 0
            if buttonPressed == 3:
                if GAMEBOARD[boxx][boxy] != 0:
                    GAMEBOARD[boxx][boxy] = 1

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawBoard(GAMEBOARD, MINELOCATION, currantSquare):
    for LINES in range(0, WINDOWWIDTH, SQUARESIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (LINES, 0), (LINES, WINDOWHEIGHT))
    for LINES in range(0, WINDOWHEIGHT, SQUARESIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (0, LINES), (WINDOWWIDTH, LINES))
    for boxX in range(BOARDWIDTH):
        for boxY in range(BOARDHEIGHT):
            xcoord, ycoord = getCoordsOfBox(boxX, boxY)
            if GAMEBOARD[boxX][boxY] == 0:
                if MINELOCATION[boxX][boxY] == "mine":
                    DISPLAYSURF.blit(Mine, (xcoord, ycoord))
                elif MINELOCATION[boxX][boxY] != 0:
                    DISPLAYSURF.blit(num[(MINELOCATION[boxX][boxY]) - 1], (xcoord, ycoord))
            elif GAMEBOARD[boxX][boxY] == 1:
                DISPLAYSURF.blit(Flag, (xcoord, ycoord))
            else:
                DISPLAYSURF.blit(Square, (xcoord, ycoord))
    if GAMEBOARD[currantSquare[0]][currantSquare[1]] == 3:
        coordx, coordy = getCoordsOfBox(currantSquare[0], currantSquare[1])
        DISPLAYSURF.blit(MouseSquare, (coordx, coordy))


def getCoordsOfBox(x, y):
    xcoord = x * SQUARESIZE
    ycoord = y * SQUARESIZE
    return xcoord, ycoord


def getBoxAtPixle(xcoord, ycoord):
        x = -1
        y = -1
        while xcoord > 0:
            xcoord -= SQUARESIZE
            x += 1
        while ycoord > 0:
            ycoord -= SQUARESIZE
            y += 1
        return x, y


def gameOver():
    i = 0
    p = 0
    j = 0
    k = 255
    myfont = pygame.font.SysFont("impact", 60)
    while True:
        if i < 101:
            if i % 3 == 0:
                DISPLAYSURF.fill((255, 51 + p, 51 + p))
            elif i % 3 == 1:
                DISPLAYSURF.fill((255, 153 + j, 51 + p))
            elif i % 3 == 2:
                DISPLAYSURF.fill((255, 225, 51 + p))
            if i % 2 == 0:
                j += 2
            i += 1
            p += 2
        if k > 2 and i % 2 == 1:
            k -= 2
        message = myfont.render("You Loose", 1, (k, k, k))
        DISPLAYSURF.blit(message, (80, 80))

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def uncoverSquares(GAMEBOARD, MINELOCATION, x, y):
    if MINELOCATION[x][y] == 0:
        GAMEBOARD[x][y] = 0
    for i in [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]:
        try:
            if (x + i[0]) >= 0 and (y + i[1]) >= 0:
                if GAMEBOARD[x + i[0]][y + i[1]] == 3:
                    GAMEBOARD[x + i[0]][y + i[1]] = 0
                    if MINELOCATION[x + i[0]][y + i[1]] == 0:
                        uncoverSquares(GAMEBOARD, MINELOCATION, x + i[0], y + i[1])
        except IndexError:
            pass
    return GAMEBOARD


def checkwin(GAMEBOARD, MINELOCATION, currentSquare):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if MINELOCATION[x][y] == "mine":
                if GAMEBOARD[x][y] != 1:
                    return None
    myfont = pygame.font.SysFont("impact", 60)
    message = myfont.render("You Win", 1, BLACK)
    i = 0
    drawBoard(GAMEBOARD, MINELOCATION, currentSquare)
    display = True
    while True:
        if i % 20 == 0:
            display = not display
        if display:
            DISPLAYSURF.blit(message, (80, 80))
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)




def generateBoard(Mines):
    GAMEBOARD = [[0 for j in range(BOARDHEIGHT)] for i in range(BOARDWIDTH)]
    while Mines >= 1:  # Generates mine locations
        randX = random.randint(0, BOARDWIDTH - 1)
        randY = random.randint(0, BOARDHEIGHT - 1)
        if GAMEBOARD[randX][randY] == 0:
            GAMEBOARD[randX][randY] = "mine"
            Mines -= 1
    for boxX in range(BOARDWIDTH):  # Generates the numbers
        for boxY in range(BOARDHEIGHT):
            if GAMEBOARD[boxX][boxY] != "mine":
                for i in [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]:
                    try:
                        if (boxX + i[0]) >= 0 and (boxY + i[1]) >= 0:
                            if GAMEBOARD[boxX + i[0]][boxY + i[1]] == "mine":
                                GAMEBOARD[boxX][boxY] += 1
                    except IndexError:
                        pass

    return GAMEBOARD


if __name__ == '__main__':
    main()