from search import *
from typing import Dict
import csv


def run_puzzles(puzzle_states: Dict):
    headers = [
        "name",
        "depth",
        "uniform_cost_max_queue",
        "misplaced_tile_max_queue",
        "manhattan_dist_max_queue",
        "uniform_cost_nodes_expanded",
        "misplaced_tile_nodes_expanded",
        "manhattan_dist_nodes_expanded",
    ]

    rows = []

    for key in puzzle_states:
        print(key)
        data = []
        puzzle = Puzzle(puzzle_states[key])
        uniform_sol = search(puzzle, uniform_queueing)
        misplaced_tile_sol = search(puzzle, misplaced_tile_queueing)
        manhattan_dist_sol = search(puzzle, manhattan_distance_queueing)

        if (
            uniform_sol is not None
            and misplaced_tile_sol is not None
            and manhattan_dist_sol is not None
        ):
            u_solved_puzzle, u_max_queue, u_expanded_nodes = uniform_sol
            mt_solved_puzzle, mt_max_queue, mt_expanded_nodes = misplaced_tile_sol
            md_solved_puzzle, md_max_queue, md_expanded_nodes = manhattan_dist_sol

            data.extend([key, len(u_solved_puzzle.path)])
            data.extend([u_max_queue, mt_max_queue, md_max_queue])
            data.extend([u_expanded_nodes, mt_expanded_nodes, md_expanded_nodes])
            rows.append(data)

    with open("search_logs.csv", "w") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(headers)
        csvwriter.writerows(rows)


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
    default = [["A", "C", "I"], ["L", "E", "G"], ["N", "A", "\u25A1"]]

    initial_states = {
        "depth_0": depth_0,
        "depth_2": depth_2,
        "depth_4": depth_4,
        "depth_8": depth_8,
        "depth_12": depth_12,
        "depth_16": depth_16,
        "depth_20": depth_20,
        "depth_24": depth_24,
        "depth_31": depth_31,
    }

    # run_puzzles(initial_states)

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
