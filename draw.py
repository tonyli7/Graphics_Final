from display import *
from matrix import *
from gmath import calculate_dot
from math import cos, sin, pi
import sys, random

MAX_STEPS = 100

#initialization of color gradient
gradient = []
for i in range(0,20):
    gradient.append([255,255,255])
for i in range(20, 200):
    c = [255, i/2, i%20]
    gradient.append(c)
for i in range(200,220):
    gradient.append([0,0,0])
gradient = gradient[::-1]

def fire(screen, length, xcor, ycor):
    #initialization of color array
    c_buf = []
    for i in range(0,100):
        c_buf.append([])
        for j in range(0,length):
            c_buf[i].append([])

    #randomization+setup
    for x in range(0, length):
        randcolor = random.randint(0,1)
        c_buf[99][x] = (len(gradient)-1)*randcolor
        if x <= 99:
            c_buf[x][0] = 0
            c_buf[x][length-1] = 0

    for y in range(98,-1,-1):
        for t in range(1,length-1):
            c_buf[y][t] = abs((c_buf[y+1][t-1]+c_buf[y+1][t]+c_buf[y+1][t+1])/3 - 1)

    
    for x in range(99,-1,-1):
        for y in range(length-1,-1,-1):
            draw_line1(screen, y+xcor, x+ycor, y+xcor, x+ycor, gradient[c_buf[::-1][x][y]])
            
    #calculating values
    

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point( points, x0, y0, z0 )
    add_point( points, x1, y1, z1 )
    add_point( points, x2, y2, z2 )

"""
def scan_ln(screen, x0, y0, x1, y1, x2, y2, color):
    cors = [[y0,x0], [y1,x1], [y2,x2]]
    cors.sort()
    
    x_b = cors[0][1]
    x_m = cors[1][1]
    x_t = cors[2][1]
    
    y_b = int(cors[0][0])
    y_m = int(cors[1][0])
    y_t = int(cors[2][0])
    
    d_0 = (x_t - x_b) / (cors[2][0] - cors[0][0])

    x_0 = x_b
    x_1 = x_b
    
    y_0 = y_b
    y_1 = y_b

    
    while (y_0 < y_t):
       
        
        if (y_0 == y_m):
            d_1 = (x_t - x_m) / (y_t - y_m)
            x_1 = x_m
         
        elif (y_0 < y_m):
            d_1 = (x_m - x_b) / (y_m - y_b)
         
    
        x_0 += d_0
        x_1 += d_1
        
        y_0 += 1
        y_1 += 1

     
        draw_line(screen,x_0, y_0,x_1, y_1, color)
"""

def scan_ln(screen, x0, y0, z0, x1, y1, z1, x2, y2, z2, color, z_buf):
    
    cors = [[y0,x0,z0], [y1,x1,z1], [y2,x2,z2]]
    cors.sort()
    
    x_b = cors[0][1]
    x_m = cors[1][1]
    x_t = cors[2][1]
    
    y_b = int(cors[0][0])
    y_m = int(cors[1][0])
    y_t = int(cors[2][0])

    z_b = cors[0][2]
    z_m = cors[0][2]
    z_t = cors[0][2]
    
    dx_0 = (x_t - x_b) / (cors[2][0] - cors[0][0])
    dz_0 = (z_t - z_b) / (cors[2][0] - cors[0][0])

    x_0 = x_b
    z_0 = z_b

    y_0 = y_b
    y_1 = y_b

    
    if (y_b != y_m):      
        x_1 = x_b
        z_1 = z_b
    else:
        x_1 = x_m
        z_1 = z_m
        

    while (y_0 < y_t):
       
        
        if (y_0 == y_m):
            dx_1 = (x_t - x_m) / (y_t - y_m)
            dz_1 = (z_t - z_m) / (y_t - y_m)
            x_1 = x_m
            z_1 = z_m
         
        elif (y_0 < y_m):
            dx_1 = (x_m - x_b) / (y_m - y_b)
            dz_1 = (z_m - z_b) / (y_m - y_b)
            
        x_0 += dx_0
        x_1 += dx_1

        z_0 += dz_0
        z_1 += dz_1
        
        y_0 += 1
        y_1 += 1

     
        draw_line(screen,x_0, y_0, z_0, x_1, y_1, z_1, color, z_buf)
        

"""
def draw_polygons( points, screen, color ):

    if len(points) < 3:
        print 'Need at least 3 points to draw a polygon!'
        return

    p = 0
    while p < len( points ) - 2:

        if calculate_dot( points, p ) < 0:
            draw_line( screen, points[p][0], points[p][1],
                       points[p+1][0], points[p+1][1], color )
            draw_line( screen, points[p+1][0], points[p+1][1],
                       points[p+2][0], points[p+2][1], color )
            draw_line( screen, points[p+2][0], points[p+2][1],
                       points[p][0], points[p][1], color )

            scan_ln(screen,
                  points[p][0], points[p][1],
                  points[p+1][0], points[p+1][1],
                  points[p+2][0], points[p+2][1],
                  color)
            
        p+= 3
"""

def draw_polygons( points, screen, color, z_buf ):
    color = [0, 255, 0]
    if len(points) < 3:
        print 'Need at least 3 points to draw a polygon!'
        return

    p = 0
    while p < len( points ) - 2:

        if calculate_dot( points, p ) < 0:
            if color[1] <= 0:
                color[1] = 255
            color[1] -= 50
            
            draw_line( screen, points[p][0], points[p][1], points[p][2],
                         points[p+1][0], points[p+1][1], points[p+1][2], color, z_buf)
            draw_line( screen, points[p+1][0], points[p+1][1], points[p+1][2],
                         points[p+2][0], points[p+2][1], points[p+2][2], color, z_buf )
            draw_line( screen, points[p+2][0], points[p+2][1], points[p+2][2],
                         points[p][0], points[p][1], points[p][2], color, z_buf )

            
            scan_ln(screen,
                    points[p][0], points[p][1], points[p][2],
                    points[p+1][0], points[p+1][1], points[p+1][2],
                    points[p+2][0], points[p+2][1], points[p+2][2],
                    color, z_buf)
                 
        p+= 3

def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon( points, 
                 x, y, z, 
                 x, y1, z,
                 x1, y1, z)
    add_polygon( points, 
                 x1, y1, z, 
                 x1, y, z,
                 x, y, z)
    #back
    add_polygon( points, 
                 x1, y, z1, 
                 x1, y1, z1,
                 x, y1, z1)
    add_polygon( points, 
                 x, y1, z1, 
                 x, y, z1,
                 x1, y, z1)
    #top
    add_polygon( points, 
                 x, y, z1, 
                 x, y, z,
                 x1, y, z)
    add_polygon( points, 
                 x1, y, z, 
                 x1, y, z1,
                 x, y, z1)
    #bottom
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y1, z,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y1, z1,
	         x1, y1, z1)
    #right side
    add_polygon( points, 
                 x1, y, z, 
                 x1, y1, z,
                 x1, y1, z1)
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y, z1,
                 x1, y, z)
    #left side
    add_polygon( points, 
                 x, y, z1, 
                 x, y1, z1,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y, z,
                 x, y, z1) 


def add_sphere( points, cx, cy, cz, r, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_sphere( temp, cx, cy, cz, r, step )
    num_points = len( temp )

    lat = 0
    lat_stop = num_steps
    longt = 0
    longt_stop = num_steps

    num_steps += 1

    while lat < lat_stop:
        longt = 0
        while longt < longt_stop:
            
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]
            
            if longt != longt_stop - 1:
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]
            else:
                px2 = temp[ (index + 1) % num_points ][0]
                py2 = temp[ (index + 1) % num_points ][1]
                pz2 = temp[ (index + 1) % num_points ][2]
                
            px3 = temp[ index + 1 ][0]
            py3 = temp[ index + 1 ][1]
            pz3 = temp[ index + 1 ][2]
      
            if longt != 0:
                add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 )

            if longt != longt_stop - 1:
                add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 )
            
            longt+= 1
        lat+= 1

def generate_sphere( points, cx, cy, cz, r, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle <= circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = r * cos( pi * circ ) + cx
            y = r * sin( pi * circ ) * cos( 2 * pi * rot ) + cy
            z = r * sin( pi * circ ) * sin( 2 * pi * rot ) + cz
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step

def add_torus( points, cx, cy, cz, r0, r1, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_torus( temp, cx, cy, cz, r0, r1, step )
    num_points = len(temp)

    lat = 0
    lat_stop = num_steps
    longt_stop = num_steps
    
    while lat < lat_stop:
        longt = 0

        while longt < longt_stop:
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]

            if longt != num_steps - 1:            
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]

                px3 = temp[ (index + 1) % num_points ][0]
                py3 = temp[ (index + 1) % num_points ][1]
                pz3 = temp[ (index + 1) % num_points ][2]
            else:
                px2 = temp[ ((lat + 1) * num_steps) % num_points ][0]
                py2 = temp[ ((lat + 1) * num_steps) % num_points ][1]
                pz2 = temp[ ((lat + 1) * num_steps) % num_points ][2]

                px3 = temp[ (lat * num_steps) % num_points ][0]
                py3 = temp[ (lat * num_steps) % num_points ][1]
                pz3 = temp[ (lat * num_steps) % num_points ][2]


            add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 );
            add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 );        
            
            longt+= 1
        lat+= 1


def generate_torus( points, cx, cy, cz, r0, r1, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle < circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = (cos( 2 * pi * rot ) *
                 (r0 * cos( 2 * pi * circ) + r1 ) + cx)
            y = r0 * sin(2 * pi * circ) + cy
            z = (sin( 2 * pi * rot ) *
                 (r0 * cos(2 * pi * circ) + r1))
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step



def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    t = step
    while t<= 1:
        
        x = r * cos( 2 * pi * t ) + cx
        y = r * sin( 2 * pi * t ) + cy

        add_edge( points, x0, y0, cz, x, y, cz )
        x0 = x
        y0 = y
        t+= step
    add_edge( points, x0, y0, cz, cx + r, cy, cz )

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    xcoefs = generate_curve_coefs( x0, x1, x2, x3, curve_type )
    ycoefs = generate_curve_coefs( y0, y1, y2, y3, curve_type )
        
    t =  step
    while t <= 1:
        
        x = xcoefs[0][0] * t * t * t + xcoefs[0][1] * t * t + xcoefs[0][2] * t + xcoefs[0][3]
        y = ycoefs[0][0] * t * t * t + ycoefs[0][1] * t * t + ycoefs[0][2] * t + ycoefs[0][3]

        add_edge( points, x0, y0, 0, x, y, 0 )
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"
        
    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, matrix[p][0], matrix[p][1], matrix[p][2],
                   matrix[p+1][0], matrix[p+1][1], matrix[p+1][2], color , z_buf)
        p+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point( matrix, x0, y0, z0 )
    add_point( matrix, x1, y1, z1 )

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line1( screen, x0, y0, x1, y1, color ):
    dx = x1 - x0
    dy = y1 - y0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    
    if dx == 0:
        y = y0
        while y <= y1:
            plot1(screen, color,  x0, y)
            y = y + 1
    elif dy == 0:
        x = x0
        while x <= x1:
            plot1(screen, color, x, y0)
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot1(screen, color, x, y)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot1(screen, color, x, y)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot1(screen, color, x, y)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot1(screen, color, x, y)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx

def draw_line( screen, x0, y0, z0, x1, y1, z1, color, z_buf ):
    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
        tmp = z0
        z0 = z1
        z1 = tmp
      

    #if dx == 0 and dy == 0:
     #   plot(screen, color, x0, y0, max(z0, z1), z_buf)
    if dx == 0:
        y = y0
        z = z0
        while y <= y1:
            plot(screen, color,  x0, y, z, z_buf)
            y = y + 1
            z += dz / dy
    elif dy == 0:
        x = x0
        z = z0
        while x <= x1:
            plot(screen, color, x, y0, z, z_buf)
            x = x + 1
            z += dz / dx
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        z = z0
        while x <= x1:
            plot(screen, color, x, y, z, z_buf)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
            z += dz / dx
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        z = z0
        while y <= y1:
            plot(screen, color, x, y, z, z_buf)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
            z = dz / dy
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        z = z0
        while x <= x1:
            plot(screen, color, x, y, z, z_buf)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
            z = dz / dx
    else:
        d = 0
        x = x0
        y = y0
        z = z0
        while y <= y1:
            plot(screen, color, x, y, z, z_buf)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx
            z += dz / dy
