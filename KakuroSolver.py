import os
import time


class KakuroSolver:
    def __init__(self):
        self.kakuroPuzzle = [[-1, -1, -1, {'D': 17}, {'D': 28}, -1, -1],
                             [-1, -1, {'D': 27, 'R': 16}, 0, 0, {'D': 17}, {'D': 17}],
                             [-1, {'D': 11, 'R': 27}, 0, 0, 0, 0, 0], [{'R': 3}, 0, 0, {'D': 14, 'R': 19}, 0, 0, 0],
                             [{'R': 34}, 0, 0, 0, 0, 0, {'D': 17}], [-1, {'R': 30}, 0, 0, 0, 0, 0],
                             [-1, {'R': 3}, 0, 0, {'R': 16}, 0, 0]]

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

    def kakuro_solver(self):
        empty = [0, 0]
        if not self.unassigned(empty):
            return True
        row = empty[0]
        col = empty[1]
        for i in range(1, 10):
            if self.can_place_digit(row, col, i):
                self.kakuroPuzzle[row][col] = i
                if self.kakuro_solver():
                    return True
                self.print_kakuro()
                time.sleep(0.02)
                os.system("clear")
                self.kakuroPuzzle[row][col] = 0
        return False

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
