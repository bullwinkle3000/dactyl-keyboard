
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
        self.build_key_matrix()

    def track_place(self, shape, offsets=(0, 0, 0)):
        pos, rot = self.position_rotation()
        pos = combine(pos, offsets)
        shape = rotate(shape, rot)
        shape = translate(shape, pos)
        return shape

    def build_key_matrix(self):
        key = None
        prev_key = None
        origin = [0, 0, 0]
        vert_off = keyswitch_height + 7
        horiz_off = keyswitch_width + 7
        off_x = 5
        top_y = -10

        c_pos, c_rot = self.position_rotation()

        z_inc = 5

        for r in range(4):
            for c in range(4):
                key = KF.NONE_KEY
                if r < 3:
                    if c > 1:
                        key = KF.new_key(KF.get_rc_id(r, c), self.locals)
                elif r == 3:
                    key = KF.new_key(KF.get_rc_id(r, c), self.locals)

                if not key.is_none():
                    key.pos = [horiz_off * c, -vert_off * r, 0]

        for r in range(1, 4):
            for c in range(4):
                key = KF.get_key_by_id(KF.get_rc_id(r, c))
                if not key.is_none():
                    key.update_pos_rot(c_pos, c_rot)
                    for top in range(c-1, 3):
                        test_key = KF.get_key_by_id(KF.get_rc_id(r - 1, top))
                        if not test_key.is_none():
                            if top == c - 1:
                                key.add_neighbor(test_key.get_id(), "tl")
                                test_key.add_neighbor(key.get_id(), "br")
                            elif top == c:
                                key.add_neighbor(test_key.get_id(), "t")
                                test_key.add_neighbor(key.get_id(), "b")
                            elif top == c + 1:
                                key.add_neighbor(test_key.get_id(), "tr")
                                test_key.add_neighbor(key.get_id(), "bl")

                    if c == 3:
                        key.add_neighbor("wall", "r")
                    elif c == 0:
                        key.add_neighbor("wall", "l")

                    if r == 3:
                        key.add_neighbor("wall", "b")
                        if c == 3:
                            key.add_neighbor("corner", "br")
                        elif c == 0:
                            key.add_neighbor("corner", "bl")

    def build_keys(self):

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

            key.update_pos_rot(c_pos, c_rot)

            if last_key is not None:
                key.add_neighbor(last_key.get_id(), "t")
                key.add_neighbor("wall", "r")
                last_key.add_neighbor(key.get_id(), "b")

            if i == 2:
                key.add_neighbor("wall", "b")
                key.add_neighbor("corner", "br")

            last_key = key

        off_y = top_y - (2 * vert_off)
        left_most_x = off_x - (3 * horiz_off)

        for i in range(3):
            key = KF.new_key(str(i + 3), self.locals)
            off_x = left_most_x + (i * horiz_off)
            key.pos = (origin[0] + off_x, origin[1] + off_y, 0)
            key.rot = (20, 0, 10)
            key.add_neighbor("wall", "b")
            if i == 0:
                key.add_neighbor("wall", "l")

            last_key = add_neighbor(key, last_key)
            key.update_pos_rot(c_pos, c_rot)

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
            key.update_pos_rot(c_pos, c_rot)

    def thumbcaps(self, side="right"):
        return self.thumb_1x_layout(sa_cap(1), True)

    def thumb_1x_layout(self, shape, cap=False):
        shapes = []
        for r in range(4):
            for c in range(4):
                key = KF.get_key_by_id(KF.get_rc_id(r, c))
                if not key.is_none():
                    shapes.append(key.render(None, cap))

        return shapes

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        return []

    def thumb_connectors(self, side="right"):
        hulls = []
        last_key = None
        last_tr_pos = self.track_place(self.tb_post_tr())
        # key0 = KF.KEYS_BY_ID["0"]
        # key1 = KF.KEYS_BY_ID["1"]
        # key2 = KF.KEYS_BY_ID["2"]
        # key3 = KF.KEYS_BY_ID["3"]
        # key4 = KF.KEYS_BY_ID["4"]
        # key5 = KF.KEYS_BY_ID["5"]
        # key6 = KF.KEYS_BY_ID["6"]
        # key7 = KF.KEYS_BY_ID["7"]





        return hulls

    def walls(self, side="right"):
        return []

    def connection(self, side="right"):
        return []



