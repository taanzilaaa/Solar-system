from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

import math

W_Width, W_Height = 500,500

station_width = 30
station_height = 60

speed = 0.75
solar_x = 0
solar_y = 0

pause = False

def circ_point(x, y, a, b):           
    glVertex2f(a + x, b + y)
    glVertex2f(a + y, b + x)
    glVertex2f(a + y, b - x)
    glVertex2f(a + x, b - y)
    glVertex2f(a - x, b - y)
    glVertex2f(a - y, b - x)
    glVertex2f(a - y, b + x)
    glVertex2f(a - x, b + y)


def midCircle(radius, a, b):         
    d = 1 - radius
    x = 0
    y = radius

    glBegin(GL_POINTS)

    circ_point(x, y, a, b)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y -= 1
        x += 1
        
        circ_point(x, y, a, b)

    glEnd()

def midCirc(radius, a, b):
    num_segments = 100
    angle = 0
    glBegin(GL_POLYGON)  # Use GL_POLYGON to fill the circle

    for _ in range(num_segments):
        x = a + radius * math.cos(angle)
        y = b + radius * math.sin(angle)
        glVertex2f(x, y)
        angle += 2.0 * math.pi / num_segments

    glEnd()

def draw_station(radius, x, y):
    glColor3f(0.5, 0.5, 0.5)  # Gray color for space station
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + station_width, y)
    glVertex2f(x + station_width, y + station_height)
    glVertex2f(x, y + station_height)
    glEnd()
    

     # Draw two vertical lines beside the circle
    glColor3f(0.2, 0.2, 0.2)  # Light gray color for the lines
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(x + station_width / 2, y)
    glVertex2f(x + station_width / 2, y + station_height)
    glEnd()

    # Draw two horizontal lines beside the circle
    glBegin(GL_LINES)
    glVertex2f(x, y + station_height / 2)
    glVertex2f(x + station_width, y + station_height / 2)
    glEnd()

    # Draw a small circle at the center for the docking point
    glColor3f(0.8, 0.8, 0.8)  # Light gray color for the docking point
    midCirc(8, x + station_width / 2, y + station_height / 2)

def draw_solar():
    glColor3f(1.0, 1.0,1.0)
    glPointSize(3.0)
    midCircle(100, 200+ solar_x, 200 + solar_y)
    midCircle(200, 200+ solar_x, 200 + solar_y)
    midCircle(300, 200+ solar_x, 200 + solar_y)
    midCircle(400, 200+ solar_x, 200 + solar_y)
    midCircle(500, 200+ solar_x, 200 + solar_y)
    midCircle(600, 200+ solar_x, 200 + solar_y)

def update_solar_center():
    global solar_x , solar_y
    solar_x -= speed
    solar_y += speed
    if solar_x < -W_Width / 2:
        solar_x = W_Width / 2 + solar_x
    if solar_y >W_Width / 2:
        solar_y = -W_Width / 2 + solar_y

def draw_star(x, y, size, color):
    glColor3f(color[0], color[1], color[2])
    midCirc(size, x, y)

def draw_stars(num_stars):
    for _ in range(num_stars):
        x = random.uniform(-W_Width / 2, W_Width / 2)
        y = random.uniform(-W_Height / 2, W_Height / 2)
        size = random.uniform(1, 3)
        color = [1.0, 1.0, 1.0]  
        draw_star(x, y, size, color)

def draw_sun():
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    midCirc(50, 200 + solar_x, 200 + solar_y)

     
def draw_planet():
    glColor4f(0.5, 0.5, 0.5, 1.0)
    midCirc(20, 100 + solar_x, 190 + solar_y)

    glColor3f(1.0, 0.0, 1.0)
    midCirc(30, -100 + solar_x, -200 + solar_y)

    glColor3f(0.0, 1.0, 0.0)
    midCirc(50, -200 + solar_x, 170 + solar_y)

    glColor3f(0.0, 0.0, 1.0)
    midCirc(40, 300 + solar_x, -390 + solar_y)

    glColor3f(1.0, 0.0, 0.0)
    midCirc(60, 240 + solar_x, -100 + solar_y)

    glColor3f(0.0, 1.0, 1.0)
    midCirc(30, 370 + solar_x, 90 + solar_y)


def keyboardListener(key, x, y):
    global pause 
    if key==b' ':
        if pause == False:
            pause = True
        else:
            pause = False

    glutPostRedisplay()



def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global speed
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            speed -= 2 
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            speed += 2  


    glutPostRedisplay()


def display():
    #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #//load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    #//initialize the matrix
    glLoadIdentity()
    #//now give three info
    #//1. where is the camera (viewer)?
    #//2. where is the camera looking?
    #//3. Which direction is the camera's UP direction?
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    draw_solar()
    draw_sun()
    draw_stars(60)
    draw_planet()
    draw_station(15, 20 + solar_x, 40 + solar_y)
    glutSwapBuffers()


def animate():
    #//codes for any changes in Models, Camera
    global speed
    if not pause:
        update_solar_center()
    
    glutPostRedisplay()

def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(104,	1,	1,	1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    #//near distance
    #//far distance


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"Solar System")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)

glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()		#The main loop of OpenGL
