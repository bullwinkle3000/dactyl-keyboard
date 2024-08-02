import numpy as np
from scipy.spatial.transform import Rotation as R


def deg2rad(degrees: float) -> float:
    return degrees * np.pi / 180


def rad2deg(rad: float) -> float:
    return rad * 180 / np.pi


def to_degrees(rots):
    return [rad2deg(a) for a in rots]


def to_radians(rots):
    return [deg2rad(a) for a in rots]


def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def rotate_around_x2(position, around_point, angle):
    dist = distance(position, around_point)
    return [position[0], position[1] - (dist * np.sin(angle)), position[2] - (dist * np.cos(angle))]


def rotate_around_y2(position, around_point, angle):
    dist = distance(position, around_point)
    return [position[0] - (dist * np.sin(angle)), 0, position[2] - (dist * np.cos(angle))]


def rotate_around_yz(position, around_point, angle):
    dist = distance(position, around_point)
    return [position[0] - (dist * np.sin(angle)), position[1] - (dist * np.cos(angle)), position[2]]


def get_rotation_transform(angles):
    rads = to_radians(angles)
    rx = R.from_euler('x', rads[0])
    ry = R.from_euler('y', rads[1])
    rz = R.from_euler('z', rads[2])
    return rx * ry * rz


def apply_rotation_to_point(angles, point):
    rads = to_radians(angles)
    rx = R.from_euler('x', rads[0]).apply(point)
    ry = R.from_euler('y', rads[1]).apply(point)
    rz = R.from_euler('z', rads[2]).apply(point)
    return rx * ry * rz


def rotate_point_around(position, angles):
    r_result = get_rotation_transform(angles)
    return r_result.apply(position)


def rotate_around_x(position, angle):
    # debugprint('rotate_around_x()')
    t_matrix = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ]
    )
    return np.matmul(t_matrix, position)


def rotate_around_y(position, angle):
    # debugprint('rotate_around_y()')
    t_matrix = np.array(
        [
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)],
        ]
    )
    return np.matmul(t_matrix, position)


def rotate_around_z(position, angle):
    # debugprint('rotate_around_y()')
    t_matrix = np.array(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )
    return np.matmul(t_matrix, position)


def avg(*argv):
    x = 0
    y = 0
    z = 0
    l = len(argv)
    for sublist in argv:
        x += sublist[0]
        y += sublist[1]
        z += sublist[2]

    return [x / l, y / l, z / l]


def rotate_rad(start, rotate_by):
    result = rotate_around_x(start, rotate_by[0])
    result = rotate_around_y(result, rotate_by[1])
    result = rotate_around_z(result, rotate_by[2])
    return result


def rotate_deg(start, rotate_by):
    return [x for x in rotate_rad(start, to_radians(rotate_by))]


def add_translate(shape, xyz):
    vals = []
    for i in range(len(shape)):
        vals.append(shape[i] + xyz[i])
    return vals
