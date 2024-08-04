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
        self.walls = []
        if parent_locals is not None:
            for item in parent_locals:
                globals()[item] = parent_locals[item]
        if parent_locals is not None:
            self.width = mount_width
            self.height = mount_height

    def __str__(self):
        return f'K-{self.get_id()}'

    def _offset_point(self, width, height, off):
        offset = [(width / 2.0) + off[0], (height / 2) + off[1], off[2]]
        new_offset = self._rot_transform.apply(offset)
        return add_translate(self._pos, offset)

    # def set_rot(self, new_rot):
    #     self._rot = new_rot
    #     self._rot_transform = get_rotation_transform(new_rot)

    # def center(self, off=(0, 0, 0)):
    #     offset = rotate_deg(off, self._rot)
    #     return add_translate(self._pos, offset)

    # def tr(self, off):
    #     # return self._offset_point(mount_width / 2.0, mount_height / 2.0, off)
    #     offset = rotate_deg([(mount_width / 2.0) + off[0], (mount_height / 2) + off[1], off[2]], self._rot)
    #     return add_translate(self._pos, offset)
    #
    # def tl(self, off):
    #     # return self._offset_point(-mount_width / 2.0, mount_height / 2.0, off)
    #     offset = rotate_deg([-(mount_width / 2.0) + off[0], (mount_height / 2) + off[1], off[2]], self._rot)
    #     return add_translate(self._pos, offset)
    #
    # def br(self, off):
    #     # return self._offset_point(mount_width / 2.0, -mount_height / 2.0, off)
    #     offset = rotate_deg([(mount_width / 2.0) + off[0], -(mount_height / 2) + off[1], off[2]], self._rot)
    #     return add_translate(self._pos, offset)
    #
    # def bl(self, off):
    #     # (-mount_width / 2.0, -mount_height / 2.0, off)
    #     offset = rotate_deg([-(mount_width / 2.0) + off[0], -(mount_height / 2) + off[1], off[2]], self._rot)
    #     return add_translate(self._pos, offset)

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

    def get_corners(self):
        corners = []

        if "left" in self.walls and "top" in self.walls:
            corners.append("tl")

        if "left" in self.walls and "bottom" in self.walls:
            corners.append("bl")

        if "right" in self.walls and "top" in self.walls:
            corners.append("tr")

        if "right" in self.walls and "bottom" in self.walls:
            corners.append("br")

        return corners

    def is_none(self):
        return self._id == "none"

    def is_present(self):
        return not self.is_none()

    def calculate_key_placement(self,
                                column,
                                row,
                                column_style="standard",
                                origin=(0, 0, 0)
                                ):

        xrot = 0
        yrot = 0
        # origin = [0, 0, 0]

        # row_radius = ((mount_height + extra_height) / 2) / (np.sin(use_alpha / 2)) + cap_top_height
        column_angle = beta * (centercol - column)
        column_x_delta_actual = column_x_delta
        if (pinky_1_5U and column == lastcol):
            if row >= first_1_5U_row and row <= last_1_5U_row:
                column_x_delta_actual = column_x_delta - 1.5
                column_angle = beta * (centercol - column - 0.27)

        if column_style == "orthographic":
            column_z_delta = column_radius * (1 - np.cos(column_angle))
            origin = add_translate(origin, [0, 0, -row_radius])
            origin = rotate_around_x(origin, alpha * (centerrow - row))
            xrot += alpha * (centerrow - row)
            origin = add_translate(origin, [0, 0, row_radius])
            origin = rotate_around_y(origin, column_angle)
            yrot += column_angle
            origin = add_translate(
                origin, [-(column - centercol) * column_x_delta_actual, 0, column_z_delta]
            )
            origin = add_translate(origin, column_offset(column))

        elif column_style == "fixed":
            origin = rotate_around_y(origin, fixed_angles[column])
            yrot += fixed_angles[column]
            origin = add_translate(origin, [fixed_x[column], 0, fixed_z[column]])
            origin = add_translate(origin, [0, 0, -(row_radius + fixed_z[column])])
            origin = rotate_around_x(origin, alpha * (centerrow - row))
            xrot += alpha * (centerrow - row)
            origin = add_translate(origin, [0, 0, row_radius + fixed_z[column]])
            origin = rotate_around_y(origin, fixed_tenting)
            yrot += fixed_tenting
            origin = add_translate(origin, [0, column_offset(column)[1], 0])

        else:
            origin = add_translate(origin, [0, 0, -row_radius])
            origin = rotate_around_x(origin, alpha * (centerrow - row))
            xrot += alpha * (centerrow - row)
            origin = add_translate(origin, [0, 0, row_radius])
            origin = add_translate(origin, [0, 0, -column_radius])
            origin = rotate_around_y(origin, column_angle)
            yrot += column_angle
            origin = add_translate(origin, [0, 0, column_radius])
            origin = add_translate(origin, column_offset(column))

        origin = rotate_around_y(origin, tenting_angle)
        yrot += tenting_angle
        origin = add_translate(origin, [0, 0, keyboard_z_offset])

        self.pos = origin
        self.rot = to_degrees([xrot, yrot, 0])

        dist = distance([0, 0, 0], self.pos)
        self._d_vec = [d / dist for d in origin]
        # print(f"{self.get_id()}: pos={self.pos}, offset={self.offset_point([0, 0, -3])}")
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
    def add_part(cls, part):
        if part.get_id() in cls.KEYS_BY_ID:
            print("WARNING: id already in keys list",  part.get_id())
        else:
            cls.KEYS_BY_ID[ part.get_id()] = part

        return part

    @classmethod
    def new_key(cls, key_id: str, parent_locals, key_type="MX", hole_type="NOTCH"):
        key = Key(key_id, parent_locals, key_type=key_type, hole_type=hole_type)
        return cls.add_part(key)

    @classmethod
    def new_key_by_row_column(cls, row: int, col: int, parent_locals, key_type="MX", hole_type="NOTCH"):
        if row > cls.MAX_ROW:
            cls.MAX_ROW = row
        if col > cls.MAX_COL:
            cls.MAX_COL = col

        return cls.new_key(cls.get_rc_id(row, col), parent_locals, key_type=key_type, hole_type=hole_type)

