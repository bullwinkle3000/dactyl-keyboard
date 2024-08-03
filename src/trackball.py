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

