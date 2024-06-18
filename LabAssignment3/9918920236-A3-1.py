import glfw
from OpenGL.GL import *
import numpy as np


default = np.eye(3, 3)
gComposedM, newM = default, np.empty(3)



def key_callback(window, key, scancode, action, mods):
    global gComposedM, newM, default
    degree = np.radians(10)

    # Translate by -0.1 in x direction w.r.t global coordinate

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window)

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            gComposedM = default
            print('Reset')

        if key == glfw.KEY_Q:
            M = np.array([[1., 0., -0.1],
                        [0., 1., 0.],
                        [0., 0., 1.]])
            newM = M
            gComposedM = newM @ gComposedM
            print('press Q')

        if key == glfw.KEY_E:
            M = np.array([[1., 0., 0.1],
                          [0., 1., 0.],
                          [0., 0., 1.]])
            newM = M
            gComposedM = newM @ gComposedM
            print('press E')

        if key == glfw.KEY_A:
            R = np.array([[np.cos(degree), -np.sin(degree), 0.],
                          [np.sin(degree), np.cos(degree), 0.],
                          [0., 0., 1]])
            newM = R
            gComposedM = newM @ gComposedM
            print('press A')

        if key == glfw.KEY_D:
            R = np.array([[np.cos(-degree), -np.sin(-degree), 0.],
                          [np.sin(-degree), np.cos(-degree), 0.],
                          [0., 0., 1]])
            newM = R
            gComposedM = newM @ gComposedM
            print('press D')





def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((T @ np.array([.0, .5, 1.]))[:-1])
    glVertex2fv((T @ np.array([.0, .0, 1.]))[:-1])
    glVertex2fv((T @ np.array([.5, .0, 1.]))[:-1])
    glEnd()


def main():
    global gComposedM

    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "9918920236-A3-1", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gComposedM)
        glfw.swap_buffers(window)

    glfw.terminate()
    print("closed")

    if __name__ == "__main__":
        main()


main()
