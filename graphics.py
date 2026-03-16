import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
from PIL import Image

from ui import *

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

def loadTexture(texture_path):
    image = Image.open(texture_path)
    image = image.convert("RGBA")

    img_data = image.tobytes()
    width, height = image.size

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBindTexture(GL_TEXTURE_2D, 0)

    return texture_id

def drawOrigin():
    glBegin(GL_LINES)
    glColor(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(100,0,0)
    glColor(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,100,0)
    glColor(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,100)
    glEnd()

def drawPoint(p, color):
    glColor(color.r, color.g, color.b)
        
    glPushMatrix()
    glTranslatef(p.pos[0], p.pos[1], p.pos[2])

    glBegin(GL_POINTS)
    glVertex3f(0, 0, 0)
    glEnd()

    glPopMatrix()

def drawFlatland(cam, flatland, size=5000, divisions=50):
    spacing = 10**(int(math.log(abs(cam.pos[1] - flatland.height) + 2, 10)) + 1)
    # size = abs(cam.pos.y) * 10

    # subdivisions
    scene_spacing = spacing / 10
    N = divisions * 10
    corner_x = (-cam.pos[0] - N * 0.5 * scene_spacing) + cam.pos[0] % (scene_spacing)
    corner_z = (-cam.pos[2] - N * 0.5 * scene_spacing) + cam.pos[2] % (scene_spacing)

    glColor(flatland.color.r/2, flatland.color.g/2, flatland.color.b/2)
    glBegin(GL_LINES)
    for i in range(N + 1):
        cx = corner_x + i * scene_spacing
        z0 = corner_z
        z1 = corner_z + N * scene_spacing
        glVertex3f(cx, flatland.height, z0)
        glVertex3f(cx, flatland.height, z1)

    for i in range(N + 1):
        x0 = corner_x
        x1 = corner_x + N * scene_spacing
        cz = corner_z + i * scene_spacing
        glVertex3f(x0, flatland.height, cz)
        glVertex3f(x1, flatland.height, cz)
    glEnd()

    # superdivisions
    scene_spacing = spacing
    N = divisions
    corner_x = (-cam.pos[0] - N * 0.5 * scene_spacing) + cam.pos[0] % (scene_spacing)
    corner_z = (-cam.pos[2] - N * 0.5 * scene_spacing) + cam.pos[2] % (scene_spacing)

    glColor(flatland.color.r, flatland.color.g, flatland.color.b)
    glBegin(GL_LINES)
    for i in range(N + 1):
        cx = corner_x + i * scene_spacing
        z0 = corner_z
        z1 = corner_z + N * scene_spacing
        glVertex3f(cx, flatland.height, z0)
        glVertex3f(cx, flatland.height, z1)

    for i in range(N + 1):
        x0 = corner_x
        x1 = corner_x + N * scene_spacing
        cz = corner_z + i * scene_spacing
        glVertex3f(x0, flatland.height, cz)
        glVertex3f(x1, flatland.height, cz)
    glEnd()

def drawCannon(cam, o):
    glColor(1, 1, 1)
    glPushMatrix()
    glTranslatef(o.pos[0], o.pos[1], o.pos[2])
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, o.base_texture_id)
    glPolygonMode(GL_FRONT, GL_FILL)
    glBegin(GL_TRIANGLES)

    for face in o.model_base.faces:
        for i in range(3):
            try:
                u = o.model_base.texture_coords[face[1][i]-1][0]
                v = o.model_base.texture_coords[face[1][i]-1][1]
            except Exception as e:
                print(e)
                print(face)
                print(i)
                print(face[1][i])

            vertex_x = o.model_base.vertices[face[0][i]-1][0]
            vertex_y = o.model_base.vertices[face[0][i]-1][1]
            vertex_z = o.model_base.vertices[face[0][i]-1][2]

            vertex_i = np.matmul(np.array([vertex_x, vertex_y, vertex_z]), o.base_orient.tolist())

            glTexCoord2f(u, 1-v)
            glVertex3f(vertex_i[0], vertex_i[1], vertex_i[2])

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    glColor(1, 1, 1)
    glPushMatrix()
    glTranslatef(o.pos[0], o.pos[1] + 2.7, o.pos[2])
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, o.barrel_texture_id)
    glPolygonMode(GL_FRONT, GL_FILL)
    glBegin(GL_TRIANGLES)

    for face in o.model_barrel.faces:
        for i in range(3):
            try:
                u = o.model_barrel.texture_coords[face[1][i]-1][0]
                v = o.model_barrel.texture_coords[face[1][i]-1][1]
            except Exception as e:
                print(e)
                print(face)
                print(i)
                print(face[1][i])

            vertex_x = o.model_barrel.vertices[face[0][i]-1][0]
            vertex_y = o.model_barrel.vertices[face[0][i]-1][1]
            vertex_z = o.model_barrel.vertices[face[0][i]-1][2]

            vertex_i = np.matmul(np.array([vertex_x, vertex_y, vertex_z]), o.barrel_orient.tolist())

            glTexCoord2f(u, 1-v)
            glVertex3f(vertex_i[0], vertex_i[1], vertex_i[2])

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def drawObject(cam, o):
    glColor(1, 1, 1)
    glPushMatrix()
    glTranslatef(o.pos[0], o.pos[1], o.pos[2])
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, o.texture_id)
    glPolygonMode(GL_FRONT, GL_FILL)
    glBegin(GL_TRIANGLES)

    for face in o.model.faces:
        for i in range(3):
            try:
                u = o.model.texture_coords[face[1][i]-1][0]
                v = o.model.texture_coords[face[1][i]-1][1]
            except Exception as e:
                print(e)
                print(face)
                print(i)
                print(face[1][i])

            vertex_x = o.model.vertices[face[0][i]-1][0]
            vertex_y = o.model.vertices[face[0][i]-1][1]
            vertex_z = o.model.vertices[face[0][i]-1][2]

            vertex_i = np.matmul(np.array([vertex_x, vertex_y, vertex_z]), o.orient.tolist())

            glTexCoord2f(u, 1-v)
            glVertex3f(vertex_i[0], vertex_i[1], vertex_i[2])

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def drawObjectScaled(cam, o, scale):
    glColor(1, 1, 1)
    glPushMatrix()
    glTranslatef(o.pos[0], o.pos[1], o.pos[2])
    glScalef(scale[0], scale[1], scale[2])
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, o.texture_id)
    glPolygonMode(GL_FRONT, GL_FILL)
    glBegin(GL_TRIANGLES)

    for face in o.model.faces:
        for i in range(3):
            try:
                u = o.model.texture_coords[face[1][i]-1][0]
                v = o.model.texture_coords[face[1][i]-1][1]
            except Exception as e:
                print(e)
                print(face)
                print(i)
                print(face[1][i])

            vertex_x = o.model.vertices[face[0][i]-1][0]
            vertex_y = o.model.vertices[face[0][i]-1][1]
            vertex_z = o.model.vertices[face[0][i]-1][2]

            vertex_i = np.matmul(np.array([vertex_x, vertex_y, vertex_z]), o.orient.tolist())

            glTexCoord2f(u, 1-v)
            glVertex3f(vertex_i[0], vertex_i[1], vertex_i[2])

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def drawRay(pos, dirc, length=100):
    glPushMatrix()
    glColor(1, 0, 0)
    glTranslatef(pos[0], pos[1], pos[2])
    glBegin(GL_LINES)

    endpoint = dirc * length
    glVertex3f(0,0,0)
    glVertex3f(endpoint[0], endpoint[1], endpoint[2])

    glEnd()
    glPopMatrix()

def drawScene(cam, cannon, ships, shells, scenery_objects, smokes, splashes, game_time, height):
    # drawFlatland(cam, flatland)

    for o in scenery_objects:
        drawObject(cam, o)
    
    for s in ships:
        drawObject(cam, s)

    for s in smokes:
        pt_size = (15 + (s.state / s.time_end) * 20) * height / (2 * np.linalg.norm(-cam.pos - s.pos) * np.tan(70 / 2))
        pt_size = max(pt_size, 1)

        if s.state == 1:
            pt_size *= 3
            
        glPointSize(pt_size)

        if s.ship.state == 0:
            drawPoint(s, Color(0.5, 0.5, 0.5))
        else:
            drawPoint(s, Color(1.0, 0.6, 0.0))
    glPointSize(1)

    for s in splashes:
        s_rel_size = 0.2 + (s.state / s.time_end) * 0.8 * 2
        s_vert_rel_size = 1 + s.state / s.time_end * 1
        drawObjectScaled(cam, s, [s_rel_size, s_vert_rel_size, s_rel_size])

    for s in shells:
        # print(np.linalg.norm(-cam.pos - s.pos))
        pt_size = s.diam * height / (2 * np.linalg.norm(-cam.pos - s.pos) * np.tan(70 / 2))
        pt_size = max(pt_size, 3)
        glPointSize(pt_size)
        drawPoint(s, Color(0.9, 0.7, 0))
    glPointSize(1)

    drawCannon(cam, cannon)

##    glLineWidth(2)
##    for b in bullets:
##        lock = cam.lock
##        if lock:
##            drawRay(b.pos, (b.vel - lock.vel) / np.linalg.norm((b.vel - lock.vel)), np.linalg.norm(b.vel) * 0.1)
##        else:
##            drawRay(b.pos, b.vel / np.linalg.norm(b.vel), np.linalg.norm(b.vel) * 0.1)
##    glLineWidth(1)

    render_AN("AZ " + str(round(np.rad2deg(cannon.az), 1)) + " EL " + str(round(np.rad2deg(cannon.el), 2)) + " PROP " + str(cannon.charges), Color(1, 0, 0), [-7, 5], cam)
    # drawLine2D(0, 0, 1, 1, Color(0, 1, 0), cam)
