from typing import List


class Puzzle:
    def __init__(self, puzzle_state: List[str], size: int = 3) -> None:
        """Input puzzle state and optionally puzzle size, return None. Construct puzzle object."""
        self.puzzle_state = puzzle_state
        self.goal_state = []

        self.__init_goal_state__()

    def __init_goal_state__(self):
        self.goal_state = [["A", "N", "G"], ["E", "L", "I"], ["C", "A", " "]]

    def __str__(self) -> None:
        """Inputs None, returns None. Overloads print of puzzle object with grid representation."""
        output = ""
        pipes = ""
        for col in range(len(self.puzzle_state)):
            pipes += "|"
            if col != range(len(self.puzzle_state) - 1):
                pipes += "   "

        for i, row in enumerate(self.puzzle_state):
            for j, char in enumerate(row):
                output += char
                if j < len(row) - 1:
                    output += " - "
            if i < len(row) - 1:
                output += "\n" + pipes + "\n"

        return output
