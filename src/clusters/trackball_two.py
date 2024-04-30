from clusters.trackball_three import TrackballThree
import json
import os


class TrackballTwo(TrackballThree):
    key_diameter = 75
    translation_offset = [
        0,
        0,
        10
    ]
    rotation_offset = [
        0,
        0,
        0
    ]
    key_translation_offsets = [
        [
            0.0,
            0.0,
            -3.0
        ],
        [
            0.0,
            0.0,
            -3.0
        ],
        [
            0.0,
            0.0,
            -3.0
        ],
        [
            0.0,
            0.0,
            -3.0
        ]
    ]
    key_rotation_offsets = [
        [
            0.0,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            0.0
        ]
    ]

    @staticmethod
    def name():
        return "TRACKBALL_TWO"

    def get_config(self):
        with open(os.path.join("src", "clusters", "json", "TRACKBALL_THREE.json"), mode='r') as fid:
            data = json.load(fid)

        superdata = super().get_config()

        # overwrite any super variables with this class' needs
        for item in data:
            superdata[item] = data[item]

        for item in superdata:
            if not hasattr(self, str(item)):
                print(self.name() + ": NO MEMBER VARIABLE FOR " + str(item))
                continue
            setattr(self, str(item), superdata[item])

        return superdata

    def __init__(self, parent_locals):
        self.num_keys = 4
        self.is_tb = True
        super().__init__(parent_locals)
        for item in parent_locals:
            globals()[item] = parent_locals[item]

    def position_rotation(self):
        rot = [10, -15, 5]
        pos = self.thumborigin()
        # Changes size based on key diameter around ball, shifting off of the top left cluster key.
        shift = [-.9 * self.key_diameter/2 + 27 - 42, -.1 * self.key_diameter / 2 + 3 - 20, -5]
        for i in range(len(pos)):
            pos[i] = pos[i] + shift[i] + self.translation_offset[i]

        for i in range(len(rot)):
            rot[i] = rot[i] + self.rotation_offset[i]

        return pos, rot

    def track_place(self, shape):
        pos, rot = self.position_rotation()
        shape = rotate(shape, rot)
        shape = translate(shape, pos)
        return shape

    def tl_place(self, shape):
        raise Exception("Nothing to see here")
        #
        # shape = rotate(shape, [0, 0, 0])
        # t_off = self.key_translation_offsets[0]
        # shape = rotate(shape, self.key_rotation_offsets[0])
        # shape = translate(shape, (t_off[0], t_off[1] + self.key_diameter / 2, t_off[2]))
        # shape = rotate(shape, [0,0,-80])
        # shape = self.track_place(shape)
        #
        # return shape

    def tr_place(self, shape):
        raise Exception("Nothing to see here")

    def mr_place(self, shape):
        shape = rotate(shape, [0, 0, 0])
        shape = rotate(shape, self.key_rotation_offsets[1])
        t_off = self.key_translation_offsets[1]
        shape = translate(shape, (t_off[0], t_off[1] + self.key_diameter/2, t_off[2]))
        shape = rotate(shape, [0,0,-118])
        shape = self.track_place(shape)

        return shape

    def br_place(self, shape):
        shape = rotate(shape, [0, 0, 180])
        shape = rotate(shape, self.key_rotation_offsets[2])
        t_off = self.key_translation_offsets[2]
        shape = translate(shape, (t_off[0], t_off[1]+self.key_diameter/2, t_off[2]))
        shape = rotate(shape, [0,0,-180])
        shape = self.track_place(shape)

        return shape

    def bl_place(self, shape):
        debugprint('thumb_bl_place()')
        shape = rotate(shape, [0, 0, 180])
        shape = rotate(shape, self.key_rotation_offsets[3])
        t_off = self.key_translation_offsets[3]
        shape = translate(shape, (t_off[0], t_off[1]+self.key_diameter/2, t_off[2]))
        shape = rotate(shape, [0,0,-230])
        shape = self.track_place(shape)

        return shape

    def thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')
        return union([
            # self.mr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),
            self.mr_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
            # self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
            # self.br_place(rotate(shape, [0, 0, self.thumb_plate_br_rotation])),
        ])

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        return self.br_place(rotate(shape, [0, 0, self.thumb_plate_br_rotation]))
        # return []

    def thumb_fx_layout(self, shape):
        return union([])

    def thumbcaps(self, side='right'):
        t1 = self.thumb_1x_layout(sa_cap(1), cap=True)
        if not default_1U_cluster:
            t1.add(self.thumb_15x_layout(rotate(sa_cap(2), (0, 0, 90)), cap=True))
        return t1


    def tb_post_r(self):
        debugprint('post_r()')
        radius = ball_diameter/2 + ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [1.0*(radius - post_adj), 0.0*(radius - post_adj), 0]
                         )

    def tb_post_tr(self):
        debugprint('post_tr()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.5*(radius - post_adj), 0.866*(radius - post_adj), 0]
                         )


    def tb_post_tl(self):
        debugprint('post_tl()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-0.5*(radius - post_adj), 0.866*(radius - post_adj), 0]
                         )


    def tb_post_l(self):
        debugprint('post_l()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-1.0*(radius - post_adj), 0.0*(radius - post_adj), 0]
                         )

    def tb_post_bl(self):
        debugprint('post_bl()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-0.5*(radius - post_adj), -0.866*(radius - post_adj), 0]
                         )


    def tb_post_br(self):
        debugprint('post_br()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.5*(radius - post_adj), -0.866*(radius - post_adj), 0]
                         )

    # def thumb(self, side="right"):
    #     print('thumb()')
    #     shape = self.thumb_fx_layout(rotate(single_plate(side=side), [0.0, 0.0, -90]))
    #     shape = union([shape, self.thumb_fx_layout(double_plate())])
    #     shape = union([shape, self.thumb_1x_layout(single_plate(side=side))])
    #
    #     # shape = union([shape, trackball_layout(trackball_socket())])
    #     # shape = self.1x_layout(single_plate(side=side))
    #     return shape

    def thumb(self, side="right"):
        print('thumb()')
        shape = self.thumb_1x_layout(rotate(single_plate(side=side), (0, 0, -90)))
        shape = union([shape, self.thumb_15x_layout(rotate(single_plate(side=side), (0, 0, -90)))])
        # shape = union([shape, self.thumb_15x_layout(rotate(double_plate(), (0, 0, -90)))])
        # shape = union([shape, self.thumb_15x_layout(double_plate(), plate=False)])

        return shape

    def thumb_connectors(self, side="right"):
        print('thumb_connectors()')
        hulls = []

        # bottom 2 to tb
        hulls.append(
            triangle_hulls(
                [
                    self.track_place(self.tb_post_l()),
                    self.br_place(web_post_tl()),
                    self.track_place(self.tb_post_bl()),
                    self.br_place(web_post_tr()),
                    self.br_place(web_post_tl()),
                    self.track_place(self.tb_post_bl()),
                    self.br_place(web_post_tr()),
                    self.track_place(self.tb_post_br()),
                    self.br_place(web_post_tr()),
                    self.track_place(self.tb_post_br()),
                    self.mr_place(web_post_br()),
                    self.track_place(self.tb_post_r()),
                    self.mr_place(web_post_bl()),
                    self.mr_place(web_post_br()),
                    self.track_place(self.tb_post_r()),
                    self.mr_place(web_post_bl()),
                    self.track_place(self.tb_post_tr()),
                    key_place(web_post_bl(), 0, cornerrow),
                    self.track_place(self.tb_post_tl()),
                ]
            )
        )

        # bottom left
        # hulls.append(
        #     triangle_hulls(
        #         [
        #             self.bl_place(web_post_tr()),
        #             self.br_place(web_post_tl()),
        #             self.bl_place(web_post_br()),
        #             self.br_place(web_post_bl()),
        #         ]
        #     )
        # )

        # bottom right
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tr()),
                    self.mr_place(web_post_br()),
                    self.br_place(web_post_br()),
                    self.mr_place(web_post_tr()),
                ]
            )
        )
        # top right
        # hulls.append(
        #     triangle_hulls(
        #         [
        #             self.mr_place(web_post_bl()),
        #             self.mr_place(web_post_br()),
        #             self.mr_place(web_post_tl()),
        #             self.mr_place(web_post_tr()),
        #         ]
        #     )
        # )

        # hulls.append(
        #     triangle_hulls(
        #         [
        #             key_place(web_post_br(), 1, cornerrow),
        #             key_place(web_post_tl(), 2, lastrow),
        #             key_place(web_post_bl(), 2, cornerrow),
        #             key_place(web_post_tr(), 2, lastrow),
        #             key_place(web_post_br(), 2, cornerrow),
        #             key_place(web_post_bl(), 3, cornerrow),
        #         ]
        #     )
        # )

        hulls.append(
            triangle_hulls(
                [
                    self.mr_place(web_post_tl()),
                    key_place(web_post_br(), 1, lastrow),
                    key_place(web_post_bl(), 2, lastrow),
                    self.mr_place(web_post_tl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    key_place(web_post_tr(), 3, lastrow),
                    key_place(web_post_br(), 3, lastrow),
                    key_place(web_post_tr(), 3, lastrow),
                    key_place(web_post_bl(), 4, cornerrow),
                ]
            )
        )

        return union(hulls)

    def walls(self, side="right"):
        print('thumb_walls()')
        # thumb, walls
        shape = wall_brace(
            self.mr_place, .5, 1, web_post_tr(),
            (lambda sh: key_place(sh, 3, lastrow)), 0, -1, web_post_bl(),
        )
        shape = union([shape, wall_brace(
            self.mr_place, .5, 1, web_post_tr(),
            self.br_place, 0, -1, web_post_br(),
        )])
        shape = union([shape, wall_brace(
            self.br_place, 0, -1, web_post_br(),
            self.br_place, 0, -1, web_post_bl(),
        )])
        shape = union([shape, wall_brace(
            self.br_place, 0, -1, web_post_bl(),
            # self.bl_place, 0, -1, web_post_br(),
            self.br_place, -2, -1, web_post_bl(),
        )])
        # shape = union([shape, wall_brace(
        #     self.bl_place, 0, -1, web_post_br(),
        #     self.bl_place, -1, -1, web_post_bl(),
        # )])

        shape = union([shape, wall_brace(
            self.track_place, -1.5, 0, self.tb_post_tl(),
            (lambda sh: left_key_place(sh, lastrow - 1, -1, side=ball_side, low_corner=True)), -1, 0, web_post(),
        )])
        shape = union([shape, wall_brace(
            self.track_place, -1.5, 0, self.tb_post_tl(),
            self.track_place, -1, 0, self.tb_post_l(),
        )])
        shape = union([shape, wall_brace(
            self.track_place, -1, 0, self.tb_post_l(),
            self.br_place, -2, 0, web_post_tl(),
        )])
        shape = union([shape, wall_brace(
            self.br_place, -2, 0, web_post_tl(),
            self.br_place, -2, -1, web_post_bl(),
        )])

        return shape

    def connection(self, side='right'):
        print('thumb_connection()')
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        hulls = []
        hulls.append(
            triangle_hulls(
                [
                    key_place(web_post_bl(), 0, cornerrow),
                    left_key_place(web_post(), lastrow - 1, -1, side=side, low_corner=True),                # left_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True),
                    self.track_place(self.tb_post_tl()),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    key_place(web_post_bl(), 0, cornerrow),
                    self.mr_place(web_post_bl()),
                    key_place(web_post_br(), 0, cornerrow),
                    self.mr_place(web_post_tl()),
                    key_place(web_post_bl(), 1, cornerrow),
                    self.mr_place(web_post_tl()),
                    key_place(web_post_br(), 1, cornerrow),
                    self.mr_place(web_post_tr()),
                    key_place(web_post_tl(), 2, lastrow),
                    key_place(web_post_bl(), 2, lastrow),
                    self.mr_place(web_post_tl()),
                    key_place(web_post_bl(), 2, lastrow),
                    self.mr_place(web_post_tl()),
                    key_place(web_post_br(), 2, lastrow),
                    key_place(web_post_bl(), 3, lastrow),
                    self.mr_place(web_post_tr()),
                    self.mr_place(web_post_tl()),
                    key_place(web_post_br(), 2, lastrow),

                    # key_place(web_post_bl(), 3, lastrow),
                    # key_place(web_post_tr(), 2, lastrow),
                    # key_place(web_post_tl(), 3, lastrow),
                    # key_place(web_post_bl(), 3, cornerrow),
                    # key_place(web_post_tr(), 3, lastrow),
                    # key_place(web_post_br(), 3, cornerrow),
                    # key_place(web_post_bl(), 4, cornerrow),
                ]
            )
        )
        shape = union(hulls)
        return shape

    def screw_positions(self):
        position = self.thumborigin()
        position = list(np.array(position) + np.array([-72, -35, -16]))
        position[2] = 0

        return position
