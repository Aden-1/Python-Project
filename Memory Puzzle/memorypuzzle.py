# Memory Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 2 # speed boxes' sliding reveals and covers #NAD CHANGE TO MAKE SLOWER
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 6 # number of columns of icons #NAD CHANGE TO SMALLER SIZE
BOARDHEIGHT = 6 # number of rows of icons #NAD CHANGE TO SMALLER (HAS TO BE EVEN)
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

## SET THE BACKGROUND IMAGE
try:
    BACK_IMAGE = pygame.image.load('background.png')
except Exception:
    sys.exit("The background image is missing.")
## SCALE THE BACKGROUND IMAGE TO FIT THE WINDOW
BACK_IMAGE = pygame.transform.scale(BACK_IMAGE, (WINDOWWIDTH, WINDOWHEIGHT))

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    # 'LH' Initialize font for displaying text
    font = pygame.font.Font(None, 36)  # font for displaying text

    pygame.mixer.init()  # initialize sound system
    pygame.mixer.music.load("backgroundmusic.mp3")  #background music
    pygame.mixer.music.play(-1)  # loop forever
    pygame.mixer.music.set_volume(0.3)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.
    # 'LH' Track consecutive misses for lives system
    misses = 0  # track consecutive misses
    # 'LH' Flag for game over state
    gameOver = False  # flag for game over state

    #DISPLAYSURF.fill(BGCOLOR)
    ## Instead of using a color use the image as the background
    # at location (0, 0) which is the top left corner of the window
    DISPLAYSURF.blit(BACK_IMAGE, (0, 0))

    startGameAnimation(mainBoard)

    while True: # main game loop
        mouseClicked = False

        #DISPLAYSURF.fill(BGCOLOR) # drawing the window
        ## Instead of using a color use the image as the background
        # at location (0, 0) which is the top left corner of the window
        DISPLAYSURF.blit(BACK_IMAGE, (0, 0))
        drawBoard(mainBoard, revealedBoxes)

        if not gameOver:
            # 'LH' Display current lives
            livesText = font.render(f"Lives: {3 - misses}", True, BLACK)
            DISPLAYSURF.blit(livesText, (10, 10))
        else:
            # 'LH' Display game over message
            gameOverText = font.render("Game Over. Press R to restart or Q to quit.", True, BLACK)
            DISPLAYSURF.blit(gameOverText, (WINDOWWIDTH // 2 - 200, WINDOWHEIGHT // 2))

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            ## if the user presses the "x" key, reveal a random box for a moment
            # pass in the current game board and the currently revealed boxes to the revealABox function
            elif event.type == KEYDOWN and event.key == K_x:
                revealABox(mainBoard, revealedBoxes)
            # 'LH' Handle restart or quit on game over
            elif gameOver and event.type == KEYDOWN:
                if event.key == K_r:
                    # 'LH' Restart the game
                    mainBoard = getRandomizedBoard()
                    revealedBoxes = generateRevealedBoxesData(False)
                    misses = 0
                    gameOver = False
                    firstSelection = None
                    DISPLAYSURF.blit(BACK_IMAGE, (0, 0))
                    startGameAnimation(mainBoard)
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()

        if not gameOver:
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            if boxx != None and boxy != None:
                # The mouse is currently over a box.
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                    revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                    if firstSelection == None: # the current box was the first box clicked
                        firstSelection = (boxx, boxy)
                    else: # the current box was the second box clicked
                        # Check if there is a match between the two icons.
                        icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                        if icon1shape != icon2shape or icon1color != icon2color:
                            # Icons don't match. Re-cover up both selections.
                            # 'LH' Increment misses on mismatch
                            misses += 1
                            if misses == 3:
                                # 'LH' Set game over if 3 misses
                                gameOver = True
                            pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                            coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False
                        else:
                            # Match found, reset misses
                            # 'LH' Reset misses on match
                            misses = 0
                            if hasWon(revealedBoxes): # check if all pairs found
                                gameWonAnimation(mainBoard)
                                pygame.time.wait(2000)

                                # Reset the board
                                mainBoard = getRandomizedBoard()
                                revealedBoxes = generateRevealedBoxesData(False)
                                # 'LH' Reset misses on win
                                misses = 0  # reset misses on win

                                # Show the fully unrevealed board for a second.
                                drawBoard(mainBoard, revealedBoxes)
                                pygame.display.update()
                                pygame.time.wait(1000)

                                ## SET THE BACKGROUND BACK TO THE IMAGES AFTER THE USER HAS WON
                                DISPLAYSURF.blit(BACK_IMAGE, (0, 0))

                                # Replay the start game animation.
                                startGameAnimation(mainBoard)
                        firstSelection = None # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    ## CHANGED WITH WINNING COLORS THAT FLASH TO BETTER MATCH THE BACKGROUND
    color1 = NAVYBLUE
    color2 = GRAY

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True

## Revel a random box for a moment.
# reference startGameAnimation
# pass in the current game board and the currently revealed boxes
# revealedBoxes is an array of booleans
def revealABox(board, revealedBoxes):

    ## Pick a random box to reveal
    boxToReveal = random.randint(0, BOARDWIDTH - 1), random.randint(0, BOARDHEIGHT - 1)

    # if boxToReveal is already revealed, keep picking a random box until an unrevealed box is found
    # and the board is not cleared
    while revealedBoxes[boxToReveal[0]][boxToReveal[1]] and not hasWon(revealedBoxes):
        boxToReveal = random.randint(0, BOARDWIDTH - 1), random.randint(0, BOARDHEIGHT - 1)

    # reveal the box at the location of boxToReveal
    revealBoxesAnimation(board, [boxToReveal])
    # cover the box after it has been revealed
    coverBoxesAnimation(board, [boxToReveal])
    return

if __name__ == '__main__':
    main()