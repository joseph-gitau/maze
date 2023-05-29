from PIL import Image, ImageDraw

def make_step(maze, m, k):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == k:
                if i > 0 and m[i-1][j] == 0 and maze[i-1][j] == 0:
                    m[i-1][j] = k + 1
                if j > 0 and m[i][j-1] == 0 and maze[i][j-1] == 0:
                    m[i][j-1] = k + 1
                if i < len(m) - 1 and m[i+1][j] == 0 and maze[i+1][j] == 0:
                    m[i+1][j] = k + 1
                if j < len(m[i]) - 1 and m[i][j+1] == 0 and maze[i][j+1] == 0:
                    m[i][j+1] = k + 1

def print_m(m):
    for row in m:
        for val in row:
            print(str(val).ljust(2), end=' ')
        print()

def draw_matrix(maze, m, the_path=[]):
    zoom = 20
    borders = 6
    im = Image.new('RGB', (zoom * len(maze[0]), zoom * len(maze)), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            color = (255, 255, 255)
            r = 0
            if maze[i][j] == 1:
                color = (0, 0, 0)
            if (i, j) == start:
                color = (0, 255, 0)
                r = borders
            if (i, j) == end:
                color = (0, 255, 0)
                r = borders
            draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom-r-1, i*zoom+zoom-r-1), fill=color)
            if m[i][j] > 0:
                r = borders
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                             fill=(255, 0, 0))
    for u in range(len(the_path)-1):
        y = the_path[u][0]*zoom + int(zoom/2)
        x = the_path[u][1]*zoom + int(zoom/2)
        y1 = the_path[u+1][0]*zoom + int(zoom/2)
        x1 = the_path[u+1][1]*zoom + int(zoom/2)
        draw.line((x, y, x1, y1), fill=(255, 0, 0), width=5)
    draw.rectangle((0, 0, zoom * len(maze[0]), zoom * len(maze)), outline=(0, 255, 0), width=2)
    return im

def solve_maze(maze_file_path):
    with open(maze_file_path, "r") as file:
        maze_content = file.read()

    maze_lines = maze_content.splitlines()
    maze = []
    start = None
    end = None

    max_columns = len(maze_lines[0])

    for i, line in enumerate(maze_lines):
        maze_row = []
        for j in range(max_columns):
            if j < len(line):
                char = line[j]
            else:
                char = ' '
            if char == '%':
                maze_row.append(1)  # Wall
            elif char == 'P':
                maze_row.append(0)  # Open path (start)
                start = (i, j)
            elif char == '.':
                maze_row.append(0)  # Open path (goal)
                end = (i, j)
            elif char == ' ':
                maze_row.append(0)
        maze.append(maze_row)

    m = [[0] * len(row) for row in maze]
    i, j = start
    m[i][j] = 1

    k = 0
    while m[end[0]][end[1]] == 0:
        k += 1
        make_step(maze, m, k)

    i, j = end
    k = m[i][j]
    the_path = [(i, j)]
    while k > 1:
        if i > 0 and m[i - 1][j] == k-1:
            i, j = i-1, j
            the_path.append((i, j))
            k -= 1
        elif j > 0 and m[i][j - 1] == k-1:
            i, j = i, j-1
            the_path.append((i, j))
            k -= 1
        elif i < len(m) - 1 and m[i + 1][j] == k-1:
            i, j = i+1, j
            the_path.append((i, j))
            k -= 1
        elif j < len(m[i]) - 1 and m[i][j + 1] == k-1:
            i, j = i, j+1
            the_path.append((i, j))

    return draw_matrix(maze, m, the_path)

def generate_gif(images, maze_save_path):
    images[0].save(maze_save_path,
                   save_all=True, append_images=images[1:],
                   optimize=False, duration=1, loop=0)

maze_lay_files = ["maze/bigMaze.lay"]
# maze_lay_files = ["maze/bigMaze.lay", "maze/mediumMaze.lay", "maze/openMaze.lay", "maze/sample maze file.lay", "maze/smallMaze.lay", "maze/smallSearch.lay", "maze/tinySearch.lay", "maze/trickySearch.lay"]
images = []

for maze_file_path in maze_lay_files:
    maze_file_name = maze_file_path.split("/")[-1].split(".")[0]
    maze_save_path = "out/" + maze_file_name + ".gif"
    image = solve_maze(maze_file_path)
    images.append(image)

generate_gif(images, maze_save_path)
