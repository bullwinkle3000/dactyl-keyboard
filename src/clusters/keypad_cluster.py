
# from clusters.default_cluster import DefaultCluster
from clusters.trackball_orbyl import TrackballOrbyl
import json
import os
from key import Key, KeyFactory as KF
from common import *
from trackball import TrackballPart


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
        trackball = TrackballPart(self.locals)
        KF.add_part(trackball)
        key = None
        prev_key = None
        origin = [0, 0, 0]
        vert_off = keyswitch_height + 7
        horiz_off = keyswitch_width + 7
        off_x = 5
        top_y = -10

        trackball.pos = self.thumborigin()

        c_pos, c_rot = self.position_rotation()

        trackball.update_pos_rot(c_pos, c_rot)

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

        key_0_2 = KF.get_key_by_row_col(0, 2)
        key_0_3 = KF.get_key_by_row_col(0, 3)
        key_1_2 = KF.get_key_by_row_col(1, 2)
        key_1_3 = KF.get_key_by_row_col(1, 3)
        key_2_0 = KF.get_key_by_row_col(2, 0)
        key_2_1 = KF.get_key_by_row_col(2, 1)
        key_2_2 = KF.get_key_by_row_col(2, 2)
        key_2_3 = KF.get_key_by_row_col(2, 3)

        key_0_2.add_neighbor(trackball, "bl")
        key_0_2.add_neighbor(key_0_3, "r")
        key_0_2.add_neighbor(key_1_2, "b")
        key_0_2.add_neighbor(key_1_3, "br")

        key_0_3.add_neighbor(key_0_2, "l")
        key_0_3.add_neighbor(key_1_2, "bl")
        key_0_3.add_neighbor(key_1_3, "b")
        key_0_3.add_neighbor("wall", "r")

        key_1_2.add_neighbor(trackball, "l")
        key_1_2.add_neighbor(key_0_2, "t")
        key_1_2.add_neighbor(key_0_3, "tr")
        key_1_2.add_neighbor(key_1_3, "r")
        key_1_2.add_neighbor(key_2_3, "br")
        key_1_2.add_neighbor(key_2_2, "b")
        key_1_2.add_neighbor(key_2_1, "bl")

        key_1_3.add_neighbor(key_0_2, "tl")
        key_1_3.add_neighbor(key_0_3, "t")
        key_1_3.add_neighbor("wall", "r")
        key_1_3.add_neighbor(key_1_2, "l")
        key_1_3.add_neighbor(key_2_3, "b")
        key_1_3.add_neighbor(key_2_2, "bl")

        key_0_2.add_neighbor(trackball, "tl")
        key_2_0.add_neighbor("wall", "l")
        key_2_0.add_neighbor("outer_corner", "bl")
        key_2_0.add_neighbor("wall", "b")
        key_2_0.add_neighbor(key_2_1, "r")

        key_2_1.add_neighbor(trackball, "t")
        key_2_1.add_neighbor(key_2_0, "l")
        key_2_1.add_neighbor("wall", "b")
        key_2_1.add_neighbor(key_2_2, "l")
        key_2_1.add_neighbor(key_1_2, "tl")

        key_2_2.add_neighbor(trackball, "tl")
        key_2_2.add_neighbor(key_1_2, "t")
        key_2_2.add_neighbor(key_1_3, "tr")
        key_2_2.add_neighbor(key_2_3, "r")
        key_2_2.add_neighbor("wall", "b")
        key_2_2.add_neighbor(key_2_1, "l")

        key_2_3.add_neighbor(key_1_2, "tr")
        key_2_3.add_neighbor(key_1_3, "t")
        key_2_3.add_neighbor("wall", "r")
        key_2_3.add_neighbor("outer_corner", "br")
        key_2_3.add_neighbor("wall", "b")
        key_2_3.add_neighbor(key_2_2, "r")



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

    def build_corner(self, part, facing, corner_type):
        pass

    def build_wall(self, part, facing, corner_type):
        pass

    def get_points(self, part):
        hulls = []
        for k, v in part.neighbors:
            if v in ["outer_corner", "inner_corner"]:
                self.build_corner(part, k, v)
            elif v == "wall":
                self.build_wall(part, k, v)
            elif k == "t":

    def thumb_connectors(self, side="right"):
        hulls = []
        for r in range(4):
            for c in range(4):
                key = KF.get_key_by_row_col(r, c)
                if not key.is_none():
                    pass
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



