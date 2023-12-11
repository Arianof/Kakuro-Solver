import copy
import os
import time


class KakuroSolver:
    def __init__(self):
        self.kakuroPuzzles = [[[-1, -1, -1, {'D': 17}, {'D': 28}, -1, -1],
                             [-1, -1, {'D': 27, 'R': 16}, 0, 0, {'D': 17}, {'D': 17}],
                             [-1, {'D': 11, 'R': 27}, 0, 0, 0, 0, 0], [{'R': 3}, 0, 0, {'D': 14, 'R': 19}, 0, 0, 0],
                             [{'R': 34}, 0, 0, 0, 0, 0, {'D': 17}], [-1, {'R': 30}, 0, 0, 0, 0, 0],
                             [-1, {'R': 3}, 0, 0, {'R': 16}, 0, 0]],

                              [[-1, {'D': 10}, {'D': 10}, -1, -1, -1, -1, -1, {'D': 23}, {'D': 16}],
                               [{'R': 4}, 0, 0, {'D': 17}, -1, -1, -1, {'D': 17, 'R': 16}, 0, 0],
                               [{'R': 23}, 0, 0, 0, {'D': 20}, -1, {'D': 30, 'R': 24}, 0, 0, 0],
                               [-1, {'R': 13}, 0, 0, 0, {'D': 20, 'R': 23}, 0, 0, 0, -1],
                               [-1, -1, -1, {'R': 11}, 0, 0, 0, 0, -1, -1],
                               [-1, -1, -1, {'D': 6, 'R': 23}, 0, 0, 0, -1, -1, -1],
                               [-1, -1, {'D': 7, 'R': 25}, 0, 0, 0, 0, {'D': 3}, {'D': 9}, -1],
                               [-1, {'D': 4, 'R': 8}, 0, 0, 0, {'R': 7}, 0, 0, 0, {'D': 4}],
                               [{'R': 6}, 0, 0, 0, -1, -1, {'R': 6}, 0, 0, 0],
                               [{'R': 3}, 0, 0, -1, -1, -1, -1, {'R': 4}, 0, 0]
                               ]
                              ]
        # set your desire puzzle in below assignment:
        # 0 is easy
        # 1 is hard
        self.kakuroPuzzle = self.kakuroPuzzles[0]
        self.kakuro_size = len(self.kakuroPuzzle[0])
        self.domains = {}
        for i in range(self.kakuro_size):
            for j in range(self.kakuro_size):
                if self.kakuroPuzzle[i][j] == 0:
                    self.domains.update({(i, j): [1, 2, 3, 4, 5, 6, 7, 8, 9]})

        self.clue_cells = {}
        for i in range(self.kakuro_size):
            for j in range(self.kakuro_size):
                if type(self.kakuroPuzzle[i][j]) is dict:
                    clue = self.kakuroPuzzle[i][j]
                    keys = clue.keys()
                    for key in keys:
                        if key == 'D':
                            self.clue_cells.update({((i, j), 'D'): []})
                        else:
                            self.clue_cells.update({((i, j), 'R'): []})
        for clue in self.clue_cells:
            clue_row = clue[0][0]
            clue_col = clue[0][1]
            clue_dir = clue[1]
            if clue_dir == 'D':
                for i in range(clue_row + 1, self.kakuro_size):
                    if type(self.kakuroPuzzle[i][clue_col]) is not dict and self.kakuroPuzzle[i][clue_col] == 0:
                        self.clue_cells[clue].append([i, clue_col])
                    else:
                        break
            elif clue_dir == 'R':
                for j in range(clue_col + 1, self.kakuro_size):
                    if type(self.kakuroPuzzle[clue_row][j]) is not dict and self.kakuroPuzzle[clue_row][j] == 0:
                        self.clue_cells[clue].append([clue_row, j])
                    else:
                        break

    def unassigned(self, empty):
        for i in range(self.kakuro_size):
            for j in range(self.kakuro_size):
                if self.kakuroPuzzle[i][j] == 0:
                    empty[0] = i
                    empty[1] = j
                    return True
        return False

    def unassigned_mrv(self, empty):
        sorted_clues = sorted(self.clue_cells, key=lambda clue: len(self.clue_cells[clue]))
        for sorted_clue in sorted_clues:
            for cell in self.clue_cells[sorted_clue]:
                if self.kakuroPuzzle[cell[0]][cell[1]] == 0:
                    empty[0] = cell[0]
                    empty[1] = cell[1]
                    return True
        return False

    def find_clue_cells(self, row, col):
        clues = []
        for i in reversed(range(0, row)):
            if type(self.kakuroPuzzle[i][col]) is dict and self.kakuroPuzzle[i][col]['D']:
                clues.append({'D': self.kakuroPuzzle[i][col]['D']})
                break
        for j in reversed(range(0, col)):
            if type(self.kakuroPuzzle[row][j]) is dict and self.kakuroPuzzle[row][j]['R']:
                clues.append({'R': self.kakuroPuzzle[row][j]['R']})
                break
        return clues

    def find_row_neighbors(self, row, col):
        res = []
        curr = [row, col]
        neighbors = self.find_neighbors(curr)
        for neighbor in neighbors:
            if neighbor[0] == row:
                res.append(neighbor)
        return res

    def find_col_neighbors(self, row, col):
        res = []
        curr = [row, col]
        neighbors = self.find_neighbors(curr)
        for neighbor in neighbors:
            if neighbor[1] == col:
                res.append(neighbor)
        return res

    def is_row_full(self, row, col):
        row_neighbors = self.find_row_neighbors(row, col)
        for row_neighbor in row_neighbors:
            if self.kakuroPuzzle[row_neighbor[0]][row_neighbor[1]] == 0:
                return False
        return True

    def is_col_full(self, row, col):
        col_neighbors = self.find_col_neighbors(row, col)
        for col_neighbor in col_neighbors:
            if self.kakuroPuzzle[col_neighbor[0]][col_neighbor[1]] == 0:
                return False
        return True

    def calc_col_sum(self, row, col, digit):
        col_sum = 0
        col_neighbors = self.find_col_neighbors(row, col)
        for col_neighbor in col_neighbors:
            col_sum += self.kakuroPuzzle[col_neighbor[0]][col_neighbor[1]]
        return col_sum + digit

    def calc_row_sum(self, row, col, digit):
        row_sum = 0
        row_neighbors = self.find_row_neighbors(row, col)
        for row_neighbor in row_neighbors:
            row_sum += self.kakuroPuzzle[row_neighbor[0]][row_neighbor[1]]
        return row_sum + digit

    def check_not_repeated(self, row, col, digit):
        neighbors = self.find_neighbors([row, col])
        for neighbor in neighbors:
            if self.kakuroPuzzle[neighbor[0]][neighbor[1]] == digit:
                return False
        return True

    def can_place_digit(self, row, col, digit):
        if not self.check_not_repeated(row, col, digit):
            return False
        clues = self.find_clue_cells(row, col)
        row_sum = self.calc_row_sum(row, col, digit)
        col_sum = self.calc_col_sum(row, col, digit)
        if self.is_col_full(row, col):
            if col_sum != clues[0]['D']:
                return False
        else:
            if col_sum >= clues[0]['D']:
                return False
        if self.is_row_full(row, col):
            if row_sum != clues[1]['R']:
                return False
        else:
            if row_sum >= clues[1]['R']:
                return False
        return True

    def forward_checking(self, current_node, digit, neighbors):
        for neighbor in neighbors:
            if self.kakuroPuzzle[neighbor[0]][neighbor[1]] != 0:
                continue
            fake_neighbor_domain = copy.deepcopy(self.domains[(neighbor[0], neighbor[1])])
            row_sum = self.calc_row_sum(current_node[0], current_node[1], digit)
            col_sum = self.calc_col_sum(current_node[0], current_node[1], digit)
            clues = self.find_clue_cells(current_node[0], current_node[1])
            for x in fake_neighbor_domain:
                if x == self.kakuroPuzzle[current_node[0]][current_node[1]]:
                    self.domains[(neighbor[0], neighbor[1])].remove(x)
                    continue
                if current_node[1] == neighbor[1] and x + col_sum > clues[0]['D']:
                    self.domains[(neighbor[0], neighbor[1])].remove(x)
                    continue
                if current_node[0] == neighbor[0] and x + row_sum > clues[1]['R']:
                    self.domains[(neighbor[0], neighbor[1])].remove(x)
                    continue
            if len(self.domains[neighbor[0], neighbor[1]]) == 0:
                return False
        return True

    def kakuro_solver(self):
        empty = [0, 0]
        if not self.unassigned_mrv(empty):
            return True
        row = empty[0]
        col = empty[1]
        for i in self.domains.get((row, col)):
            if self.can_place_digit(row, col, i):
                self.kakuroPuzzle[row][col] = i
                ex_puzzle = copy.deepcopy(self.kakuroPuzzle)
                ex_domain = copy.deepcopy(self.domains)
                self.domains[(row, col)] = [i]
                neighbors = self.find_neighbors([row, col])
                if self.forward_checking([row, col], i, neighbors):
                    if self.kakuro_solver():
                        return True
                #self.print_kakuro()
                #time.sleep(0.03)
                #print()
                #os.system("clear")
                self.kakuroPuzzle = ex_puzzle
                self.kakuroPuzzle[row][col] = 0
                self.domains = ex_domain
        return False

    def find_neighbors(self, neighbor):
        row = neighbor[0]
        col = neighbor[1]
        res = []
        for i in reversed(range(row)):
            if type(self.kakuroPuzzle[i][col]) == dict or self.kakuroPuzzle[i][col] == -1:
                break
            res.append([i, col])
        for i in range(row + 1, self.kakuro_size):
            if type(self.kakuroPuzzle[i][col]) == dict or self.kakuroPuzzle[i][col] == -1:
                break
            res.append([i, col])
        for j in reversed(range(col)):
            if type(self.kakuroPuzzle[row][j]) == dict or self.kakuroPuzzle[row][j] == -1:
                break
            res.append([row, j])
        for j in range(col + 1, self.kakuro_size):
            if type(self.kakuroPuzzle[row][j]) == dict or self.kakuroPuzzle[row][j] == -1:
                break
            res.append([row, j])
        return res

    def print_kakuro(self):
        for i in range(self.kakuro_size):
            for j in range(self.kakuro_size):
                if self.kakuroPuzzle[i][j] == -1:
                    print('B', end=" ")
                elif type(self.kakuroPuzzle[i][j]) == dict:
                    print('C', end=" ")
                else:
                    print(self.kakuroPuzzle[i][j], end=" ")
            print()
