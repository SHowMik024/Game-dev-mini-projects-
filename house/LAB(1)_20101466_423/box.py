from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as r
import time


WIDTH, HEIGHT = 1180, 750

points = []
point_speed = .5
is_frozen = False
blink_colors = [GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT]
current_blink_color = 0
last_blink_time = 0

background_color = (0.0, 0.0, 0.0)

def draw_points(x, y, color):
    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(color[0], color[1], color[2])
    glVertex2f(x, y)
    glEnd()

def randomColor():
    return (r.random(), r.random(), r.random())

def randomDirection():
    return (r.choice([-1, 1]), r.choice([-1, 1]))


def generate_point(x, y):
    return {
        "x": x,
        "y": y,
        "color": randomColor(),
        "direction": randomDirection(),
        "is_blinking": False,
    }

def start_blink_animation():
    global is_frozen
    is_frozen = True
    current_time = time.time()
    for point in points:
        point["is_blinking"] = True

    while time.time() - current_time < 1:
        showScreen()
    is_frozen = False

def mouseClick(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if not is_frozen:
            points.append(generate_point(x, HEIGHT - y))

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        start_blink_animation()
def specialKey(key, x, y):
    global point_speed
    if key == GLUT_KEY_UP:
        point_speed += 0.1
    elif key == GLUT_KEY_DOWN:
        point_speed -= 0.1
        if point_speed < 0:
            point_speed = 0


def keyPressed(key, x, y):
    global is_frozen
    if key == b" ":
        is_frozen = not is_frozen

def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global is_frozen
    global current_blink_color
    global last_blink_time

    glClearColor(*background_color, 1.0)  # Use the background color
    glClear(blink_colors[current_blink_color])
    glLoadIdentity()
    iterate()

    for point in points:
        if not is_frozen:
            point["x"] += point_speed * point["direction"][0]
            point["y"] += point_speed * point["direction"][1]

            # Handle blinking
            if point["is_blinking"]:
                point["color"] = randomColor()

        draw_points(point["x"], point["y"], point["color"])

    current_time = int(time.time())
    if current_time - last_blink_time >= 1:
        current_blink_color = 1 - current_blink_color
        last_blink_time = current_time

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WIDTH, HEIGHT) # window size
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"box")
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)

    glutMouseFunc(mouseClick)
    glutSpecialFunc(specialKey)
    glutKeyboardFunc(keyPressed)

    glutMainLoop()

if __name__ == "__main__":
    main()