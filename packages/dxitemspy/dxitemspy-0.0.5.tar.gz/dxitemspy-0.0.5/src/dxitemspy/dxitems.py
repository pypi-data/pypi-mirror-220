import json
import csv
import re
from pkg_resources import resource_filename as rscfn
class DXIEngine:

    def __init__(self):

        self.dxi_mapping = {}
        self.dxi_metadata = {}
        fn_mapping = rscfn(__name__, 'dxi_mapping.json')
        with open(fn_mapping, "r") as fp:
            self.dxi_mapping = json.load(fp)   
        fn_metadata = rscfn(__name__, 'dxi_metadata.json')
        with open(fn_metadata, "r") as fp:
            self.dxi_metadata = json.load(fp)   

    def get_dxi(self, dx_lst):

        dx2dxi = {} 
        labels = []
        for dx in set(dx_lst):
            if dx in self.dxi_mapping:
                dx2dxi[dx] = self.dxi_mapping[dx]["labels"][:]
                labels += dx2dxi[dx]
        
        labels = list(set(labels))
        lb2meta = {}
        score = 0.0
        for lb in labels:
            if lb in self.dxi_metadata:
                lb2meta[lb] = self.dxi_metadata[lb]
                if lb2meta[lb].get("has_default_coeff", False):
                    score = lb2meta[lb].get("score", 0)

        out = {"labels": labels,
                "labels_info": lb2meta,
                "dx2dxi": dx2dxi,
                "score": score}

        return out



