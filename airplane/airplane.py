import math
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import os

airp_text_coord = 1.0
plan_color = [(0.52, 0.52, 0.78, 1.0)]
airp_color = [(0.3, 0.52, 0.18, 1.0)]
airp_p = [0, 2, -3]
airp_a = [0, 0, 0, 0]
plan_text = None
airp_text = None

animate = False
WIDTH = 800
HEIGHT = 800

watch = [0.0, 7.0, 0.0]
lk_pos = [0.0, 3.0, 0.0]

text = 1
t_xz = 0
r_xz = 6

coord_text_airp = [(-airp_text_coord, -airp_text_coord),
                   (airp_text_coord, -airp_text_coord),
                   (airp_text_coord, airp_text_coord),
                   (-airp_text_coord, airp_text_coord)]


# function that makes the automatic movement
def animate_func(ctx):
    global animate

    if animate:
        compair()
        glutPostRedisplay()
        glutTimerFunc(10, animate_func, 1)


# Function that deals the movement of airplane
def compair():
    global airp_p, airp_a

    if int(airp_a[0] % 90) == 0:
        if int(airp_a[0]) == 0 or int(airp_a[0]) == 360:
            airp_p[2] += 0.005
        elif int(airp_a[0]) == 90:
            airp_p[0] += 0.005
        elif int(airp_a[0]) == 180:
            airp_p[2] -= 0.005
        elif int(airp_a[0]) == 270:
            airp_p[0] -= 0.005
    else:
        q = ((int(airp_a[0]) % 360) // 90) + 1
        if q == 1:
            airp_p[0] += 0.005
            airp_p[2] += 0.005
        elif q == 2:
            airp_p[2] -= 0.005
            airp_p[0] += 0.005
        elif q == 3:
            airp_p[2] -= 0.005
            airp_p[0] -= 0.005
        elif q == 4:
            airp_p[2] += 0.005
            airp_p[0] -= 0.005


# Reshape window function
def reshape(width, height):
    global WIDTH, HEIGHT

    WIDTH = width
    HEIGHT = height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, width/height, 0.1, 30)


# Function that deals with keyboard special keys
def specials(ctx, x, y):
    global watch, lk_pos, t_xz
    if ctx == GLUT_KEY_UP:  # go up on the y axis
        watch[1] += 1
        glutPostRedisplay()
    elif ctx == GLUT_KEY_DOWN:  # Descend on the y axis
        watch[1] -= 1
        glutPostRedisplay()
    elif ctx == GLUT_KEY_LEFT:  # move right on the x axis
        t_xz += 2
        glutPostRedisplay()
    elif ctx == GLUT_KEY_RIGHT: # move left on the x axis
        t_xz -= 2
        glutPostRedisplay()


# Keyboard function
def keyboard(key, x, y):
    global r_xz, airp_p, airp_a, animate

    if key == b'\x1b':  # Esc
        os._exit(0)
    elif key == b'Z':   # zoom in
        r_xz += 1
        glutPostRedisplay()
    elif key == b'z':   # zoom out
        r_xz -= 1
        if r_xz == 0:
            r_xz = 1
        glutPostRedisplay()
    elif key == b'w':   # move forward
        compair()
        glutPostRedisplay()
    elif key == b'a':   # turn left
        airp_a[0] += 1
        airp_a[2] = 1
        if airp_a[0] > 360:
            airp_a[0] -= 360
        glutPostRedisplay()
    elif key == b'd':   # turn right
        airp_a[0] -= 1
        airp_a[2] = 1
        if airp_a[0] < 0:
            airp_a[0] += 360
        glutPostRedisplay()
    elif key == b'y':   # automatic movement on
        animate = True
        glutTimerFunc(10, animate_func, 1)
        glutPostRedisplay()
    elif key == b'n':   # automatic movement off
        animate = False


# Display function
def display():
    global airp_text, plan_text, airp_color, plan_color
    global airp_p, airp_a

    glEnable(GL_DEPTH_TEST)

    glDepthMask(GL_TRUE)
    glClearColor(0.3, 0.5, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()

    watch[0] = r_xz * math.cos(2 * 3.14 * t_xz / 360)
    watch[2] = r_xz * math.sin(2 * 3.14 * t_xz / 360)
    gluLookAt(watch[0], watch[1], watch[2], lk_pos[0], lk_pos[1], lk_pos[2], 0, 1, 0)

    glEnable(GL_TEXTURE_2D)

    glColor4f(plan_color[0][0], plan_color[0][1], plan_color[0][2], plan_color[0][3])
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glBindTexture(GL_TEXTURE_2D, plan_text)

    glBegin(GL_QUADS)
    glTexCoord2fv([0, 0])
    glVertex3f(-20, 0, 20)
    glTexCoord2fv([0, 1])
    glVertex3f(20, 0, 20)
    glTexCoord2fv([1, 1])
    glVertex3f(20, 0, -20)
    glTexCoord2fv([1, 0])
    glVertex3f(-20, 0, -20)
    glEnd()

    glTranslatef(airp_p[0], airp_p[1], airp_p[2])
    glRotatef(airp_a[0], airp_a[1], airp_a[2], airp_a[3])
    glScalef(0.5, 0.5, 0.5)

    glColor4f(airp_color[0][0], airp_color[0][1], airp_color[0][2], airp_color[0][3])
    glBindTexture(GL_TEXTURE_2D, airp_text)
    glCallList(airp)

    glPopMatrix()
    glutSwapBuffers()


# Airplane draws function
def airp_draw():
    # coordinates of wing
    wing = [(-4, 0, 0),
            (4, 0, 0),
            (0, 0, 3)]

    # coordinates of tail
    tail = [(0, 0, 0),
            (0, 2, -1),
            (0, 2, 0),
            (0, 0, 2)]

    global airp, airp_text
    global coord_text_airp

    airp = glGenLists(1)
    glNewList(airp, GL_COMPILE)

    # wing
    glBegin(GL_TRIANGLES)
    glTexCoord2fv(coord_text_airp[0])
    glVertex3fv(wing[0])
    glTexCoord2fv(coord_text_airp[1])
    glVertex3fv(wing[1])
    glTexCoord2fv(coord_text_airp[2])
    glVertex3fv(wing[2])
    glEnd()

    # body
    cylinder = gluNewQuadric()
    gluQuadricTexture(cylinder, GL_TRUE)
    gluCylinder(cylinder, 0.5, 0.5, 4, 12, 3)
    # still doing body construction
    cylinder = gluNewQuadric()
    gluQuadricTexture(cylinder, GL_TRUE)
    # nose
    glPushMatrix()
    glTranslatef(0, 0, 4)
    gluCylinder(cylinder, 0.5, 0.0, 1.5, 12, 3)
    glPopMatrix()

    # tail
    glBegin(GL_POLYGON)
    glTexCoord2fv(coord_text_airp[0])
    glVertex3fv(tail[0])
    glTexCoord2fv(coord_text_airp[1])
    glVertex3fv(tail[1])
    glTexCoord2fv(coord_text_airp[2])
    glVertex3fv(tail[2])
    glTexCoord2fv(coord_text_airp[3])
    glVertex3fv(tail[3])
    glEnd()

    # pilot cabin
    glTranslatef(0, 0.3, 3.5)
    glPushMatrix()
    glScalef(0.7, 0.7, 2.0)
    polygon = gluNewQuadric()
    glColor3f(0.3, 0.5, 1)
    glDisable(GL_TEXTURE_2D)
    gluSphere(polygon, 0.5, 12, 12)
    glPopMatrix()

    glEndList()


def text_load():
    global plan_text, airp_text

    # loading the ground texture image
    img = Image.open("texture_base/macz.jpg")
    img_data = numpy.array(list(img.getdata()), numpy.int8)

    plan_text = glGenTextures(1)    # texture name generated
    glBindTexture(GL_TEXTURE_2D, plan_text)     # link the texture to that name

    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, img.size[0], img.size[1],
                      GL_RGB, GL_UNSIGNED_BYTE, img_data)   # Load texture

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)    # directions axis that texture will be repeated for
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)  # filters used
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)    # how texture is recognized

    # loading the airplane texture image
    img2 = Image.open("texture_base/camuflagem.jpg")
    img_data2 = numpy.array(list(img2.getdata()), numpy.int8)

    airp_text = glGenTextures(1)    # texture name generated
    glBindTexture(GL_TEXTURE_2D, airp_text)     # link the texture to that name

    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, img2.size[0], img2.size[1],
                      GL_RGB, GL_UNSIGNED_BYTE, img_data2)      # Load texture

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)    # directions axis that texture will be repeated for
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)  # filters used
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)    # how texture is recognized


def init():
    text_load()  # Call the function that loads the textures
    airp_draw()  # Call the function that draw the airplane
    glShadeModel(GL_FLAT)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.1, 0.1, 0.1, 1))  # Parameters of lighting model

    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1))    # difuse light
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))     # specular light
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1))    # ambient light
    glLightfv(GL_LIGHT0, GL_POSITION, (1.2, 0.1, 1.2, 0))   # light position

    glEnable(GL_LIGHTING)   # Enable light
    glEnable(GL_LIGHT0)     # enable 1 of the 8 possible lights utilizable in openGL

    glEnable(GL_COLOR_MATERIAL)     # Enable the utilization of material original color
    glEnable(GL_AUTO_NORMAL)

    glEnable(GL_TEXTURE_2D)


if __name__ == '__main__':
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    glutCreateWindow("Airplanes planes")

    init()  # Program init function

    glutKeyboardFunc(keyboard)  # callback to function that handle keyboard events
    glutSpecialFunc(specials)   # callback to function that handle keyboard special events
    glutDisplayFunc(display)    # callback to function that draw in display
    glutReshapeFunc(reshape)    # callback to function that deals reshape
    glutTimerFunc(10, animate_func, 1)  # callback function that makes the automatic movement

    glutMainLoop()
