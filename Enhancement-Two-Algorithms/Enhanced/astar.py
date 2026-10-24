"""
CS499 Computer Science Capstone SNHU.
Artifact: Pirate Intelligent Agent

A* pathfinding algorithm for the Pirate Intelligent Agent enhancement.
This module provides a deterministic maze-solving approach that can be
compared with the existing Deep Q-Learning solution.

Enhanced by Derek Lopez
Year 2026
"""

from dataclasses import dataclass
from heapq import heappop, heappush
from time import perf_counter

import numpy as np


@dataclass
class AStarResult:
    """Store the results of one A* search."""

    path: list
    path_length: int
    explored_count: int
    execution_time: float
    success: bool


def manhattan_distance(cell, goal):
    """Calculate Manhattan distance between two maze cells."""

    row1, col1 = cell
    row2, col2 = goal

    return abs(row1 - row2) + abs(col1 - col2)


def validate_maze(maze):
    """Validate the maze before running A*."""

    maze = np.asarray(maze)

    if maze.ndim != 2:
        raise ValueError(
            "Maze must be a two-dimensional array."
        )

    rows, cols = maze.shape

    if rows < 2 or cols < 2:
        raise ValueError(
            "Maze must contain at least 2 rows and 2 columns."
        )

    return maze


def validate_cell(maze, cell, name="cell"):
    """Validate a start or goal coordinate."""

    if not isinstance(cell, (tuple, list)) or len(cell) != 2:
        raise ValueError(
            f"{name} must be a (row, column) coordinate."
        )

    row, col = cell

    if (
        not isinstance(row, (int, np.integer))
        or not isinstance(col, (int, np.integer))
    ):
        raise TypeError(
            f"{name} row and column must be integers."
        )

    rows, cols = maze.shape

    if not (0 <= row < rows and 0 <= col < cols):
        raise ValueError(
            f"{name} is outside the maze boundaries."
        )

    if maze[row, col] != 1.0:
        raise ValueError(
            f"{name} must be located on a free cell."
        )

    return row, col


def get_neighbors(maze, cell):
    """
    Return all valid neighboring cells.

    Movement is limited to four directions:
    left, up, right, and down.
    """

    row, col = cell
    rows, cols = maze.shape

    possible_neighbors = [
        (row, col - 1),  # Left
        (row - 1, col),  # Up
        (row, col + 1),  # Right
        (row + 1, col),  # Down
    ]

    neighbors = []

    for next_row, next_col in possible_neighbors:

        if not (
            0 <= next_row < rows
            and 0 <= next_col < cols
        ):
            continue

        if maze[next_row, next_col] != 1.0:
            continue

        neighbors.append(
            (next_row, next_col)
        )

    return neighbors


def reconstruct_path(parent, goal):
    """
    Reconstruct the path by following parent links
    from the goal back to the start.
    """

    path = [goal]
    current = goal

    while current in parent:
        current = parent[current]
        path.append(current)

    path.reverse()

    return path


def astar_search(maze, start, goal=None):
    """
    Find the shortest path through the maze using A*.

    Maze values:
        1.0 = open cell
        0.0 = blocked cell

    Args:
        maze: Two-dimensional maze array.
        start: Starting (row, column) coordinate.
        goal: Goal coordinate. If omitted, the bottom-right
              cell is used.

    Returns:
        AStarResult containing the path, path length,
        explored-cell count, execution time, and success status.
    """

    start_time = perf_counter()

    maze = validate_maze(maze)

    rows, cols = maze.shape

    # Use the bottom-right cell as the default goal.
    if goal is None:
        goal = (
            rows - 1,
            cols - 1
        )

    # Validate both start and goal regardless of whether
    # the goal was supplied explicitly or generated above.
    start = validate_cell(
        maze,
        start,
        "Start"
    )

    goal = validate_cell(
        maze,
        goal,
        "Goal"
    )

    # The starting position is already the goal.
    if start == goal:
        elapsed = perf_counter() - start_time

        return AStarResult(
            path=[start],
            path_length=0,
            explored_count=1,
            execution_time=elapsed,
            success=True
        )

    # Priority queue entries:
    # (estimated total cost, actual cost, cell)
    open_heap = []

    start_h = manhattan_distance(
        start,
        goal
    )

    heappush(
        open_heap,
        (
            start_h,
            0,
            start
        )
    )

    # Lowest known cost from the start to each cell.
    g_cost = {
        start: 0
    }

    # Parent links used to reconstruct the final path.
    parent = {}

    # Cells that have already been explored.
    explored = set()

    while open_heap:

        _, current_g, current = heappop(
            open_heap
        )

        if current in explored:
            continue

        explored.add(current)

        # Goal reached.
        if current == goal:
            path = reconstruct_path(
                parent,
                goal
            )

            elapsed = (
                perf_counter() - start_time
            )

            return AStarResult(
                path=path,
                path_length=len(path) - 1,
                explored_count=len(explored),
                execution_time=elapsed,
                success=True
            )

        for neighbor in get_neighbors(
            maze,
            current
        ):

            if neighbor in explored:
                continue

            # Every maze movement has a cost of 1.
            tentative_g = current_g + 1

            old_g = g_cost.get(
                neighbor,
                float("inf")
            )

            if tentative_g < old_g:
                parent[neighbor] = current

                g_cost[neighbor] = tentative_g

                heuristic = manhattan_distance(
                    neighbor,
                    goal
                )

                estimated_total = (
                    tentative_g + heuristic
                )

                heappush(
                    open_heap,
                    (
                        estimated_total,
                        tentative_g,
                        neighbor
                    )
                )

    # No path was found.
    elapsed = (
        perf_counter() - start_time
    )

    return AStarResult(
        path=[],
        path_length=0,
        explored_count=len(explored),
        execution_time=elapsed,
        success=False
    )