
import numpy as np
from OpenGL.GL import *

def texture(arr):
    """ Create a new OpenGL texture and return its texture ID. """
    if len(arr.shape) == 2:
        arr = np.tile(np.expand_dims(arr, 2), (1, 1, 3))
    assert arr.shape[2] == 3

    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, arr.shape[1], arr.shape[0],
                 0, GL_RGB, GL_UNSIGNED_BYTE, arr)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    return texid


def rm_textures(tex_ids):
    """ Delete a list of OpenGL textures. """
    glDeleteTextures(tex_ids)


def rm_texture(tex_id):
    """ Delete a single OpenGL texture. """
    glDeleteTextures([tex_id])


def replace_texture(arr, prev_tex_id):
    """ Delete the previous texture, if not None, and create a new one, returning its texture ID. """
    if prev_tex_id is not None:
        rm_texture(prev_tex_id)
    return texture(arr)
