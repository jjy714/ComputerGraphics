import numpy as np
from OpenGL.GL import *
import glfw

GeoFeatures = {
                1: GL_POINTS,
                2: GL_LINES,
                3: GL_LINE_STRIP,
                4: GL_LINE_LOOP,
                5: GL_TRIANGLES,
                6: GL_TRIANGLE_STRIP,
                7: GL_TRIANGLE_FAN,
                8: GL_QUADS,
                9: GL_QUAD_STRIP,
                0: GL_POLYGON}

features = GL_POLYGON

def key_callback(window, key, scancode, action, mods):
    global features
    if key == glfw.KEY_0:
        if action == glfw.PRESS:
            print("press 0")
        features = GeoFeatures[0]
    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            print("press 1")
        features = GeoFeatures[1]
    if key == glfw.KEY_2:
        if action == glfw.PRESS:
            print("press 2")
        features = GeoFeatures[2]
    if key == glfw.KEY_3:
        if action == glfw.PRESS:
            print("press 3")
        features = GeoFeatures[3]
    if key == glfw.KEY_4:
        if action == glfw.PRESS:
            print("press 4")
        features = GeoFeatures[4]
    if key == glfw.KEY_5:
        if action == glfw.PRESS:
            print("press 5")
        features = GeoFeatures[5]
    if key == glfw.KEY_6:
        if action == glfw.PRESS:
            print("press 6")
        features = GeoFeatures[6]
    if key == glfw.KEY_7:
        if action == glfw.PRESS:
            print("press 7")
        features = GeoFeatures[7]
    if key == glfw.KEY_8:
        if action == glfw.PRESS:
            print("press 8")
        features = GeoFeatures[8]
    if key == glfw.KEY_9:
        if action == glfw.PRESS:
            print("press 9")
        features = GeoFeatures[9]

def window_close_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE:
        if action == glfw.PRESS:
            print("ESC pressed")
            glfw.window_should_close(window)


def render(features):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(features)
    glColor3ub(255, 255, 255)
    vertices = np.radians(np.arange(12.) * 30)
    for i in vertices:
        glVertex2d(np.cos(i), np.sin(i))
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "A2", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_window_close_callback(window, window_close_callback)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(features)
        glfw.swap_buffers(window)

    glfw.terminate()

    if __name__ == "__main__":
        main()

main()