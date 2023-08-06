"""
Take labels/_coco.json as input and split it into train, val, and test.
"""

from splitter.coco import COCO_Splitter
import os


def main():
    dir_root = os.path.join(os.path.dirname(__file__), "balloon", "labels")
    splitter = COCO_Splitter(dir_root=dir_root)
    splitter.shuffle_train_test()
    splitter.write_dataset()


if __name__ == "__main__":
    main()
