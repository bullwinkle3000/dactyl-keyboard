from helpers_cadquery import *
import os.path as path
import numpy as np

ball_diam = 34  # ball diameter
ball_space = 2.0  # additional room around ball in socket, 1mm


def get_ball(with_space: False):
    diam = ball_diam
    if with_space:
        diam += ball_space
    return sphere(diam / 2)


def gen_holder():
    # PMW3360 dimensions
    # 28mm x 21mm
    l = 28  # not used for now, fudged with base_shape build
    w = 24
    h = 5.9

    # 24mm between screw centers
    screw_dist = 24
    # Screw holes 2.44mm, 2.2mm for snug tapped fit
    screw_hole_d = 2.2

    # circles at either side
    cyl1 = translate(cylinder(w / 2, h, 100), (0, 5, 0))
    cyl2 = translate(cylinder(w / 2, h, 100), (0, -5, 0))

    plate = box(w, 10, h)
    # tape those bits together
    base_shape = union([plate, cyl1, cyl2])

    # Ball with 2mm space extra diameter for socket
    ball = translate(rotate(get_ball(True), (180, 0, 0)), (0, 0, 15))

    # Screw holes with a bit of extra height to subtract cleanly
    # May need to be offset by one, as per the bottom hole...?
    screw1 = translate(cylinder(screw_hole_d / 2, h + 1, 20), (0, screw_dist / 2, 0))
    screw2 = translate(cylinder(screw_hole_d / 2, h + 1, 20), (0, -(screw_dist / 2), 0))

    # Attempt at bottom hole, numbers mostly fudged but seems in ballpark
    bottom_hole = union([translate(box(4.5, 4, 6), (0, -2, 0)), translate(cylinder(2.25, 6, 40), (0, 0, 0))])

    final = translate(difference(base_shape, [ball, screw1, screw2, bottom_hole]), (0, 0, -15))

    return final


def coords(angle, dist):
    x = np.sin(angle) * dist
    y = np.cos(angle) * dist
    return x, y


def gen_socket_shape(radius, wall):
    diam = radius * 2
    ball = sphere(radius)
    socket_base = difference(ball, [translate(box(diam + 1, diam + 1, diam), (0, 0, diam / 2))])
    top_cylinder = translate(difference(cylinder(radius, 4), [cylinder(radius - wall, 6)]), (0, 0, 2))
    socket_base = union([socket_base, top_cylinder])

    return socket_base


def socket_bearing_fin(outer_r, outer_depth, axle_r, axle_depth, cut_offset, groove):
    pi3 = (np.pi / 2)
    l = 20

    x, y = coords(0, l)
    t1 = translate(cylinder(outer_r, outer_depth), (x, y, 0))

    x, y = coords(pi3, l)
    t2 = translate(cylinder(outer_r, outer_depth), (x, y, 0))

    x, y = coords(pi3 * 2, l)
    t3 = translate(cylinder(outer_r, outer_depth), (x, y, 0))

    big_triangle = hull_from_shapes([t1, t2, t3])

    x, y = coords(0, l)
    t4 = translate(cylinder(axle_r, axle_depth), (x, y, 0))

    x, y = coords(pi3, l)
    t5 = translate(cylinder(axle_r, axle_depth), (x, y, 0))

    x, y = coords(pi3 * 2, l)
    t6 = translate(cylinder(axle_r, axle_depth), (x, y, 0))

    if groove:
        t6 = t4

    axle_shaft = hull_from_shapes([t4, t5, t6])
    base_shape = union([big_triangle, axle_shaft])
    cutter = rotate(translate(box(80, 80, 20), (0, cut_offset, 0)), (0, 0, 15))

    return rotate(difference(base_shape, [cutter]), (0, -90, 0))


def track_outer():
    wall = 4
    ball = gen_socket_shape((ball_diam + wall) / 2, wall / 2)
    outer_radius = 4
    outer_width = 5
    axle_radius = 3
    axle_width = 8
    base_fin = socket_bearing_fin(outer_radius, outer_width, axle_radius, axle_width, -22, False)
    offsets = (0, -2, -6)

    cutter1 = translate(base_fin, offsets)
    cutter2 = rotate(translate(base_fin, offsets), (0, 0, 120))
    cutter3 = rotate(translate(base_fin, offsets), (0, 0, 240))

    return union([ball, cutter1, cutter2, cutter3])


def track_cutter():
    wall = 4
    ball = gen_socket_shape(ball_diam / 2, wall / 2)
    outer_radius = 2.5
    outer_width = 3
    axle_radius = 1.5
    axle_width = 6.5
    base_fin = socket_bearing_fin(outer_radius, outer_width, axle_radius, axle_width, -25, True)
    offsets = (0, -2, -6)

    cutter1 = translate(base_fin, offsets)
    cutter2 = rotate(translate(base_fin, offsets), (0, 0, 120))
    cutter3 = rotate(translate(base_fin, offsets), (0, 0, 240))

    return union([ball, cutter1, cutter2, cutter3])


def gen_track_socket():
    return difference(track_outer(), [track_cutter()])


# cutter_fin = socket_bearing_fin(7, 3, 2, 7, -35)
# main_fin = socket_bearing_fin(10, 7, 5, 10, -25)

# result = difference(main_fin, [cutter_fin])
export_file(shape=gen_holder(), fname=path.join(".", "things", "gen_holder"))

