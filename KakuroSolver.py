import copy
import os
import time


class KakuroSolver:
    def __init__(self):
        self.kakuroPuzzle = [[-1, -1, -1, {'D': 17}, {'D': 28}, -1, -1],
                             [-1, -1, {'D': 27, 'R': 16}, 0, 0, {'D': 17}, {'D': 17}],
                             [-1, {'D': 11, 'R': 27}, 0, 0, 0, 0, 0], [{'R': 3}, 0, 0, {'D': 14, 'R': 19}, 0, 0, 0],
                             [{'R': 34}, 0, 0, 0, 0, 0, {'D': 17}], [-1, {'R': 30}, 0, 0, 0, 0, 0],
                             [-1, {'R': 3}, 0, 0, {'R': 16}, 0, 0]]
        self.domains = {}
        for i in range(7):
            for j in range(7):
                if self.kakuroPuzzle[i][j] == 0:
                    self.domains.update({(i, j): [1, 2, 3, 4, 5, 6, 7, 8, 9]})

    def unassigned(self, empty):
        for i in range(7):
            for j in range(7):
                if self.kakuroPuzzle[i][j] == 0:
                    empty[0] = i
                    empty[1] = j
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

    def is_row_full(self, row, col):
        for j in reversed(range(0, col - 1)):
            if self.kakuroPuzzle[row][j] == 0:
                return False
        if col == 6:
            return True
        if type(self.kakuroPuzzle[row][col + 1]) == dict:
            return True
        return False

    def is_col_full(self, row, col):
        for i in reversed(range(0, row - 1)):
            if self.kakuroPuzzle[i][col] == 0:
                return False
        if row == 6:
            return True
        if type(self.kakuroPuzzle[row + 1][col]) == dict:
            return True
        return False

    def calc_col_sum(self, row, col, digit):
        col_sum = 0
        for i in reversed(range(0, row)):
            if type(self.kakuroPuzzle[i][col]) == dict:
                break
            col_sum += self.kakuroPuzzle[i][col]
        for i in range(row + 1, 7):
            if type(self.kakuroPuzzle[i][col]) == dict:
                break
            col_sum += self.kakuroPuzzle[i][col]
        return col_sum + digit

    def calc_row_sum(self, row, col, digit):
        row_sum = 0
        for j in reversed(range(0, col)):
            if type(self.kakuroPuzzle[row][j]) == dict:
                break
            row_sum += self.kakuroPuzzle[row][j]
        for j in range(col + 1, 7):
            if type(self.kakuroPuzzle[row][j]) == dict:
                break
            row_sum += self.kakuroPuzzle[row][j]
        return row_sum + digit

    def can_place_digit(self, row, col, digit):
        for i in reversed(range(0, row)):
            if type(self.kakuroPuzzle[i][col]) == dict:
                break
            if digit == self.kakuroPuzzle[i][col]:
                return False
        for j in reversed(range(0, col)):
            if type(self.kakuroPuzzle[row][j]) == dict:
                break
            if digit == self.kakuroPuzzle[row][j]:
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

    def ac_3(self, q):
        while len(q) != 0:
            neighbor = q.pop(0)
            if self.remove_inconsistent_values(neighbor):
                if len(self.domains[(neighbor[0][0], neighbor[0][1])]) == 0:
                    return False
                new_neighbors = self.find_neighbors(neighbor[0])
                for new_neighbor in new_neighbors:
                    q.append((new_neighbor, neighbor[0]))
        return True

    def remove_inconsistent_values(self, neighbor):
        #tail = neighbor[0]
        #head = neighbor[1]
        #for i in self.domains[(tail[0], tail[1])]:
        pass
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
        if not self.unassigned(empty):
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
                #time.sleep(0.02)
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
            if type(self.kakuroPuzzle[i][col]) == dict:
                break
            res.append([i, col])
        for i in range(row + 1, 7):
            if type(self.kakuroPuzzle[i][col]) == dict:
                break
            res.append([i, col])
        for j in reversed(range(col)):
            if type(self.kakuroPuzzle[row][j]) == dict:
                break
            res.append([row, j])
        for j in range(col + 1, 7):
            if type(self.kakuroPuzzle[row][j]) == dict:
                break
            res.append([row, j])
        return res

    def print_kakuro(self):
        for i in range(7):
            for j in range(7):
                if self.kakuroPuzzle[i][j] == -1:
                    print('B', end=" ")
                elif type(self.kakuroPuzzle[i][j]) == dict:
                    print('C', end=" ")
                else:
                    print(self.kakuroPuzzle[i][j], end=" ")
            print()
