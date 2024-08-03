from geom import *
from common import *
from part import Part


class TrackballPart(Part):

    def __init__(self, parent_locals, trackball_type="ceramic"):
        super().__init__("trackball")
        self.type = trackball_type
        if parent_locals is not None:
            for item in parent_locals:
                globals()[item] = parent_locals[item]
        self.width = 40
        self.height = 40

    def tl(self):
        x = np.sin(-np.pi / 4) * (-self.width / 2)
        y = np.cos(-np.pi / 4) * (self.width / 2)
        return self.offset_point([x, y, 0])

    def bl(self):
        x = np.sin(np.pi / 4) * (-self.width / 2)
        y = np.cos(np.pi / 4) * (-self.width / 2)
        return self.offset_point([x, y, 0])

    def tr(self):
        x = np.sin(-np.pi / 4) * (self.width / 2)
        y = np.cos(-np.pi / 4) * (self.width / 2)
        return self.offset_point([x, y, 0])

    def br(self):
        x = np.sin(np.pi / 4) * (self.width / 2)
        y = np.cos(np.pi / 4) * (-self.width / 2)
        return self.offset_point([x, y, 0])



