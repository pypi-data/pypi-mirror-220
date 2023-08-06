"""
Folder structure:

/root
    images/
        img_1.jpg
        img_2.jpg
        ...
    labels/
        _coco.json       <input>
        _coco_train.json <output>
        _coco_val.json   <output>
        _coco_test.json  <output>
        ...
"""

import os
import json
import random

from .splitter import Splitter


class CocoSplitter(Splitter):
    def __init__(
        self,
        root: str,  # root directory of the dataset, e.g. niche_cv/detection/data/balloon
        ratio_train: float = 0.64,
        ratio_val: float = 0.16,
        ratio_test: float = 0.2,
    ):
        super().__init__(root, ratio_train, ratio_val, ratio_test)
        self.dir_labels = os.path.join(self.root, "labels")
        self._set_dataset()

    def shuffle_train_test(self):
        """
        shuffle all ids into lists of train, val, and test
        """
        random.shuffle(self.ids)
        n = len(self.ids)
        n_train = int(self.ratio_train * n)
        n_val = int(self.ratio_val * n)
        # assignment
        self.id_train = self.ids[:n_train]
        self.id_val = self.ids[n_train : n_train + n_val]
        self.id_test = self.ids[n_train + n_val :]

    def write_dataset(self, name_json: str = "_coco"):
        dict_id = dict(
            train=self.id_train,
            val=self.id_val,
            test=self.id_test,
        )
        for split in dict_id:
            json_out = make_json(image_ids=dict_id[split], coco_annot=self.config)
            path_out = os.path.join(
                self.dir_labels, "{}_{}.json".format(name_json, split)
            )
            with open(path_out, "w") as f:
                json.dump(json_out, f)

    def _get_ids(self):
        return [img["id"] for img in self.config["images"]]

    def _set_dataset(self, name_json: str = "_coco"):
        """
        name_json: str
            name of the json file, e.g. _coco
        """
        # read or open the config file
        path_json = os.path.join(self.dir_labels, name_json + ".json")
        with open(path_json, "r") as f:
            coco_annot = json.load(f)

        # set ids from the config file
        self.config = coco_annot
        self._set_ids()


def make_json(image_ids: list, coco_annot: dict) -> dict:
    json_out = dict(
        info=coco_annot["info"],
        licenses=coco_annot["licenses"],
        images=[],
        annotations=[],
        categories=coco_annot["categories"],
    )
    for img in coco_annot["images"]:
        if img["id"] in image_ids:
            json_out["images"].append(img)
    for ann in coco_annot["annotations"]:
        if ann["image_id"] in image_ids:
            json_out["annotations"].append(ann)
    return json_out
