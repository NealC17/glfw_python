import glfw


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

while not glfw.window_should_close(window):
    glfw.poll_events()

    glfw.swap_buffers(window)

glfw.terminate()



