import glfw
from OpenGL.GL import *
import numpy as np


def compileShader(shaderType, src):
    id = glCreateShader(shaderType)
    glShaderSource(id, src)
    glCompileShader(id)

    return id

def createShader(vertex, fragment):

    vs = compileShader(GL_VERTEX_SHADER, vertex)
    fs = compileShader(GL_FRAGMENT_SHADER, fragment)

    program = glCreateProgram()
    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)
    glValidateProgram(program)

    glDeleteShader(vs)
    glDeleteShader(fs)

    return program

def main():
    if not glfw.init():
        return
    # Создаем окно
    window = glfw.create_window(600, 400, "PythonOpenGL", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    vertices = [
        -1.0, -1.0,
         1.0, -1.0,
         1.0,  1.0,

         1.0,  1.0,
        -1.0,  1.0,
        -1.0, -1.0,
    ]

    # Конвертация в сишный массив
    converted = np.array(vertices, dtype = np.float32)
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, converted, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * 4, None)
    glEnableVertexAttribArray(0)

    vertex = open("vertex.shader").read()
    fragment = open("fragment.shader").read()
    
    shader = createShader(vertex, fragment)
    glUseProgram(shader)



    glUniform2f(glGetUniformLocation(shader, "iResolution"), 600, 400)

    while not glfw.window_should_close(window):
        # Рендер с помощью pyOpenGL


        glUniform1f(glGetUniformLocation(shader, "iTime"), glfw.get_time())
        glDrawArrays(GL_TRIANGLES, 0, 6)


        glfw.swap_buffers(window)

        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()