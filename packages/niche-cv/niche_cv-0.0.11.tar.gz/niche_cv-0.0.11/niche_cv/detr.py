import os
import json
import numpy as np
from torch.utils import data
from transformers import (
    DetrConfig,
    DetrModel,
    DetrForObjectDetection,
    DetrImageProcessor,
)

# local imports
from detection.data.loaders.coco import CocoDetectionDataModule
from detection.data.splitter.coco import CocoSplitter
from detection.models.detr import Detr

BACKBONE = "facebook/detr-resnet-50"
DIR_DATA = os.path.join(os.path.dirname(__file__), "detection", "data", "balloon")

# DETR fine-tuning note
# https://github.com/NielsRogge/Transformers-Tutorials/blob/master/DETR/Fine_tuning_DetrForObjectDetection_on_custom_dataset_(balloon).ipynb
# https://huggingface.co/docs/transformers/main/en/main_classes/configuration#transformers.PretrainedConfig

# shuffle the dataset
splitter = CocoSplitter(DIR_DATA)
splitter.shuffle_train_test()
splitter.write_dataset()

# load the dataset
processor = DetrImageProcessor.from_pretrained(BACKBONE)
data_module = CocoDetectionDataModule(DIR_DATA, processor, batch_size=4)
data_module.setup()
id2label = {k: v["name"] for k, v in data_module.train.coco.cats.items()}

# check the batch
batch = next(iter(data_module.train_dataloader()))
batch.keys()
# pixel_values, target = data_module.train[0]

# model
model = Detr(BACKBONE, len(id2label))
outputs = model(pixel_values=batch["pixel_values"], pixel_mask=batch["pixel_mask"])
outputs.logits.shape

from visualization.coco import show_dataset

show_dataset(train_dataset)

train_dataset.coco.getImgIds()


config = DetrConfig.from_pretrained(BACKBONE, num_labels=1)

model = DetrModel(config)
model.config.hidden_size

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")

model.train()
