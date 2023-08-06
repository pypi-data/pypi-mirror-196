# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)

from copy import copy

import scipp as sc

from plopp.backends.pythreejs.canvas import Canvas
from plopp.backends.pythreejs.outline import Outline


def _make_limits():
    return (sc.array(dims=['x'], values=[1.5, 3.5],
                     unit='m'), sc.array(dims=['y'], values=[-5.0, 5.0], unit='m'),
            sc.array(dims=['z'], values=[-0.1, 17.0], unit='m'))


def test_creation():
    canvas = Canvas(figsize=(700, 450))
    assert canvas.renderer.width == 700
    assert canvas.renderer.height == 450
    assert all(
        [canvas.camera, canvas.scene, canvas.controls, canvas.renderer, canvas.axes_3d])
    assert canvas.outline is None


def test_make_outline():
    canvas = Canvas()
    assert canvas.outline is None
    canvas.make_outline(limits=_make_limits())
    assert isinstance(canvas.outline, Outline)
    assert canvas.outline.visible


def test_camera_home():
    canvas = Canvas()
    canvas._update_camera(limits=_make_limits())
    original = copy(canvas.camera.position)
    canvas.camera.position = [10, 20, 30]
    canvas.home()
    assert canvas.camera.position == original


def test_camera_x():
    canvas = Canvas()
    canvas._update_camera(limits=_make_limits())
    center = copy(canvas.camera_backup["center"])
    canvas.camera.position = [10, 20, 30]
    canvas.camera_x_normal()
    assert canvas.camera.position[0] < center[0]
    assert canvas.camera.position[1] == center[1]
    assert canvas.camera.position[2] == center[2]
    canvas.camera_x_normal()
    assert canvas.camera.position[0] > center[0]
    assert canvas.camera.position[1] == center[1]
    assert canvas.camera.position[2] == center[2]


def test_camera_y():
    canvas = Canvas()
    canvas._update_camera(limits=_make_limits())
    center = copy(canvas.camera_backup["center"])
    canvas.camera.position = [10, 20, 30]
    canvas.camera_y_normal()
    assert canvas.camera.position[0] == center[0]
    assert canvas.camera.position[1] < center[1]
    assert canvas.camera.position[2] == center[2]
    canvas.camera_y_normal()
    assert canvas.camera.position[0] == center[0]
    assert canvas.camera.position[1] > center[1]
    assert canvas.camera.position[2] == center[2]


def test_camera_z():
    canvas = Canvas()
    canvas._update_camera(limits=_make_limits())
    center = copy(canvas.camera_backup["center"])
    canvas.camera.position = [10, 20, 30]
    canvas.camera_z_normal()
    assert canvas.camera.position[0] == center[0]
    assert canvas.camera.position[1] == center[1]
    assert canvas.camera.position[2] < center[2]
    canvas.camera_z_normal()
    assert canvas.camera.position[0] == center[0]
    assert canvas.camera.position[1] == center[1]
    assert canvas.camera.position[2] > center[2]


def test_toggle_axes_3d():
    canvas = Canvas()
    assert canvas.axes_3d.visible
    canvas.toggle_axes3d()
    assert not canvas.axes_3d.visible
    canvas.toggle_axes3d()
    assert canvas.axes_3d.visible


def test_toggle_outline():
    canvas = Canvas()
    canvas.make_outline(limits=_make_limits())
    assert canvas.outline.visible
    canvas.toggle_outline()
    assert not canvas.outline.visible
    canvas.toggle_outline()
    assert canvas.outline.visible


def test_creation_with_title():
    text = 'My title'
    canvas = Canvas(figsize=(700, 450), title=text)
    assert canvas.title == text
    html = '<i>My</i> <b>title</b>'
    canvas = Canvas(figsize=(700, 450), title=html)
    assert canvas.title == html
