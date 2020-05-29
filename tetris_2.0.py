"""
File: tetris_2.0.py
----------------

My second attempt at tetris using Python and Tkinter.
Functionalities include:
- Tetrominos can rotate
- Completed lines disappear
- Detects end of game
- Hard drop with space bar (technically it is just falling super fast)
- Advancing levels increases fall speed
- Displays score and level during game play
- Tetris song if soundplay module is installed

TODO: Show preview (spawn tetromino above the canvas, move once previous tetromino is placed)
TODO: Legal move for rotating pieces
TODO: Could I make the line flash before it disappears?
TODO: Decompose objects_left, objects_right, objects_below
TODO: Create levels with blocks in the way
TODO: Pause the game
"""

import tkinter
import random
import time
import math
# from soundplay import soundplay
# soundplay("tetris_theme_song.mp3")

# Constants for canvas
CANVAS_WIDTH = 500      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 1000    # Height of drawing canvas in pixels
CANVAS_MID = CANVAS_WIDTH // 2
UNIT_SIZE = 50          # Size of unit block within tetromino
Y_SPEED = UNIT_SIZE
X_SPEED = UNIT_SIZE


# Vertices for individual squares, created above the canvas, o and l are spawned in middle
# The rest of the tetrominos are spawned middle left
BLOCK_1_POINTS = [CANVAS_MID - UNIT_SIZE * 2, -UNIT_SIZE * 2, CANVAS_MID - UNIT_SIZE, -UNIT_SIZE]
BLOCK_2_POINTS = [CANVAS_MID - UNIT_SIZE, -UNIT_SIZE * 2, CANVAS_MID, -UNIT_SIZE]
BLOCK_3_POINTS = [CANVAS_MID, -UNIT_SIZE * 2, CANVAS_MID + UNIT_SIZE, -UNIT_SIZE]
BLOCK_4_POINTS = [CANVAS_MID + UNIT_SIZE, -UNIT_SIZE * 2, CANVAS_MID + UNIT_SIZE * 2, -UNIT_SIZE]
BLOCK_5_POINTS = [CANVAS_MID - UNIT_SIZE * 2, -UNIT_SIZE, CANVAS_MID - UNIT_SIZE, 0]
BLOCK_6_POINTS = [CANVAS_MID - UNIT_SIZE, -UNIT_SIZE, CANVAS_MID, 0]
BLOCK_7_POINTS = [CANVAS_MID, -UNIT_SIZE, CANVAS_MID + UNIT_SIZE, 0]
BLOCK_8_POINTS = [CANVAS_MID + UNIT_SIZE, -UNIT_SIZE, CANVAS_MID + UNIT_SIZE * 2, 0]


def create_game_board():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Tetris 2.0')
    draw_grid(canvas)
    return canvas


def create_score_label(canvas, total_score):
    return canvas.create_text(
        20, 20, 
        anchor='w', 
        fill='white', 
        font='Times 14', 
        text=f"Score: {total_score}"
    )


def create_level_label(canvas, level):
    return canvas.create_text(
        CANVAS_WIDTH - 20, 20, 
        anchor='e', 
        fill='white', 
        font='Times 14', 
        text=f"Level: {level}"
    )


def make_tetromino_fall(canvas, tetromino, level):
    while not touching_game_floor(canvas, tetromino) and not objects_below(canvas, tetromino):
        for i in range(4):  # Tetrominos are made of 4 squares, must move all 4 squares in tandem
            canvas.move(tetromino[i], 0, Y_SPEED)
        canvas.update()
        time.sleep(1 / (level / 2 + 3))  # Calculation for fall speed based on level


def touching_game_floor(canvas, tetromino):
    return get_bottom_y(canvas, tetromino) >= CANVAS_HEIGHT


def objects_below(canvas, tetromino):
    coords = get_tetromino_coords(canvas, tetromino)  # Returns list of 4 lists
    for coord in coords:
        x1, y1, x2, y2 = coord[0], coord[1], coord[2], coord[3]
        coord_bottom_y = canvas.find_overlapping(x1, y2, x2, y2)
        coord_right_x = canvas.find_overlapping(x2, y1, x2, y2)
        coord_left_x = canvas.find_overlapping(x1, y1, x1, y2)

        for neighbor in coord_bottom_y:
            if canvas.gettags(neighbor) == ('tetromino',) and not is_self(canvas, tetromino, neighbor):
                if neighbor in coord_right_x and neighbor in coord_left_x:
                    return True
    return False


def is_self(canvas, tetromino, object_num):
    """
    This function detects if an object number is itself.
    Note: each tetromino is made of 4 squares, each with its own object number
    """
    if object_num < tetromino[0] or object_num > tetromino[3]:
        return False
    return True


def objects_left(canvas, tetromino):
    coords = get_tetromino_coords(canvas, tetromino)
    for coord in coords:
        x1, y1, x2, y2 = coord[0], coord[1], coord[2], coord[3]
        coord_bottom_y = canvas.find_overlapping(x1, y2, x2, y2)
        coord_right_x = canvas.find_overlapping(x2, y1, x2, y2)
        coord_left_x = canvas.find_overlapping(x1, y1, x1, y2)
        coord_top_y = canvas.find_overlapping(x1, y1, x2, y1)

        for neighbor in coord_left_x:
            if canvas.gettags(neighbor) == ('tetromino',) and not is_self(canvas, tetromino, neighbor):
                if neighbor in coord_top_y and neighbor in coord_bottom_y:
                    return True
    return False


def objects_right(canvas, tetromino):
    coords = get_tetromino_coords(canvas, tetromino)
    for coord in coords:
        x1, y1, x2, y2 = coord[0], coord[1], coord[2], coord[3]
        coord_bottom_y = canvas.find_overlapping(x1, y2, x2, y2)
        coord_right_x = canvas.find_overlapping(x2, y1, x2, y2)
        coord_left_x = canvas.find_overlapping(x1, y1, x1, y2)
        coord_top_y = canvas.find_overlapping(x1, y1, x2, y1)

        for neighbor in coord_right_x:
            if canvas.gettags(neighbor) == ('tetromino',) and not is_self(canvas, tetromino, neighbor):
                if neighbor in coord_top_y and neighbor in coord_bottom_y:
                    return True
    return False



def valid_move(canvas, tetromino):
    if get_left_x(canvas, tetromino) <= 0:
        return False
    if get_right_x(canvas, tetromino) >= CANVAS_WIDTH:
        return False
    return True

    
# Get position functions
def get_all_x_y_coords(canvas, tetromino):
    tetromino_coords = get_tetromino_coords(canvas, tetromino)
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for tetra_coord in tetromino_coords:
        x1.append(tetra_coord[0])
        y1.append(tetra_coord[1])
        x2.append(tetra_coord[2])
        y2.append(tetra_coord[3])
    return tuple([x1, y1, x2, y2])


def get_left_x(canvas, tetromino):
    coords = get_all_x_y_coords(canvas, tetromino)
    return min(coords[0])


def get_top_y(canvas, tetromino):
    coords = get_all_x_y_coords(canvas, tetromino)
    return min(coords[1])


def get_right_x(canvas, tetromino):
    coords = get_all_x_y_coords(canvas, tetromino)
    return max(coords[2])


def get_bottom_y(canvas, tetromino):
    coords = (get_all_x_y_coords(canvas, tetromino))
    return max(coords[3])


def make_randomized_tetromino(canvas):
    num = random.randint(1, 7)
    if num == 1:
        return make_z_tetromino(canvas)
    elif num == 2:
        return make_s_tetromino(canvas)
    elif num == 3:
        return make_t_tetromino(canvas)
    elif num == 4:
        return make_l_tetromino(canvas)
    elif num == 5:
        return make_j_tetromino(canvas)
    elif num == 6:
        return make_long_rect(canvas)
    elif num == 7:
        return make_square_tetromino(canvas)


# Create tetromino methods
def make_z_tetromino(canvas):
    block1 = make_unit_block(canvas, BLOCK_7_POINTS, 'red')
    block2 = make_unit_block(canvas, BLOCK_6_POINTS, 'red')
    block3 = make_unit_block(canvas, BLOCK_2_POINTS, 'red')
    block4 = make_unit_block(canvas, BLOCK_1_POINTS, 'red')

    return [block1, block2, block3, block4]


def make_s_tetromino(canvas):
    block1 = make_unit_block(canvas, BLOCK_5_POINTS, 'green')
    block2 = make_unit_block(canvas, BLOCK_6_POINTS, 'green')
    block3 = make_unit_block(canvas, BLOCK_2_POINTS, 'green')
    block4 = make_unit_block(canvas, BLOCK_3_POINTS, 'green')

    return [block1, block2, block3, block4]


def make_t_tetromino(canvas):
    block1 = make_unit_block(canvas, BLOCK_2_POINTS, 'purple')
    block2 = make_unit_block(canvas, BLOCK_5_POINTS, 'purple')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'purple')
    block4 = make_unit_block(canvas, BLOCK_7_POINTS, 'purple')

    return [block1, block2, block3, block4]


def make_l_tetromino(canvas):
    block1 = make_unit_block(canvas, BLOCK_3_POINTS, 'orange')
    block2 = make_unit_block(canvas, BLOCK_7_POINTS, 'orange')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'orange')
    block4 = make_unit_block(canvas, BLOCK_5_POINTS, 'orange')

    return [block1, block2, block3, block4]


def make_j_tetromino(canvas):
    block1 = make_unit_block(canvas, BLOCK_1_POINTS, 'blue')
    block2 = make_unit_block(canvas, BLOCK_5_POINTS, 'blue')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'blue')
    block4 = make_unit_block(canvas, BLOCK_7_POINTS, 'blue')

    return [block1, block2, block3, block4]


def make_long_rect(canvas):
    block1 = make_unit_block(canvas, BLOCK_1_POINTS, 'cyan')
    block2 = make_unit_block(canvas, BLOCK_2_POINTS, 'cyan')
    block3 = make_unit_block(canvas, BLOCK_3_POINTS, 'cyan')
    block4 = make_unit_block(canvas, BLOCK_4_POINTS, 'cyan')

    return [block1, block2, block3, block4]


def make_square_tetromino(canvas):
    block1 = make_unit_block(canvas, BLOCK_2_POINTS, 'yellow')
    block2 = make_unit_block(canvas, BLOCK_3_POINTS, 'yellow')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'yellow')
    block4 = make_unit_block(canvas, BLOCK_7_POINTS, 'yellow')

    return [block1, block2, block3, block4]


def make_unit_block(canvas, block, color):
    return canvas.create_rectangle(block[0], block[1], block[2], block[3], outline='grey30', fill=color, tags='tetromino')


def make_canvas(width, height, title):
    """
    Create a canvas with specified dimension
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1, bg='black')
    canvas.pack()
    return canvas


def draw_grid(canvas):
    for i in range(0, CANVAS_HEIGHT + 1, UNIT_SIZE):
        canvas.create_line(0, i, CANVAS_WIDTH, i, fill='grey10')
    for i in range(UNIT_SIZE, CANVAS_WIDTH, UNIT_SIZE):
        canvas.create_line(i, 0, i, CANVAS_HEIGHT, fill='grey10')


def all_boxes(canvas):
    all_boxes = []
    all_objects = canvas.find_all()
    for thing in objects:
        if canvas.gettags(thing) == ('tetromino',):
            all_boxes.append(thing)
    return all_boxes


def remove_completed_row(canvas):
    rows_removed = 0
    for y in range(-1, CANVAS_HEIGHT - UNIT_SIZE, UNIT_SIZE):
        overlap = canvas.find_enclosed(-1, y, CANVAS_WIDTH + 1, y + 52)
        if len(overlap) > 11:
            for item in overlap:
                if canvas.gettags(item) == ('tetromino',):
                    canvas.delete(item)
                    rows_removed += 1
            blocks_above_line = canvas.find_enclosed(-1, -1, CANVAS_WIDTH + 1, overlap[0] * UNIT_SIZE)
            time.sleep(1/5)
            for block in blocks_above_line:
                if canvas.gettags(block) == ('tetromino',):
                    canvas.move(block, 0, UNIT_SIZE)
    return rows_removed // 10
    

def rotate(canvas, tetromino):
    """
    Pivot = Obtain the coordinates for the block that will not be moving
    All the other blocks will move around this block
    In this game, this block will always be the third block in 'tetromino'
    """
    pivot = (get_tetromino_coords(canvas, tetromino)[2])
    px1 = pivot[0]
    py1 = pivot[1]
    px2 = pivot[2]
    py2 = pivot[3]
    lst = tetromino.copy()
    lst.pop(2)

    # Something to add to not rotate a square
    overlap = canvas.find_overlapping(px2, py1, px2, py1)
    count = 0
    for item in overlap:
        if canvas.gettags(item) == ('tetromino',):
            count += 1
    if count == 4:
        return

    for block in lst:
        coord = canvas.coords(block)
        bx1 = coord[0]
        by1 = coord[1]
        bx2 = coord[2]
        by2 = coord[3]
        
        x_diff = bx1 - px1
        y_diff = by1 - py1

        x_move = -x_diff + y_diff
        y_move = -x_diff - y_diff

        canvas.move(block, x_move, y_move)


def key_pressed(event, canvas, tetromino):
    """
    Respond to different arrow keys
    This was written with the help of Code In Place Section Leader
    """
    sym = event.keysym.lower()
    if sym == "left" and get_left_x(canvas, tetromino) >= 0 + UNIT_SIZE and not objects_left(canvas, tetromino):
        for i in range(4):
            canvas.move(tetromino[i], -UNIT_SIZE, 0)
    elif sym == "right" and get_right_x(canvas, tetromino) <= CANVAS_WIDTH - UNIT_SIZE and not objects_right(canvas, tetromino):
        for i in range(4):
            canvas.move(tetromino[i], UNIT_SIZE, 0)
    elif sym == "up":
        rotate(canvas, tetromino)
    elif sym == "down" and get_bottom_y(canvas, tetromino) <= CANVAS_HEIGHT - UNIT_SIZE and not objects_below(canvas, tetromino):
        for i in range(4):
            canvas.move(tetromino[i], 0, UNIT_SIZE)
    elif sym == "space":
        while not touching_game_floor(canvas, tetromino) and not objects_below(canvas, tetromino):
            for i in range(4):
                canvas.move(tetromino[i], 0, Y_SPEED)
            canvas.update()
            time.sleep(1/3000)


def get_tetromino_coords(canvas, tetromino):
    """ Gets the coordinates of all the squares as a list of lists """
    tetromino_coords = []
    for tetra in tetromino:
        tetromino_coords.append(canvas.coords(tetra))
    return tetromino_coords


def game_over(canvas):
    return len(canvas.find_enclosed(-1, -1, CANVAS_WIDTH + 1, UNIT_SIZE + 1)) > 4


def get_score(rows_removed, level):
    update_score = 0
    if rows_removed == 1:
        update_score += 40 * (level + 1)
    elif rows_removed == 2:
        update_score += 100 * (level + 1)
    elif rows_removed == 3:
        update_score += 300 * (level + 1)
    elif rows_removed == 4:
        update_score += 1200 * (level + 1)
    return update_score


def play_tetromino(canvas, level):
    """ Plays one tetromino until it is placed """
    tetromino = make_randomized_tetromino(canvas)
    canvas.bind("<Key>", lambda event: key_pressed(event, canvas, tetromino))
    canvas.focus_set()  # Canvas now has the keyboard focus
    make_tetromino_fall(canvas, tetromino, level)
    return tetromino


def display_game_over(canvas, level, total_score):
    # Create gray 'transparent' overlay
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill="grey50", stipple="gray50")

    # Create text - GAME OVER, final level and final score
    canvas.create_text(CANVAS_MID, CANVAS_HEIGHT // 3, font='Times 40 bold', text='GAME OVER!', fill='white')
    canvas.create_text(CANVAS_MID, CANVAS_HEIGHT // 2, font='Times 25 bold', text=f"You reached level {level}!", fill='white')
    canvas.create_text(CANVAS_MID, CANVAS_HEIGHT - CANVAS_HEIGHT // 3, font='Times 25 bold', text=f"Your score: {total_score}", fill = 'white')


def main():
    canvas = create_game_board()

    total_score = total_rows_removed = level = 0

    score_label = create_score_label(canvas, total_score)
    level_label = create_level_label(canvas, level)

    while not game_over(canvas):
        play_tetromino(canvas, level)
        rows_removed = remove_completed_row(canvas)
        total_rows_removed += rows_removed
        level = (total_rows_removed // 10)  # For every 10 rows removed, level increases by 1
        total_score += get_score(rows_removed, level)

        if get_score(rows_removed, level) > 0:  # Update the score if rows were removed
            canvas.delete(score_label)
            score_label = create_score_label(canvas, total_score)

        canvas.delete(level_label)  # Currently updates every play, change to increase level
        level_label = create_level_label(canvas, level)

    display_game_over(canvas, level, total_score)
    canvas.mainloop()


if __name__ == '__main__':
    main()
