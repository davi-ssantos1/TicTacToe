def is_valid_move(x,y, free_slots):
    if [x,y] in free_slots:
            return True
    return False

def won(state, player):
    if (('' != state[0][0] == state[0][1] == state[0][2] == player) | 
        ('' != state[1][0] == state[1][1] == state[1][2] == player) |
        ('' != state[2][0] == state[2][1] == state[2][2] == player) |
        ('' != state[0][0] == state[1][0] == state[2][0] == player) |
        ('' != state[0][1] == state[1][1] == state[2][1] == player) |
        ('' != state[0][2] == state[1][2] == state[2][2] == player) |
        ('' != state[0][0] == state[1][1] == state[2][2] == player) |
        ('' != state[0][2] == state[1][1] == state[2][0] == player)):
        return True
    else:
        return False
    
def evaluate(state, player):
    if (won(state, player) == True):
        return 1 if player == +1 else -1
    else:
        return 0