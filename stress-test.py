#!/usr/bin/python

import pygame, fasterobj, sys, cPickle, pickle
from math import sin, cos, pi, sqrt
from fasterobj import OBJ, OBJ_array, OBJ_vbo
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

nsprites = 40  # Number of sprites to render
tmax = 60.     # Number of seconds to run each test for
spritename = "elder.obj"  # OBJ file for the sprite

print "testing %s sprites for %s seconds" % (nsprites, tmax)
print "    type  list? parse save load   render"

spritesize = 6.
d = sqrt(nsprites) * spritesize * 3

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
 
glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)
glMatrixMode(GL_PROJECTION)

# Six different methods are tested: fixed function, vertex array, and VBO,
#   each without and with a display list
formats = ((x,y) for x in ("fixed", "array", "vbo") for y in (False, True))
for nformat, (format, use_list) in enumerate(formats):
	oclass = OBJ_vbo if format == "vbo" else OBJ_array if format == "array" else OBJ
	oclass.use_list = use_list

    # Time how long it takes to parse, meaning read the model from the OBJ file
	start = pygame.time.get_ticks()
	obj = oclass(spritename)
	parsetime = pygame.time.get_ticks() - start

    # Time how long it takes to save, meaning dump the parsed model to a pickle file
	start = pygame.time.get_ticks()
	cPickle.dump(obj, open("stress-test.pickle", "wb"), -1)
	savetime = pygame.time.get_ticks() - start

	del obj

    # The previous two steps usually only need to be run once, by the programmer
    # Distribute the pickle file with your game, and your players will only need to do the following step

    # Time how long it takes to load, meaning get the model from the pickle file
	start = pygame.time.get_ticks()
	obj = cPickle.load(open("stress-test.pickle", "rb"))
	loadtime = pygame.time.get_ticks() - start

	glLoadIdentity()
	width, height = viewport
	gluPerspective(45.0, width/float(height), 1, 10000.0)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_MODELVIEW)

	isquit = lambda e: e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE)

    # Get the framerate for rendering
	t = 0.
	jframe = 0
	clock = pygame.time.Clock()
	while t < tmax:
		dt = clock.tick() * 0.001
		t += dt
		jframe += 1
		if any(isquit(e) for e in pygame.event.get()): break

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		for j in range(nsprites):
			r, theta = sqrt(j)*spritesize, j*2.4
			glLoadIdentity()
			gluLookAt(d*sin(t),d*cos(t),d/2.,0,0,0,0,0,1)
			glTranslate(r*sin(theta), r*cos(theta), spritesize*sin(t*1.77+j**2*1.22+t*j*0.02))
			obj.render()

		pygame.display.flip()
	del obj
	fps = jframe / t
	print "#%s: %s %s %s %s %s %.2ffps" % (nformat+1, format, use_list, parsetime, savetime, loadtime, fps)

