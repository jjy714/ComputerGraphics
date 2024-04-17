import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pdb


pressedKey = ""


def key_callback(window, key, scancode, action, mods):
    # Translate by -0.1 in x direction w.r.t global coordinate

    if key == glfw.KEY_Q:
        pressedKey = "Q"
        if action == glfw.PRESS:
            print('press Q')

        elif action == glfw.RELEASE:
            print('release Q')
            pressedKey = "Q"
        elif action == glfw.REPEAT:
            print('repeat Q')


    if key == glfw.KEY_E:
        if action == glfw.PRESS:
            print('press E')
        elif action == glfw.RELEASE:
            print('release E')
            pressedKey = "E"
        elif action == glfw.REPEAT:
            print('repeat E')
            pressedKey = "E"

    if key == glfw.KEY_A:
        if action == glfw.PRESS:
            print('press A')
        elif action == glfw.RELEASE:
            print('release A')
            pressedKey = "A"
            return pressedKey
        elif action == glfw.REPEAT:
            print('repeat A')
            return pressedKey

    if key == glfw.KEY_D:
        if action == glfw.PRESS:
            print('press D')
        elif action == glfw.RELEASE:
            print('release D')
            pressedKey = "D"
            return pressedKey
        elif action == glfw.REPEAT:
            print('repeat D')
            return pressedKey

    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            print('press 1')
        elif action == glfw.RELEASE:
            print('release 1')
            pressedKey = "1"
            return pressedKey
        elif action == glfw.REPEAT:
            print('repeat 1')
            return pressedKey


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
    T = np.ones(shape=(3, 3))
    gComposedM = np.empty(0)
    degree = 0.17
    print(T)
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "A3", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)


    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(T)
        if pressedKey == "1":
            render(T)

        if pressedKey == "Q":
            M = np.array([[1., 0., -0.1],
                        [0., 1., 0.],
                        [0., 0., 1.]])
            newM = M
            if gComposedM is not None:
                gComposedM = newM @ gComposedM
                render(gComposedM)
            else:
                render(newM)

        if pressedKey == "E":
            M = np.array([[1., 0., 0.1],
                        [0., 1., 0.],
                        [0., 0., 1.]])
            newM = M
            if gComposedM is not None:
                gComposedM = newM @ gComposedM
                render(gComposedM)
            else:
                render(newM)

        if pressedKey == "A":

            R = np.array([[np.cos(degree), -np.sin(degree), 0.],
                          [np.sin(degree), np.cos(degree), 0.],
                          [0., 0., 1]])
            newM = R
            if gComposedM is not None:
                gComposedM = newM @ gComposedM
                render(gComposedM)
            else:
                render(newM)


        if pressedKey == "D":
            R = np.array([[np.cos(-degree), -np.sin(-degree), 0.],
                          [np.sin(-degree), np.cos(-degree), 0.],
                          [0., 0., 1]])
            newM = R
            if gComposedM is not None:
                gComposedM = newM @ gComposedM
                render(gComposedM)
            else:
                render(newM)


        glfw.swap_buffers(window)

    glfw.terminate()

    if __name__ == "__main__":
        main()


main()
