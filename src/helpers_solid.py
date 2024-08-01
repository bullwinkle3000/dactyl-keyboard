import solid as sl
from subprocess import run
import os

debug_trace = False

def debugprint(info):
    if debug_trace:
        print(info)

def box(width, height, depth):
    return sl.cube([width, height, depth], center=True)


def cylinder(radius, height, segments=100):
    return sl.cylinder(r=radius, h=height, segments=segments, center=True)


def sphere(radius):
    return sl.sphere(radius)


def cone(r1, r2, height):
    return sl.cylinder(r1=r1, r2=r2, h=height, center=True)  # , center=True)


def solidify(shape):
    return shape


def rotate(shape, angle):
    return sl.rotate(angle)(shape)


def translate(shape, vector):
    return sl.translate(tuple(vector))(shape)


def mirror(shape, plane=None):
    debugprint('mirror()')
    planes = {
        'XY': [0, 0, 1],
        'YX': [0, 0, -1],
        'XZ': [0, 1, 0],
        'ZX': [0, -1, 0],
        'YZ': [1, 0, 0],
        'ZY': [-1, 0, 0],
    }
    return sl.mirror(planes[plane])(shape)


def union(shapes):
    debugprint('union()')
    shape = None
    for item in shapes:
        if shape is None:
            shape = item
        else:
            shape += item
    return shape


def add(shapes):
    debugprint('union()')
    shape = None
    for item in shapes:
        if shape is None:
            shape = item
        else:
            shape += item
    return shape


def difference(shape, shapes):
    debugprint('difference()')
    for item in shapes:
        shape -= item
    return shape


def intersect(shape1, shape2):
    return sl.intersection()(shape1, shape2)


def hull_from_points(points):
    return sl.hull()(*points)


def hull_from_shapes(shapes, points=None):
    hs = []
    if points is not None:
        hs.extend(points)
    if shapes is not None:
        hs.extend(shapes)
    return sl.hull()(*hs)


def tess_hull(shapes, sl_tol=.5, sl_angTol=1):
    return sl.hull()(*shapes)


def triangle_hulls(shapes):
    debugprint('triangle_hulls()')
    hulls = []
    for i in range(len(shapes) - 2):
        hulls.append(hull_from_shapes(shapes[i: (i + 3)]))

    return union(hulls)



def bottom_hull(p, height=0.001):
    debugprint("bottom_hull()")
    shape = None
    for item in p:
        proj = sl.projection()(p)
        t_shape = sl.linear_extrude(height=height, twist=0, convexity=0, center=True)(
            proj
        )
        t_shape = sl.translate([0, 0, height / 2 - 10])(t_shape)
        if shape is None:
            shape = t_shape
        shape = sl.hull()(p, shape, t_shape)
    return shape

def polyline(point_list):
    return sl.polygon(point_list)


# def project_to_plate():
#     square = cq.Workplane('XY').rect(1000, 1000)
#     for wire in square.wires().objects:
#         plane = cq.Workplane('XY').add(cq.Face.makeFromWires(wire))

def extrude_poly(outer_poly, inner_polys=None, height=1):
    if inner_polys is not None:
        return sl.linear_extrude(height=height, twist=0, convexity=0, center=True)(outer_poly, *inner_polys)
    else:
        return sl.linear_extrude(height=height, twist=0, convexity=0, center=True)(outer_poly)


def import_file(fname, convexity=4):
    full_name = fname + r".stl"
    print("IMPORTING FROM {}".format(full_name))

    return sl.import_stl(full_name, convexity=convexity)


def export_file(shape, fname):
    print("EXPORTING TO {}".format(fname))
    sl.scad_render_to_file(shape, fname + ".scad")

def export_stl(shape, fname):
    print("EXPORTING STL TO {}".format(fname))
    run(["C:\\Program Files\\OpenSCAD\\openscad.com", "-o",  fname + "_openscad.stl", fname + ".scad"])


def export_dxf(shape, fname):
    print("NO DXF EXPORT FOR SOLID".format(fname))
    pass


def render_samples(override_name, num_cols, dir_path):
    dist = (num_cols * 75)
    x_off = [
        0, 0, 0, 0, 0, 25, 15, 0
    ]
    angles = [
        0, 0, 0, 0, 0, 20, 30, 32
    ]

    for filename in os.listdir(dir_path):
        if "TOP.scad" in filename:
            x_mult = -1 if "RIGHT" in filename else 1
            out_file = filename.replace(".scad", ".png")
            cmd_args = [
                '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD',
                f"/Users/andrew/OneDrive/Sales/Models/Customers/{override_name}/{filename}",
                '-o',
                f"/Users/andrew/OneDrive/Sales/Models/Customers/{override_name}/{out_file}",
                f"--camera={x_off[num_cols] * x_mult},-100,200,{angles[num_cols]},0,0,{dist}",
                # '--camera=0,0.91,-10.7,0,0,0,40',
                '--preview',
                # '--viewall',
                # '--autocenter',
                '--enable=manifold',
            ]
            run(cmd_args)
