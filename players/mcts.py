import chess
import math
import random
from .naive import Naive

class MCTSNode(object):
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.win_counts = {chess.BLACK: 0, chess.WHITE: 0}
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = board.legal_moves

    def add_random_child(self):
        index = random.randint(0, self.unvisited_moves.count()- 1)
        new_move = list(self.unvisited_moves).pop(index)
        new_board = self.board.copy()
        new_board.push(new_move)
        new_node = MCTSNode(new_board, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner):
        if winner == chess.WHITE or winner == chess.BLACK:
            self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return self.unvisited_moves.count() > 0

    def is_terminal(self):
        return self.board.is_game_over()

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)

class MCTS():
    def __init__(self, num_rounds, temperature):
        self.num_rounds = num_rounds
        self.temperature = temperature

    def move(self, board):
        root = MCTSNode(board)
        for i in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

            if node.can_add_child():
                node = node.add_random_child()

            winner = self.simulate_random_game(node.board)
            while node is not None:
                node.record_win(winner)
                node = node.parent

        scored_moves = [
            (child.winning_frac(board.turn),
            child.move,
            child.num_rollouts) for child in root.children
        ]
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        for s, m, n in scored_moves[:10]:
            print('%s - %.3f (%d)' % (m, s, n))

        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(board.turn)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        print('Select move %s with win pct %.3f' % (best_move, best_pct))
        return best_move.uci()

    def select_child(self, node):
        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None
        for child in node.children:
            win_percentage = child.winning_frac(node.board.next_player)
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    @staticmethod
    def simulate_random_game(game):
        player1 = Naive()
        player2 = Naive()
        while not game.is_game_over():
            if game.turn == chess.WHITE:
                uci = player1.move(game)
            else:
                uci = player2.move(game)
            game.push_uci(uci)
        if game.result() == '1-0':
            return chess.WHITE
        elif game.result() == '0-1':
            return chess.BLACK
        return None
