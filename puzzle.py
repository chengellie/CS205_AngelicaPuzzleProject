from util import Direction
from typing import List, Optional
from enum import Enum
import copy


class Puzzle:
    def __init__(
        self,
        puzzle_state: List[List[str]],
        goal_state: Optional[List[List[str]]] = None,
        blank: str = "\u25A1",
    ) -> None:
        """Input puzzle state and optionally puzzle size, return None. Construct puzzle object."""
        self.size = len(puzzle_state)
        self.blank = blank
        self.puzzle_state = puzzle_state
        self.goal_state = []
        self.tile_goal_pos = {}
        self.blank_coord = []
        self.path = []
        self.cost = 0
        self.misplaced_tile_heuristic = 0
        self.manhattan_distance_heuristic = 0

        self.__init_goal_state(goal_state)
        self.__init_blank_coord()

    def __init_goal_state(self, goal_state: Optional[List[List[str]]]) -> None:
        """Inputs goal state, returns None. Initializes goal state of puzzle and positions of tiles in the goal state."""
        self.goal_state = (
            [["A", "N", "G"], ["E", "L", "I"], ["C", "A", "\u25A1"]]
            if goal_state is None
            else goal_state
        )

        for i in range(self.size):
            for j in range(self.size):
                tile = self.goal_state[i][j]
                if tile != self.blank:
                    if tile not in self.tile_goal_pos:
                        self.tile_goal_pos[tile] = [(i, j)]
                    else:
                        self.tile_goal_pos[tile].append((i, j))

    def __init_blank_coord(self) -> None:
        """Inputs None, returns None. Initialize coordinates of blank."""
        for i in range(self.size):
            for j in range(self.size):
                if self.puzzle_state[i][j] == self.blank:
                    self.blank_coord = [i, j]
                    return

    def __str__(self) -> str:
        """Inputs None, returns grid representation of puzzle.
        Overloads print function for puzzle object.
        """
        output = ""
        pipes = ""
        for col in range(self.size):
            pipes += "|"
            if col != range(self.size - 1):
                pipes += "   "

        for i, row in enumerate(self.puzzle_state):
            for j, char in enumerate(row):
                output += char
                if j < len(row) - 1:
                    output += " - "
            if i < len(row) - 1:
                output += "\n" + pipes + "\n"

        return output

    def set_misplaced_tile_heuristic(self) -> None:
        """Inputs None, returns None. Finds number of misplaced tiles."""
        h = 0
        for i in range(self.size):
            for j in range(self.size):
                if (
                    self.puzzle_state[i][j] != self.blank
                    and self.puzzle_state[i][j] != self.goal_state[i][j]
                ):
                    h += 1

        self.misplaced_tile_heuristic = h

    def set_manhattan_distance_heuristic(self) -> None:
        """Inputs None, returns None. Finds sum of manhattan distances between each misplaced tile and its goal state position."""
        h = 0
        for i in range(self.size):
            for j in range(self.size):
                tile = self.puzzle_state[i][j]
                if tile != self.blank and tile != self.goal_state[i][j]:
                    h += min(
                        [
                            abs(i - goal_pos[0]) + abs(j - goal_pos[1])
                            for goal_pos in self.tile_goal_pos[tile]
                        ]
                    )

        self.manhattan_distance_heuristic = h

    def key(self) -> str:
        """Inputs None, returns string. Generates key, stringified puzzle state."""
        # https://stackoverflow.com/questions/103844/how-do-i-merge-a-2d-array-in-python-into-one-string-with-list-comprehension
        return "".join([j for i in self.puzzle_state for j in i])

    def is_solution(self) -> bool:
        """Inputs None, returns bool. Determines whether puzzle is goal state."""
        return self.puzzle_state == self.goal_state

    def __is_valid_move(self, dir: Enum) -> bool:
        """Inputs direction, returns bool. Determines whether moving in given direction is valid."""
        if (
            (dir == Direction.LEFT and self.blank_coord[1] - 1 < 0)
            or (dir == Direction.RIGHT and self.blank_coord[1] + 1 >= self.size)
            or (dir == Direction.UP and self.blank_coord[0] - 1 < 0)
            or (dir == Direction.DOWN and self.blank_coord[0] + 1 >= self.size)
        ):
            return False
        else:
            return True

    def __swap_tiles(self, new_coord: List[int]) -> None:
        """Inputs new coordinates of blank, returns None. Swap content of the current and new blank coordinates."""
        (
            self.puzzle_state[self.blank_coord[0]][self.blank_coord[1]],
            self.puzzle_state[new_coord[0]][new_coord[1]],
        ) = (
            self.puzzle_state[new_coord[0]][new_coord[1]],
            self.puzzle_state[self.blank_coord[0]][self.blank_coord[1]],
        )
        self.blank_coord = new_coord

    def move(self, dir: Enum) -> Optional["Puzzle"]:
        """Inputs direction of move, returns new puzzle. Performs move if legal."""
        if not self.__is_valid_move(dir):
            return

        # https://stackoverflow.com/questions/18713321/element-wise-addition-of-2-lists
        new_puzzle = copy.deepcopy(self)
        new_puzzle.__swap_tiles([sum(x) for x in zip(self.blank_coord, dir.value)])
        new_puzzle.cost += 1
        new_puzzle.path.append(dir.name)

        return new_puzzle

    def get_path_nodes(self, initial_node: "Puzzle") -> List["Puzzle"]:
        """Inputs initial node, returns list of puzzle nodes. Finds puzzle nodes on path to current node."""
        path_nodes = [initial_node]
        for idx, dir in enumerate(self.path):
            # https://www.programiz.com/python-programming/methods/built-in/getattr
            next_node = path_nodes[idx].move(getattr(Direction, dir))
            if next_node is None:
                raise Exception(f"Move {idx + 1} is not valid")
            path_nodes.append(next_node)

        return path_nodes


if __name__ == "__main__":
    puzzle = Puzzle([["A", "N", "G"], ["E", "L", "C"], ["I", "\u25A1", "A"]])
    puzzle.set_misplaced_tile_heuristic()
    puzzle.set_manhattan_distance_heuristic()
    print(puzzle.misplaced_tile_heuristic)
    print(puzzle.manhattan_distance_heuristic)
