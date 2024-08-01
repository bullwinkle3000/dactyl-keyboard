
from default_cluster import  DefaultCluster
import json, os
class KeypadCluster(DefaultCluster):

    keys = []
    @staticmethod
    def name():
        return "KEYPAD_CLUSTER"

    def __init__(self, parent_locals):
        super().__init__(parent_locals)
        for item in parent_locals:
            globals()[item] = parent_locals[item]

        self.build_keys()

    def build_keys(self):



