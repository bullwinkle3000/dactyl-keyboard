from common import combine

from geom import *
from geom import rotate_deg, add_translate


class Part(object):

    def __init__(self, part_id):
        self._rot_transform = None
        self._rot = [0, 0, 0]
        self.neighbors = {}
        self._pos = [0, 0, 0]
        self._d_vec = [0, 0, 0]
        self._id = part_id
        self._rot_transform = None
        self.width = 0
        self.height = 0
        self._origin = [0, 0, 0]

    def _update_d_vec(self):
        dist = distance([0, 0, 0], self._pos)
        self._d_vec = [d / dist for d in self._origin]

    def set_origin(self, new_origin):
        if len(new_origin) == 3:
            self._origin = new_origin
            self._update_d_vec()
        else:
            raise ValueError('Invalid pos')

    def _set_pos(self, new_pos):
        if len(new_pos) == 3:
            self._pos = new_pos
            self._update_d_vec()
        else:
            raise ValueError('Invalid pos')

    def _get_pos(self):
        return self._pos

    pos = property(fget=_get_pos, fset=_set_pos, doc='Get/Set position')

    def set_rot(self, new_rot):
        if len(new_rot) == 3:
            self._rot = new_rot
            self._rot_transform = get_rotation_transform(new_rot)
        else:
            raise ValueError('Invalid rot')

    def get_rot(self):
        return self._rot

    rot = property(fget=get_rot, fset=set_rot, doc="Get/Set rot")

    def update_rot_by(self, deltas):
        self.rot = ([self._rot[i] + deltas[i] for i in range(len(self._rot))])

    def get_id(self):
        return self._id

    def rotate_deg(self, rotate_by):
        self.pos = rotate_deg(self._pos, rotate_by)
        self.update_rot_by(rotate_by)
        return self.pos

    def rotate_rad(self, rotate_by):
        self.pos = rotate_rad(self._pos, rotate_by)
        self.update_rot_by([rad2deg(rotate_by[i]) for i in range(len(rotate_by))])
        return self.pos

    def translate(self, position):
        self.pos = add_translate(self.pos, position)
        return self.pos

    def offset_point(self, offsets):
        calc_offsets = rotate_rad(offsets, self.rot)
        return [calc_offsets[i] + self.pos[i] for i in range(len(self._pos))]

    def add_neighbor(self, neighbor, side):
        if side not in ["t", "r", "l", "b", "tr", "br", "tl", "bl"]:
            raise Exception("side value out of range")

        self.neighbors[side] = neighbor

    def get_neighbor(self, side):
        if side not in ["t", "r", "l", "b", "tr", "br", "tl", "bl"]:
            raise Exception("side value out of range")
        return self.neighbors[side]

    def _get_neighbors(self, ids):
        found = []
        for id in ids:
            key = self.get_neighbor(id)
            if key is not None and not key.is_none():
                found.append(key)

        return found

    def get_left_neighbors(self):
        return self._get_neighbors(["tl", "l", "bl"])

    def get_right_neighbors(self):
        return self._get_neighbors(["tr", "r", "br"])

    def get_top_neighbors(self):
        return self._get_neighbors(["tl", "t", "tr"])

    def get_bottom_neighbors(self):
        return self._get_neighbors(["bl", "b", "br"])

    # def offset_by(self, off):
    #     off = self.offset_point(off)
    #     return combine(self._pos, off)

    def center(self, off=(0, 0, 0)):
        return self.offset_point(off)

    def get_point_at(self, side, off=(0, 0, 0)):
        match side:
            case "t": return self.top(off=off)
            case "b": return self.bottom(off=off)
            case "r": return self.right(off=off)
            case "l": return self.left(off=off)
            case "tl": return self.tl(off=off)
            case "bl": return self.bl(off=off)
            case "tr": return self.tr(off=off)
            case "br": return self.br(off=off)

        raise ValueError("No such side: ", side)


    def left(self, off=(0, 0, 0)):
        return self.offset_point(combine([-self.width / 2, 0, 0], off))

    def right(self, off=(0, 0, 0)):
        return self.offset_point(combine([self.width / 2, 0, 0], off))

    def top(self, off=(0, 0, 0)):
        return self.offset_point(combine([0, self.height / 2, 0], off))

    def bottom(self, off=(0, 0, 0)):
        return self.offset_point(combine([0, -self.height / 2, 0], off))

    def tl(self, off=(0, 0, 0)):
        return self.offset_point(combine([-self.width / 2, self.height / 2, 0], off))

    def bl(self, off=(0, 0, 0)):
        return self.offset_point(combine([-self.width / 2, -self.height / 2, 0], off))

    def tr(self, off=(0, 0, 0)):
        return self.offset_point(combine([self.width / 2, self.height / 2, 0], off))

    def br(self, off=(0, 0, 0)):
        return self.offset_point(combine([self.width / 2, -self.height / 2, 0], off))

    def update_pos_rot(self, pos, rot):
        self.pos = combine(self.pos, pos)
        self.rot = combine(self.rot, rot)

    # def top_edge(self):
    #     return [self.tl_wide(), self.tr_wide()]
    #
    # def bottom_edge(self):
    #     return [self.bl_wide(), self.br_wide()]
    #
    # def inner_edge(self, side="right"):
    #     if side == "right":
    #         return [self.tl_wide(), self.bl_wide()]
    #
    #     return [self.tr_wide(), self.br_wide()]
    #
    # def outer_edge(self, side="right"):
    #     if side == "left":
    #         return self.inner_edge(side="right")
    #     return self.inner_edge(side="left")




    ###### RECONSIDER THE BELOW
    #
    # def closest_corner(self, rel_pos):
    #     dist = 99999999999.0
    #     all_dist = [
    #         distance(rel_pos, self.tl_wide()),
    #         distance(rel_pos, self.tr_wide()),
    #         distance(rel_pos, self.bl_wide()),
    #         distance(rel_pos, self.br_wide())
    #     ]
    #
    #     index = -1
    #
    #     for i in range(4):
    #         if all_dist[i] < dist:
    #             index = i
    #             dist = all_dist[i]
    #
    #     if index == 0:
    #         return self.tl_wide()
    #     elif index == 1:
    #         return self.tr_wide()
    #     elif index == 2:
    #         return self.bl_wide()
    #
    #     return self.br_wide()
    #

    #
    # def tr_wide(self, off=(0, 0, 0)):
    #     # return self._offset_point(mount_width / 2.0, mount_height / 2.0, off)
    #     offset = rotate_deg([(mount_width / 2.0) + off[0], (mount_height / 2) + off[1], off[2]], self._rot)
    #     return add_translate(self._pos, offset)
    #
    # def tl_wide(self, off=(0, 0, 0)):
    #     # return self._offset_point(-mount_width / 2.0, mount_height / 2.0, off)
    #     offset = rotate_deg([-(mount_width / 2.0) - off[0], (mount_height / 2) + off[1], off[2]], self._rot)
    #     return add_translate(self._pos, offset)
    #
    # def br_wide(self, off=(0, 0, 0)):
    #     # return self._offset_point(mount_width / 2.0, -mount_height / 2.0, off)
    #     offset = rotate_deg([(mount_width / 2.0) + off[0], -(mount_height / 2) - off[1], off[2]], self._rot)
    #     return add_translate(self._pos, offset)
    #
    # def bl_wide(self, off=(0, 0, 0)):
    #     # (-mount_width / 2.0, -mount_height / 2.0, off)
    #     offset = rotate_deg([-(mount_width / 2.0) - off[0], -(mount_height / 2) - off[1], off[2]], self._rot)
    #     return add_translate(self._pos, offset)
