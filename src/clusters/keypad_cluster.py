
# from clusters.default_cluster import DefaultCluster
from clusters.trackball_orbyl import TrackballOrbyl
import json
import os
from key import Key, KeyFactory


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

    # def position_rotation(self):
    #     rot = [10, -15, 5]
    #     pos = self.thumborigin()
    #     # Changes size based on key diameter around ball, shifting off of the top left cluster key.
    #     shift = [-.9 * self.key_diameter/2 + 27 - 42, -.1 * self.key_diameter / 2 + 3 - 20, -5]
    #     for i in range(len(pos)):
    #         pos[i] = pos[i] + shift[i] + self.translation_offset[i]
    #
    #     for i in range(len(rot)):
    #         rot[i] = rot[i] + self.rotation_offset[i]
    #
    #     return pos, rot

    def build_keys(self):
        origin = self.thumborigin()
        vert_off = keyswitch_height + 7
        horiz_off = keyswitch_width + 7
        off_x = 5
        top_y = -10

        top_z = origin[2] - 15
        z_inc = 5

        for i in range(3):
            key = KeyFactory.new_key(str(i), self.locals)
            off_y = top_y - (vert_off * i)
            key.pos = (origin[0] + off_x, origin[1] + off_y, top_z - (i * z_inc))
            key.rot = (20, 0, 10)

        off_y = top_y - (2 * vert_off)
        left_most_x = off_x - (3 * horiz_off)

        height = 3 * z_inc
        for i in range(3):
            key = KeyFactory.new_key(str(i + 3), self.locals)
            off_x = left_most_x + (i * horiz_off)
            key.pos = (origin[0] + off_x, origin[1] + off_y, top_z - height)
            key.rot = (20, 0, 10)

        height = 2 * z_inc
        off_x = left_most_x + (2 * horiz_off)
        off_y += vert_off
        for i in range(2):
            key = KeyFactory.new_key(str(i + 6), self.locals)
            off_y = off_y + (vert_off * i)
            key.pos = (origin[0] + off_x, origin[1] + off_y, top_z - height + (i * z_inc))
            key.rot = (20, 0, 10)

    def thumbcaps(self, side="right"):
        return self.thumb_1x_layout(sa_cap(1), True)

    def thumb_1x_layout(self, shape, cap=False):
        shapes = []
        for i in range(8):
            key = KeyFactory.KEYS_BY_ID[str(i)]
            shapes.append(key.render(None, cap))

        return shapes

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        return []

    def thumb_connectors(self, side="right"):
        return []

    def walls(self, side="right"):
        return []

    def connection(self, side="right"):
        return []



