"""
ده المكان الاساسي في اللعبة زي شكل البورد و ال gui و ال input من اليوزر
 اللي بيروح علي الشيس انجين ياخد انفورميشن و يرجعله تاني
"""
import pygame as p

import ChessEngine
import ChessAi

Width = Height = 512
Dimension = 8
SqSize = Height//Dimension
MaxFps = 15
Images = {}
#Initialize a global dict for images 3shan t execute mra wa7da bs w myb2ash fy lag


def loadimages():
    pieces = ['wR', 'wQ', 'wp', 'wN', 'wK', 'wB', 'bR', 'bQ', 'bp', 'bN', 'bK', 'bB']
    #loop 3la el swr 3shan ad5lha el array w ast5dmha fy el board
    for piece in pieces:
        Images[piece] = p.transform.scale(p.image.load("Perfaps/images/"+piece+".png"), (SqSize, SqSize))

#Starting Main Game


def main():
    p.init()
    screen = p.display.set_mode((Width, Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag value to check opponent's King  State
    animate = False
    loadimages()
    running = True
    sqSelected = ()   #keep track for last mouse click
    playerClicks = []
    gameOver = gs.is_check_mate() or gs.is_stale_mate()
    playerOne = True  #if human is playing white then this will be true
    playerTwo = False  # if human is playing black then this will be true
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
                exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SqSize
                    row = location[1]//SqSize
                    if sqSelected == (row, col):  # lw 3mlt select lnfs el colm w el row h3ml disselect
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:  #lw das click tany hy3ml aeh
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_r:  #reset when push R
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    gameOver = False
                    moveMade = False
                    animate = False

        #############################################Ai Logic#################################################
        if not gameOver and not humanTurn:
            AiMove = ChessAi.findBestMove(gs, gs.getValidMoves())
            if AiMove is None:
                AiMove = ChessAi.findRandomMove(validMoves)
            gs.makeMove(AiMove)
            moveMade = True
            animate = True
        #############################################Ai Logic#################################################

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        drawGameState(screen, gs, validMoves, sqSelected)
        #GameOver statment
        if gs.is_check_mate():
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'You Lose')
            else:
                drawText(screen, 'You Win')
        elif gs.is_stale_mate():
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(MaxFps)
        p.display.flip()

#Highlight square  selected


def highlightSquares(screen, gs, validMoved, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SqSize, SqSize))
            s.set_alpha(100)
            s.fill(p.Color(0, 0, 0))
            screen.blit(s, (c*SqSize, r*SqSize))
            s.fill(p.Color(1, 135, 0))
            for move in validMoved:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SqSize*move.endCol, SqSize*move.endRow))
#defult board color etc


def drawBoard(screen):
    global colors
    colors = [p.Color(255, 223, 136), p.Color(125, 81, 0)]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SqSize, r*SqSize, SqSize, SqSize))

#draw pieces during game state


def drawPieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(Images[piece], p.Rect(c*SqSize, r*SqSize, SqSize, SqSize))


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

#animating


def animateMove(move, screen, board, clock):
    global colors
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SqSize, move.endRow*SqSize, SqSize, SqSize)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        s = move.pieceCaptured+'p'
        if move.pieceCaptured != '--':
            screen.blit(Images[move.pieceCaptured], endSquare)

        screen.blit(Images[move.pieceMoved], p.Rect(c*SqSize, r*SqSize, SqSize, SqSize))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    surface = p.Surface((Width, Height))
    # Changing surface color
    surface.set_alpha(128)
    surface.fill((255, 255, 255))
    font = p.font.SysFont("verdana", 32, True, False)
    textObject = font.render(text, False, p.Color('Gray'))
    textLocation = p.Rect(0, 0, Width, Height).move(Width/2 - textObject.get_width()/2, Height/2 - textObject.get_height()/2)
    screen.blit(surface, (0, 0))
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
