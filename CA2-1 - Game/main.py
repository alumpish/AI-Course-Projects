import turtle
import math
import random
import time
import sys


def calc_connected_lines(dots: list[str]):
    count = 0
    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            if (dots[i][0] == dots[j][0] or dots[i][0] == dots[j][1] or
                    dots[i][1] == dots[j][0] or dots[i][1] == dots[j][1]):
                count += 1
    return count


class Sim:
    # Set true for graphical interface
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i + 1, 6):
                self.available_moves.append((i, j))

        if random.randint(0, 1) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'

        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI:
            turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI:
            return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        time.sleep(0.5)

    def _swap_turn(self):
        if self.turn == 'red':
            self.turn = 'blue'
        else:
            self.turn = 'red'

    def _evaluate(self):
        evaluation = calc_connected_lines(self.blue) - calc_connected_lines(self.red)
        return evaluation * 100

    def minimax(self, depth, player_turn, alpha=-math.inf, beta=math.inf):
        if self.gameover(self.red, self.blue) == 'blue':
            return -350, None

        if self.gameover(self.red, self.blue) == 'red':
            return 350, None

        if depth <= 0 or not self.available_moves:
            return self._evaluate(), None

        if player_turn == 'red':
            res_move: str
            max_score = -math.inf
            for move in self.available_moves:
                self.available_moves.remove(move)
                self.red.append(move)
                score, _ = self.minimax(depth - 1, 'blue', alpha, beta)
                self.available_moves.append(move)
                self.red.remove(move)

                if score >= max_score:
                    max_score = score
                    res_move = move
                    alpha = max(alpha, max_score)
                    if self.prune and max_score >= beta:
                        break

            return max_score, res_move

        if player_turn == 'blue':
            res_move: str
            min_score = math.inf
            for move in self.available_moves:
                self.available_moves.remove(move)
                self.blue.append(move)
                score, _ = self.minimax(depth - 1, 'red', alpha, beta)
                self.available_moves.append(move)
                self.blue.remove(move)

                if score <= min_score:
                    min_score = score
                    res_move = move
                    beta = min(beta, min_score)
                    if self.prune and min_score <= alpha:
                        break

            return min_score, res_move

    def enemy(self):
        return random.choice(self.available_moves)

    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                _, selection = self.minimax(self.minimax_depth, self.turn)
                self.red.append(selection)
            else:
                selection = self.enemy()
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self._swap_turn()
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(self, r, b):
        if len(r) < 3 and len(b) < 3:
            return 0

        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'

        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0


if __name__ == "__main__":

    game = Sim(minimax_depth=int(sys.argv[1]), prune=True, gui=bool(int(sys.argv[2])))

    tic = time.time()

    results = {"red": 0, "blue": 0}

    test_count = 1
    for i in range(test_count):
        print(i, end="\r")
        results[game.play()] += 1

    tac = time.time()

    print(tac - tic)
    print(results)
    print(results['red']/test_count*100)
