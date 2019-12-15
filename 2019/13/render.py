import array

WALL_PIX = """
11111111
11111111
11111111
11111111
11111111
11111111
11111111
11111111
11111111
"""

BALL_PIX = """
00000000
00111000
01111100
11111110
11111110
01111100
00111000
00000000
00000000
"""

BLOCK_PIX = """
00000000
00000000
01111111
01111111
01111111
01111111
00000000
00000000
00000000
"""

PADDLE_PIX = """
00000000
00000000
11111111
11111111
11111111
00000000
00000000
00000000
00000000
"""

CHAR_WIDTH = 8
CHAR_HEIGHT = 9
OFFSET_X = 4 * CHAR_WIDTH
OFFSET_Y = 2 * CHAR_HEIGHT
WIDTH = 60
HEIGHT = 30

BALL_COLOR = (222, 140, 255)
BLOCK_COLOR = (103, 172, 255)
WALL_COLOR = (150, 150, 150)
PADDLE_COLOR = (110, 255, 210)
SCORE_COLOR = (0, 255, 0)

ZERO_PIX = """
........
..1111..
.11..11.
.11.111.
.111.11.
.11..11.
..1111..
........
"""

ONE_PIX = """
........
.....11.
...1111.
..11.11.
.....11.
.....11.
.....11.
........
"""

TWO_PIX = """
........
..1111..
.11..11.
.....11.
...111..
..11....
.111111.
........
"""

THREE_PIX = """
........
..1111..
.11..11.
...111..
.....11.
.11..11.
..1111..
........
"""

FOUR_PIX = """
........
.....11.
...1111.
..11.11.
.111111.
.....11.
.....11.
........
"""

FIVE_PIX = """
........
.111111.
.11.....
.11111..
.....11.
.....11.
.11111..
........
"""

SIX_PIX = """
........
...111..
..11....
.11111..
.11..11.
.11..11.
..1111..
........
"""

SEVEN_PIX = """
........
.111111.
.....11.
....11..
...11...
..11....
.11.....
........
"""

EIGHT_PIX = """
........
..1111..
.11..11.
...11...
.11..11.
.11..11.
..1111..
........
"""

NINE_PIX = """
........
..1111..
.11..11.
.11..11.
.111111.
.....11.
..1111..
........
"""

DIGITS = [ZERO_PIX, ONE_PIX, TWO_PIX, THREE_PIX, FOUR_PIX,
          FIVE_PIX, SIX_PIX, SEVEN_PIX, EIGHT_PIX, NINE_PIX]

DIGIT_HEIGHT = 8
DIGIT_WIDTH = 8


def get_sprite(char):
    if char == 'x':  # wall
        return WALL_PIX, WALL_COLOR
    elif char == '#':  # block
        return BLOCK_PIX, BLOCK_COLOR
    elif char == 'o':  # ball
        return BALL_PIX, BALL_COLOR
    elif char == "_":  # paddle
        return PADDLE_PIX, PADDLE_COLOR
    else:
        return ''.join(['0' * 8 + '\n' for _ in range(8)]), (0, 0, 0)


def write_sprite(image, image_width, x, y, sprite, width, height, color):
    sprite = sprite.strip().split('\n')
    index = 3 * ((y * height + OFFSET_Y) * image_width + x * width + OFFSET_X)
    for sprite_row in sprite:
        row_index = index
        for bits in list(sprite_row):
            if bits == '1':
                image[index] = color[0]
                image[index + 1] = color[1]
                image[index + 2] = color[2]
            index += 3
        index = row_index + 3 * image_width


def create_image(screen, frame, score):
    # PPM header
    width = CHAR_WIDTH * WIDTH
    height = CHAR_HEIGHT * HEIGHT
    maxval = 255
    ppm_header = f'P6 {width} {height} {maxval}\n'

    # PPM image data (filled with black)
    image = array.array('B', [0, 0, 0] * width * height)

    lines = screen.rstrip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            sprite, color = get_sprite(char)
            write_sprite(image, width, x, y, sprite, CHAR_WIDTH, CHAR_HEIGHT, color)

    for i, digit in enumerate(str(score)):
        sprite = DIGITS[int(digit)]
        write_sprite(image, width, 42 + i, 2, sprite, DIGIT_WIDTH, DIGIT_HEIGHT, SCORE_COLOR)

    imgname = "/tmp/frame{:04d}".format(frame)

    # Save the PPM image as a binary file
    with open(imgname + '.ppm', 'wb') as f:
        f.write(bytearray(ppm_header, 'ascii'))
        image.tofile(f)
    # run in /tmp
    # ffmpeg -r 24 -y -f image2 -s 480x270 -i frame%04d.ppm -vcodec libx264 -crf 25  -pix_fmt yuv420p aoc2019_13.mp4


def minmax_tuples(tuple_list, element=0):
    res = sorted(tuple_list, key=lambda k: k[element])
    return res[0][element], res[-1][element]


def render_grid(grid):
    coords = list(grid.keys())
    min_x, max_x = minmax_tuples(coords, 0)
    min_y, max_y = minmax_tuples(coords, 1)
    screen = ""
    for line in range(min_y, max_y + 1):
        for col in range(min_x, max_x + 1):
            pos = col, line
            screen += grid[pos].get_pixel()
        screen += '\n'
    return screen


def print_grid(grid):
    print(render_grid(grid))


def save_grid(grid, frame, score):
    create_image(render_grid(grid), frame, score)
