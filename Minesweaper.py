__author__ = 'Alastair'
import random, pygame, sys, time
from pygame.locals import *
BOARDWIDTH = 0
BOARDHEIGHT = 0
SQUARESIZE = 20
MINES = 0
WINDOWWIDTH = 0
WINDOWHEIGHT = 0
FONTSIZE = 0
FPS = 30
MODE = ""
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BGCOLOUR = GRAY
Square = pygame.image.load('MinesweaperSquare20px.jpg')  # Loads in icons
PressedSquare = pygame.image.load('MinesweaperPressedSquare.jpg')
MouseSquare = pygame.image.load('MinesweaperMouseSquare.jpg')
Mine = pygame.image.load('MinesweaperMine.png')
Flag = pygame.image.load('MinesweaperFlag.jpg')
ExplodedMine = pygame.image.load('MinesweaperExplodedMine.png')
FalseMine = pygame.image.load('MinesweaperFalseMine.png')
UnpressedButton = pygame.image.load('MinesweaperUnpressedButton.png')
PressedButton = pygame.image.load('MinesweaperPressedButton.png')
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

    global FPSCLOCK, DISPLAYSURF, BOARDWIDTH, BOARDHEIGHT, MINES, WINDOWWIDTH, WINDOWHEIGHT, FONTSIZE, MODE
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    BOARDWIDTH, BOARDHEIGHT, MINES, FONTSIZE, MODE = titleScreen()
    WINDOWWIDTH = (BOARDWIDTH * SQUARESIZE) + 1
    WINDOWHEIGHT = (BOARDHEIGHT * SQUARESIZE) + 1
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    TimeStart = time.clock()
    pygame.display.set_caption('Minesweaper :o  ' + str(180 - int(time.clock() // 1)) + ' seconds')
    currentSquare = [0, 0]
    GameOver = False
    DISPLAYSURF.fill(BGCOLOUR)
    MINELOCATION = generateBoard(MINES)  # Generates mine locations and numbers
    GAMEBOARD = [[3 for j in range(BOARDHEIGHT)] for i in range(BOARDWIDTH)]  # Sets all squares to blank (3 is blank 0 is uncovered)
    while True:
        face = ":)"
        mouseClicked = False
        checkwin(GAMEBOARD, MINELOCATION, currentSquare)
        drawBoard(GAMEBOARD, MINELOCATION, currentSquare, False)
        MouseDown = False
        if MODE == "Time trial" and 180 - int(time.clock() // 1) <= 0:
            gameOver(MINELOCATION, GAMEBOARD, currentSquare)
        elif MODE == "Time trial":
            currentTime = 180 - int(time.clock() // 1)
        else:
            currentTime = int(time.clock() // 1)
        pygame.display.set_caption('Minesweaper ' + face + '   ' + str(currentTime) + ' seconds')
        if GameOver:
            gameOver(MINELOCATION, GAMEBOARD, currentSquare)
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
                face = ":o"
            elif event.type == MOUSEBUTTONUP:
                face = ":)"
                buttonPressed = event.button
                mousex, mousey = event.pos
                boxx, boxy = getBoxAtPixle(mousex, mousey)
                mouseClicked = True
            elif event.type == KEYUP and event.key == K_SPACE:
                mouseClicked = True
                buttonPressed = 2
        if mouseClicked:
            if buttonPressed == 1:
                if GAMEBOARD[boxx][boxy] != 0:
                    if MINELOCATION[boxx][boxy] == "mine":
                        GameOver = True
                    else:
                        if MINELOCATION[boxx][boxy] == 0:
                            GAMEBOARD = uncoverSquares(GAMEBOARD, MINELOCATION, boxx, boxy)
                        else:
                            GAMEBOARD[boxx][boxy] = 0
            if buttonPressed == 3:
                if GAMEBOARD[boxx][boxy] == 3:
                    GAMEBOARD[boxx][boxy] = 1
                elif GAMEBOARD[boxx][boxy] == 1:
                    GAMEBOARD[boxx][boxy] = 3
            if buttonPressed == 2:
                if GAMEBOARD[boxx][boxy] == 0:
                    mineNum = 0
                    for i in [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]:
                        try:
                            if (boxx + i[0]) >= 0 and (boxy + i[1]) >= 0:
                                if GAMEBOARD[boxx + i[0]][boxy + i[1]] == 1:
                                    mineNum += 1
                        except IndexError:
                            pass
                    if mineNum == MINELOCATION[boxx][boxy]:
                        for i in [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]:
                            try:
                                if (boxx + i[0]) >= 0 and (boxy + i[1]) >= 0:
                                    if GAMEBOARD[boxx + i[0]][boxy + i[1]] == 3:
                                        if MINELOCATION[boxx + i[0]][boxy + i[1]] == 0:
                                            GAMEBOARD = uncoverSquares(GAMEBOARD, MINELOCATION, boxx + i[0], boxy + i[1])
                                        elif MINELOCATION[boxx + i[0]][boxy + i[1]] == "mine":
                                            GameOver = True
                                        else:
                                            GAMEBOARD[boxx + i[0]][boxy + i[1]] = 0
                            except IndexError:
                                pass
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawBoard(GAMEBOARD, MINELOCATION, currantSquare, gameOver):
    DISPLAYSURF.fill(BGCOLOUR)
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
    coordx, coordy = getCoordsOfBox(currantSquare[0], currantSquare[1])
    if GAMEBOARD[currantSquare[0]][currantSquare[1]] == 3:
        DISPLAYSURF.blit(MouseSquare, (coordx, coordy))
    elif GAMEBOARD[currantSquare[0]][currantSquare[1]] == 0 and MINELOCATION[currantSquare[0]][currantSquare[1]] == "mine":
        DISPLAYSURF.blit(ExplodedMine, (coordx, coordy))
    elif gameOver:
        for i in [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]:
            if MINELOCATION[currantSquare[0] + i[0]][currantSquare[1] + i[1]] == "mine":
                coordx, coordy = getCoordsOfBox(currantSquare[0] + i[0], currantSquare[1] + i[1])
                DISPLAYSURF.blit(ExplodedMine, (coordx, coordy))
            elif GAMEBOARD[currantSquare[0] + i[0]][currantSquare[1] + i[1]] == 1:
                coordx, coordy = getCoordsOfBox(currantSquare[0] + i[0], currantSquare[1] + i[1])
                DISPLAYSURF.blit(FalseMine, (coordx, coordy))



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


def gameOver(MINELOCATION, GAMEBOARD, currentSquare):
    pygame.display.set_caption('Minesweaper x(')
    for boxX in range(BOARDWIDTH):
        for boxY in range(BOARDHEIGHT):
            if MINELOCATION[boxX][boxY] == "mine":
                GAMEBOARD[boxX][boxY] = 0
    drawBoard(GAMEBOARD, MINELOCATION, currentSquare, True)
    myfont = pygame.font.SysFont("consolas", FONTSIZE)
    message = myfont.render("You Lose", 1, BLACK)
    DISPLAYSURF.blit(message, (20, 20))
    i = 0
    p = 0
    Colour = BLACK
    while True:
        i += 1

        if i % 40 == 0:
            Colour = BLACK
        elif i % 20 == 0:
            Colour = RED
        message = myfont.render("You Lose", 1, Colour)
        DISPLAYSURF.blit(message, (20, 20))
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def titleScreen():
    button1 = UnpressedButton
    button2 = UnpressedButton
    button3 = UnpressedButton
    button4 = UnpressedButton
    DISPLAYSURF = pygame.display.set_mode((400, 400))
    myfont = pygame.font.SysFont("consolas", 35)
    myfont2 = pygame.font.SysFont("consolas", 60)
    while True:
        DISPLAYSURF.fill(BGCOLOUR)
        DISPLAYSURF.blit(button1, (100, 120))
        DISPLAYSURF.blit(button2, (100, 200))
        DISPLAYSURF.blit(button3, (100, 270))
        DISPLAYSURF.blit(button4, (100, 340))
        message1 = myfont.render("Easy", 1, BLACK)
        message2 = myfont.render("Medium", 1, BLACK)
        message3 = myfont.render("Hard", 1, BLACK)
        message4 = myfont.render("Time trial", 1, BLACK)
        message5 = myfont2.render("MINESWEEPER", 1, BLACK)
        DISPLAYSURF.blit(message1, (165, 130))
        DISPLAYSURF.blit(message2, (145, 210))
        DISPLAYSURF.blit(message3, (165, 280))
        DISPLAYSURF.blit(message4, (105, 350))
        DISPLAYSURF.blit(message5, (22, 30))
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                buttonRect1 = pygame.Rect(100, 120, 200, 50)
                if buttonRect1.collidepoint(mousex, mousey):
                    button1 = PressedButton
                buttonRect2 = pygame.Rect(100, 200, 200, 50)
                if buttonRect2.collidepoint(mousex, mousey):
                    button2 = PressedButton
                buttonRect3 = pygame.Rect(100, 270, 200, 50)
                if buttonRect3.collidepoint(mousex, mousey):
                    button3 = PressedButton
                buttonRect4 = pygame.Rect(100, 340, 200, 50)
                if buttonRect4.collidepoint(mousex, mousey):
                    button4 = PressedButton
            elif event.type == MOUSEBUTTONUP:
                buttonRect1 = pygame.Rect(100, 120, 200, 50)
                if buttonRect1.collidepoint(mousex, mousey):
                    return 10, 10, 15, 35, "Easy"
                buttonRect2 = pygame.Rect(100, 200, 200, 50)
                if buttonRect2.collidepoint(mousex, mousey):
                    return 25, 25, 80, 105, "Medium"
                buttonRect3 = pygame.Rect(100, 270, 200, 50)
                if buttonRect3.collidepoint(mousex, mousey):
                    return 60, 40, 300, 260, "Hard"
                buttonRect4 = pygame.Rect(100, 340, 200, 50)
                if buttonRect4.collidepoint(mousex, mousey):
                    return 60, 40, 300, 260, "Time trial"
                button1 = UnpressedButton
                button2 = UnpressedButton
                button3 = UnpressedButton
                button4 = UnpressedButton
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
    myfont = pygame.font.SysFont("consolas", FONTSIZE)
    message = myfont.render("You Win", 1, BLACK)
    i = 0
    drawBoard(GAMEBOARD, MINELOCATION, currentSquare, False)
    display = True
    while True:
        if i % 20 == 0:
            display = not display
        if display:
            DISPLAYSURF.blit(message, (20, 20))
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