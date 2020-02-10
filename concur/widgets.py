""" A collection of widgets based off of ImGui.

By convention, all widgets take a string identifier as the first parameter, and return the `(identifier, value)` pair.
This is done to increase convenience, as Python syntax for mapping values is a bit busy.

Most widgets are just thin wrappers over [widgets in PyImGui](https://pyimgui.readthedocs.io/en/latest/reference/imgui.core.html).
If any widget from ImGui is not listed here, it is mostly trivial to add it. New widgets can be created by writing
generators, or by using helper functions `concur.core.interactive_elem` or `concur.core.lift` from `concur.core`.

Some widgets don't do any drawing and serve purely for control flow, or user interaction.

All of the functions in this module are re-exported in the root module for convenience.
"""


import numpy as np # for `transform`
from typing import Iterable, Any, Tuple
import imgui

from concur.core import orr, lift, Widget, interactive_elem


def orr_same_line(widgets):
    """ Use instead of `concur.core.orr` to layout child widgets horizontally instead of vertically. """
    def intersperse(delimiter, seq):
        """ https://stackoverflow.com/questions/5655708/python-most-elegant-way-to-intersperse-a-list-with-an-element """
        from itertools import chain, repeat
        return list(chain.from_iterable(zip(repeat(delimiter), seq)))[1:]

    def group(widget):
        return orr([lift(imgui.begin_group), widget, lift(imgui.end_group)])

    return orr(intersperse(same_line(), [group(w) for w in widgets]))


def window(title: str,
           widget: Widget,
           position: Tuple[int, int] = None,
           size: Tuple[int, int] = None,
           flags: int = 0) -> Widget:
    """ Create a window with a given `widget` inside.

    Window title must be unique. Contents are drawn only if the window is opened.
    """
    while True:
        if position is not None:
            imgui.set_next_window_position(*position)
        if size is not None:
            imgui.set_next_window_size(*size)
        expanded, opened = imgui.begin(title, flags=flags)
        try:
            if expanded and opened:
                next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.end()
        yield


def child(name, widget, width, height, border=False, flags=0):
    """ Create a sized box with a `widget` inside a window. """
    while True:
        imgui.begin_child(name, width, height, border, flags)
        try:
            next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.end_child()
        yield


def collapsing_header(text, widget, open=True):
    """Display a collapsible section header. It can be open or closed by default (parameter `open`).
    """
    while True:
        expanded, visible = imgui.collapsing_header(text, flags=open and imgui.TREE_NODE_DEFAULT_OPEN)
        try:
            if expanded:
                next(widget)
        except StopIteration as e:
            return e.value
        yield


def button(text, tag=None):
    """ Button. Returns `(text, value)` on click, or `(tag, value)` if tag is specified. """
    while not imgui.button(text):
        yield
    return tag if tag is not None else text, None


def color_button(text, color, tag=None):
    """ Colored button. Color is specified as a tuple (R,G,B,A), each in range 0..1.

    Returns `(text, value)` on click, or `(tag, value)` if tag is specified.
    """
    r, g, b, a = color
    while not imgui.color_button(text, r, g, b, a):
        yield
    return tag if tag is not None else text, None


def radio_button(text, active, tag=None):
    """ Radio button. Returns ``(text, value)`` on click. """
    while not imgui.radio_button(text, active):
        yield
    return (tag if tag is not None else text), None


def input_text(name, value, buffer_length, tag=None):
    """ Text input. """
    while True:
        changed, new_value = imgui.input_text(name, value, buffer_length)
        if changed:
            return (name if tag is None else tag), new_value
        else:
            yield


# NOTE: the key_pressed function require a forked version of ImGui:
# https://github.com/potocpav/pyimgui
#
# def key_pressed(name, key_index, repeat=True):
#     """ Invisible widget that waits for a given key to be pressed.
#
#     Key codes are specified by the integration layer, e.g. `glfw.KEY_A`.
#     """
#     while True:
#         if imgui.is_key_pressed(key_index, repeat):
#             return name, None
#         yield


def text(s):
    """ Passive text display widget. """
    return lift(imgui.text, s)

def text_colored(s, r, g, b, a=1.):
    """ Passive colored text display widget. """
    return lift(imgui.text_colored, s, r, g, b, a)

def test_window():
    """ ImGui test window with a multitude of widgets. """
    return lift(imgui.show_test_window)

def separator():
    """ Horizontal separator. """
    return lift(imgui.separator)

def spacing():
    """ Extra horizontal space. """
    return lift(imgui.spacing)

def same_line():
    """ Call between widgets to layout them horizontally.

    Consider using `concur.widgets.orr_same_line` instead.
    """
    return lift(imgui.same_line)

def checkbox(label, checked, *args, **kwargs):
    """ Two-state checkbox. """
    return interactive_elem(imgui.checkbox, label, checked, *args, **kwargs)

def drag_float(label, value, *args, **kwargs):
    """ Float selection widget without a slider. """
    return interactive_elem(imgui.drag_float, label, value, *args, **kwargs)

def drag_float2(label, values, *args, **kwargs):
    """ Float selection widget for selecting two `values`. """
    value0, value1 = values
    return interactive_elem(imgui.drag_float2, label, value0, value1, *args, **kwargs)

def drag_float3(label, values, *args, **kwargs):
    """ Float selection widget for selecting three `values`. """
    value0, value1, value2 = values
    return interactive_elem(imgui.drag_float3, label, value0, value1, value2, *args, **kwargs)

def drag_float4(label, values, *args, **kwargs):
    """ Float selection widget without a slider for selecting four `values`. """
    value0, value1, value2, value3 = values
    return interactive_elem(imgui.drag_float4, label, value0, value1, value2, value3, *args, **kwargs)

def input_float(label, value, *args, **kwargs):
    """ Float input widget. """
    return interactive_elem(imgui.input_float, label, value, *args, **kwargs)

def slider_int(label, value, min_value, max_value, *args, **kwargs):
    """ Int selection slider. """
    return interactive_elem(imgui.slider_int, label, value, min_value, max_value, *args, **kwargs)

def slider_float(label, value, min_value, max_value, *args, **kwargs):
    """ Float selection slider. """
    return interactive_elem(imgui.slider_float, label, value, min_value, max_value, *args, **kwargs)


def columns(elems, identifier=None, border=True, widths=[]):
    """ Table, using the imgui columns API.

    `elems` is a 2D array of widgets
    `widths` is a optional vector of column widths in pixels. May contain
    None values.
    """
    n_columns = len(elems[0])
    for e in elems:
        assert len(e) == n_columns
    accum = []
    accum.append(lift(imgui.columns, n_columns, identifier, border))
    for i, w in enumerate(widths):
        if w is not None:
            accum.append(lift(imgui.set_column_width, i, w))
    for row in elems:
        for widget in row:
            accum.append(widget)
            accum.append(lift(imgui.next_column))
    accum.append(lift(imgui.columns, 1))
    return orr(accum)


def transform(x, y, widget, tf=None):
    # TODO: move somewhere else
    """ Use `concur.extra_widgets.pan_zoom.TF` and a specified position `x, y` to transform a widget.

    Only widget position will be affected (not scaling), and it will be positioned so that its upper left corner
    is at `[x, y]`.
    """
    old_pos = imgui.get_cursor_screen_pos()
    if tf is not None:
        x, y = np.matmul(tf.c2s, [x, y, 1])
    while True:
        try:
            imgui.set_cursor_screen_pos((x, y))
            next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.set_cursor_screen_pos(old_pos)
        yield
