from puzzle import Puzzle
from util import PrioritizedPuzzle, Direction
from typing import Optional, Callable
from queue import PriorityQueue


def uniform_queueing(nodes: PriorityQueue, new_node: Puzzle) -> None:
    nodes.put(PrioritizedPuzzle(new_node.cost, new_node))


def misplaced_tile_queueing(nodes: PriorityQueue, new_node: Puzzle) -> None:
    new_node.set_misplaced_tile_heuristic()
    nodes.put(
        PrioritizedPuzzle(new_node.cost + new_node.misplaced_tile_heuristic, new_node)
    )


def manhattan_distance_queueing(nodes: PriorityQueue, new_node: Puzzle) -> None:
    pass


def init_queue(puzzle: Puzzle, queueing_func: Callable) -> PriorityQueue:
    """Inputs initial puzzle state and queueing function, returns None.
    Initializes cost of initial state based on given queueing function, constructs priority queue with initial state.
    """
    nodes = PriorityQueue()
    # https://stackoverflow.com/questions/60491475/pylint-w0143-warning-comparing-against-a-callable
    if queueing_func is uniform_queueing:
        nodes.put(PrioritizedPuzzle(puzzle.cost, puzzle))
    elif queueing_func is misplaced_tile_queueing:
        puzzle.set_misplaced_tile_heuristic()
        nodes.put(
            PrioritizedPuzzle(puzzle.cost + puzzle.misplaced_tile_heuristic, puzzle)
        )
    elif queueing_func is manhattan_distance_queueing:
        pass

    return nodes


def search(puzzle: Puzzle, queueing_func: Callable) -> Optional[Puzzle]:
    """Inputs initial state of puzzle and queueing function, returns solved puzzle or None if no solution.
    Performs appropriate search using given queueing function.
    """
    nodes = init_queue(puzzle, queueing_func)
    dups = {puzzle.key()}

    while not nodes.empty():
        prio_puzzle = nodes.get()
        node = prio_puzzle.item
        print("curr node:", node, "\n")
        if node.is_solution():
            return node

        for dir in Direction:
            new_node = node.move(dir)
            if new_node is not None and new_node.key() not in dups:
                queueing_func(nodes, new_node)
                dups.add(new_node.key())

    return None


if __name__ == "__main__":
    # https://www.fileformat.info/info/unicode/char/25a1/index.htm
    initial_state = [["A", "N", "G"], ["E", "L", "I"], ["\u25A1", "C", "A"]]
    puzzle = Puzzle(initial_state)
    print("Initial state:\n", puzzle, sep="", end="\n\n")

    sol = search(puzzle, uniform_queueing)
    print("sol:\n", sol, sep="")
    print("Cost:", sol.cost) if sol is not None else print("No solution")
    print("Path:", sol.path) if sol is not None else print("", end="")

    if sol is not None:
        path = sol.get_path_nodes(puzzle)
        for node in path:
            print(node, end="\n\n")
