import matplotlib.pyplot as plt
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from vectors import *


def normal(face_):
    return cross(subtract(face_[1], face_[0]), subtract(face_[2], face_[0]))


blues = plt.get_cmap('Blues')


def shade(face_, color_map=blues, light_=(1, 2, 3)):
    return color_map(1 - dot(unit(normal(face_)), unit(light_)))


light = (1, 2, 3)
faces = [
    [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    [(1, 0, 0), (0, 0, -1), (0, 1, 0)],
    [(1, 0, 0), (0, 0, 1), (0, -1, 0)],
    [(1, 0, 0), (0, -1, 0), (0, 0, -1)],
    [(-1, 0, 0), (0, 0, 1), (0, 1, 0)],
    [(-1, 0, 0), (0, 1, 0), (0, 0, -1)],
    [(-1, 0, 0), (0, -1, 0), (0, 0, 1)],
    [(-1, 0, 0), (0, 0, -1), (0, -1, 0)],
]


def Axes():
    axes = [
        [(-1000, 0, 0), (1000, 0, 0)],
        [(0, -1000, 0), (0, 1000, 0)],
        [(0, 0, -1000), (0, 0, 1000)]
    ]
    glBegin(GL_LINES)
    for axis in axes:
        for vertex_ in axis:
            glColor3fv((1, 1, 1))
            glVertex3fv(vertex_)
    glEnd()


pygame.init()
display = (400, 400)
window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45, 1, 0.1, 50.0)

glTranslatef(0.0, 0.0, -5)

glEnable(GL_CULL_FACE)
glEnable(GL_DEPTH_TEST)
glCullFace(GL_BACK)

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    degrees_per_second = 360. / 5.
    degrees_per_millisecond = degrees_per_second / 1000.
    milliseconds = clock.tick()
    degrees = degrees_per_millisecond * milliseconds
    glRotatef(degrees, 1, 1, 1)

    glBegin(GL_TRIANGLES)
    for face in faces:
        color = shade(face, blues, light)
        for vertex in face:
            glColor3fv((color[0], color[1], color[2]))
            glVertex3fv(vertex)
    glEnd()
    pygame.display.flip()

    print(clock.get_fps())
