from display import *
from matrix import *
import os
home_dir = os.path.expanduser('~')
Documents_dir = os.path.join(home_dir, 'Documents\\Graphics\\3d-graphics')

  # ====================
  # add the points for a rectagular prism whose
  # upper-left corner is (x, y, z) with width,
  # height and depth dimensions.
  # ====================
def add_box( points, x, y, z, width, height, depth ):
    add_edge(points, x, y, z, x + width, y, z)
    add_edge(points, x, y, z, x, y - height, z)
    add_edge(points, x, y, z, x, y, z - depth)
    add_edge(points, x + width, y, z, x + width, y - height, z)
    add_edge(points, x + width, y, z, x + width, y, z - depth)
    add_edge(points, x + width, y - height, z, x + width, y - height, z - depth)
    add_edge(points, x, y - height, z, x + width, y - height, z)
    add_edge(points, x, y - height, z, x, y - height, z - depth)
    add_edge(points, x, y, z - depth, x + width, y, z - depth)
    add_edge(points, x, y, z - depth, x, y - height, z - depth)
    add_edge(points, x + width, y - height, z, x + width, y - height, z - depth)
    add_edge(points, x + width, y, z - depth, x + width, y - height, z - depth)
    add_edge(points, x, y - height, z - depth, x + width, y - height, z - depth)

  # ====================
  # Generates all the points along the surface
  # of a sphere with center (cx, cy, cz) and
  # radius r.
  # Returns a matrix of those points
  # ====================
def generate_sphere( points, cx, cy, cz, r, step ):
    matrix = new_matrix(0, 0)
    rot = 0
    circ = 0
    pi2 = 2 * math.pi
    while (rot < 1):
        # print("rot: "+ str(rot))
        while (circ < 1):
            # print("circ: "+ str(circ))
            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(pi2 * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(pi2 * rot) + cz
            add_point(matrix, x, y, z)
            circ += step
        rot += step
        circ = 0
    return matrix

  # ====================
  # adds all the points for a sphere with center
  # (cx, cy, cz) and radius r to points
  # should call generate_sphere to create the
  # necessary points
  # ====================
def add_sphere( points, cx, cy, cz, r, step ):
    matrix = generate_sphere(points, cx, cy, cz, r, step)
    for point in matrix:
        add_edge(points, point[0], point[1], point[2], point[0], point[1], point[2])


  # ====================
  # Generates all the points along the surface
  # of a torus with center (cx, cy, cz) and
  # radii r0 and r1.
  # Returns a matrix of those points
  # ====================
def generate_torus( points, cx, cy, cz, r0, r1, step ):
    matrix = new_matrix(0, 0)
    rot = 0
    circ = 0
    pi2 = 2 * math.pi
    while (rot < 1):
        # print("rot: "+ str(rot))
        while (circ < 2):
            # print("circ: "+ str(circ))
            x = math.cos(pi2 * rot) * (r0 * math.cos(math.pi * circ) + r1) + cx
            y = r0 * math.sin(math.pi * circ) + cy
            z =-math.sin(pi2 * rot) * (r0 * math.cos(math.pi * circ) + r1) + cz
            add_point(matrix, x, y, z)
            circ += step
        rot += step
        circ = 0
    return matrix

  # ====================
  # adds all the points for a torus with center
  # (cx, cy, cz) and radii r0, r1 to points
  # should call generate_torus to create the
  # necessary points
  # ====================
def add_torus( points, cx, cy, cz, r0, r1, step ):
    matrix = generate_torus(points, cx, cy, cz, r0, r1, step)
    for point in matrix:
        add_edge(points, point[0], point[1], point[2], point[0], point[1], point[2])



def add_circle( points, cx, cy, cz, r, step ):
    full_rot = 2 * math.pi
    t = 0
    x0 = r * math.cos(0) + cx
    y0 = r * math.sin(0) + cy
    while (t < 1):
        t += step
        theta = full_rot * t
        x1 = r * math.cos(theta) + cx
        y1 = r * math.sin(theta) + cy
        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    x_coefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)
    y_coefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)
    # print_matrix(x_coefs)
    # print_matrix(y_coefs)
    first_x = x0
    first_y = y0
    t = 0
    while (t < 1):
        t += step
        t2 = t * t
        t3 = t2 * t
        second_x = x_coefs[0][0] * t3 + x_coefs[0][1] * t2 + x_coefs[0][2] * t + x_coefs[0][3]
        second_y = y_coefs[0][0] * t3 + y_coefs[0][1] * t2 + y_coefs[0][2] * t + y_coefs[0][3]
        add_edge(points, first_x, first_y, 0, second_x ,second_y, 0)
        first_x = second_x
        first_y = second_y


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )

def picarray(file_name):
    f = open(file_name, "r")
    lines = f.readlines()
    # print(lines)
    array = [[[]]] #3d array of pixels 500 x 500 x 3
    row = 0 #represents # row in 2d array of pixels 500 x 3
    color = 0
    for line in lines:
        if (row == 1):
            txt = line.split(" ")
            length = int(txt[0])
            width = int(txt[1])
            # print(length)
            # print(width)
        pixel = 0 #represents # pixel in 1d array of colors 1 x 3
        if (row >= 2): #not P3 and size declaration
            # print(array)
            # print(array[row - 2])
            # print(array[row - 2][pixel])
            # print("row: "+ str(row) + " pixel: "+ str(pixel))
            txt = line.split(" ")
            # print("text: ")
            # print(txt)
            for num in txt: #colors come in 3's
                # print("''"+ str(num) + "''")
                # print(num != "\n")
                if (num != "\n"):
                    # print(array)
                    array[row- 2][pixel].append(int(num))
                    color += 1
                    if color == 3: #pixel completed
                        pixel += 1
                        color = 0
                        if (pixel <= width):
                            array[row - 2].append([])
                            # print(array)
                        # else:
                        #     print("else")
                        #     print(array)
                        #     array[row - 2].pop()
                        #     print(array)
                        # print("row: "+ str(row) + " pixel: "+ str(pixel))
            array[row - 2].pop()
            if (row <= length):
                array.append([[]]) #add another row
            # else:
            #     array.pop()
        row += 1
    return array

def concat_pic(pic):
    string = ""
    # print(len(pic))
    # print(len(pic[0]))
    for row in pic:
        for pixel in row:
            string += str(pixel[0]) + " "
            string += str(pixel[1]) + " "
            string += str(pixel[2]) + " "
        string += "\n"
    # print(string)
    return string

def fill(x, y, new_color, file_name, screen):
    # print(color)
    pic = picarray(file_name)
    # print(pic[0][0])
    # print(screen[0][0])
    # print(pic)
    # print(screen)
    checked = [[]]
    old_color = pic[x][y]
    # old_color = screen[y][x]
    print(new_color)
    print(old_color)
    f = open(file_name, 'r')
    f.readline()
    line = f.readline()
    f.close()
    line = line.split(" ")
    length = int(line[0])
    width = int(line[1])
    # print(length)
    # print(width)
    stack = [(x, y)]
    # checked = []
    while (len(stack) > 0):
        # print(stack)
        # set(stack)
        x, y = stack.pop()
        # checked.append((x, y))
        # print("x: "+ str(x) + " y: " + str(y))
        if (y >= 0 and y < length and x >= 0 and x < length):
            # print(pic[x][y])
            if (pic[x][y] == old_color):
            # if (screen[y][x] == old_color):
                # continue
                pic[x][y] = new_color
                # plot(screen, new_color, x, y)
                # print("Changed color at (" + str(x) + ", " + str(y) + ")" )
                if (x + 1 < width):
                # if (x + 1 < length and not in_list((x + 1, y), checked)):
                    stack.append( (x + 1, y) )  # right
                    # checked.append( (x + 1, y))
                    # set(checked)
                if (x - 1 >= 0):
                # if (x - 1 >= 0 and not in_list((x - 1, y), checked)):
                    stack.append( (x - 1, y) )  # left
                    # checked.append( (x - 1, y))
                    # set(checked)
                if (y + 1 < length):
                # if (y + 1 < length and not in_list((x, y + 1), checked)):
                    stack.append( (x, y + 1) )  # down
                    # checked.append( (x, y + 1))
                    # set(checked)
                if (y - 1 >= 0):
                # if (y - 1 >= 0 and not in_list((x, y - 1), checked)):
                    stack.append( (x, y - 1) )  # up
                    # checked.append( (x, y - 1))
                    # set(checked)
    # fillhelper(y, x, pic[x][y], color, pic, checked)
    text = concat_pic(pic)
    print(text)
    output = "P3 \n" + str(length) + " " + str(width) + " 255 \n" + text
    # print(output)
    # print(file_name)
    with open(os.path.join(Documents_dir, file_name),'w') as savefile:
        savefile.write(output)
    # fd = open(file_name, 'w')
    # fd.write(output)
    # fd.close()
    # print(screen)
#
# def fillhelper(col, row, old_color, new_color, pic, checked):
#     print("col: "+ str(col)+ "row: "+str(row))
#
#     if (col >= 0 and col <= 499 and row >= 0 and row <= 499 and not find_in_list([col, row], checked)):
#         if (pic[col][row] == old_color):
#             pic[col][row] = new_color
#             checked.append([col, row])
#             fillhelper(col + 1, row, old_color, new_color, pic, checked)
#             fillhelper(col - 1, row, old_color, new_color, pic, checked)
#             fillhelper(col, row + 1, old_color, new_color, pic, checked)
#             fillhelper(col, row - 1, old_color, new_color, pic, checked)
#     return pic

def in_list(element, list):
    for el in list:
        if element == el:
            return True
    return False
def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
