from search import *
from typing import Dict, Tuple
import csv
import argparse
import time


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
        "uniform_cost_time",
        "misplaced_tile_time",
        "manhattan_dist_time",
    ]

    rows = []

    for key in puzzle_states:
        print(key)
        data = []
        puzzle = Puzzle(puzzle_states[key])

        start = time.time()
        uniform_sol = search(puzzle, uniform_queueing)
        u_time = time.time() - start
        start = time.time()
        misplaced_tile_sol = search(puzzle, misplaced_tile_queueing)
        mt_time = time.time() - start
        start = time.time()
        manhattan_dist_sol = search(puzzle, manhattan_distance_queueing)
        md_time = time.time() - start

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
            data.extend([u_time, mt_time, md_time])
            rows.append(data)

    with open("search_logs.csv", "w") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(headers)
        csvwriter.writerows(rows)


def user_input() -> Tuple:
    parser = argparse.ArgumentParser(description="Custom input for Angelica Puzzle.")
    parser.add_argument(
        "-f",
        type=str,
        metavar="{filename.txt}",
        help="Input file name with custom puzzle",
    )
    parser.add_argument(
        "-s",
        choices=["uniform-cost", "misplaced-tile", "manhattan-distance"],
        type=str,
        help="Choose search algorithm",
    )
    args = parser.parse_args()

    custom_state = []
    with open(args.f, "r") as file:
        lines = file.readlines()
        for line in lines:
            row = line.split()
            for idx, char in enumerate(row):
                if char == ".":
                    row[idx] = "\u25A1"
            custom_state.append(row)

    return custom_state, args.s


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

    run_puzzles(initial_states)
    quit()

    custom_state, search_alg = user_input()
    puzzle = Puzzle(custom_state)

    start = time.time()
    if search_alg == "uniform-cost":
        sol = search(puzzle, uniform_queueing)
    elif search_alg == "misplaced-tile":
        sol = search(puzzle, misplaced_tile_queueing)
    elif search_alg == "manhattan-distance":
        sol = search(puzzle, manhattan_distance_queueing)
    end = time.time() - start

    print("Initial State:", puzzle, sep="\n", end="\n\n")
    if sol is not None:
        solved_puzzle, max_queue, expanded_nodes = sol
        path = solved_puzzle.get_path_nodes(puzzle)
        # for node in path:
        #     print(node, end="\n\n")
        print("Solution State:", solved_puzzle, sep="\n", end="\n\n")
        print("Depth:", solved_puzzle.cost)
        print("Path:", solved_puzzle.path)
        print("Maximum Queue Size:", max_queue)
        print("Nodes Expanded:", expanded_nodes)
        print("Time:", round(end, 3), "seconds")
    else:
        print(puzzle)
        print("No solution")
