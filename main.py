from bit_solver import Solution
import numpy as np
import argparse
from tqdm import tqdm

def print_board(board, title="Sudoku Board"):
    """
    Prints a Sudoku board in a readable format.
    :param board: List[List[str]] - 9x9 board to print
    :param title: str - Title for the printed board
    """
    print(f"\n{title}:")
    for row in board:
        print(" ".join(row))

def verify_solution(solved_board, solution):
    """
    Verifies if the solved board matches the expected solution.
    :param solved_board: List[List[str]] - Solved Sudoku board
    :param solution: np.array - Expected solution as a 9x9 numpy array
    :return: bool - Whether the solution is correct
    """
    for i in range(9):
        for j in range(9):
            if solved_board[i][j] == '.' or int(solved_board[i][j]) != solution[i, j]: return False
    return True

def test_min_possib():
    solution = Solution()
    
    corr = [
        ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
        [['1', '2'], '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', ['1'], '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
        [['3'], ['1','2'], '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_']
    ]

    expected = (4, 1)

    result = solution.min_possib(corr)

    print(f"Test corr matrix:\n{corr}")
    print(f"Expected position with min possibilities: {expected}")
    print(f"Result from min_possib: {result}")
    assert result == expected, "Test failed!"
    print("Test passed!")

def main():
    parser = argparse.ArgumentParser(description="Solve Sudoku Quizzes")
    parser.add_argument('--num_quizzes', type=int, default=1000, help="Number of quizzes to load and solve")
    args = parser.parse_args()

    quizzes = np.zeros((args.num_quizzes, 81), np.int32)
    solutions = np.zeros((args.num_quizzes, 81), np.int32)
    
    with open('data/sudoku.csv', 'r') as file:
        for i, line in enumerate(file.read().splitlines()[1:args.num_quizzes+1]):
            quiz, solution = line.split(",")
            for j, (q, s) in enumerate(zip(quiz, solution)):
                quizzes[i, j] = int(q)
                solutions[i, j] = int(s)

    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))

    solution_solver = Solution()

    count = 0
    for idx, quiz in enumerate(tqdm(quizzes, desc="Solving Quizzes")):
        board = [[str(quiz[i][j]) if quiz[i][j] != 0 else '.' for j in range(9)] for i in range(9)]
        solution_solver.solveSudoku(board)

        if verify_solution(board, solutions[idx]):
            count += 1
        else:
            print(f"\nPuzzle {idx+1} solved incorrectly.")
            print("Incorrect puzzle state:")
            print_board(board, "Board after attempt")
            print("\nExpected solution:")
            correct_sol = solutions[idx]
            expected_board = [[str(correct_sol[i, j]) for j in range(9)] for i in range(9)]
            print_board(expected_board, "Expected Solution")
            break

    print(f"\n{count} out of {args.num_quizzes} quizzes solved correctly.")

if __name__ == "__main__":
    main()
