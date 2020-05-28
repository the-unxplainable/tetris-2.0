"""
File: tetris_2.0.py
----------------

My second attempt at tetris using Python and Tkinter.
Functionalities include:
- Tetrominos can rotate
- Completed lines disappear
- Detects end of game
- Hard drop with space bar (technically it is just falling super fast)

TODO: Show score
TODO: Show preview (spawn shape above the canvas, move once previous shape is placed)
TODO: Legal move for rotating pieces
TODO: Could I make the line flash before it disappears?
TODO: Decompose objects_left, objects_right, objects_below
TODO: Add music: playsound('/path/to/a/sound/file/you/want/to/play.mp3', block=False)
TODO: Create multiple levels?
TODO: Create levels with blocks in the way
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
UNIT_SIZE = 50          # Size of unit block within shape
Y_SPEED = 50
X_SPEED = 50
DELAY = 1/4


# Vertices for individual squares
BLOCK_1_POINTS = [CANVAS_MID - UNIT_SIZE * 2, -UNIT_SIZE * 2, CANVAS_MID - UNIT_SIZE, -UNIT_SIZE]
BLOCK_2_POINTS = [CANVAS_MID - UNIT_SIZE, -UNIT_SIZE * 2, CANVAS_MID, -UNIT_SIZE]
BLOCK_3_POINTS = [CANVAS_MID, -UNIT_SIZE * 2, CANVAS_MID + UNIT_SIZE, -UNIT_SIZE]
BLOCK_4_POINTS = [CANVAS_MID + UNIT_SIZE, -UNIT_SIZE * 2, CANVAS_MID + UNIT_SIZE * 2, -UNIT_SIZE]
BLOCK_5_POINTS = [CANVAS_MID - UNIT_SIZE * 2, -UNIT_SIZE, CANVAS_MID - UNIT_SIZE, 0]
BLOCK_6_POINTS = [CANVAS_MID - UNIT_SIZE, -UNIT_SIZE, CANVAS_MID, 0]
BLOCK_7_POINTS = [CANVAS_MID, -UNIT_SIZE, CANVAS_MID + UNIT_SIZE, 0]
BLOCK_8_POINTS = [CANVAS_MID + UNIT_SIZE, -UNIT_SIZE, CANVAS_MID + UNIT_SIZE * 2, 0]


def is_self(canvas, shape, object_num):
    """
    This function detects if an object number is itself.
    Note: each shape is made of 4 squares, each with its own object number
    """
    if object_num < shape[0] or object_num > shape[3]:
        return False
    return True


def objects_left(canvas, shape):
    coords = get_shape_coords(canvas, shape)
    for coord in coords:
        x1, y1, x2, y2 = coord[0], coord[1], coord[2], coord[3]
        coord_bottom_y = canvas.find_overlapping(x1, y2, x2, y2)
        coord_right_x = canvas.find_overlapping(x2, y1, x2, y2)
        coord_left_x = canvas.find_overlapping(x1, y1, x1, y2)
        coord_top_y = canvas.find_overlapping(x1, y1, x2, y1)

        for neighbor in coord_left_x:
            if neighbor > 30 and not is_self(canvas, shape, neighbor):
                if neighbor in coord_top_y and neighbor in coord_bottom_y:
                    return True
    return False


def objects_right(canvas, shape):
    coords = get_shape_coords(canvas, shape)
    for coord in coords:
        x1, y1, x2, y2 = coord[0], coord[1], coord[2], coord[3]
        coord_bottom_y = canvas.find_overlapping(x1, y2, x2, y2)
        coord_right_x = canvas.find_overlapping(x2, y1, x2, y2)
        coord_left_x = canvas.find_overlapping(x1, y1, x1, y2)
        coord_top_y = canvas.find_overlapping(x1, y1, x2, y1)

        for neighbor in coord_right_x:
            if neighbor > 30 and not is_self(canvas, shape, neighbor):
                if neighbor in coord_top_y and neighbor in coord_bottom_y:
                    return True
    return False


def objects_below(canvas, shape):
    coords = get_shape_coords(canvas, shape)
    for coord in coords:
        x1, y1, x2, y2 = coord[0], coord[1], coord[2], coord[3]
        coord_y = canvas.find_overlapping(x1, y2, x2, y2)
        coord_right_x = canvas.find_overlapping(x2, y1, x2, y2)
        coord_left_x = canvas.find_overlapping(x1, y1, x1, y2)

        for neighbor in coord_y:
            if neighbor > 30 and not is_self(canvas, shape, neighbor):
                if neighbor in coord_right_x and neighbor in coord_left_x:
                    return True
    return False


def is_touching_bottom(canvas, shape):
    if get_bottom_y(canvas, shape) >= CANVAS_HEIGHT:
        return True


def valid_move(canvas, shape):
    if get_left_x(canvas, shape) <= 0:
        return False
    if get_right_x(canvas, shape) >= CANVAS_WIDTH:
        return False
    return True

    
# Get position functions
def get_all_x_y_coords(canvas, shape):
    shape_coords = get_shape_coords(canvas, shape)
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for tetra_coord in shape_coords:
        x1.append(tetra_coord[0])
        y1.append(tetra_coord[1])
        x2.append(tetra_coord[2])
        y2.append(tetra_coord[3])
    return tuple([x1, y1, x2, y2])


def get_left_x(canvas, shape):
    coords = get_all_x_y_coords(canvas, shape)
    return min(coords[0])


def get_top_y(canvas, shape):
    coords = get_all_x_y_coords(canvas, shape)
    return min(coords[1])


def get_right_x(canvas, shape):
    coords = get_all_x_y_coords(canvas, shape)
    return max(coords[2])


def get_bottom_y(canvas, shape):
    coords = get_all_x_y_coords(canvas, shape)
    return max(coords[3])


def make_randomized_shape(canvas):
    num = random.randint(1, 7)
    if num == 1:
        return make_z_shape(canvas)
    elif num == 2:
        return make_s_shape(canvas)
    elif num == 3:
        return make_t_shape(canvas)
    elif num == 4:
        return make_l_shape(canvas)
    elif num == 5:
        return make_j_shape(canvas)
    elif num == 6:
        return make_long_rect(canvas)
    elif num == 7:
        return make_square_shape(canvas)


# Create shape methods
def make_z_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_7_POINTS, 'red')
    block2 = make_unit_block(canvas, BLOCK_6_POINTS, 'red')
    block3 = make_unit_block(canvas, BLOCK_2_POINTS, 'red')
    block4 = make_unit_block(canvas, BLOCK_1_POINTS, 'red')

    return [block1, block2, block3, block4]


def make_s_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_5_POINTS, 'green')
    block2 = make_unit_block(canvas, BLOCK_6_POINTS, 'green')
    block3 = make_unit_block(canvas, BLOCK_2_POINTS, 'green')
    block4 = make_unit_block(canvas, BLOCK_3_POINTS, 'green')

    return [block1, block2, block3, block4]


def make_t_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_2_POINTS, 'purple')
    block2 = make_unit_block(canvas, BLOCK_5_POINTS, 'purple')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'purple')
    block4 = make_unit_block(canvas, BLOCK_7_POINTS, 'purple')

    return [block1, block2, block3, block4]


def make_l_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_3_POINTS, 'orange')
    block2 = make_unit_block(canvas, BLOCK_7_POINTS, 'orange')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'orange')
    block4 = make_unit_block(canvas, BLOCK_5_POINTS, 'orange')

    return [block1, block2, block3, block4]


def make_j_shape(canvas):
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


def make_square_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_2_POINTS, 'yellow')
    block2 = make_unit_block(canvas, BLOCK_3_POINTS, 'yellow')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'yellow')
    block4 = make_unit_block(canvas, BLOCK_7_POINTS, 'yellow')

    return [block1, block2, block3, block4]


def make_unit_block(canvas, block, color):
    return canvas.create_rectangle(block[0], block[1], block[2], block[3], outline='grey30', fill=color, tags='shape')


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
        canvas.create_line(i, 0, i, 1000, fill='grey10')


def all_boxes(canvas):
    all_boxes = []
    all_objects = canvas.find_all()
    for thing in objects:
        if thing > 30:
            all_boxes.append(thing)
    return all_boxes


def remove_completed_row(canvas):

    for y in range(-1, CANVAS_HEIGHT - UNIT_SIZE, UNIT_SIZE):
        overlap = canvas.find_enclosed(-1, y, CANVAS_WIDTH + 1, y + 52)
        if len(overlap) > 11:
            for item in overlap:
                if item > 30:
                    canvas.delete(item)
            blocks_above_line = canvas.find_enclosed(-1, -1, CANVAS_WIDTH + 1, overlap[0] * UNIT_SIZE)
            time.sleep(1/5)
            for block in blocks_above_line:
                if block > 30:
                    canvas.move(block, 0, UNIT_SIZE)
    

def rotate(canvas, shape):
    """
    Pivot = Obtain the coordinates for the block that will not be moving
    All the other blocks will move around this block
    In this game, this block will always be the third block in 'shape'
    """
    pivot = (get_shape_coords(canvas, shape)[2])
    px1 = pivot[0]
    py1 = pivot[1]
    px2 = pivot[2]
    py2 = pivot[3]
    lst = shape.copy()
    lst.pop(2)

    # Something to add to not rotate a square
    overlap = canvas.find_overlapping(px2, py1, px2, py1)
    count = 0
    for item in overlap:
        if item > 30:
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


def key_pressed(event, canvas, shape):
    """
    Respond to different arrow keys
    This was written with the help of Code In Place Section Leader
    """
    sym = event.keysym.lower()
    if sym == "left" and get_left_x(canvas, shape) >= 0 + UNIT_SIZE and not objects_left(canvas, shape):
        for i in range(4):
            canvas.move(shape[i], -UNIT_SIZE, 0)
    elif sym == "right" and get_right_x(canvas, shape) <= CANVAS_WIDTH - UNIT_SIZE and not objects_right(canvas, shape):
        for i in range(4):
            canvas.move(shape[i], UNIT_SIZE, 0)
    elif sym == "up":
        rotate(canvas, shape)
    elif sym == "down" and get_bottom_y(canvas, shape) <= CANVAS_HEIGHT - UNIT_SIZE and not objects_below(canvas, shape):
        for i in range(4):
            canvas.move(shape[i], 0, UNIT_SIZE)
    elif sym == "space":
        while not is_touching_bottom(canvas, shape) and not objects_below(canvas, shape):
            for i in range(4):
                canvas.move(shape[i], 0, Y_SPEED)
            canvas.update()
            time.sleep(1/3000)


def get_shape_coords(canvas, shape):
    """ Gets the coordinates of all the squares as a list of lists """
    shape_coords = []
    for tetra in shape:
        shape_coords.append(canvas.coords(tetra))
    return shape_coords


def play_shape(canvas):
    """ Plays one shape until shape is placed """
    shape = make_randomized_shape(canvas)
    canvas.bind("<Key>", lambda event: key_pressed(event, canvas, shape))
    canvas.focus_set()  # Canvas now has the keyboard focus
    make_shape_fall(canvas, shape)
    return shape


def make_shape_fall(canvas, shape):
    while not is_touching_bottom(canvas, shape) and not objects_below(canvas, shape):
        for i in range(4):
            canvas.move(shape[i], 0, Y_SPEED)
        canvas.update()
        time.sleep(DELAY)


def game_over(canvas):
    return len(canvas.find_enclosed(-1, -1, CANVAS_WIDTH + 1, UNIT_SIZE + 1)) > 2


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Tetris 2.0')
    draw_grid(canvas)
    while not game_over(canvas):
        play_shape(canvas)
        remove_completed_row(canvas)

    canvas.create_text(40, 500, anchor='w', font='Times 40 bold', text='GAME OVER!', fill='white')
    canvas.mainloop()


if __name__ == '__main__':
    main()
