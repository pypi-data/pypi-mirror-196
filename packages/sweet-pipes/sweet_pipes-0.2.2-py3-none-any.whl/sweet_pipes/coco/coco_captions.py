from __future__ import annotations

import os
from collections import defaultdict
from typing import Dict, List, Optional, Sequence, Tuple

import torch
from PIL import Image
from torchdata.datapipes.iter import IterableWrapper, IterDataPipe

from sweet_pipes.coco.common import ParallelSampleDownloader, get_coco_captions_json

CACHE_DIR = os.path.join(torch.hub.get_dir(), "coco")


def _get_captions_by_image_id(annotations: Sequence[Dict]) -> Dict[int, List[str]]:
    out: Dict[int, List[str]] = defaultdict(list)
    for ann in annotations:
        image_id = ann["image_id"]
        out[image_id].append(ann["caption"])

    return out


def coco_captions(
    split: str = "train",
    buffer_size: int = 128,
    shuffle: bool = False,
    cache_dir: Optional[str] = CACHE_DIR,
) -> IterDataPipe[Tuple[Image.Image, List[str]]]:
    captions_json = get_coco_captions_json(split=split)
    images, annotations = captions_json["images"], captions_json["annotations"]
    captions_by_image_id = _get_captions_by_image_id(annotations)
    images_with_captions = [
        (image["coco_url"], captions_by_image_id[image["id"]]) for image in images
    ]

    pipe: IterDataPipe = IterableWrapper(images_with_captions, deepcopy=False)
    if shuffle:
        pipe = pipe.shuffle()

    pipe = pipe.sharding_filter()
    pipe = pipe.batch(buffer_size)
    pipe = ParallelSampleDownloader(pipe, cache_dir=cache_dir)
    pipe = pipe.unbatch()

    return pipe
