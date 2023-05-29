import heapq
import os
from PIL import Image, ImageDraw

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

def astar_search(maze, start, goal):
    open_set = [(0, start)]  # priority queue: (f_score, position)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(maze, current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)

                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # No path found

# Define the maze files to be used
MazeFiles = ["./maze/smallMaze.lay", "./maze/mediumMaze.lay", "./maze/bigMaze.lay", "./maze/openMaze.lay"]

# Create the 'out' directory if it doesn't exist
os.makedirs("out", exist_ok=True)

# Loop through all the maze files
for maze_file_path in MazeFiles:
    with open(maze_file_path, "r") as file:
        maze = file.read().splitlines()

    start = None
    goal = None

    # Find the start ('P') and goal ('.')
    for i, row in enumerate(maze):
        if 'P' in row:
            start = (i, row.index('P'))
        if '.' in row:
            goal = (i, row.index('.'))
        if start and goal:
            break

    path = astar_search(maze, start, goal)
    if path:
        print("Path found:")
        for row_num, row in enumerate(maze):
            new_row = list(row)
            for col_num, _ in enumerate(row):
                if (row_num, col_num) == start:
                    new_row[col_num] = 'P'
                elif (row_num, col_num) == goal:
                    new_row[col_num] = '.'
                elif (row_num, col_num) in path:
                    new_row[col_num] = '.'
            print("".join(new_row))
    else:
        print("No path found.")

    # Create an image of the maze
    image_width = len(maze[0]) * 20
    image_height = len(maze) * 20
    maze_image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(maze_image)

    for row_num, row in enumerate(maze):
        for col_num, char in enumerate(row):
            if char == '%':
                draw.rectangle([(col_num * 20, row_num * 20), ((col_num + 1) * 20, (row_num + 1) * 20)], fill="black")
            elif char == 'P':
                draw.rectangle([(col_num * 20, row_num * 20), ((col_num + 1) * 20, (row_num + 1) * 20)], fill="green")
            elif char == '.':
                draw.rectangle([(col_num * 20, row_num * 20), ((col_num + 1) * 20, (row_num + 1) * 20)], fill="red")

    # Highlight the path
    for step in path:
        row_num, col_num = step
        draw.rectangle([(col_num * 20, row_num * 20), ((col_num + 1) * 20, (row_num + 1) * 20)], fill="yellow")

    # Add start and goal markers
    start_x, start_y = start
    goal_x, goal_y = goal
    draw.rectangle([(start_y * 20, start_x * 20), ((start_y + 1) * 20, (start_x + 1) * 20)], fill="red")
    draw.rectangle([(goal_y * 20, goal_x * 20), ((goal_y + 1) * 20, (goal_x + 1) * 20)], fill="green")

    # Save the maze image as a GIF file
    maze_file_name = maze_file_path.split("/")[-1].split(".")[0]
    maze_save_path = f"Task choice 2/out/{maze_file_name}.gif"
    maze_image.save(maze_save_path)

    print(f"Maze image saved as {maze_save_path}")
