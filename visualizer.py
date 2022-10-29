import numpy as np
import matplotlib
from uib_inf100_graphics import *
from algorithms import *

SORTING_SIZE = 20
GRAPH_SIZE = 50
WALL_FREQ = 1500
WALL_WEIGHT = 50
MARGIN = 50
WALL_LIMIT = WALL_FREQ*3

BOARD_COLOR = 'gainsboro'
WHITE_TEXT = 'gainsboro'
INSTRUCTION_COLOR = WHITE_TEXT

ARRAY_COLOR = 'mediumseagreen'
SRC_NODE_COLOR = 'lime'
END_NODE_COLOR = 'orangered'
WALL_COLOR = 'gray'
PATH_COLOR = 'sandybrown'
PATH_THROUGH_WALL_COLOR = 'chocolate'
VISITED_COLOR = 'cornflowerblue'
VISITED_WALL_COLOR = 'lightskyblue'
BG_COLOR = 'lightslategray'

def bubble_sort_mod(arr, i, j):
    n = len(arr)-1
    if i == n:
        return (arr, i, j)
    if arr[j] > arr[j+1]:
        arr[j], arr[j+1] = swap(arr[j], arr[j+1])
    j += 1
    if j == n-i: 
        j = 0
        i += 1
    return (arr, i, j)


# declaring variables
def app_started(app):
    app.display = False
    app.starting_screen = True
    app.timer_delay = 1
    app.sorting = True
    app.unsorted = True
    app.swap_count = 0
    app.i = 0
    app.j = 0

    app.graph = True
    app.wall_freq = WALL_FREQ
    app.path_found = False
    # app.wall_weight = WALL_WEIGHT

    if app.sorting:
        app.board = set_board()
        app.array = set_unsorted(app)
        app.sorted_array = sorted(app.array)

    if app.graph:
        app.board2 = set_board_with_walls(app)
        app.src = get_source_node(app)
        app.end = get_end_node(app)
        app.path_dist = 0
        app.wall_count = 0


def timer_fired(app):
    if app.display and app.unsorted:
        display_bubble_sort(app)
    
    
def display_dijkstra(app):
    app.board = set_board_with_walls(app)
    app.src = get_source_node(app)
    app.end = get_end_node(app)
    app.path_dist = 0
    app.wall_count = 0
    draw_dijkstra(app, app.src, app.end)

def display_bubble_sort(app):
    app.board = set_board()
    draw_bubble_sort(app)


def key_pressed(app, event):
    if event.key == 'q':
        exit(0)
    
    if app.starting_screen:
        if event.key == 'Space':
            app.starting_screen = False
    
    if event.key == 'Escape':
        app.starting_screen = True
        app.display = False
        reset_all(app)
    
    if not app.starting_screen:

        if app.graph:
            if event.key == 'k':
                app.board2 = set_board_with_walls(app)
                app.src = get_source_node(app)
                app.end = get_end_node(app)
                app.path_dist = 0
                app.wall_count = 0
                app.path_found = False
            
            if event.key == 'Up':
                increase_wall_weight(app)
            if event.key == 'Down':
                decrease_wall_weight(app)

            if not app.path_found:
                if event.key == 'l':
                    app.path_dist = 0
                    app.wall_count = 0
                    draw_dijkstra(app, app.src, app.end)
            
        if app.sorting:
            if event.key == 's':
                app.board = set_board()
                app.array = set_unsorted(app)
                app.swap_count = 0
                app.unsorted = True
                app.display = False
                app.i = 0
                app.j = 0
                
            
            if app.unsorted:
                if event.key == 'd':
                    app.display = not app.display
                    app.i = 0
                    app.j = 0
                    app.board = set_board()
                    draw_bubble_sort(app)
                    
def reset_all(app):
    app.board2 = set_board_with_walls(app)
    app.src = get_source_node(app)
    app.end = get_end_node(app)
    app.path_dist = 0
    app.wall_count = 0
    app.path_found = False
    app.board = set_board()
    app.array = set_unsorted(app)
    app.swap_count = 0
    app.unsorted = True
    app.display = False
    app.i = 0
    app.j = 0
    app.wall_freq = WALL_FREQ

# initilizing the board with all zeros
def set_board():
    return np.ones((SORTING_SIZE, SORTING_SIZE))

def set_board_with_walls(app):
    board = np.ones((GRAPH_SIZE, GRAPH_SIZE))
    for _ in range(app.wall_freq):
        random_row_idx = np.random.randint(0, GRAPH_SIZE)
        random_col_idx = np.random.randint(0, GRAPH_SIZE)
        if board[random_row_idx][random_col_idx] >= 0:
            board[random_row_idx][random_col_idx] = WALL_WEIGHT
    
    return board

# graph functions
def get_source_node(app):
    random_row_idx = np.random.randint(GRAPH_SIZE/2, GRAPH_SIZE)
    random_col_idx = np.random.randint(GRAPH_SIZE/2, GRAPH_SIZE)
    app.board2[random_row_idx][random_col_idx] = 2
    return random_row_idx, random_col_idx

def get_end_node(app):
    random_row_idx = np.random.randint(0, GRAPH_SIZE/2)
    random_col_idx = np.random.randint(0, GRAPH_SIZE/2)
    app.board2[random_row_idx][random_col_idx] = 3
    return random_row_idx, random_col_idx

def draw_dijkstra(app, src, end):
    dist, prev, visited = dijkstra(app.board2, src)
    path = find_shortest_path(prev, end)

    if len(path) > 0:
        path.pop(0)
        path.pop(len(path)-1)

    for row in range(GRAPH_SIZE):
        for col in range(GRAPH_SIZE):
            if visited[row][col]:
                val = app.board2[row][col]
                if val not in (2, 3):
                    if val == 1: 
                        app.board2[row][col] = -5
                    if val == WALL_WEIGHT: 
                        app.board2[row][col] = -6

    for point in path:
        if app.board2[point[0]][point[1]] == -5:
            # app.path_dist += WALL_WEIGHT
            app.board2[point[0]][point[1]] = -3
        else:
            app.wall_count += 1
            # app.path_dist += 1
            app.board2[point[0]][point[1]] = -4
    
    app.path_found = True

def increase_wall_weight(app):
    if app.wall_freq < WALL_LIMIT:
        app.wall_freq += 100

def decrease_wall_weight(app):
    if app.wall_freq != 0:    
        app.wall_freq -= 100

# sorting functions
def set_unsorted(app):
    arrays = []
    for row_idx in range(SORTING_SIZE):
        random_limit = np.random.randint(0, SORTING_SIZE)
        arrays.append(random_limit)
        app.board[row_idx][:random_limit] = -7
    
    turn_board(app)
    app.array = np.array(arrays)
    return arrays


def draw_bubble_sort(app):
    app.array, app.i, app.j = bubble_sort_mod(app.array, app.i, app.j)

    for i in range(SORTING_SIZE):
        app.board[i][:app.array[i]] = -7
    turn_board(app)
    

def turn_board(app):
    app.board = np.flip(app.board, axis=1).T

# getting the colors
def get_color(num):
    if num == 1:
        return BOARD_COLOR
    if num == WALL_WEIGHT:
        return WALL_COLOR
    if num == 2:
        return SRC_NODE_COLOR
    if num == 3:
        return END_NODE_COLOR
    if num == -3:
        return PATH_COLOR
    if num == -4: 
        return PATH_THROUGH_WALL_COLOR
    if num == -5:
        return VISITED_WALL_COLOR
    if num == -6:    
        return VISITED_COLOR
    if num == -7:
        return ARRAY_COLOR
    else: 
        return BG_COLOR

def get_random_color():
    colors = list(matplotlib.colors.cnames.keys())
    colors.remove('rebeccapurple')
    random_idx = np.random.randint(0, len(colors))
    return colors[random_idx]

# drawing the game board
def draw_board(canvas, x1, y1, x2, y2, board, size):
    width = abs(x1-x2) / size
    height = abs(y1-y2) / size

    for row in range(size):
        for col in range(size):
            cx1 = x1 + (width*col)
            cy1 = y1 + (height*row)
            cx2 = cx1 + width
            cy2 = cy1 + height

            color = get_color(board[row][col])
            canvas.create_rectangle(cx1, cy1, cx2, cy2, fill=color, outline='black')

def draw_white_board(canvas, x1, y1, x2, y2, size):
    width = abs(x1-x2) / size
    height = abs(y1-y2) / size

    for row in range(size):
        for col in range(size):
            cx1 = x1 + (width*col)
            cy1 = y1 + (height*row)
            cx2 = cx1 + width
            cy2 = cy1 + height

            color = BG_COLOR
            canvas.create_rectangle(cx1, cy1, cx2, cy2, fill=color, outline=color)


def redraw_all(app, canvas):

    # drawing the board
    canvas.create_rectangle(0, 0, app.width, app.height, fill=BG_COLOR, outline=BG_COLOR)
    draw_board(canvas, MARGIN, MARGIN*2, (app.width/2)-MARGIN, app.height-MARGIN, app.board, SORTING_SIZE)
    draw_board(canvas, (app.width/2)+MARGIN, MARGIN*2, (app.width)-MARGIN, app.height-MARGIN, app.board2, GRAPH_SIZE)

    if app.starting_screen:
        draw_white_board(canvas, 0, 0, app.width, app.height, GRAPH_SIZE)
        canvas.create_text(app.width/2, app.height/2.5, text='ALGORITHM\nVISUALIZER',
                        font='Arial 100 bold', fill='black')
        
        canvas.create_text(app.width/2, app.height/1.25, text='PRESS SPACE TO START',
                        font='Arial 40 bold', fill=INSTRUCTION_COLOR)

    if not app.starting_screen:
        # top text
        canvas.create_text(app.width/4, MARGIN/2, text='SORTING VISUALIZER',
                        font='Arial 30 bold', fill='black')
        
        canvas.create_text(app.width/1.33, MARGIN/2, text='PATH FINDER VISUALIZER',
                        font='Arial 30 bold', fill='black')
        
        if app.wall_count == 1:
            canvas.create_text(app.width/1.33, MARGIN*1.2, text=f'Went through {app.wall_count} wall',
                            font='Arial 20 bold', fill='black')
        else:
            canvas.create_text(app.width/1.33, MARGIN*1.2, text=f'Went through {app.wall_count} walls',
                            font='Arial 20 bold', fill='black')
        
        canvas.create_text(app.width/1.33, MARGIN*1.7, text=f'Wall frequency: {app.wall_freq}',
                            font='Arial 15 bold', fill='black')

        canvas.create_text(MARGIN/1.25, MARGIN/2, text='ESC\nto quit',
                        font='Arial 12 bold', fill=INSTRUCTION_COLOR)

        canvas.create_text(app.width-(MARGIN*1.5), MARGIN/1.5, text='Adjust wall\nfrequency with\nUP/DOWN',
                        font='Arial 12 bold', fill=INSTRUCTION_COLOR)
        
        
        canvas.create_text(app.width/4, MARGIN*1.2, text='Bubble Sort',
                        font='Arial 20 bold', fill='black')
        

        # bottom text
        canvas.create_text(app.width/8, app.height-(MARGIN/2), text='press S to shuffle',
                        font='Arial 25 bold', fill=INSTRUCTION_COLOR)
        
        canvas.create_text(app.width/2.6, app.height-(MARGIN/2), text='press D to sort',
                        font='Arial 25 bold', fill=INSTRUCTION_COLOR)

        canvas.create_text(app.width/1.6, app.height-(MARGIN/2), text='press K to shuffle',
                        font='Arial 25 bold', fill=INSTRUCTION_COLOR)
        
        canvas.create_text(app.width/1.15, app.height-(MARGIN/2), text='press L to find path',
                        font='Arial 25 bold', fill=INSTRUCTION_COLOR)

l = [0, 0, 0, 4, 5, 5, 6, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 17, 18, 0]

# print(l)
# for _ in range(5):
#     print(bubble_sort_mod(l))

# starting the game
run_app(width=1440, height=775, title="VISUALIZER")