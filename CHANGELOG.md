
## 0.7.0 (planned release - master branch)

**Breaking Changes**

* [x] Change colored widgets `text_colored` and `color_button` to use the same color spec as the draw functions.
* [x] Rename `key_pressed` to `key_press`
* [x] Remove the name parameter from `mouse_click`.
* [x] Remove `TF.hovered`. Left mouse click & drag is now handled by the `pan_zoom` object.
* [x] Add left mouse interaction support to `image` and `frame`. New arguments `drag_tag` and `down_tag`, and `hover_tag`.
  - `pan_zoom.is_hovered` is no longer present.
  - `image` event handling was substantially reworked. Starting the drag outside image window no longer triggers panning.
* [ ] Make `polylines` handle a color list
* [x] `key_press` now respects local keyboard layout

**Other changes**

* add `TF.inv_transform` to tranasform from screen-space to content-space
* Make `scatter` also work with empty one-dimensional arrays
* Add an `invisible_button`, and an `image_button`
* Add `selectable` text
* Enable empty polylines
* Add `drag_int2`, `drag_int3`, and `drag_int4` widgets
* Add modifier key support to `key_press`
* Add `main_menu_bar`, `menu`, and `menu_item`


## 0.6.4

* Fix a bug where long polylines were sometimes corrupted (use-after-free).

## 0.6.3

* Move the documentation and homepage to a [separate repository](https://github.com/potocpav/python-concur-docs)

## 0.6.2

* Implement the square marker `'.'` for scatter plot.
* Implement `draw.polygon` and `draw.polygons` - filled convex polygons.

## 0.6.1

* Add `concur.widgets.mouse_click` widget, which returns mouse position on click
* Add `c.quick_*` functions for quick asynchronous plotting without worrying about the threading and event details
* Add a `fps` argument to `c.main`
    - this is breaking if screencast arguments were used positionally.
* Flexible [color specification](https://potocpav.github.io/python-concur-docs/master/draw.html) including [xkcd strings](https://xkcd.com/color/rgb/). Colors like `(0,1,1)`, `'dark red'`, `('blue', 0.5)`, or `0xffaa0000` are now possible.

## 0.6.0

**Breaking Changes**

* Change the argument order for `c.draw.text` from `(x, y, color, text)` to `(text, x, y, color)`.

**Other Changes**

* Improve frame tick labels
* Add this changelog
* Add `c.draw.polylines` for optimized multiple-polyline rendering. It is possible to draw ~100k lines in 60 FPS using this function (instead of ~500 lines). Using this function, it was possible to implement:
    * `c.draw.ellipses` for optimized multiple ellipse drawing
    * `c.draw.rects` for optimized multiple rectangle drawing
    * `c.draw.scatter` for scatter plots with fancy markers
* Add experimental benchmarking setup
