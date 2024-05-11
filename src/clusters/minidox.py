from clusters.default_cluster import DefaultCluster
import os
import json


class MinidoxCluster(DefaultCluster):
    minidox_Usize = 1.6

    @staticmethod
    def name():
        return "MINIDOX"

    def get_config(self):
        with open(os.path.join("src", "clusters", "json", "MINIDOX.json"), mode='r') as fid:
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
        self.num_keys = 3
        super().__init__(parent_locals)
        # have to repeat this for all classes/namespaces
        for item in parent_locals:
            globals()[item] = parent_locals[item]

    def thumborigin(self):
        # debugprint('thumborigin()')
        origin = super().thumborigin()
        origin[1] = origin[1] - .4 * (trackball_Usize - 1) * sa_length
        return origin

    def tl_place(self, shape):
        shape = rotate(shape, [10, -23, 25])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-35, -16, -2])
        return shape

    def tr_place(self, shape):
        shape = rotate(shape, [14, -15, 10])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-15, -10, 5])
        return shape

    def ml_place(self, shape):
        shape = rotate(shape, [6, -34, 40])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-53, -26, -12])
        return shape

    def mr_place(self, shape):
        shape = rotate(shape, [10, -23, 25])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-23, -34, -6])
        return shape

    def br_place(self, shape):
        shape = rotate(shape, [6, -32, 35])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-51, -25, -11.5])
        return shape

    def bl_place(self, shape):
        shape = rotate(shape, [6, -32, 35])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-51, -25, -11.5])
        return shape

    def fl_place(self, shape):
        shape = rotate(shape, [0, -32, 40])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-25, -45, -15.5])
        return shape

    def thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')
        return union([
            self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),
            self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation])),
            self.ml_place(rotate(shape, [0, 0, self.thumb_plate_ml_rotation])),
        ])

    def thumb_fx_layout(self, shape):
        return union([
            self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),
            self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation])),
            self.ml_place(rotate(shape, [0, 0, self.thumb_plate_ml_rotation])),
            # self.fl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
        ])

    # def thumb_15x_layout(self, shape, cap=False, plate=True):
    #     debugprint('thumb_15x_layout()')
    #     if plate:
    #         return union([
    #             self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
    #             self.ml_place(rotate(shape, [0, 0, self.thumb_plate_ml_rotation]))
    #         ])
    #     else:
    #         return union([
    #             self.bl_place(shape),
    #             self.ml_place(shape)
    #         ])

    def thumbcaps(self, side='right'):
        t1 = self.thumb_1x_layout(sa_cap(1))
        return t1

    def thumb(self, side="right"):
        print('thumb()')
        shape = self.thumb_fx_layout(rotate(single_plate(side=side), [0.0, 0.0, -90]))
        shape = union([shape, self.thumb_fx_layout(adjustable_plate(self.minidox_Usize))])

        return shape

    def thumb_post_tr(self):
        debugprint('thumb_post_tr()')
        return translate(web_post(),
                         [(mount_width / 2) - post_adj, ((mount_height/2) + adjustable_plate_size(self.minidox_Usize)) - post_adj, 0]
                         )

    def thumb_post_tl(self):
        debugprint('thumb_post_tl()')
        return translate(web_post(),
                         [-(mount_width / 2) + post_adj, ((mount_height/2) + adjustable_plate_size(self.minidox_Usize)) - post_adj, 0]
                         )

    def thumb_post_bl(self):
        debugprint('thumb_post_bl()')
        return translate(web_post(),
                         [-(mount_width / 2) + post_adj, -((mount_height/2) + adjustable_plate_size(self.minidox_Usize)) + post_adj, 0]
                         )

    def thumb_post_br(self):
        debugprint('thumb_post_br()')
        return translate(web_post(),
                         [(mount_width / 2) - post_adj, -((mount_height/2) + adjustable_plate_size(self.minidox_Usize)) + post_adj, 0]
                         )

    def thumb_connectors(self, side="right"):
        print('thumb_connectors()')
        hulls = []

        # Top two
        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(self.thumb_post_tr()),
                    self.tl_place(self.thumb_post_br()),
                    self.tr_place(self.thumb_post_tl()),
                    self.tr_place(self.thumb_post_bl()),
                ]
            )
        )

        # bottom two on the right
        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(self.thumb_post_tl()),
                    self.tl_place(self.thumb_post_bl()),
                    self.ml_place(self.thumb_post_tr()),
                    self.ml_place(self.thumb_post_br()),
                ]
            )
        )


        # top two to the main keyboard, starting on the left
        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(self.thumb_post_tl()),
                    cluster_key_place(web_post_bl(), 0, cornerrow),
                    self.tl_place(self.thumb_post_tr()),
                    cluster_key_place(web_post_br(), 0, cornerrow),
                    self.tr_place(self.thumb_post_tl()),
                    cluster_key_place(web_post_bl(), 1, cornerrow),
                    self.tr_place(self.thumb_post_tr()),
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_tl(), 2, lastrow),
                    cluster_key_place(web_post_bl(), 2, lastrow),
                    self.tr_place(self.thumb_post_tr()),
                    cluster_key_place(web_post_bl(), 2, lastrow),
                    self.tr_place(self.thumb_post_br()),
                    cluster_key_place(web_post_br(), 2, lastrow),
                    cluster_key_place(web_post_bl(), 3, lastrow),
                    cluster_key_place(web_post_tr(), 2, lastrow),
                    cluster_key_place(web_post_tl(), 3, lastrow),
                    cluster_key_place(web_post_bl(), 3, cornerrow),
                    cluster_key_place(web_post_tr(), 3, lastrow),
                    cluster_key_place(web_post_br(), 3, cornerrow),
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_tr(), 3, lastrow),
                    cluster_key_place(web_post_br(), 3, lastrow),
                    cluster_key_place(web_post_bl(), 4, cornerrow),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_tr(), 3, lastrow),
                    cluster_key_place(web_post_br(), 3, cornerrow),
                    cluster_key_place(web_post_bl(), 4, cornerrow),
                ]
            )
        )
        hulls.append(
            triangle_hulls(
                [
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_tl(), 2, lastrow),
                    cluster_key_place(web_post_bl(), 2, cornerrow),
                    cluster_key_place(web_post_tr(), 2, lastrow),
                    cluster_key_place(web_post_br(), 2, cornerrow),
                    cluster_key_place(web_post_bl(), 3, cornerrow),
                ]
            )
        )

        return union(hulls)

    def walls(self, side="right"):
        print('thumb_walls()')
        # thumb, walls
        shape = union([wall_brace(self.tr_place, 0, -1, self.thumb_post_br(), self.tr_place, 0, -1, self.thumb_post_bl())])
        shape = union([shape, wall_brace(self.tr_place, 0, -1, self.thumb_post_bl(), self.tl_place, 0, -1, self.thumb_post_br())])
        shape = union([shape, wall_brace(self.tl_place, 0, -1, self.thumb_post_br(), self.tl_place, 0, -1, self.thumb_post_bl())])
        shape = union([shape, wall_brace(self.tl_place, 0, -1, self.thumb_post_bl(), self.ml_place, -1, -1, self.thumb_post_br())])
        shape = union([shape, wall_brace(self.ml_place, -1, -1, self.thumb_post_br(), self.ml_place, 0, -1, self.thumb_post_bl())])
        shape = union([shape, wall_brace(self.ml_place, 0, -1, self.thumb_post_bl(), self.ml_place, -1, 0, self.thumb_post_bl())])
        # thumb, corners
        shape = union([shape, wall_brace(self.ml_place, -1, 0, self.thumb_post_bl(), self.ml_place, -1, 0, self.thumb_post_tl())])
        shape = union([shape, wall_brace(self.ml_place, -1, 0, self.thumb_post_tl(), self.ml_place, 0, 1, self.thumb_post_tl())])
        # thumb, tweeners
        shape = union([shape, wall_brace(self.ml_place, 0, 1, self.thumb_post_tr(), self.ml_place, 0, 1, self.thumb_post_tl())])
        shape = union([shape, wall_brace(self.tr_place, 0, -1, self.thumb_post_br(), (lambda sh: cluster_key_place(sh, 3, lastrow)), 0, -1, web_post_bl())])

        return shape

    def connection(self, side='right'):
        print('thumb_connection()')
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        shape = union([bottom_hull(
            [
                left_cluster_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                left_cluster_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                self.bl_place(translate(self.thumb_post_tr(), wall_locate2(-0.3, 1))),
                self.bl_place(translate(self.thumb_post_tr(), wall_locate3(-0.3, 1))),
            ]
        )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_cluster_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                               left_cluster_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                               self.ml_place(translate(self.thumb_post_tr(), wall_locate2(-0.3, 1))),
                               self.ml_place(translate(self.thumb_post_tr(), wall_locate3(-0.3, 1))),
                               self.tl_place(self.thumb_post_tl()),
                           ]
                       )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_cluster_key_place(web_post(), cornerrow, -1, low_corner=True, side=side),
                               left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                               left_cluster_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                               left_cluster_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                               self.tl_place(self.thumb_post_tl()),
                           ]
                       )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_cluster_key_place(web_post(), cornerrow, -1, low_corner=True, side=side),
                               left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                               cluster_key_place(web_post_bl(), 0, cornerrow),
                               # cluster_key_place(translate(web_post_bl(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True),
                               self.tl_place(self.thumb_post_tl()),
                           ]
                       )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               self.ml_place(self.thumb_post_tr()),
                               self.ml_place(translate(self.thumb_post_tr(), wall_locate1(0, 1))),
                               self.ml_place(translate(self.thumb_post_tr(), wall_locate2(0, 1))),
                               self.ml_place(translate(self.thumb_post_tr(), wall_locate3(0, 1))),
                               self.tl_place(self.thumb_post_tl()),
                           ]
                       )])

        return shape

    def screw_positions(self):
        position = self.thumborigin()
        position = list(np.array(position) + np.array([-37, -32, -16]))
        position[1] = position[1] - .4 * (self.minidox_Usize - 1) * sa_length
        position[2] = 0

        return position
