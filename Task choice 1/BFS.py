# Breadth First Search (BFS) algorithm

# Import Image, ImageDraw
from PIL import Image, ImageDraw

# Define helper functions (make_step, print_m, draw_matrix)

# Helper functions

expanded_nodes = 0  # Number of nodes expanded
max_tree_depth = 0  # Maximum tree depth searched
max_fringe_size = 0  # Maximum size of the fringe


def make_step(k):
    global expanded_nodes, max_tree_depth, max_fringe_size
    
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == k:
                if i > 0 and m[i - 1][j] == 0 and maze[i - 1][j] == 0:
                    m[i - 1][j] = k + 1
                    expanded_nodes += 1
                    max_tree_depth = max(max_tree_depth, k + 1)
                    max_fringe_size = max(max_fringe_size, count_fringe_size(m))
                if j > 0 and m[i][j - 1] == 0 and maze[i][j - 1] == 0:
                    m[i][j - 1] = k + 1
                    expanded_nodes += 1
                    max_tree_depth = max(max_tree_depth, k + 1)
                    max_fringe_size = max(max_fringe_size, count_fringe_size(m))
                if i < len(m) - 1 and m[i + 1][j] == 0 and maze[i + 1][j] == 0:
                    m[i + 1][j] = k + 1
                    expanded_nodes += 1
                    max_tree_depth = max(max_tree_depth, k + 1)
                    max_fringe_size = max(max_fringe_size, count_fringe_size(m))
                if j < len(m[i]) - 1 and m[i][j + 1] == 0 and maze[i][j + 1] == 0:
                    m[i][j + 1] = k + 1
                    expanded_nodes += 1
                    max_tree_depth = max(max_tree_depth, k + 1)
                    max_fringe_size = max(max_fringe_size, count_fringe_size(m))


def count_fringe_size(m):
    fringe_size = 0
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] > 0:
                fringe_size += 1
    return fringe_size


def print_m(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(str(m[i][j]).ljust(2), end=' ')
        print()


def draw_matrix(maze, m, the_path=[]):
    im = Image.new('RGB', (zoom * len(maze[0]), zoom * len(maze)), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            color = (255, 255, 255)
            r = 0
            if maze[i][j] == 1:
                color = (0, 0, 0)
            if i == start[0] and j == start[1]:
                color = (0, 255, 0)
                r = borders
            if i == end[0] and j == end[1]:
                color = (0, 255, 0)
                r = borders
            draw.rectangle((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                           fill=color)
            if m[i][j] > 0:
                r = borders
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                             fill=(255, 0, 0))
    for u in range(len(the_path) - 1):
        y = the_path[u][0] * zoom + int(zoom / 2)
        x = the_path[u][1] * zoom + int(zoom / 2)
        y1 = the_path[u + 1][0] * zoom + int(zoom / 2)
        x1 = the_path[u + 1][1] * zoom + int(zoom / 2)
        draw.line((x, y, x1, y1), fill=(255, 0, 0), width=5)
    draw.rectangle((0, 0, zoom * len(maze[0]), zoom * len(maze)), outline=(0, 255, 0), width=2)
    images.append(im)


# Maze lay files
mazeLayFiles = ["./maze/smallMaze.lay", "./maze/mediumMaze.lay", "./maze/bigMaze.lay", "./maze/openMaze.lay"]

# Loop through each maze lay file and solve it
for maze_file_path in mazeLayFiles:
    # Define images as a list
    images = []

    # Define the maze file path
    maze_file_path = maze_file_path
    # Get the maze file name
    maze_file_name = maze_file_path.split("/")[-1].split(".")[0]
    # maze save path
    maze_save_path = "Task choice 1/out/" + maze_file_name + ".gif"

    # Read the contents of the maze file
    with open(maze_file_path, "r") as file:
        maze_content = file.read()

    # Split the maze content into lines
    maze_lines = maze_content.splitlines()

    # Initialize the maze matrix
    maze = []
    start = None
    end = None

    # Determine the maximum number of columns based on the first row
    max_columns = len(maze_lines[0])

    # Process each line in the maze content
    for i, line in enumerate(maze_lines):
        maze_row = []
        for j in range(max_columns):
            if j < len(line):
                char = line[j]
            else:
                char = ' '  # Fill empty spaces with ' ' (assumed open path)
            if char == '%':
                maze_row.append(1)  # Wall
            elif char == 'P':
                maze_row.append(0)  # Open path (start)
                start = (i, j)  # Store the start position
            elif char == '.':
                maze_row.append(0)  # Open path (goal)
                end = (i, j)  # Store the goal position
            elif char == ' ':
                maze_row.append(0)
        maze.append(maze_row)

    # Define maze-specific parameters
    zoom = 20
    borders = 6

    m = []
    for i in range(len(maze)):
        m.append([])
        for j in range(len(maze[i])):
            m[-1].append(0)
    i, j = start
    print("start", start)
    m[i][j] = 1

    k = 0
    while m[end[0]][end[1]] == 0:
        k += 1
        make_step(k)
        draw_matrix(maze, m)

    # Trace back the path
    i, j = end
    k = m[i][j]
    the_path = [(i, j)]
    while k > 1:
        if i > 0 and m[i - 1][j] == k - 1:
            i, j = i - 1, j
            the_path.append((i, j))
            k -= 1
        elif j > 0 and m[i][j - 1] == k - 1:
            i, j = i, j - 1
            the_path.append((i, j))
            k -= 1
        elif i < len(m) - 1 and m[i + 1][j] == k - 1:
            i, j = i + 1, j
            the_path.append((i, j))
            k -= 1
        elif j < len(m[i]) - 1 and m[i][j + 1] == k - 1:
            i, j = i, j + 1
            the_path.append((i, j))
            k -= 1
        draw_matrix(maze, m, the_path)

    for i in range(10):
        if i % 2 == 0:
            draw_matrix(maze, m, the_path)
        else:
            draw_matrix(maze, m)

    # Generate the GIF
    print_m(m)
    print(the_path)

    # Print the solution and its path cost
    print("Solution:")
    print_m(m)
    print("Path Cost:", len(the_path) - 1)

    # Print the number of nodes expanded
    print("Number of Nodes Expanded:", expanded_nodes)

    # Print the maximum tree depth searched
    print("Maximum Tree Depth Searched:", max_tree_depth)

    # Print the maximum size of the fringe
    print("Maximum Size of the Fringe:", max_fringe_size)

    # Save GIF file
    images[0].save(maze_save_path,
                   save_all=True, append_images=images[1:],
                   optimize=False, duration=1, loop=0)
