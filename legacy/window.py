import glfw
from OpenGL.GL import *
#from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileProgram, compileShader 
from helper import vertex_src, fragment_src
import numpy as np

#start glfw
if not glfw.init():
    exit("GLFW failed") 


#create the glfw window
window = glfw.create_window(1280, 720, "title", None, None)


#window creation failed
if not window:
    glfw.terminate()
    exit("Window creation failed")


#set the position of the window on the screen
glfw.set_window_pos(window, 400, 200)


#Create an OpenGL context which is a state machine that stores all data related to rendering
#destroyed when program exits
glfw.make_context_current(window)


vertices = [-0.5, -0.5, 0, 1.0, 0.0, 0.0,
             0.5, -0.5, 0, 0.0, 1.0, 0.0,
             0.0,  0.5, 0, 0.0, 0.0, 1.0,]


vertices = np.array(vertices, dtype=np.float32)
vel = np.array([1, 0, 0, 0, 0, 0, 
                1, 0, 0, 0, 0, 0,
                1, 0, 0, 0, 0, 0], dtype=np.float32)/100


shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER)) #Does the Linking for you so you d o not need to worry about using stuff


VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

position = glGetAttribLocation(shader, "a_position") #has to be the same as the variable in the helper.py file for vertex_src

glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

color = glGetAttribLocation(shader, "a_color")
glEnableVertexAttribArray(color)
glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(shader) #set the binary to the shader
glClearColor(0, 0, 0.1, 0.1) #Takes (R, G, B, A) 
#0 0 is the center
while not glfw.window_should_close(window):
    glfw.poll_events()
    
    
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    #vertices += vel
    glfw.swap_buffers(window)

glfw.terminate()



