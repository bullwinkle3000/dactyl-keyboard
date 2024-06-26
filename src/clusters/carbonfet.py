from clusters.default_cluster import DefaultCluster
import json
import os


class CarbonfetCluster(DefaultCluster):

    @staticmethod
    def name():
        return "CARBONFET"

    def get_config(self):
        with open(os.path.join("src", "clusters", "json", "CARBONFET.json"), mode='r') as fid:
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
        super().__init__(parent_locals)
        for item in parent_locals:
            globals()[item] = parent_locals[item]

    def tl_place(self, shape):
        shape = rotate(shape, [10, -24, 10])
        # shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-13, -9.8, 4])
        shape = self.thumb_place(shape)
        return shape

    def tl_wall(self, shape):
        return translate(self.tl_place(shape), (1.7, 1, 0))

    def tr_place(self, shape):
        shape = rotate(shape, [6, -25, 10])
        # shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-7.5, -29.5, 0])
        shape = self.thumb_place(shape)
        return shape


    def ml_place(self, shape):
        shape = rotate(shape, [8, -31, 14])
        # shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-30.5, -17, -6])
        shape = self.thumb_place(shape)
        return shape

    def mr_place(self, shape):
        shape = rotate(shape, [4, -31, 14])
        # shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-22.2, -41, -10.3])
        shape = self.thumb_place(shape)
        return shape

    def br_place(self, shape):
        shape = rotate(shape, [2, -37, 18])
        # shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-37, -46.4, -22])
        shape = self.thumb_place(shape)
        return shape

    def bl_place(self, shape):
        shape = rotate(shape, [6, -37, 18])
        # shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-47, -23, -19])
        shape = self.thumb_place(shape)
        return shape

    def thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')
        return union([
            self.tr_place(rotate(shape, [0, 0, thumb_plate_tr_rotation])),
            self.mr_place(rotate(shape, [0, 0, thumb_plate_mr_rotation])),
            self.br_place(rotate(shape, [0, 0, thumb_plate_br_rotation])),
            self.tl_place(rotate(shape, [0, 0, thumb_plate_tl_rotation])),
        ])

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        debugprint('thumb_15x_layout()')
        if plate:
            return union([
                self.bl_place(rotate(shape, [0, 0, thumb_plate_bl_rotation])),
                self.ml_place(rotate(shape, [0, 0, thumb_plate_ml_rotation]))
            ])
        else:
            return union([
                self.bl_place(shape),
                self.ml_place(shape)
            ])

    def thumbcaps(self, side='right'):
        t1 = self.thumb_1x_layout(sa_cap(1))
        t15 = self.thumb_15x_layout(rotate(sa_cap(1.5), [0, 0, rad2deg(pi / 2)]))
        return t1.add(t15)

    def thumb(self, side="right"):
        print('thumb()')
        shape = self.thumb_1x_layout(single_plate(side=side))
        shape = union([shape, self.thumb_15x_layout(double_plate_half(), plate=False)])
        shape = union([shape, self.thumb_15x_layout(single_plate(side=side))])

        return shape

    def thumb_connectors(self, side="right"):
        print('thumb_connectors()')
        hulls = []

        hulls.append(
            triangle_hulls(
                [
                    self.tl_wall(web_post_tl()),
                    self.tl_wall(web_post_tr()),
                    self.tl_place(web_post_tr()),
                    self.tl_place(web_post_tl()),
                    self.tl_wall(web_post_tl()),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_wall(web_post_tr()),
                    self.tl_wall(web_post_br()),
                    self.tl_place(web_post_br()),
                    self.tl_place(web_post_tr()),
                    self.tl_wall(web_post_tr()),
                ]
            )
        )

        # Top two
        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tl()),
                    self.tl_place(web_post_bl()),
                    self.ml_place(self.thumb_post_tr()),
                    self.ml_place(web_post_br()),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.ml_place(self.thumb_post_tl()),
                    self.ml_place(web_post_bl()),
                    self.bl_place(self.thumb_post_tr()),
                    self.bl_place(web_post_br()),
                ]
            )
        )

        # bottom two on the right
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tr()),
                    self.br_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.mr_place(web_post_bl()),
                ]
            )
        )

        # bottom two on the left
        hulls.append(
            triangle_hulls(
                [
                    self.mr_place(web_post_tr()),
                    self.mr_place(web_post_br()),
                    self.tr_place(web_post_tl()),
                    self.tr_place(web_post_bl()),
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    self.tr_place(web_post_br()),
                    self.tr_place(web_post_bl()),
                    self.mr_place(web_post_br()),
                ]
            )
        )

        # between top and bottom row
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tl()),
                    self.bl_place(web_post_bl()),
                    self.br_place(web_post_tr()),
                    self.bl_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.ml_place(web_post_bl()),
                    self.mr_place(web_post_tr()),
                    self.ml_place(web_post_br()),
                    self.tr_place(web_post_tl()),
                    self.tl_place(web_post_bl()),
                    self.tr_place(web_post_tr()),
                    self.tl_wall(web_post_br()),
                ]
            )
        )
        # top two to the main keyboard, starting on the left
        hulls.append(
            triangle_hulls(
                [
                    key_place(web_post_bl(), 0, cornerrow),
                    self.ml_place(self.thumb_post_tl()),
                    cluster_key_place(web_post_bl(), 0, cornerrow),

                    self.ml_place(self.thumb_post_tr()),
                    cluster_key_place(web_post_br(), 0, cornerrow),
                    self.tl_place(web_post_tl()),
                    cluster_key_place(web_post_bl(), 1, cornerrow),
                    self.tl_wall(web_post_tr()),
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_bl(), 2, lastrow),
                    cluster_key_place(web_post_bl(), 2, lastrow),
                    self.tl_wall(web_post_tr()),
                    cluster_key_place(web_post_bl(), 2, lastrow),
                    self.tl_wall(web_post_br()),
                    cluster_key_place(web_post_br(), 2, lastrow),
                    cluster_key_place(web_post_bl(), 3, lastrow),
                    self.tl_wall(web_post_br()),
                    self.tr_place(web_post_tr()),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 3, lastrow),
                    cluster_key_place(web_post_br(), 3, cornerrow),
                    cluster_key_place(web_post_bl(), 3, lastrow),
                    cluster_key_place(web_post_bl(), 3, cornerrow),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 2, lastrow),
                    cluster_key_place(web_post_br(), 2, lastrow),
                    cluster_key_place(web_post_bl(), 3, lastrow),
                    cluster_key_place(web_post_bl(), 3, lastrow),
                ]
            )
        )
        #
        hulls.append(
            triangle_hulls(
                [
                    self.tr_place(web_post_br()),
                    self.tr_place(web_post_tr()),
                    cluster_key_place(web_post_bl(), 3, lastrow),
                ]
            )
        )
        #
        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_bl(), 2, lastrow),
                    cluster_key_place(web_post_bl(), 2, cornerrow),
                    cluster_key_place(web_post_br(), 2, lastrow),
                    cluster_key_place(web_post_br(), 2, cornerrow),
                    cluster_key_place(web_post_bl(), 3, lastrow),
                    cluster_key_place(web_post_bl(), 3, cornerrow),
                ]
            )
        )
        #
        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 3, lastrow),
                    cluster_key_place(web_post_br(), 3, lastrow),
                    cluster_key_place(web_post_bl(), 4, lastrow),
                ]
            )
        )
        #
        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 3, lastrow),
                    cluster_key_place(web_post_br(), 3, cornerrow),
                    cluster_key_place(web_post_bl(), 4, lastrow),
                ]
            )
        )

        return union(hulls)

    def walls(self, side="right"):
        print('thumb_walls()')
        # thumb, walls
        shape = union([wall_brace(self.mr_place, 0, -1, web_post_br(), self.tr_place, 0, -1, web_post_br())])
        shape = union([shape, wall_brace(self.mr_place, 0, -1, web_post_br(), self.mr_place, 0, -1.15, web_post_bl())])
        shape = union([shape, wall_brace(self.br_place, 0, -1, web_post_br(), self.br_place, 0, -1, web_post_bl())])
        shape = union(
            [shape, wall_brace(self.bl_place, -.3, 1, self.thumb_post_tr(), self.bl_place, 0, 1, self.thumb_post_tl())])
        shape = union([shape, wall_brace(self.br_place, -1, 0, web_post_tl(), self.br_place, -1, 0, web_post_bl())])
        shape = union(
            [shape, wall_brace(self.bl_place, -1, 0, self.thumb_post_tl(), self.bl_place, -1, 0, web_post_bl())])
        # thumb, corners
        shape = union([shape, wall_brace(self.br_place, -1, 0, web_post_bl(), self.br_place, 0, -1, web_post_bl())])
        shape = union(
            [shape, wall_brace(self.bl_place, -1, 0, self.thumb_post_tl(), self.bl_place, 0, 1, self.thumb_post_tl())])
        # thumb, tweeners
        shape = union([shape, wall_brace(self.mr_place, 0, -1.15, web_post_bl(), self.br_place, 0, -1, web_post_br())])
        shape = union([shape, wall_brace(self.bl_place, -1, 0, web_post_bl(), self.br_place, -1, 0, web_post_tl())])
        shape = union([shape,
                       wall_brace(self.tr_place, 0, -1, web_post_br(), (lambda sh: cluster_key_place(sh, 3, lastrow)), 0, -1,
                                  web_post_bl())])
        return shape

    def connection(self, side='right'):
        print('thumb_connection()')
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        shape = bottom_hull(
            [
                left_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                left_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                self.bl_place(translate(self.thumb_post_tr(), wall_locate2(-0.3, 1))),
                self.bl_place(translate(self.thumb_post_tr(), wall_locate3(-0.3, 1))),
            ]
        )

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               self.bl_place(translate(self.thumb_post_tr(), wall_locate2(-0.3, 1))),
                               self.bl_place(translate(self.thumb_post_tr(), wall_locate3(-0.3, 1))),
                               self.ml_place(self.thumb_post_tl()),
                           ]
                       )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_key_place(web_post(), cornerrow, -1, low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               self.ml_place(self.thumb_post_tl()),
                           ]
                       )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_key_place(web_post(), cornerrow, -1, low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               key_place(web_post_bl(), 0, cornerrow),
                               self.ml_place(self.thumb_post_tl()),
                           ]
                       )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               self.bl_place(self.thumb_post_tr()),
                               self.bl_place(translate(self.thumb_post_tr(), wall_locate1(-0.3, 1))),
                               self.bl_place(translate(self.thumb_post_tr(), wall_locate2(-0.3, 1))),
                               self.bl_place(translate(self.thumb_post_tr(), wall_locate3(-0.3, 1))),
                               self.ml_place(self.thumb_post_tl()),
                           ]
                       )])

        return shape

    def screw_positions(self):
        position = self.thumborigin()
        position = list(np.array(position) + np.array([-25, -57, 0]))
        position[2] = 0

        return position
