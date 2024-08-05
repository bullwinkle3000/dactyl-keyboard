
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
        # trackball = TrackballPart(self.locals)
        # KF.add_part(trackball)
        key = None
        prev_key = None
        origin = [0, 0, 0]
        vert_off = keyswitch_height + 7
        horiz_off = keyswitch_width + 7
        off_x = 5
        top_y = -10

        # trackball.pos = self.thumborigin()

        c_pos, c_rot = self.position_rotation()

        # trackball.update_pos_rot(c_pos, c_rot)

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
                    key.update_pos_rot(c_pos, c_rot)

        key_0_2 = KF.get_key_by_row_col(0, 2)
        key_0_3 = KF.get_key_by_row_col(0, 3)
        key_1_2 = KF.get_key_by_row_col(1, 2)
        key_1_3 = KF.get_key_by_row_col(1, 3)
        key_2_0 = KF.get_key_by_row_col(2, 0)
        key_2_1 = KF.get_key_by_row_col(2, 1)
        key_2_2 = KF.get_key_by_row_col(2, 2)
        key_2_3 = KF.get_key_by_row_col(2, 3)

        # trackball.add_neighbor(key_0_2, "tr")
        # key_0_2.add_neighbor(trackball, "bl")
        key_0_2.add_neighbor(key_0_3, "r")
        key_0_2.add_neighbor(key_1_2, "b")
        key_0_2.add_neighbor(key_1_3, "br")

        key_0_3.add_neighbor(key_0_2, "l")
        key_0_3.add_neighbor(key_1_2, "bl")
        key_0_3.add_neighbor(key_1_3, "b")
        key_0_3.add_neighbor("wall", "r")

        # trackball.add_neighbor(key_1_2, "r")
        # key_1_2.add_neighbor(trackball, "l")
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

        # trackball.add_neighbor(key_0_2, "br")
        # key_0_2.add_neighbor(trackball, "tl")
        key_2_0.add_neighbor("wall", "l")
        key_2_0.add_neighbor("outer_corner", "bl")
        key_2_0.add_neighbor("wall", "b")
        key_2_0.add_neighbor(key_2_1, "r")

        # trackball.add_neighbor(key_2_1, "b")
        # key_2_1.add_neighbor(trackball, "t")
        key_2_1.add_neighbor(key_2_0, "l")
        key_2_1.add_neighbor("wall", "b")
        key_2_1.add_neighbor(key_2_2, "l")
        key_2_1.add_neighbor(key_1_2, "tl")

        # trackball.add_neighbor(key_2_2, "br")
        # key_2_2.add_neighbor(trackball, "tl")
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

        return union(shapes)

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        return []

    def build_corner(self, part, facing, corner_type):
        return []

    def build_wall(self, part, facing):
        return []

    def get_join(self, part, neighb):
        for k in neighb.neighbors:
            v = neighb.neighbors[k]
            if v is part:
                return k

        return None

    def get_points(self, part1, side1, part2, side2):
        side_points = {
            "t": ["tl", "t", "tr"],
            "b": ["bl", "b", "br"],
            "l": ["tl", "l", "bl"],
            "r": ["tr", "r", "br"],
            "tl": ["t", "tl", "l"],
            "bl": ["b", "bl", "l"],
            "tr": ["t", "tr", "r"],
            "br": ["b", "br", "r"]
        }

        sp1 = side_points[side1]
        sp2 = side_points[side2]

        return [
            hull_from_points([
                part1.get_point_at(sp1[0]),
                part2.get_point_at(sp2[1]),
                part1.get_point_at(sp1[2])
            ]),
            hull_from_points([
                part2.get_point_at(sp2[0]),
                part1.get_point_at(sp1[1]),
                part2.get_point_at(sp2[2])
            ])

        ]

    def get_connection(self, part, side, neighb):
        neighb_side = self.get_join(part, neighb)
        points = self.get_points(part, side, neighb, neighb_side)

        return hull_from_points(points)

    def thumb_connectors(self, side="right"):
        processed = {}
        hulls = []
        for r in range(4):
            for c in range(4):
                key = KF.get_key_by_row_col(r, c)
                if key.get_id() not in processed.keys():
                    processed[key.get_id()] = []
                if not key.is_none():
                    for side in key.neighbors:
                        neighb = key.neighbors[side]
                        if side in processed[key.get_id()]:
                            continue
                        if neighb in ["inner_corner", "outer_corner"]:
                            pass
                            # hulls.append(union(self.build_corner(key, side, neighb)))
                        elif neighb == "wall":
                            pass
                            # hulls.append(union(self.build_wall(key, side)))
                        else:
                            if neighb.get_id() not in processed.keys():
                                processed[neighb.get_id()] = []
                            neighb_side = self.get_join(key, neighb)
                            points = self.get_points(key, side, neighb, neighb_side)
                            # hull = hull_from_points(points)
                            hulls = hulls + points
                            processed[neighb.get_id()].append(neighb_side)
                            processed[key.get_id()].append(side)


                            return union(hulls)

    def walls(self, side="right"):
        return []

    def connection(self, side="right"):
        return []

    # def thumb(self, side="right"):
    #     return []



