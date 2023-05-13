from search import *

if __name__ == "__main__":
    # https://www.fileformat.info/info/unicode/char/25a1/index.htm
    depth_0 = [["A", "N", "G"], ["E", "L", "I"], ["C", "A", "\u25A1"]]
    depth_2 = [["A", "N", "G"], ["E", "L", "I"], ["\u25A1", "C", "A"]]
    depth_4 = [["A", "N", "G"], ["L", "\u25A1", "I"], ["E", "C", "A"]]
    depth_8 = [["A", "G", "I"], ["L", "\u25A1", "N"], ["E", "C", "A"]]
    depth_12 = [["A", "G", "I"], ["L", "\u25A1", "C"], ["E", "A", "N"]]
    depth_16 = [["A", "I", "C"], ["L", "\u25A1", "G"], ["E", "A", "N"]]
    depth_20 = [["C", "A", "N"], ["E", "A", "L"], ["I", "G", "\u25A1"]]
    depth_24 = [["\u25A1", "C", "N"], ["E", "I", "A"], ["G", "L", "A"]]
    depth_31 = [["A", "I", "C"], ["N", "L", "E"], ["G", "\u25A1", "A"]]
    bridge = [["A", "N", "G"], ["E", "L", "I"], ["A", "C", "\u25A1"]]

    puzzle = Puzzle(depth_31)
    sol = search(puzzle, uniform_queueing)

    if sol is not None:
        solved_puzzle, max_queue, expanded_nodes = sol
        path = solved_puzzle.get_path_nodes(puzzle)
        for node in path:
            print(node, end="\n\n")

        print("Depth:", solved_puzzle.cost)
        print("Path:", solved_puzzle.path)
        print("Maximum Queue Size:", max_queue)
        print("Nodes Expanded:", expanded_nodes)
    else:
        print(puzzle)
        print("No solution")
