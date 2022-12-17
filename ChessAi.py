import random
CHECKMATE = 1000
initial_depth = 3
strength = {'Q': 10, 'R': 5, 'N': 3, 'B': 3, 'p': 1, 'K': 0}
#CHECKMATE ITS DEPENDEDING ON MINIMAX ALGORITHM LIKE WHITE BOARD THATS HUMAN TURN TRYING TO MAXMAIZING THAT CHECK MATE
#AS LONG AS HE COULD AND BLACK THATS AI TRYING TO MINIMIZING THIS CHECK MATE AS LONG AS HE COULD

# Any 'We, our or us' refers to the Ai


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(state, valid_moves):
    global next_move, counter  # The final move to be made by us
    next_move = None
    counter = 0
    searching_moves(state, valid_moves, initial_depth, -CHECKMATE, CHECKMATE, -1)  # Starting the search
    print(next_move)
    return next_move


def searching_moves(state, valid_moves, depth, alpha, beta, multiplier):
    global next_move, counter
    if depth == 0:  # If we got to the deepest depth we are allowed to search
        return multiplier * get_board_score(state)  # Start backtracking
    max_score = -CHECKMATE  # If it's we initialize there max score as the lowest and they shall max it to win
    for move in valid_moves:  # We check every valid move we got for them
        state.makeMove(move)  # We make the move and check the score after using it
        next_moves = state.getValidMoves()  # We get the children of the state after playing this game
        score1 = -searching_moves(state, next_moves, depth - 1, -beta, -alpha, -multiplier)
        if score1 > max_score:
            max_score = score1
            if depth == initial_depth:
                next_move = move
        state.undoMove()
        counter += 1
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def get_board_score(state):  # Getting the score of each square on the bord
    if state.is_check_mate():
        if state.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif state.is_stale_mate():
        return 0
    score = 0
    for row in state.board:
        for piece in row:
            if piece[0] == 'w':
                score += strength[piece[1]]
            elif piece[0] == 'b':
                score -= strength[piece[1]]
    return score
