import copy
import os

def print_board_from_mask(boardMask, title="Sudoku Board"):
    # Clears the terminal screen and prints the updated board.
    os.system('clear')
    print(f"\n{title}:")
    for r in range(9):
        row = []
        for c in range(9):
            mask = boardMask[r][c]
            if bin(mask).count('1') > 1:  # More than one possibility
                row.append(".")
            else:  # Only one possibility
                digit = str(mask.bit_length())  # Determine the digit (1-based index)
                row.append(digit)
        print(" ".join(row))
class Solution(object):
    def solveSudoku(self, board):
        FULL_MASK = 0x1FF
        boardMask = [[FULL_MASK for _ in range(9)] for _ in range(9)]
        rowMask = [0]*9
        colMask = [0]*9
        boxMask = [0]*9

        for r in range(9):
            for c in range(9):
                ch = board[r][c]
                if ch != '.':
                    digit = int(ch)
                    mask = 1 << (digit - 1)
                    boardMask[r][c] = mask
                    box = (r//3)*3 + (c//3)
                    rowMask[r] |= mask
                    colMask[c] |= mask
                    boxMask[box] |= mask

        if not self.propagate(boardMask, rowMask, colMask, boxMask): return
        if self.is_solved(boardMask):
            self.set_board(board, boardMask)
            return

        stack = [(copy.deepcopy(boardMask), list(rowMask), list(colMask), list(boxMask))]
        while stack:
            currBoardMask, currRowMask, currColMask, currBoxMask = stack.pop()
            if self.is_solved(currBoardMask):
                self.set_board(board, currBoardMask)
                return

            r, c = self.min_cell(currBoardMask)
            candidate = currBoardMask[r][c]
            while candidate:
                p = candidate & (-candidate)
                candidate &= candidate - 1

                newBoardMask = copy.deepcopy(currBoardMask)
                newRowMask = currRowMask[:]
                newColMask = currColMask[:]
                newBoxMask = currBoxMask[:]

                box = (r//3)*3 + (c//3)
                if (newRowMask[r] & p) or (newColMask[c] & p) or (newBoxMask[box] & p): continue

                newBoardMask[r][c] = p
                newRowMask[r] |= p
                newColMask[c] |= p
                newBoxMask[box] |= p

                # print_board_from_mask(newBoardMask)

                if not self.propagate(newBoardMask, newRowMask, newColMask, newBoxMask): continue
                stack.append((newBoardMask, newRowMask, newColMask, newBoxMask))

    def propagate(self, boardMask, rowMask, colMask, boxMask):
        changed = True
        while changed:
            changed = False
            for r in range(9):
                for c in range(9):
                    mask = boardMask[r][c]
                    if (mask & (mask-1)) == 0: continue
                    box = (r//3)*3 + (c//3)
                    used = rowMask[r] | colMask[c] | boxMask[box]
                    newMask = mask & (~used)
                    if newMask == 0: return False
                    if newMask != mask:
                        boardMask[r][c] = newMask
                        changed = True
                        if (newMask & (newMask-1)) == 0:
                            rowMask[r] |= newMask
                            colMask[c] |= newMask
                            boxMask[box] |= newMask
        return True

    def is_solved(self, boardMask):
        for r in range(9):
            for c in range(9):
                mask = boardMask[r][c]
                if mask == 0 or (mask & (mask-1)) != 0: return False
        return True

    def min_cell(self, boardMask):
        min_count = 10
        cell_pos = (0,0)
        for r in range(9):
            for c in range(9):
                mask = boardMask[r][c]
                if (mask & (mask - 1)) == 0: continue
                count = bin(mask).count('1')
                if count < min_count:
                    min_count = count
                    cell_pos = (r,c)
        return cell_pos

    def set_board(self, board, boardMask):
        for r in range(9):
            for c in range(9):
                mask = boardMask[r][c]
                digit = (mask.bit_length())
                board[r][c] = str(digit)