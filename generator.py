from random import randint
from random import uniform

matrix = []
n = 50
m = 50

min_n_room = 10
min_m_room = 10

dist_between_room = 1
rand = 0.3
constraint_ratio_of_sides_area = 1.4

count_room = 0
room_number = {}
room_doors = {}
cell_room_number = {}
room_cells = {}


# class graph:


def build_room_in_area(x1, y1, x2, y2):
    global count_room
    global room_number
    global room_cells
    global cell_room_number
    global matrix
    global min_n_room
    global min_m_room

    n_room = randint(min_n_room, x2 - x1 - 1)
    m_room = randint(min_m_room, y2 - y1 - 1)

    rem_x = (x2 - x1 + 1) - 2 - n_room
    rem_y = (y2 - y1 + 1) - 2 - m_room

    x1_room = x1 + randint(0, rem_x)
    x2_room = x1_room + n_room + 1

    y1_room = y1 + randint(0, rem_y)
    y2_room = y1_room + m_room + 1


    for i in range(x1_room, x2_room + 1):
        matrix[i][y1_room] = '#'
        matrix[i][y2_room] = '#'

    for i in range(y1_room, y2_room + 1):
        matrix[x1_room][i] = '#'
        matrix[x2_room][i] = '#'

    room_cells[count_room] = []
    room_number[x1_room, y1_room, x2_room, y2_room] = count_room

    for i in range(x1_room + 1, x2_room):
        for j in range(y1_room + 1, y2_room):
            matrix[i][j] = '*'
            room_cells[count_room].append((i, j))
            cell_room_number[(i, j)] = count_room

    count_room += 1

    return x1_room, y1_room, x2_room, y2_room


def most_up(a, b):
    return a if a[0] < b[0] else b

def most_down(a, b):
    return a if a[2] > b[2] else b

def most_left(a, b):
    return a if a[1] < b[1] else b

def most_right(a, b):
    return a if a[3] > b[3] else b


def build_vertical_tunnels_between_room(up_room, down_room):
    up_y = randint(up_room[1] + 1, up_room[3] - 1)
    down_y = randint(down_room[1] + 1, down_room[3] - 1)

    global matrix

    global cell_room_number
    global room_doors

    room_doors[room_number[up_room]] = room_doors.get(room_number[up_room], []) + [(up_room[2], up_y)]
    room_doors[room_number[down_room]] = room_doors.get(room_number[down_room], []) + [(down_room[0], down_y)]

    y = up_y

    for x in range(up_room[2], down_room[0] + 1):
        matrix[x][y] = '*'
        matrix[x][y + 1] = '#'
        matrix[x][y - 1] = '#'

        if x == up_room[2] + 1:

            pos = 1

            if down_y < y:
                pos *= -1
            
            matrix[x + 1][y - pos] = '#'
            matrix[x + 1][y] = '#'

            while y != down_y:
                y += pos
                matrix[x][y] = '*'
                matrix[x - 1][y] = '#'
                matrix[x + 1][y] = '#'
            
            matrix[x - 1][y + pos] = '#'
            matrix[x][y + pos] = '#'


def build_horizontal_tunnels_between_room(left_room, right_room):
    left_x = randint(left_room[0] + 1, left_room[2] - 1)
    right_x = randint(right_room[0] + 1, right_room[2] - 1)

    global cell_room_number
    global room_doors

    room_doors[room_number[left_room]] = room_doors.get(room_number[left_room], []) + [(left_x, left_room[3])]
    room_doors[room_number[right_room]] = room_doors.get(room_number[right_room], []) + [(right_x, right_room[1])]

    x = left_x

    for y in range(left_room[3], right_room[1] + 1):
        matrix[x][y] = '*'
        matrix[x + 1][y] = '#'
        matrix[x - 1][y] = '#'

        if y == left_room[3] + 1:

            pos = 1

            if right_x < x:
                pos *= -1
            
            matrix[x - pos][y + 1] = '#'
            matrix[x][y + 1] = '#'

            while x != right_x:
                x += pos
                matrix[x][y] = '*'
                matrix[x][y + 1] = '#'
                matrix[x][y - 1] = '#'
            
            matrix[x + pos][y] = '#'
            matrix[x + pos][y - 1] = '#'


def gen(x1, y1, x2, y2):
        # print(x1, y1, x2, y2)

        global min_n_room
        global min_m_room


        global rand_n
        global rand_m
        
        if (x2 - x1 + 1 - dist_between_room - 4) // 2 < min_n_room and (y2 - y1 + 1 - dist_between_room - 4) // 2 < min_m_room:
            room = build_room_in_area(x1, y1, x2, y2)
            return room, room, room, room
                
        type_cut = randint(0, 1)

        if (x2 - x1 + 1 - dist_between_room - 4) // 2 < min_n_room or (y2 - y1 + 1 - dist_between_room - 4) // 2 < min_m_room:
            type_cut = 1 if (x2 - x1 + 1 - dist_between_room - 4) // 2 < min_n_room else 0

        if type_cut == 0:
            # print('??')
            previos_cut = (x1 + x2) // 2 + int((x2 - x1 + 1) * uniform(-rand, rand))
            cut = max(x1 + min_n_room + 2, previos_cut)
            cut = min(cut, x2 - min_n_room - 2)

            up = gen(x1, y1, cut - 1, y2)
            down = gen(cut + 1, y1, x2, y2)

            build_vertical_tunnels_between_room(up[1], down[0])

            return up[0], down[1], most_left(up[2], down[2]), most_right(up[3], down[3])
        else:
            # print('?')
            previos_cut = (y1 + y2) // 2 + int((y2 - y1 + 1) * uniform(-rand, rand))
            cut = max(y1 + min_m_room + 2, previos_cut)
            cut = min(cut, y2 - min_m_room - 2)

            left = gen(x1, y1, x2, cut - 1)
            right = gen(x1, cut + 1, x2, y2)

            build_horizontal_tunnels_between_room(left[3], right[2])

            return most_up(left[0], right[0]), most_down(left[1], right[2]), left[2], right[3]
            

def get_matrix_of_level():

    global matrix

    global n
    global m
    matrix = [['.' for i in range(n)] for j in range(m)]
        
    gen(0, 0, n - 1, m - 1)

    for x in matrix:
        print(''.join(x))

    return matrix, room_cells, room_doors, room_number, cell_room_number
