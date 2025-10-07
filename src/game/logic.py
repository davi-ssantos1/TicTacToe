def is_valid_move(x, y, free_slots):
    """
    Verifica se a jogada é válida, ou seja, se a posição está livre.

    Args:
        x (int): Linha da jogada.
        y (int): Coluna da jogada.
        free_slots (list): Lista de posições livres no tabuleiro.

    Returns:
        bool: True se a jogada for válida, False caso contrário.
    """
    if [x, y] in free_slots:
        return True
    return False


def won(state, player):
    """
    Verifica se o jogador venceu o jogo.

    Args:
        state (list): Estado atual do tabuleiro (matriz 3x3).
        player (int): Jogador a ser verificado (+1 ou -1).

    Returns:
        bool: True se o jogador venceu, False caso contrário.
    """
    if (
        ("" != state[0][0] == state[0][1] == state[0][2] == player)
        | ("" != state[1][0] == state[1][1] == state[1][2] == player)
        | ("" != state[2][0] == state[2][1] == state[2][2] == player)
        | ("" != state[0][0] == state[1][0] == state[2][0] == player)
        | ("" != state[0][1] == state[1][1] == state[2][1] == player)
        | ("" != state[0][2] == state[1][2] == state[2][2] == player)
        | ("" != state[0][0] == state[1][1] == state[2][2] == player)
        | ("" != state[0][2] == state[1][1] == state[2][0] == player)
    ):
        return True
    else:
        return False


def evaluate(state, player):
    """
    Avalia o estado atual do tabuleiro para o jogador informado.

    Args:
        state (list): Estado atual do tabuleiro (matriz 3x3).
        player (int): Jogador a ser avaliado (+1 ou -1).

    Returns:
        int: 1 se o jogador venceu, -1 se perdeu, 0 caso contrário.
    """
    if won(state, player) == True:
        return 1 if player == +1 else -1
    else:
        return 0
