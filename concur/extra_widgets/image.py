""" Scrollable, zoomable image widget with overlay support. """


import copy

import numpy as np
import imgui
from concur.integrations import replace_texture, texture
from concur.widgets import child
from concur.draw import image as raw_image
from concur.extra_widgets.pan_zoom import PanZoom, pan_zoom
from concur.core import orr, optional


def image(name, state, width=None, height=None, content_gen=None):
    """ The image widget.

    `state` is an instance of `concur.extra_widgets.image.Image`. Width and
    height are optional; if not specified, the widget stretches to fill
    the parent element. Returns a modified `Image` object on user interaction.

    `content_gen` is a function that takes as an argument a transformation
    object `concur.extra_widgets.pan_zoom.TF`, and returns a widget that will be displayed as image
    overlay. Any events fired by the overlay widget are passed through unchanged.

    The transformation object can be used to display overlay on the image, positioned
    and scaled appropriately. It can be used explicitly, or passed as the `tf` argument to any
    Geometrical objects. See the [image example](https://github.com/potocpav/python-concur/blob/master/examples/image.py) for example usage.
    """
    while True:
        _, (st, child_event) = yield from pan_zoom(name, state.pan_zoom, width, height, content_gen=lambda tf: orr(
            [ raw_image(state.tex_id, state.tex_w, state.tex_h, tf)
            , optional(content_gen is not None, content_gen, tf)
            ]))
        if st is not None:
            state.pan_zoom = st
            return name, state
        else:
            return child_event
        yield


class Image(object):
    """ Image state, containing pan and zoom information, and texture data. """
    def __init__(self, image=None):
        """ `image` must be something convertible to `numpy.array`: greyscale or RGB, channel is
        in the last dimension.
        """
        # TODO: remove this hack with last_{w,h}; create a more principled way of changing content size
        self.last_w, self.last_h = None, None
        self.tex_id = None
        self.pan_zoom = PanZoom((0, 0), (1, 1))
        self.change_image(image)

    def change_image(self, image):
        """ Change the image for a different one. `image` must be None, or something convertible to
        `numpy.array` in greyscale or RGB format, channel is in the last dimension. If None, a black placeholder
        image is displayed.
        """
        if image is None:
            self.tex_id = replace_texture(np.zeros((1,1,3)), self.tex_id)
            self.tex_w, self.tex_h = 1, 1
        else:
            image = np.array(image)
            self.tex_id = replace_texture(image, self.tex_id)
            self.tex_w, self.tex_h = image.shape[1], image.shape[0]

            if self.last_w != self.tex_w or self.last_h != self.tex_h:
                self.last_w, self.last_h = self.tex_w, self.tex_h
                self.pan_zoom.reset_view((0,0), (self.tex_w, self.tex_h))

    def reset_view(self):
        """ Reset view so that the whole image fits into the widget. """
        return self.pan_zoom.reset_view()
