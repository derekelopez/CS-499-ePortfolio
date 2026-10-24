"""
CS499 Computer Science Capstone SNHU.
Artifact: Pirate Intelligent Agent

Enhanced TreasureMaze environment for the Pirate Intelligent Agent.

Enhancements include:
- Maze validation
- Starting-position validation
- Action validation
- Correct state initialization
- Improved reward handling
- Clear error handling
- Valid-action filtering

Enhanced by Derek Lopez
Year 2026
"""

import numpy as np


# Visual markers used when drawing the maze.
visited_mark = 0.8
pirate_mark = 0.5


# The agent can move in one of four directions.
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3


class TreasureMaze(object):
    """
    Represent the Treasure Hunt maze environment.

    Maze cells:
        1.0 = free cell
        0.0 = blocked cell

    The pirate attempts to navigate from a valid starting
    position to the treasure located in the bottom-right cell.
    """

    def __init__(self, maze, pirate=(0, 0)):
        """Initialize and validate the maze environment."""

        self._maze = np.asarray(
            maze,
            dtype=float
        )

        # The maze must be two-dimensional.
        if self._maze.ndim != 2:
            raise ValueError(
                "Maze must be a two-dimensional array."
            )

        nrows, ncols = self._maze.shape

        # Require a usable maze size.
        if nrows < 2 or ncols < 2:
            raise ValueError(
                "Maze must contain at least 2 rows and 2 columns."
            )

        # Maze cells must contain only 0.0 or 1.0.
        if not np.all(
            np.isin(
                self._maze,
                [0.0, 1.0]
            )
        ):
            raise ValueError(
                "Maze cells must contain only 0.0 or 1.0."
            )

        # The treasure is located in the bottom-right cell.
        self.target = (
            nrows - 1,
            ncols - 1
        )

        if self._maze[self.target] == 0.0:
            raise ValueError(
                "Invalid maze: target cell cannot be blocked."
            )

        # Build the list of valid starting cells.
        self.free_cells = [
            (row, col)
            for row in range(nrows)
            for col in range(ncols)
            if self._maze[row, col] == 1.0
        ]

        # The treasure itself is not a valid starting cell.
        self.free_cells.remove(
            self.target
        )

        if pirate not in self.free_cells:
            raise ValueError(
                "Invalid pirate location: "
                "pirate must start on a free cell."
            )

        # Initialize the first episode.
        self.reset(pirate)

    def reset(self, pirate):
        """
        Reset the maze and place the pirate at a valid
        starting cell.
        """

        # Validate coordinate structure.
        if (
            not isinstance(
                pirate,
                (tuple, list)
            )
            or len(pirate) != 2
        ):
            raise ValueError(
                "Pirate position must be a "
                "(row, column) coordinate."
            )

        row, col = pirate

        # Coordinates must be integer values.
        if (
            not isinstance(
                row,
                (int, np.integer)
            )
            or not isinstance(
                col,
                (int, np.integer)
            )
        ):
            raise TypeError(
                "Pirate row and column must be integers."
            )

        nrows, ncols = self._maze.shape

        # Validate maze boundaries.
        if not (
            0 <= row < nrows
            and 0 <= col < ncols
        ):
            raise ValueError(
                "Pirate position is outside "
                "the maze boundaries."
            )

        # The pirate cannot begin on the treasure.
        if (row, col) == self.target:
            raise ValueError(
                "Pirate cannot start on the treasure cell."
            )

        # The starting position must be open.
        if self._maze[row, col] != 1.0:
            raise ValueError(
                "Pirate must start on a free cell."
            )

        self.pirate = (
            row,
            col
        )

        self.maze = np.copy(
            self._maze
        )

        # Initialize the current state.
        #
        # State format:
        # (row, column, movement mode)
        self.state = (
            row,
            col,
            "start"
        )

        # Prevent an episode from running indefinitely.
        self.min_reward = (
            -0.5 * self.maze.size
        )

        self.total_reward = 0

        # Track previously visited cells.
        self.visited = set()

    def update_state(self, action):
        """
        Update the pirate state after performing an action.
        """

        # Action must be an integer.
        if not isinstance(
            action,
            (int, np.integer)
        ):
            raise TypeError(
                "Action must be an integer."
            )

        # Action must correspond to one of the four directions.
        if action not in (
            LEFT,
            UP,
            RIGHT,
            DOWN
        ):
            raise ValueError(
                "Action must be LEFT, UP, RIGHT, or DOWN."
            )

        pirate_row, pirate_col, mode = self.state

        # Initialize the next position using the current position.
        nrow = pirate_row
        ncol = pirate_col
        nmode = mode

        # Record the current free cell as visited.
        if self.maze[
            pirate_row,
            pirate_col
        ] > 0.0:
            self.visited.add(
                (
                    pirate_row,
                    pirate_col
                )
            )

        valid_actions = self.valid_actions()

        # No legal movement is available.
        if not valid_actions:
            nmode = "blocked"

        # Perform a valid movement.
        elif action in valid_actions:
            nmode = "valid"

            if action == LEFT:
                ncol -= 1

            elif action == UP:
                nrow -= 1

            elif action == RIGHT:
                ncol += 1

            elif action == DOWN:
                nrow += 1

        # Invalid action leaves the pirate in place.
        else:
            nmode = "invalid"

        self.state = (
            nrow,
            ncol,
            nmode
        )

    def get_reward(self):
        """
        Calculate the reward for the current state.
        """

        pirate_row, pirate_col, mode = self.state

        # Maximum positive reward for reaching the treasure.
        if (
            pirate_row,
            pirate_col
        ) == self.target:
            return 1.0

        # Strong penalty when the pirate becomes blocked.
        if mode == "blocked":
            return self.min_reward - 1

        # Invalid moves receive their intended penalty
        # before checking whether the cell was visited.
        if mode == "invalid":
            return -0.75

        # Revisiting a cell receives a smaller penalty.
        if (
            pirate_row,
            pirate_col
        ) in self.visited:
            return -0.25

        # Valid movement has a small step penalty.
        if mode == "valid":
            return -0.04

        # "start" should not normally request a reward.
        if mode == "start":
            return 0.0

        raise ValueError(
            f"Unexpected state mode: {mode}"
        )

    def act(self, action):
        """
        Perform an action and return the resulting
        observation, reward, and game status.
        """

        self.update_state(action)

        reward = self.get_reward()

        self.total_reward += reward

        status = self.game_status()

        envstate = self.observe()

        return (
            envstate,
            reward,
            status
        )

    def observe(self):
        """
        Flatten the maze into an observation vector.
        """

        canvas = self.draw_env()

        envstate = canvas.reshape(
            (1, -1)
        )

        return envstate

    def draw_env(self):
        """
        Return a visual representation of the maze.
        """

        canvas = np.copy(
            self.maze
        )

        nrows, ncols = self.maze.shape

        # Clear previous visual marks.
        for row in range(nrows):
            for col in range(ncols):
                if canvas[
                    row,
                    col
                ] > 0.0:
                    canvas[
                        row,
                        col
                    ] = 1.0

        # Draw the pirate at the current position.
        row, col, _ = self.state

        canvas[
            row,
            col
        ] = pirate_mark

        return canvas

    def game_status(self):
        """
        Return win, lose, or not_over based on
        the current episode state.
        """

        # If cumulative reward drops below the minimum,
        # the episode is considered lost.
        if self.total_reward < self.min_reward:
            return "lose"

        pirate_row, pirate_col, _ = self.state

        # Reaching the treasure wins the game.
        if (
            pirate_row,
            pirate_col
        ) == self.target:
            return "win"

        return "not_over"

    def valid_actions(self, cell=None):
        """
        Return the valid movement actions from either
        the current position or a supplied cell.
        """

        if cell is None:
            row, col, _ = self.state

        else:
            if (
                not isinstance(
                    cell,
                    (tuple, list)
                )
                or len(cell) != 2
            ):
                raise ValueError(
                    "Cell must be a "
                    "(row, column) coordinate."
                )

            row, col = cell

            if (
                not isinstance(
                    row,
                    (int, np.integer)
                )
                or not isinstance(
                    col,
                    (int, np.integer)
                )
            ):
                raise TypeError(
                    "Cell row and column must be integers."
                )

            nrows, ncols = self.maze.shape

            if not (
                0 <= row < nrows
                and 0 <= col < ncols
            ):
                raise ValueError(
                    "Cell is outside the maze boundaries."
                )

        actions = [
            LEFT,
            UP,
            RIGHT,
            DOWN
        ]

        nrows, ncols = self.maze.shape

        # Remove actions that would leave the maze.
        if row == 0:
            actions.remove(UP)

        elif row == nrows - 1:
            actions.remove(DOWN)

        if col == 0:
            actions.remove(LEFT)

        elif col == ncols - 1:
            actions.remove(RIGHT)

        # Remove movements into blocked cells.
        if (
            row > 0
            and self.maze[
                row - 1,
                col
            ] == 0.0
            and UP in actions
        ):
            actions.remove(UP)

        if (
            row < nrows - 1
            and self.maze[
                row + 1,
                col
            ] == 0.0
            and DOWN in actions
        ):
            actions.remove(DOWN)

        if (
            col > 0
            and self.maze[
                row,
                col - 1
            ] == 0.0
            and LEFT in actions
        ):
            actions.remove(LEFT)

        if (
            col < ncols - 1
            and self.maze[
                row,
                col + 1
            ] == 0.0
            and RIGHT in actions
        ):
            actions.remove(RIGHT)

        return actions