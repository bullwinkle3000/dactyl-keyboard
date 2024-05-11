import cadquery as cq
from scipy.spatial import ConvexHull as sphull
import numpy as np
import os

debug_trace = False


def wp(orient="XY"):
    return cq.Workplane(orient)


def debugprint(info):
    if debug_trace:
        print(info)


def box(width, height, depth):
    return cq.Workplane("XY").box(width, height, depth)


def cylinder(radius, height, segments=100):
    shape = cq.Workplane("XY").union(cq.Solid.makeCylinder(radius=radius, height=height))
    shape = translate(shape, (0, 0, -height/2))
    return shape


def sphere(radius):
    return cq.Workplane('XY').union(cq.Solid.makeSphere(radius))


def cone(r1, r2, height):
    return cq.Workplane('XY').union(
        cq.Solid.makeCone(radius1=r1, radius2=r2, height=height))


def rotate(shape, angle):
    origin = (0, 0, 0)
    shape = shape.rotate(axisStartPoint=origin, axisEndPoint=(1, 0, 0), angleDegrees=angle[0])
    shape = shape.rotate(axisStartPoint=origin, axisEndPoint=(0, 1, 0), angleDegrees=angle[1])
    shape = shape.rotate(axisStartPoint=origin, axisEndPoint=(0, 0, 1), angleDegrees=angle[2])
    return shape


def translate(shape, vector):
    return shape.translate(tuple(vector))


def mirror(shape, plane=None):
    debugprint('mirror()')
    return shape.mirror(mirrorPlane=plane)


def union(shapes):
    debugprint('union()')
    shape = None
    for item in shapes:
        if shape is None:
            shape = item
        else:
            shape = shape.union(item)
    return shape


def add(shapes):
    debugprint('union()')
    shape = None
    for item in shapes:
        if shape is None:
            shape = item
        else:
            shape = shape.add(item)
    return shape


def difference(shape, shapes):
    debugprint('difference()')
    for item in shapes:
        shape = shape.cut(item)
    return shape


def intersect(shape1, shape2):
    return shape1.intersect(shape2)


def face_from_points(points):
    # debugprint('face_from_points()')
    edges = []
    num_pnts = len(points)
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % num_pnts]
        edges.append(
            cq.Edge.makeLine(
                cq.Vector(p1[0], p1[1], p1[2]),
                cq.Vector(p2[0], p2[1], p2[2]),
            )
        )

    face = cq.Face.makeFromWires(cq.Wire.assembleEdges(edges))

    return face


def hull_from_points(points):
    # debugprint('hull_from_points()')
    hull_calc = sphull(points)
    n_faces = len(hull_calc.simplices)

    faces = []
    for i in range(n_faces):
        face_items = hull_calc.simplices[i]
        fpnts = []
        for item in face_items:
            fpnts.append(points[item])
        faces.append(face_from_points(fpnts))

    shape = cq.Solid.makeSolid(cq.Shell.makeShell(faces))
    shape = cq.Workplane('XY').union(shape)
    return shape


def hull_from_shapes(shapes, points=None):
    # debugprint('hull_from_shapes()')
    vertices = []
    for shape in shapes:
        verts = shape.vertices()
        for vert in verts.objects:
            vertices.append(np.array(vert.toTuple()))
    if points is not None:
        for point in points:
            vertices.append(np.array(point))

    shape = hull_from_points(vertices)
    return shape


def tess_hull(shapes, sl_tol=.5, sl_angTol=1):
    # debugprint('hull_from_shapes()')
    vertices = []
    solids = []
    for wp in shapes:
        for item in wp.solids().objects:
            solids.append(item)

    for shape in solids:
        verts = shape.tessellate(sl_tol, sl_angTol)[0]
        for vert in verts:
            vertices.append(np.array(vert.toTuple()))

    shape = hull_from_points(vertices)
    return shape


def triangle_hulls(shapes):
    debugprint('triangle_hulls()')
    hulls = [cq.Workplane('XY')]
    for i in range(len(shapes) - 2):
        hulls.append(hull_from_shapes(shapes[i: (i + 3)]))

    return union(hulls)


def bottom_hull(p, height=0.001):
    debugprint("bottom_hull()")
    shape = None
    for item in p:
        vertices = []
        # verts = item.faces('<Z').vertices()
        verts = item.faces().vertices()
        for vert in verts.objects:
            v0 = vert.toTuple()
            v1 = [v0[0], v0[1], -10]
            vertices.append(np.array(v0))
            vertices.append(np.array(v1))

        t_shape = hull_from_points(vertices)

        # t_shape = translate(t_shape, [0, 0, height / 2 - 10])

        if shape is None:
            shape = t_shape

        for shp in (*p, shape, t_shape):
            try:
                shp.vertices()
            except:
                0
        shape = union([shape, hull_from_shapes((shape, t_shape))])

    return shape


def polyline(point_list):
    return cq.Workplane('XY').polyline(point_list)


# def project_to_plate():
#     square = cq.Workplane('XY').rect(1000, 1000)
#     for wire in square.wires().objects:
#         plane = cq.Workplane('XY').add(cq.Face.makeFromWires(wire))


def extrude_poly(outer_poly, inner_polys=None, height=1):  # vector=(0,0,1)):
    outer_wires = cq.Wire.assembleEdges(outer_poly.edges().objects)
    inner_wires = []
    if inner_polys is not None:
        for item in inner_polys:
            inner_wires.append(cq.Wire.assembleEdges(item.edges().objects))

    return cq.Workplane('XY').add(
        cq.Solid.extrudeLinear(outerWire=outer_wires, innerWires=inner_wires, vecNormal=cq.Vector(0, 0, height)))


def soften(shape, mm=0.5):
    return shape.edges().fillet(mm)


def import_file(fname, convexity=None):
    print("IMPORTING FROM {}".format(fname))
    return cq.Workplane('XY').add(cq.importers.importShape(
        cq.exporters.ExportTypes.STEP,
        fname + ".step"))

def export_stl(shape, fname):
    print("EXPORTING STL TO {}".format(fname))
    cq.exporters.export(shape, fname=fname + "_cadquery.stl", exportType="STL")

def export_file(shape, fname):
    print("EXPORTING TO {}".format(fname))
    cq.exporters.export(w=shape, fname=fname + ".step",
                        exportType='STEP')

    export_stl(shape, fname)

puck_height = 3
puck_r = 41.1 / 2
base_top_r = puck_r + 2
base_bottom_r = base_top_r + 5
base_z_offset = 2
base_height = puck_height + base_z_offset
hole_dist = 38.1 / 2


def get_puck_base():
    # main_puck = wp().cylinder(puck_height + 1, puck_r).translate((-65, 0, (puck_height / 2) - 2))
    base_bottom = cq.Sketch().circle(base_bottom_r)
    base_top = cq.Sketch().circle(base_top_r)
    puck_base = wp().placeSketch(base_bottom, base_top.moved(cq.Location(cq.Vector(0, 0, base_height)))).loft()
    # puck_base = puck_base.translate((-65, 0, (base_height / 2) - 2))

    # holes = [
    #     [1, 0],
    #     [0, 1],
    #     [-1, 0],
    #     [0, -1]
    # ]
    #
    # hole_shapes = []
    # for hole in holes:
    #     hole_shapes.append(wp().cylinder(30, 1.55).translate((hole[0] * hole_dist, hole[1] * hole_dist, base_height)))
    #
    # puck_base = difference(puck_base, hole_shapes)

    return puck_base


def export_dxf(shape, fname):
    print("EXPORTING TO {}".format(fname))
    cq.exporters.export(w=shape, fname=fname + ".dxf",
                        exportType='DXF')

def mount_plate():
    height = 7.0
    result = (
        wp()
        .circle(20)
        .workplane(offset=height)
        .circle(12)
        .loft(combine=True)
    )
    os.path.abspath(os.path.join(r"src", "parts"))

    screw = cq.importers.importStep(os.path.abspath(os.path.join(r"src", "parts", "quarter_inch_screw.step"))).translate([0, 0, -8])

    return result.cut(screw)  # .translate([0, 0, height / 2.0])

def blockerize(shape):
    #####
    # Inputs
    ######
    lbumps = 40  # number of bumps long
    wbumps = 40  # number of bumps wide
    thin = True  # True for thin, False for thick

    #
    # Lego Brick Constants-- these make a Lego brick a Lego :)
    #
    pitch = 8.0
    clearance = 1
    bumpDiam = 4.85
    bumpHeight = 1.8
    if thin:
        height = 3.2
    else:
        height = 9.6

    t = (pitch - (2 * clearance) - bumpDiam) / 2.0
    postDiam = 6.5  # pitch  t  # works out to 6.5
    total_length = lbumps * pitch - 2.0 * clearance
    total_width = wbumps * pitch - 2.0 * clearance

    # make the base
    # s = cq.Workplane("XY").box(total_length, total_width, height)

    # shell inwards not outwards
    s = shape.faces("<Z").shell(-2.5 * t)

    # make the bumps on the top
    s = (s.faces(">Z").workplane().
         rarray(pitch, pitch, lbumps, wbumps, True).circle(bumpDiam / 2.0)
         .extrude(bumpHeight))

    # add posts on the bottom. posts are different diameter depending on geometry
    # solid studs for 1 bump, tubes for multiple, none for 1x1
    tmp = s.faces("<Z").workplane(invert=True)

    if lbumps > 1 and wbumps > 1:
        tmp = (tmp.rarray(pitch, pitch, lbumps - 1, wbumps - 1, center=True).
               circle(postDiam / 2.0).circle(bumpDiam / 2.0).extrude(height - t))
    elif lbumps > 1:
        tmp = (tmp.rarray(pitch, pitch, lbumps - 1, 1, center=True).
               circle(t).extrude(height - t))
    elif wbumps > 1:
        tmp = (tmp.rarray(pitch, pitch, 1, wbumps - 1, center=True).
               circle(t).extrude(height - t))
    else:
        tmp = s

    return intersect(shape, tmp)

# generate a cutter to exact size/shape of an M3 4mm x 4mm brass insert
# size is scaled a bit for non-resin prints, so heat-set works
def insert_cutter(radii=(2.35, 2.0), heights=(2.8, 1.5), scale_by=1):
    if len(radii) != len(heights):
        raise Exception("radii and heights collections must have equal length")

    top_radius = 4.7 / 2
    top_height = 2.8
    medium_radius = 4.0 / 2
    medium_height = 1.5
    # medium2_radius = 5.1 / 2
    # medium2_height = 0.8
    # bottom_radius = 4.85 / 2
    # bottom_height = 1.6

    total_height = sum(heights) + 0.3  # add 0.3 for a titch extra

    half_height = total_height / 2
    offset = half_height
    cyl = None
    for i in range(len(radii)):
        radius = radii[i] * scale_by
        height = heights[i]
        offset -= height / 2
        new_cyl = cq.Workplane('XY').cylinder(height, radius).translate((0, 0, offset))
        if cyl is None:
            cyl = new_cyl
        else:
            cyl = cyl.union(new_cyl)
        offset -= height / 2

    return cyl

pcb_v1 = {
    "l": 52.2,
    "w": 34.0,
    "h1": 1.15,
    "h2": 4.3,
    "h3": 9.5,
    "offsets": {
        "l": 1,
        "w": 1,
        "h": 2
    },
    "port_cuts": [
        {
            "rot": [0, 0, 0],
            "offset": [5, 17, 4],
            "w": 10,
            "h": 4,
            "l": 15
        },
        {
            "rot": [0, 0, 0],
            "offset": [25, 17, 0],
            "w": 3.2,
            "h": 10,
            "l": 15
        }
    ]
}

pcb_v2 = {
    "l": 52.2,
    "w": 33.0,
    "h": 1.15,
    "h2": -2.2,
    "h3": 4.4,
    "offsets": {
        "l": 0,
        "w": 0,
        "h": 3
    },
    "port_cuts": [
        {
            "rot": [0, 0, 0],
            "relative_to": "h",
            "offset": [15.25, 17, -6],
            "w": 11,
            "h": 4.5,
            "l": 25
        },
        {
            "rot": [0, 0, 0],
            "offset": [15.25, 17, 0.25],
            "w": 11,
            "h": 4.5,
            "l": 40
        },
        {
            "rot": [0, 0, 0],
            "offset": [15.25, 17, -3],
            "w": 11,
            "h": 10,
            "l": 40
        },
    ]
}


def build_holder(pcb):
    pcb_box = wp().box(pcb["w"], pcb["l"], pcb["h"])

    left_x = -pcb["w"] / 2
    back_y = pcb["l"] / 2
    h_off = pcb["offsets"]["h"]

    for data in pcb["port_cuts"]:
        off = data["offset"]
        port = wp().box(data["w"], data["l"], data["h"]).translate(
            [left_x + off[0] + data["w"] / 2, back_y, off[2] + data["h"] / 2 + pcb["h"] / 2])
        port = port.edges("|Y").fillet(1)
        pcb_box = pcb_box.union(port)

    base = wp().box(pcb["w"] + 3.5, pcb["l"] + 3.5, 1).translate([0, 0, -1])
    base = base.edges("|Z and >Y").chamfer(2.5)
    base = base.cut(wp().box(pcb["w"] + 0.5, pcb["l"] + 0.5, 2).translate([0, 0, 1]))
    pin_row1 = wp().box(3, 49, 3).translate([left_x + 15.25 + 9 + 5.5, -1, 0])
    pin_row2 = wp().box(3, 49, 3).translate([left_x + 15.25 - 9 + 5.5, -1, 0])

    # base = base.cut(pin_row2).cut(pin_row1)

    base = base.translate([0, 0, -7.5])
    holder_hole_width = 29.2
    holder_hole_height = 16.5
    # front wall

    wall = wp().box(holder_hole_width + 8, 9, holder_hole_height + 1).translate([0, back_y + 4, -0.25])
    wall = wall.edges(">Z and |Y").fillet(3)
    groove_neg = wp().box(holder_hole_width + 10, 7, holder_hole_height + 11).translate([0, back_y + 3, 2.25])
    groove_neg = groove_neg.cut(
        wp().box(holder_hole_width, 30, holder_hole_height + 1).translate([0, back_y + 3, -2.3]))
    inset = wp().box(holder_hole_width - 2, 10, holder_hole_height + 1).translate([0, back_y + 7, -2.75])
    inset = inset.edges(">Z and |Y").fillet(2)
    wall = wall.cut(inset)
    wall = wall.cut(groove_neg)
    pcb_box = pcb_box.translate([0, 0, -2])
    posts1 = wp().box(3, pcb["l"], 5.5).translate([-pcb["w"] / 2 + 1, 0, -5.8])
    posts2 = wp().box(3, pcb["l"], 5.5).translate([pcb["w"] / 2 - 1, 0, -5.8])
    rear_guard = wp().box(pcb["w"], 3.0, 7.5).translate([0, -pcb["l"] / 2 - 1, -4.8])
    wall = wall.cut(pcb_box)
    base = base.union(posts1).union(posts2).union(rear_guard)
    wall = wall.union(base)

    return wall


def get_holder():
    return build_holder(pcb_v2)


def puck_plate():
    offset = 19.55
    border = 5
    border_half = border / 2
    width = offset * 5
    height = offset * 4

    # plate = box(width, height, 2)

    plate_bottom = wp().sketch().rect(width, height).edges().fillet(15)
    plate = plate_bottom.workplane(offset=3).sketch().rect(width / 3, height / 3).fillet(5).loft()

    holes = [
        [offset, 0, 0],
        [0, offset, 0],
        [-offset, 0, 0],
        [0, -offset, 0]
    ]

    plate = plate.edges("|Z").fillet(15)
    # plate = plate.edges(">Y").chamfer(1)
    plate = plate.faces(">Z").workplane().rect(38.1, 38.1, forConstruction=True).vertices().cboreHole(2.2, 3, 1.5, 3)
    return plate
