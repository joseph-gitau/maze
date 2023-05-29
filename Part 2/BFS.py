import heapq
from PIL import Image, ImageDraw
import os

def manhattan_distance(start, goal):
    # Calculate the Manhattan distance between two points
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def get_neighbors(maze, position):
    row, col = position
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        # Check if the new position is within the maze boundaries and not a wall ('%')
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] != '%':
            neighbors.append((new_row, new_col))

    return neighbors

def reconstruct_path(came_from, current):
    # Reconstruct the path from the start to the current position using the 'came_from' dictionary
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def astar_search(maze, start, goals):
    open_set = [(0, start)]  # priority queue: (f_score, position)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goals[0])}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in goals:
            goals.remove(current)
            if not goals:
                return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(maze, current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goals[0])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # No path found

def count_nodes_expanded(expanded_goals):
    count = 0
    for goal in expanded_goals:
        count += len(expanded_goals[goal])
    return count

def solve_maze_with_goals(maze_file_path):
    with open(maze_file_path, "r") as file:
        maze = file.read().splitlines()

    start = None
    goals = []

    # Find the start ('P') and goals ('.')
    for i, row in enumerate(maze):
        if 'P' in row:
            start = (i, row.index('P'))
        if '.' in row:
            goal_indices = [index for index, char in enumerate(row) if char == '.']
            for index in goal_indices:
                goals.append((i, index))

    path = astar_search(maze, start, goals)
    goals_expanded = {}

    if path:
        print("Path found:")
        for row_num, row in enumerate(maze):
            new_row = list(row)
            for col_num, _ in enumerate(row):
                if (row_num, col_num) == start:
                    new_row[col_num] = 'P'
                elif (row_num, col_num) in goals:
                    new_row[col_num] = '.'
                elif (row_num, col_num) in path:
                    new_row[col_num] = '.'
            print("".join(new_row))
    else:
        print("No path found.")

    for goal in goals:
        if goal in path:
            goals_expanded[goal] = reconstruct_path({goal: start}, goal)

    return path, goals_expanded

# Define the maze files to be used
# maze_files = ["./maze/tinySearch.lay"]
maze_files = ["./maze/tinySearch.lay", "./maze/smallSearch.lay", "./maze/trickySearch.lay"]

# Loop through all the maze files
for maze_file_path in maze_files:
    path, goals_expanded = solve_maze_with_goals(maze_file_path)
    print("Solution cost:", len(path))
    print("Number of nodes expanded:", count_nodes_expanded(goals_expanded))

