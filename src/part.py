from geom import *
from scipy.spatial.transform import Rotation as R


class Part(object):
    _pos = [0, 0, 0]
    _rot = [0, 0, 0]
    _rot_tranform: R = None
    _id = None
    w = 0
    h = 0
    d = 0

    def __init__(self, part_id,):
        self._id = part_id
        self._rot_transform = None

    def set_pos(self, new_pos):
        self._pos = new_pos

    def get_pos(self):
        return self._pos

    pos = property(get_pos, set_pos)

    def set_rot(self, new_rot):
        self._rot = new_rot
        self._rot_transform = get_rotation_transform(new_rot)

    def get_rot(self):
        return self._rot

    def update_rot_by(self, deltas):
        self._rot = [self._rot[i] + deltas[i] for i in range(len(self._rot))]

    rot = property(get_rot, set_rot)

    def get_id(self):
        return self._id

    def rotate_deg(self, rotate_by):
        self._pos = rotate_deg(self._pos, rotate_by)
        self.update_rot_by(rotate_by)
        return self._pos

    def rotate_rad(self, rotate_by):
        self._pos = rotate_rad(self._pos, rotate_by)
        self.update_rot_by([rad2deg(rotate_by[i]) for i in range(len(rotate_by))])
        return self._pos

    def translate(self, position):
        self._pos = add_translate(self._pos, position)
        return self._pos

    def offset_point(self, offsets):
        calc_offsets = rotate_rad(offsets, self.rot)
        return [calc_offsets[i] + self.pos[i] for i in range(len(self._pos))]
