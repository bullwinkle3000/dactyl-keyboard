
# from clusters.default_cluster import DefaultCluster
from clusters.trackball_orbyl import TrackballOrbyl
import json
import os
from key import Key, KeyFactory as KF
from common import *

class KeypadCluster(TrackballOrbyl):

    @staticmethod
    def name():
        return "KEYPAD_CLUSTER"

    def __init__(self, parent_locals):
        super().__init__(parent_locals)
        self.locals = parent_locals
        for item in parent_locals:
            globals()[item] = parent_locals[item]
        self.is_tb = True
        self.build_keys()

    def track_place(self, shape, offsets=(0, 0, 0)):
        pos, rot = self.position_rotation()
        pos = combine(pos, offsets)
        shape = rotate(shape, rot)
        shape = translate(shape, pos)
        return shape

    def build_keys(self):
        def add_neighbor(this_key, prev_key):
            if prev_key is not None:
                this_key.add_neighbor(prev_key)
                prev_key.add_neighbor(this_key)

            return this_key

        origin = [0, 0, 0]
        vert_off = keyswitch_height + 7
        horiz_off = keyswitch_width + 7
        off_x = 5
        top_y = -10

        c_pos, c_rot = self.position_rotation()

        z_inc = 5
        last_key = None
        for i in range(3):
            key = KF.new_key(str(i), self.locals)
            off_y = top_y - (vert_off * i)
            key.pos = (origin[0] + off_x, origin[1] + off_y, 0)
            key.rot = (20, 0, 10)
            key.add_wall("right")
            if i == 2:
                key.add_wall("bottom")

            key.update_key_pos_rot(c_pos, c_rot)
            last_key = add_neighbor(key, last_key)

        off_y = top_y - (2 * vert_off)
        left_most_x = off_x - (3 * horiz_off)

        height = 3 * z_inc
        for i in range(3):
            key = KF.new_key(str(i + 3), self.locals)
            off_x = left_most_x + (i * horiz_off)
            key.pos = (origin[0] + off_x, origin[1] + off_y, 0)
            key.rot = (20, 0, 10)
            key.add_wall("bottom")
            if i == 0:
                key.add_wall("left")

            last_key = add_neighbor(key, last_key)
            key.update_key_pos_rot(c_pos, c_rot)

        height = 2 * z_inc
        off_x = left_most_x + (2 * horiz_off)
        off_y += vert_off
        for i in range(2):
            key = KF.new_key(str(i + 6), self.locals)
            off_y = off_y + (vert_off * i)
            key.pos = (origin[0] + off_x, origin[1] + off_y, 0)
            key.rot = (20, 0, 10)
            key.add_wall("left")
            last_key = add_neighbor(key, last_key)
            key.update_key_pos_rot(c_pos, c_rot)

    def thumbcaps(self, side="right"):
        return self.thumb_1x_layout(sa_cap(1), True)

    def thumb_1x_layout(self, shape, cap=False):
        shapes = []
        for i in range(8):
            key = KF.KEYS_BY_ID[str(i)]
            shapes.append(key.render(None, cap))

        return shapes

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        return []

    def thumb_connectors(self, side="right"):
        hulls = []
        last_key = None
        last_tr_pos = self.track_place(self.tb_post_tr())
        key0 = KF.KEYS_BY_ID["0"]
        key1 = KF.KEYS_BY_ID["1"]
        key2 = KF.KEYS_BY_ID["2"]
        key3 = KF.KEYS_BY_ID["3"]
        key4 = KF.KEYS_BY_ID["4"]
        key5 = KF.KEYS_BY_ID["5"]
        key6 = KF.KEYS_BY_ID["6"]
        key7 = KF.KEYS_BY_ID["7"]





        return []

    def walls(self, side="right"):
        return []

    def connection(self, side="right"):
        return []


