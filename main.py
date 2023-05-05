from puzzle import Puzzle

if __name__ == "__main__":
    # Unicode for blank square: https://www.fileformat.info/info/unicode/char/25a1/index.htm
    initial_state = [["A", "N", "G"], ["E", "L", "I"], ["C", "A", "\u25A1"]]
    puzzle = Puzzle(initial_state)
    print(puzzle)
