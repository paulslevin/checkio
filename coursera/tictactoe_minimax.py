# play an unwinnable game of Noughts and Crosses
# template: http://www.codeskulptor.org/#poc_tttmm_template.py
# play online: http://www.codeskulptor.org/#user40_O7z06XY2Gt_0.py
"""
Mini-max Tic-Tac-Toe Player
"""
import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def max_key(lst, key):
    """Adds a keyword argument to the max function."""
    new_lst = map(key, lst)
    for idx, val in enumerate(lst):
        if new_lst[idx] == max(new_lst):
            return val

def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """

    if board.check_win():
        return SCORES[board.check_win()], (-1, -1)
    other_player = provided.switch_player(player)
    move_score_dict = {}
    for square in board.get_empty_squares():
        new_board = board.clone()
        new_board.move(square[0], square[1], player)
        movetup = mm_move(new_board, other_player)
        if movetup[0] == SCORES[player]:
            return SCORES[player], square
        score = movetup[0]
        move_score_dict[square] = score
    best_move = max_key(move_score_dict,
                        lambda x: SCORES[player] * move_score_dict[x])
    return move_score_dict[best_move], best_move


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

# TESTING
# import user40_pXk75nXxLn_18 as testing
# testing.test(mm_move)
