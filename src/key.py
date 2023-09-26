from geom import *
from part import Part


SIZES = {
    "MX": {"w": 14, "h": 14, "d": 10},
    "ALPS": {"w": 15.5, "h": 12.8, "d": 10}
}

KEY_NONE = None


class Key(Part):
    type = "MX"
    hole = "NOTCH"
    plate_rot_z = 0

    def __init__(self, key_id, parent_locals, key_type="MX", hole_type="NOTCH"):
        super().__init__(key_id)
        self.type = key_type
        self.hole = hole_type
        self.w = SIZES[key_type]["w"]
        self.h = SIZES[key_type]["h"]
        self.d = SIZES[key_type]["d"]
        self.neighbors = {}
        self.walls = []
        if parent_locals is not None:
            for item in parent_locals:
                globals()[item] = parent_locals[item]

    def __str__(self):
        return f'K-{self.get_id()}'

    def _offset_point(self, width, height, off):
        offset = rotate_deg([(width / 2.0) + off[0], (height / 2) + off[1], off[2]], self._rot)
        return add_translate(self._pos, offset)

    def center(self, off=(0, 0, 0)):
        return self._offset_point(0, 0, off)

    def tr(self, off=(0, 0, 0)):
        # return self._offset_point(mount_width / 2.0, mount_height / 2.0, off)
        offset = rotate_deg([(mount_width / 2.0) + off[0], (mount_height / 2) + off[1], off[2]], self._rot)
        return add_translate(self._pos, offset)

    def tl(self, off=(0, 0, 0)):
        # return self._offset_point(-mount_width / 2.0, mount_height / 2.0, off)
        offset = rotate_deg([-(mount_width / 2.0) - off[0], (mount_height / 2) + off[1], off[2]], self._rot)
        return add_translate(self._pos, offset)

    def br(self, off=(0, 0, 0)):
        # return self._offset_point(mount_width / 2.0, -mount_height / 2.0, off)
        offset = rotate_deg([(mount_width / 2.0) + off[0], -(mount_height / 2) - off[1], off[2]], self._rot)
        return add_translate(self._pos, offset)

    def bl(self, off=(0, 0, 0)):
        # return self._offset_point(-mount_width / 2.0, -mount_height / 2.0, off)
        offset = rotate_deg([-(mount_width / 2.0) - off[0], -(mount_height / 2) - off[1], off[2]], self._rot)
        return add_translate(self._pos, offset)

    def is_wall_key(self):
        return len(self.walls) > 0

    def has_wall(self, wall):
        if wall not in ["top", "left", "right", "bottom"]:
            raise Exception("wall must be top, left, right, or bottom")

        return wall in self.walls

    def get_walls(self):
        return self.walls.copy()

    def add_wall(self, wall):
        if wall not in ["top", "left", "right", "bottom"]:
            raise Exception("wall must be top, left, right, or bottom")

        if wall in self.walls:
            return

        self.walls.append(wall)

    def is_corner(self):
        if "left" in self.walls and "top" in self.walls:
            return True

        if "left" in self.walls and "bottom" in self.walls:
            return True

        if "right" in self.walls and "top" in self.walls:
            return True

        if "right" in self.walls and "bottom" in self.walls:
            return True

        return False

    def add_neighbor(self, neighbor, side):
        if side not in ["t", "r", "l", "b", "tr", "br", "tl", "bl"]:
            raise Exception("side value out of range")
        if neighbor.is_none():
            raise Exception("neighbor cannot be NONE key")

        self.neighbors[side] = neighbor

    def get_neighbor(self, side):
        if side not in ["t", "r", "l", "b", "tr", "br", "tl", "bl"]:
            raise Exception("side value out of range")
        if side in self.neighbors.keys():
            return self.neighbors[side]
        return KeyFactory.NONE_KEY

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

    def top_edge(self):
        return [self.tl(), self.tr()]

    def bottom_edge(self):
        return [self.bl(), self.br()]

    def inner_edge(self, side="right"):
        if side == "right":
            return [self.tl(), self.bl()]

        return [self.tr(), self.br()]

    def outer_edge(self, side="right"):
        if side == "left":
            return self.inner_edge(side="right")
        return self.inner_edge(side="left")

    def is_none(self):
        return self._id == "none"

    def closest_corner(self, rel_pos):
        dist = 99999999999.0
        all_dist = [
            distance(rel_pos, self.tl()),
            distance(rel_pos, self.tr()),
            distance(rel_pos, self.bl()),
            distance(rel_pos, self.br())
        ]

        index = -1

        for i in range(4):
            if all_dist[i] < dist:
                index = i
                dist = all_dist[i]

        if index == 0:
            return self.tl()
        elif index == 1:
            return self.tr()
        elif index == 2:
            return self.bl()

        return self.br()

    def calculate_key_placement(self,
                                column,
                                row,
                                column_style="standard",
                                ):

        xrot = 0
        yrot = 0
        position = [0, 0, 0]

        use_alpha = alpha + ((nrows - row) * 0.1)
        # row_radius = ((mount_height + extra_height) / 2) / (np.sin(use_alpha / 2)) + cap_top_height
        column_angle = beta * (centercol - column)
        column_x_delta_actual = column_x_delta
        if (pinky_1_5U and column == lastcol):
            if row >= first_1_5U_row and row <= last_1_5U_row:
                column_x_delta_actual = column_x_delta - 1.5
                column_angle = beta * (centercol - column - 0.27)

        if column_style == "orthographic":
            column_z_delta = column_radius * (1 - np.cos(column_angle))
            position = add_translate(position, [0, 0, -row_radius])
            position = rotate_around_x(position, alpha * (centerrow - row))
            xrot += alpha * (centerrow - row)
            position = add_translate(position, [0, 0, row_radius])
            position = rotate_around_y(position, column_angle)
            yrot += column_angle
            position = add_translate(
                position, [-(column - centercol) * column_x_delta_actual, 0, column_z_delta]
            )
            position = add_translate(position, column_offset(column))

        elif column_style == "fixed":
            position = rotate_around_y(position, fixed_angles[column])
            yrot += fixed_angles[column]
            position = add_translate(position, [fixed_x[column], 0, fixed_z[column]])
            position = add_translate(position, [0, 0, -(row_radius + fixed_z[column])])
            position = rotate_around_x(position, alpha * (centerrow - row))
            xrot += alpha * (centerrow - row)
            position = add_translate(position, [0, 0, row_radius + fixed_z[column]])
            position = rotate_around_y(position, fixed_tenting)
            yrot += fixed_tenting
            position = add_translate(position, [0, column_offset(column)[1], 0])

        else:
            position = add_translate(position, [0, 0, -row_radius])
            position = rotate_around_x(position, alpha * (centerrow - row))
            xrot += alpha * (centerrow - row)
            position = add_translate(position, [0, 0, row_radius])
            position = add_translate(position, [0, 0, -column_radius])
            position = rotate_around_y(position, column_angle)
            yrot += column_angle
            position = add_translate(position, [0, 0, column_radius])
            position = add_translate(position, column_offset(column))

        position = rotate_around_y(position, tenting_angle)
        yrot += tenting_angle
        position = add_translate(position, [0, 0, keyboard_z_offset])

        self.pos = position
        self.rot = to_degrees([xrot, yrot, 0])
        return [self.pos, self.rot]

    def render(self, plate_file, side="right"):
        if plate_style in ['NUB', 'HS_NUB']:
            tb_border = (mount_height - keyswitch_height) / 2
            top_wall = box(mount_width, tb_border, plate_thickness)
            top_wall = translate(top_wall, (0, (tb_border / 2) + (keyswitch_height / 2), plate_thickness / 2))

            lr_border = (mount_width - keyswitch_width) / 2
            left_wall = box(lr_border, mount_height, plate_thickness)
            left_wall = translate(left_wall, ((lr_border / 2) + (keyswitch_width / 2), 0, plate_thickness / 2))

            side_nub = cylinder(radius=1, height=2.75)
            side_nub = rotate(side_nub, (90, 0, 0))
            side_nub = translate(side_nub, (keyswitch_width / 2, 0, 1))

            nub_cube = box(1.5, 2.75, plate_thickness)
            nub_cube = translate(nub_cube, ((1.5 / 2) + (keyswitch_width / 2), 0, plate_thickness / 2))

            side_nub2 = tess_hull(shapes=(side_nub, nub_cube))
            side_nub2 = union([side_nub2, side_nub, nub_cube])

            plate_half1 = union([top_wall, left_wall, side_nub2])
            plate_half2 = plate_half1
            plate_half2 = mirror(plate_half2, 'XZ')
            plate_half2 = mirror(plate_half2, 'YZ')

            plate = union([plate_half1, plate_half2])

        else:  # 'HOLE' or default, square cutout for non-nub designs.
            plate = box(mount_width, mount_height, mount_thickness)
            plate = translate(plate, (0.0, 0.0, mount_thickness / 2.0))

            shape_cut = box(keyswitch_width, keyswitch_height, mount_thickness * 2 + .02)
            shape_cut = translate(shape_cut, (0.0, 0.0, mount_thickness - .01))

            plate = difference(plate, [shape_cut])

        if plate_file is not None:
            socket = import_file(plate_file)
            socket = translate(socket, [0, 0, plate_thickness + plate_offset])
            plate = union([plate, socket])

        if plate_style in ['UNDERCUT', 'HS_UNDERCUT', 'NOTCH', 'HS_NOTCH', 'AMOEBA']:
            if plate_style in ['UNDERCUT', 'HS_UNDERCUT']:
                undercut = box(
                    keyswitch_width + 2 * clip_undercut,
                    keyswitch_height + 2 * clip_undercut,
                    mount_thickness
                )

            if plate_style in ['NOTCH', 'HS_NOTCH', 'AMOEBA']:
                undercut = box(
                    notch_width,
                    keyswitch_height + 2 * clip_undercut,
                    mount_thickness
                )
                undercut = union([undercut,
                                  box(
                                      keyswitch_width + 2 * clip_undercut,
                                      notch_width,
                                      mount_thickness
                                  )
                                  ])

            undercut = translate(undercut, (0.0, 0.0, -clip_thickness + mount_thickness / 2.0))

            if ENGINE == 'cadquery' and undercut_transition > 0:
                undercut = undercut.faces("+Z").chamfer(undercut_transition, clip_undercut)

            plate = difference(plate, [undercut])

        if side == "left":
            plate = mirror(plate, 'YZ')

        plate = rotate(plate, self.rot)
        if self.plate_rot_z != 0:
            plate = rotate(plate, [0, 0, self.plate_rot_z])
        plate = translate(plate, self.pos)

        return plate


class KeyFactory(object):

    NONE_KEY = Key("none", None)

    KEYS_BY_ID = {
        "none": NONE_KEY
    }

    MAX_ROW = -1
    MAX_COL = -1

    MATRIX = None
    ROWS = None
    WALL_KEYS = None

    @staticmethod
    def get_key_by_id(key_id: str) -> Key:
        if key_id not in KeyFactory.KEYS_BY_ID.keys():
            return KeyFactory.KEYS_BY_ID["none"]
        return KeyFactory.KEYS_BY_ID[key_id]

    @classmethod
    def get_key_by_row_col(cls, row, col) -> Key:
        return cls.get_key_by_id(cls.get_rc_id(row, col))

    @staticmethod
    def get_rc_id(row, col):
        return "r" + str(row) + "c" + str(col)

    @classmethod
    def build_matrix(cls):
        if len(cls.KEYS_BY_ID) <= 1:
            raise Exception("No keys present to build matrix.")

        cls.MATRIX = []
        top_wall = [cls.KEYS_BY_ID["none"] for x in range(cls.MAX_COL + 1)]
        bottom_wall = [cls.KEYS_BY_ID["none"] for x in range(cls.MAX_COL + 1)]
        inner_wall = [cls.KEYS_BY_ID["none"] for x in range(cls.MAX_ROW + 1)]
        outer_wall = [cls.KEYS_BY_ID["none"] for x in range(cls.MAX_ROW + 1)]
        all_rows = [[] for x in range(0, cls.MAX_ROW + 1)]

        for col in range(cls.MAX_COL + 1):
            column_keys = []
            for row in range(cls.MAX_ROW + 1):
                key = cls.get_key_by_row_col(row, col)

                if key.get_id() != "none":
                    column_keys.append(key)
                    all_rows[row].append(key)
                    if top_wall[col].get_id() == "none":
                        top_wall[col] = key
                    if inner_wall[row].get_id() == "none":
                        inner_wall[row] = key
                    bottom_wall[col] = key
                    outer_wall[row] = key

            cls.MATRIX.append(column_keys)

        wall_keys = []
        for key in top_wall:
            key.add_wall("top")
            if key not in wall_keys:
                wall_keys.append(key)
        for key in inner_wall:
            key.add_wall("left")
            if key not in wall_keys:
                wall_keys.append(key)
        for key in bottom_wall:
            key.add_wall("bottom")
            if key not in wall_keys:
                wall_keys.append(key)
        for key in outer_wall:
            key.add_wall("right")
            if key not in wall_keys:
                wall_keys.append(key)

        cls.WALL_KEYS = wall_keys
        cls.ROWS = all_rows

        for col in range(len(cls.MATRIX)):
            column = cls.MATRIX[col]
            for row in range(len(column)):
                key = cls.MATRIX[col][row]
                if key.is_none():
                    continue

                if row > 0:
                    top = cls.MATRIX[col][row - 1]
                    if not top.is_none():
                        key.add_neighbor(top, "t")
                        top.add_neighbor(key, "b")

                    if col > 0:
                        tl = cls.MATRIX[col - 1][row - 1]
                        if not tl.is_none():
                            key.add_neighbor(tl, "tl")
                            tl.add_neighbor(key, "br")

                if col > 0:
                    last_column = cls.MATRIX[col - 1]
                    if len(last_column) > row:
                        left = last_column[row]
                        if not left.is_none():
                            key.add_neighbor(left, "l")
                            left.add_neighbor(key, "r")

                    if len(last_column) > row + 1:
                        bl = last_column[row + 1]
                        if not bl.is_none():
                            key.add_neighbor(bl, "bl")
                            bl.add_neighbor(key, "tr")

        print("KeyFactory: Matrix built.")

    @classmethod
    def get_column(cls, col) -> [Key]:
        return cls.MATRIX[col]

    @classmethod
    def get_row(cls, row) -> [Key]:
        return cls.ROWS[row]

    @classmethod
    def inner_keys(cls):
        return cls.WALL_KEYS["right"]

    @classmethod
    def outer_keys(cls):
        return cls.WALL_KEYS["left"]

    @classmethod
    def top_keys(cls):
        return cls.WALL_KEYS["top"]

    @classmethod
    def bottom_keys(cls):
        return cls.WALL_KEYS["bottom"]

    @staticmethod
    def clear_keys():
        KeyFactory.KEYS_BY_ID = {"none": Key("none", None)}
        KeyFactory.MAX_ROW = -1
        KeyFactory.MAX_COL = -1
        KeyFactory.MATRIX = None
        KeyFactory.ROWS = None
        KeyFactory.WALL_KEYS = None

    @classmethod
    def new_key(cls, key_id: str, parent_locals, key_type="MX", hole_type="NOTCH"):
        key = Key(key_id, parent_locals, key_type=key_type, hole_type=hole_type)
        if key_id in cls.KEYS_BY_ID:
            print("WARNING: key_id already in keys list", key_id)
        else:
            cls.KEYS_BY_ID[key_id] = key
        return key

    @classmethod
    def new_key_by_row_column(cls, row: int, col: int, parent_locals, key_type="MX", hole_type="NOTCH"):
        if row > cls.MAX_ROW:
            cls.MAX_ROW = row
        if col > cls.MAX_COL:
            cls.MAX_COL = col

        return cls.new_key(cls.get_rc_id(row, col), parent_locals, key_type=key_type, hole_type=hole_type)
