from game.logic import evaluate, won
from copy import deepcopy

def best_move(player, state, free_slots):
    """
    Calcula a melhor jogada possível para o jogador atual utilizando busca em árvore (Minimax).

    Args:
        player (int): Jogador atual (+1 ou -1).
        state (list): Estado atual do tabuleiro (matriz 3x3).
        free_slots (list): Lista de posições livres no tabuleiro.

    Returns:
        list: Uma lista contendo [linha, coluna, pontuação] da melhor jogada encontrada.
    """
    if player == +1:
        best = [-1, -1, -float("inf")]
    else:
        best = [-1, -1, +float("inf")]

    if (free_slots == []) | (won(state, -player)):
        return [-1, -1, evaluate(state, -player)]

    for slot in free_slots:
        x, y = slot

        pseudo_free_slots = deepcopy(free_slots)
        pseudo_state = deepcopy(state)

        pseudo_state[x][y] = player

        pseudo_free_slots.remove(slot)

        score = best_move(-player, pseudo_state, pseudo_free_slots)

        score[0], score[1] = x, y

        if player == +1:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    return best
