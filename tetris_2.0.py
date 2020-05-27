"""
File: tetris_2.0.py
----------------

"""

import tkinter
import random
import time

"test"

# Constants for canvas
CANVAS_WIDTH = 500      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 1000    # Height of drawing canvas in pixels
CANVAS_MID = CANVAS_WIDTH // 2
UNIT_SIZE = 50          # Size of unit block within shape
Y_SPEED = 50
X_SPEED = 50


# Vertices for individual squares
BLOCK_1_POINTS = [CANVAS_MID - UNIT_SIZE * 2, 0, CANVAS_MID - UNIT_SIZE, UNIT_SIZE]
BLOCK_2_POINTS = [CANVAS_MID - UNIT_SIZE, 0, CANVAS_MID, UNIT_SIZE]
BLOCK_3_POINTS = [CANVAS_MID, 0, CANVAS_MID + UNIT_SIZE, UNIT_SIZE]
BLOCK_4_POINTS = [CANVAS_MID + UNIT_SIZE, 0, CANVAS_MID + UNIT_SIZE * 2, UNIT_SIZE]
BLOCK_5_POINTS = [CANVAS_MID - UNIT_SIZE * 2, UNIT_SIZE, CANVAS_MID - UNIT_SIZE, UNIT_SIZE * 2]
BLOCK_6_POINTS = [CANVAS_MID - UNIT_SIZE, UNIT_SIZE, CANVAS_MID, UNIT_SIZE * 2]
BLOCK_7_POINTS = [CANVAS_MID, UNIT_SIZE, CANVAS_MID + UNIT_SIZE, UNIT_SIZE * 2]
BLOCK_8_POINTS = [CANVAS_MID + UNIT_SIZE, UNIT_SIZE, CANVAS_MID + UNIT_SIZE * 2, UNIT_SIZE * 2]


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Simplified Tetris')
    draw_grid(canvas)
 
    while True:
        play_shape(canvas)
        
    canvas.mainloop()
    

def own_shape(canvas, shape, object_num):
    if object_num < shape[0] or object_num > shape[3]:
        return False
    return True


def hit_objects(canvas, shape):
    coords = get_shape_coords(canvas, shape)
    neighbors = []
    for coord in coords:
        x1, y1, x2, y2 = coord[0], coord[1], coord[2], coord[3]
        neighbors.append(canvas.find_overlapping(x1, y1, x2, y2))

    for neighbor in neighbors:
        for item in neighbor:
            if item > 28 and not own_shape(canvas, shape, item):
                return True
    return False


def objects_left(canvas, shape):
    coords = get_shape_coords(canvas, shape)
    for coord in coords:
        x1, y1, x2, y2 = coord[0], coord[1], coord[2], coord[3]
        coord_bottom_y = canvas.find_overlapping(x1, y2, x2, y2)
        coord_right_x = canvas.find_overlapping(x2, y1, x2, y2)
        coord_left_x = canvas.find_overlapping(x1, y1, x1, y2)
        coord_top_y = canvas.find_overlapping(x1, y1, x2, y1)

        for neighbor in coord_left_x:
            if neighbor > 28 and not own_shape(canvas, shape, neighbor):
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
            if neighbor > 28 and not own_shape(canvas, shape, neighbor):
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
            if neighbor > 28 and not own_shape(canvas, shape, neighbor):
                if neighbor in coord_right_x and neighbor in coord_left_x:
                    return True
    return False


    # find the bottom y of each shape
    # using canvas.coords, determine if this y matches the top y of an object
    # and the X is x1 difference
    # so if 

def get_shape_coords_dict(canvas, shape):
    shape_coords = {}
    for tetra in shape:
        shape_coords[tetra] = canvas.coords(tetra)
    print(shape_coords)


def get_shape_coords(canvas, shape):
    shape_coords = []
    for tetra in shape:
        shape_coords.append(canvas.coords(tetra))
    return shape_coords


    
    """
    overlap = set(canvas.find_overlapping(
        (coords[0] + coords[2]) / 2 + x, 
        (coords[1] + coords[3]) / 2 + y, 
        (coords[0] + coords[2]) / 2 + x,
        (coords[1] + coords[3]) / 2 + y
            ))
    """
    # x1, y1, x2, y2 = canvas.coords(shape[0])
    # x3, y3, x4, y4 = canvas.coords(shape[1])
    # x5, y5, x6, y6 = canvas.coords(shape[2])
    # x7, y7, x8, y8 = canvas.coords(shape[3])

    # colliding_list = canvas.find_overlapping(y2, y4, y6, y8)
    # #(canvas.find_overlapping(x3, y3, x4, y4)), (canvas.find_overlapping(x5, y5, x6, y6)), (canvas.find_overlapping(x7, y7, x8, y8))
    # print(colliding_list)

    # count = 0
    # for el in colliding_list:
    #     if el not in shape and el >= 29:
    #         count += 1
    # if count >= 2:
    #     return True
    # else:
    #     return False


# def rotate(canvas, shape):
#     canvas.move(shape[0], UNIT_SIZE * 2, -UNIT_SIZE * 2)
#     canvas.move(shape[1], UNIT_SIZE * 1, -UNIT_SIZE * 1)
#     canvas.move(shape[3], UNIT_SIZE * -1, -UNIT_SIZE * -1)


# Plays one shape until shape is placed
def play_shape(canvas):
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
        time.sleep(1/2)


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


# Creates a shape
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


def make_z_shape(canvas): 
    block1 = make_unit_block(canvas, BLOCK_2_POINTS, 'blue')
    block2 = make_unit_block(canvas, BLOCK_3_POINTS, 'blue')
    block3 = make_unit_block(canvas, BLOCK_7_POINTS, 'blue')
    block4 = make_unit_block(canvas, BLOCK_8_POINTS, 'blue')

    return [block1, block2, block3, block4]


def make_s_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_2_POINTS, 'blue')
    block2 = make_unit_block(canvas, BLOCK_3_POINTS, 'blue')
    block3 = make_unit_block(canvas, BLOCK_5_POINTS, 'blue')
    block4 = make_unit_block(canvas, BLOCK_6_POINTS, 'blue')

    return [block1, block2, block3, block4]


def make_t_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_2_POINTS, 'blue')
    block2 = make_unit_block(canvas, BLOCK_5_POINTS, 'blue')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'blue')
    block4 = make_unit_block(canvas, BLOCK_7_POINTS, 'blue')

    return [block1, block2, block3, block4]


def make_l_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_4_POINTS, 'blue')
    block2 = make_unit_block(canvas, BLOCK_6_POINTS, 'blue')
    block3 = make_unit_block(canvas, BLOCK_7_POINTS, 'blue')
    block4 = make_unit_block(canvas, BLOCK_8_POINTS, 'blue')

    return [block1, block2, block3, block4]


def make_j_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_1_POINTS, 'blue')
    block2 = make_unit_block(canvas, BLOCK_5_POINTS, 'blue')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'blue')
    block4 = make_unit_block(canvas, BLOCK_7_POINTS, 'blue')

    return [block1, block2, block3, block4]


def make_long_rect(canvas):
    block1 = make_unit_block(canvas, BLOCK_1_POINTS, 'blue')
    block2 = make_unit_block(canvas, BLOCK_2_POINTS, 'blue')
    block3 = make_unit_block(canvas, BLOCK_3_POINTS, 'blue')
    block4 = make_unit_block(canvas, BLOCK_4_POINTS, 'blue')

    return [block1, block2, block3, block4]


def make_square_shape(canvas):
    block1 = make_unit_block(canvas, BLOCK_2_POINTS, 'blue')
    block2 = make_unit_block(canvas, BLOCK_3_POINTS, 'blue')
    block3 = make_unit_block(canvas, BLOCK_6_POINTS, 'blue')
    block4 = make_unit_block(canvas, BLOCK_7_POINTS, 'blue')

    return [block1, block2, block3, block4]


def make_unit_block(canvas, block, color):
    return canvas.create_rectangle(block[0], block[1], block[2], block[3], outline='grey95', fill=color, tags='shape')


# DO NOT MODIFY - Creates and returns a drawing canvas
def make_canvas(width, height, title):
    """
    Create a canvas with specified dimension
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


def draw_grid(canvas):
    for i in range(50, 500, 50):
        canvas.create_line(i, 0, i, 1000, fill='grey95')
    for i in range(50, 1000, 50):
        canvas.create_line(0, i, 500, i, fill='grey95')


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
        #rotate(canvas, shape)
        pass
    elif sym == "down" and get_bottom_y(canvas, shape) <= CANVAS_HEIGHT - UNIT_SIZE and not hit_objects(canvas, shape):
        for i in range(4):
            canvas.move(shape[i], 0, UNIT_SIZE)


if __name__ == '__main__':
    main()
