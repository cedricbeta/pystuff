from OpenGL.GL import glCallList, glClear, glClearColor, glColorMaterial, glCullFace, glDepthFunc, glDisable, glEnable,\
                      glFlush, glGetFloatv, glLightfv, glLoadIdentity, glMatrixMode, glMultMatrixf, glPopMatrix, \
                      glPushMatrix, glTranslated, glViewport, \
                      GL_AMBIENT_AND_DIFFUSE, GL_BACK, GL_CULL_FACE, GL_COLOR_BUFFER_BIT, GL_COLOR_MATERIAL, \
                      GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_FRONT_AND_BACK, GL_LESS, GL_LIGHT0, GL_LIGHTING, \
                      GL_MODELVIEW, GL_MODELVIEW_MATRIX, GL_POSITION, GL_PROJECTION, GL_SPOT_DIRECTION

from OpenGL.constants import GLfloat_3, GLfloat_4

from OpenGL.GLU import gluPerspective, gluUnProject

from OpenGL.GLUT import glutCreateWindow, glutDisplayFunc, glutGet, glutInit, glutInitDisplayMode, \
                        glutInitWindowSize, glutMainLoop, \
                        GLUT_SINGLE, GLUT_RGB, GLUT_WINDOW_HEIGHT, GLUT_WINDOW_WIDTH

import numpy
from numpy.linalg import norm, inv

from primitive import init_primitives
import color 
from scene import Scene
from primitive import init_primitives, G_OBJ_PLANE
from node import Sphere, Cube, SnowFigure
from interaction import Interaction

class Viewer(object):
	def __init__(self):
		self.init_interface()
		self.init_opengl()
		self.init_scene()
		self.init_interaction()
		init_primitives()

	def init_interface(self):
		glutInit()
		glutInitWindowSize(640, 480)
		glutCreateWindow("3D Maker")
		glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
		glutDisplayFunc(self.render)

	def init_opengl(self):
		self.inverseModelView = numpy.identity(4)
		self.modelView = numpy.identity(4)

		glEnable(GL_CULL_FACE)
		glCullFace(GL_BACK)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LESS)
		glEnable(GL_LIGHT0)
		glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 1, 0))
		glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0, 0, -1))
		glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
		glEnable(GL_COLOR_MATERIAL)
		glClearColor(0.4, 0.4, 0.4, 0.0)

	def init_scene(self):
		self.scene = Scene()
		self.create_sample_scene()

	def create_sample_scene(self):
		sphere_node = Sphere()
		sphere_node.color_index = 3
		sphere_node.translate(2,2,0)
		sphere_node.scale(2)
		self.scene.add_node(sphere_node)
		hierarchical_node = SnowFigure()
		hierarchical_node.translate(-4, 0, -4)
		hierarchical_node.scale(3)
		self.scene.add_node(hierarchical_node)

	def init_interaction(self):
		self.interaction = Interaction()
		self.interaction.register_callback('pick', self.pick)
		self.interaction.register_callback('move', self.move)
		self.interaction.register_callback('place', self.place)
		self.interaction.register_callback('rotate_color', self.rotate_color)
		self.interaction.register_callback('scale', self.scale)

	def pick(self, x, y):
		start, direction = self.get_ray(x, y)
		self.scene.pick(start, direction, self.modelView)
		

	def move(self, x, y):
		pass

	def place(self, shape, x, y):
		start, direction = self.get_ray(x, y)
		self.scene.place(shape, start, direction, self.inverseModelView)

	def rotate_color(self, forward):
		start, direction = self.get_ray(x, y)
		self.scene.move_selected(start, direction, self.inverseModelView)

	def scale(self, up):
		pass

	def main_loop(self):
		glutMainLoop()

	def render(self):
		self.init_view()
		glEnable(GL_LIGHTING)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		glMultMatrixf(self.interaction.trackball.matrix)
		currentModelView = numpy.array(glGetFloatv(GL_MODELVIEW_MATRIX))
		self.modelView = numpy.transpose(currentModelView)
		self.inverseModelView = inv(numpy.transpose(currentModelView))
		
		self.scene.render()
		glDisable(GL_LIGHTING)
		glCallList(G_OBJ_PLANE)
		glPopMatrix()
		glFlush()

	def init_view(self):
		xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
		aspect_ratio = float(xSize) / float(ySize)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glViewport(0, 0, xSize, ySize)
		gluPerspective(70, aspect_ratio, 0.1, 1000.0)
		glTranslated(0, 0, -15)

	def get_ray(self, x, y):
		self.init_view()
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		start = numpy.array(gluUnProject(x, y, 0.001))
		end = numpy.array(gluUnProject(x, y, 0.999))
		direction = end - start
		direction = direction / norm(direction)
		return (start, direction)




if __name__=="__main__":
	viewer = Viewer()
	viewer.main_loop()



