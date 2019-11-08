""" Passive geometric shape widgets to be drawn as `concur.extra_widgets.image.image` overlay, or on their own.

All these widgets have the following in common:

* They are passive, so they don't need names. For active overlay, use normal widgets such as buttons.
* `color` is specified as RGBA tuple with values between 0 and 1. For example, `(0.5, 0.5, 1, 1)` is light blue.
* `tf` is the `concur.extra_widgets.pan_zoom.TF` object specifying transformations from screen-space to image-space and back.
  If no transformation is supplied, the element is drawn in screen space units.
"""


import numpy as np
import imgui


def line(x0, y0, x1, y1, color, thickness=1, tf=None):
    """ Line connecting two points. """
    while(True):
        if tf is not None:
            [x0, y0], [x1, y1] = np.matmul(tf.c2s, [x0, y0, 1]), np.matmul(tf.c2s, [x1, y1, 1])
        draw_list = imgui.get_window_draw_list()
        draw_list.add_line(x0, y0, x1, y1, imgui.get_color_u32_rgba(*color), thickness)
        yield


def rect(x0, y0, x1, y1, color, thickness=1, rounding=0, tf=None):
    """ Straight non-filled rectangle specified by its two corners. """
    while(True):
        if tf is not None:
            [x0, y0], [x1, y1] = np.matmul(tf.c2s, [x0, y0, 1]), np.matmul(tf.c2s, [x1, y1, 1])
        # Avoid issues with disappearing lines on very large rectangles
        x0, x1 = np.clip([x0, x1], -8192, 8192)
        y0, y1 = np.clip([y0, y1], -8192, 8192)
        draw_list = imgui.get_window_draw_list()
        draw_list.add_rect(x0, y0, x1, y1, imgui.get_color_u32_rgba(*color), rounding, 15 if rounding else 0, thickness)
        yield


def rect_filled(x0, y0, x1, y1, color, rounding=0, tf=None):
    """ Straight non-filled rectangle specified by its two corners. """
    while(True):
        if tf is not None:
            [x0, y0], [x1, y1] = np.matmul(tf.c2s, [x0, y0, 1]), np.matmul(tf.c2s, [x1, y1, 1])
        # Avoid issues with disappearing lines on very large rectangles
        x0, x1 = np.clip([x0, x1], -8192, 8192)
        y0, y1 = np.clip([y0, y1], -8192, 8192)
        draw_list = imgui.get_window_draw_list()
        draw_list.add_rect_filled(x0, y0, x1, y1, imgui.get_color_u32_rgba(*color), rounding, 15 if rounding else 0)
        yield


def circle(cx, cy, radius, color, thickness=1, num_segments=16, tf=None):
    """ Circle specified by its center and radius. """
    while(True):
        if tf is not None:
            assert np.allclose(tf.c2s[0,0], tf.c2s[1,1])
            [cx, cy], radius = np.matmul(tf.c2s, [cx, cy, 1]), radius * tf.c2s[0,0]
        draw_list = imgui.get_window_draw_list()
        draw_list.add_circle(cx, cy, radius, imgui.get_color_u32_rgba(*color), num_segments=num_segments, thickness=thickness)
        yield


def polyline(points, color, closed=False, thickness=1, tf=None):
    """ Polygonal line or a closed polygon. """
    while(True):
        if tf is not None:
            points = [list(np.matmul(tf.c2s, [x, y, 1])) for x, y in points]
        draw_list = imgui.get_window_draw_list()
        draw_list.add_polyline(points, imgui.get_color_u32_rgba(*color), closed, thickness)
        yield


def text(x, y, color, string, tf=None):
    """ Text, using the default font and font size.

    This is a raw drawing function. Use `concur.widgets.text` instead if you want a text widget.
    """
    while(True):
        if tf is not None:
            x, y = np.matmul(tf.c2s, [x, y, 1])
        # Text was hanging the application if too far away
        if -8192 < x < 8192 and -8192 < y < 8192:
            draw_list = imgui.get_window_draw_list()
            draw_list.add_text(x, y, imgui.get_color_u32_rgba(*color), string)
        yield


def image(tex_id, w, h, tf):
    """ Draw an image with given width and height.

    This is a raw drawing function. Use `concur.extra_widgets.image.image` instead if you want an image widget.
    """
    while True:
        draw_list = imgui.get_window_draw_list()
        l, t, r, b = tf.view_s
        a_s = tf.view_s[:2]
        b_s = tf.view_s[2:]
        a_i = tf.view_i[0] / w, tf.view_i[1] / h
        b_i = tf.view_i[2] / w, tf.view_i[3] / h
        draw_list.add_image(tex_id, tuple(a_s), tuple(b_s), tuple(a_i), tuple(b_i))
        yield
