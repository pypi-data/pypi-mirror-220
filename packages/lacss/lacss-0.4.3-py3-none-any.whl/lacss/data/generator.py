""" Common data generators.
"""
from __future__ import annotations

import glob
import json
import typing as tp
from functools import partial
from os.path import join

import imageio.v2 as imageio
import numpy as np
import tensorflow as tf
from skimage.measure import regionprops


# A adaptation of tf.image.crop_and_resize to use edge-based indexing
# Edge-based indexing is more accurate for float-value bboxes
# i.e. value (0, 0) refers to the top-left cornor (not center) of the top-left pixel
def _crop_and_resize(masks, boxes, target_shape):
    box_h = boxes[:, 2] - boxes[:, 0]
    box_w = boxes[:, 3] - boxes[:, 1]
    dh = box_h / target_shape[0] / 2
    dw = box_w / target_shape[1] / 2
    boxes = tf.stack([dh, dw, -dh, -dw], axis=-1) + boxes - 0.5
    H, W = masks.shape[1:3]
    segs = tf.image.crop_and_resize(
        masks[..., None],
        boxes / [H - 1, W - 1, H - 1, W - 1],
        tf.range(len(boxes)),
        target_shape,
    )
    return tf.squeeze(segs, axis=-1)


def coco_generator_full(
    annotation_file: str,
    image_path: str,
    mask_shape: tp.Optional[tp.Tuple[int, int]] = None,
):
    """A generator function to produce coco-annotated data

    Args:
        annotation_file: Path to coco annotation files
        image_path: Path to image directory
        mask_shape: If supplied, all the instance segmentations will be croped and resized to the specifed size. Otherwise,
            the segmentations are uncropped (in original image size)

    Yields:
        A data dictionary.
            * id: data id
            * filename: image filename
            * image: an array [H, W, C]
            * masks: segmentation masks. [N, H, W] or [N,] + mask_shape
            * centroids: yx format.
            * bboxes: y0x0y1x1 format.
            * label: an array [H, W] representing pixel labels of all instances.

    """

    from pycocotools.coco import COCO

    coco = COCO(annotation_file=annotation_file)
    for imgid in coco.getImgIds():
        imginfo = coco.imgs[imgid]
        bboxes = []
        locs = []
        masks = []
        # segs = []
        for ann_id in coco.getAnnIds(imgIds=imgid):
            ann = coco.anns[ann_id]
            bbox = ann["bbox"]
            bbox = np.array([bbox[1], bbox[0], bbox[1] + bbox[3], bbox[0] + bbox[2]])
            bboxes.append(bbox)

            mask = coco.annToMask(ann)
            masks.append(mask)

            mi = np.stack(np.where(mask >= 0.5), axis=-1)
            locs.append(mi.mean(axis=0) + 0.5)

        bboxes = np.array(bboxes, dtype="float32")
        locs = np.array(locs, dtype="float32")
        masks = np.array(masks, dtype="float32")

        filepath = glob.glob(join(image_path, "**", imginfo["file_name"]))
        assert len(filepath) == 1
        image = imageio.imread(filepath[0])

        if len(image.shape) == 2:
            image = image[:, :, None]
        image = (image / 255.0).astype("float32")

        img_h, img_w, _ = image.shape
        bboxes = np.clip(
            bboxes / [img_h, img_w, img_h, img_w],
            0.0,
            1.0,
        ) * [img_h, img_w, img_h, img_w]
        bboxes = bboxes.astype("float32")

        locs = np.clip(
            locs / [img_h, img_w],
            0.0,
            1.0,
        ) * [img_h, img_w]
        locs = locs.astype("float32")

        if mask_shape is not None:
            segs = _crop_and_resize(masks, bboxes, mask_shape).numpy()
        else:
            segs = masks

        n_cells = masks.shape[0]
        masks = masks.astype("int32") * np.arange(1, n_cells + 1).reshape(n_cells, 1, 1)
        label = masks.max(axis=0).astype("int32")

        yield {
            "id": imgid,
            "filename": imginfo["file_name"],
            "image": image,
            "masks": segs,
            "centroids": locs,
            "bboxes": bboxes,
            "label": label,
        }


def coco_generator(annotation_file, image_path):
    from pycocotools.coco import COCO

    coco = COCO(annotation_file=annotation_file)
    for imgid in coco.getImgIds():
        imginfo = coco.imgs[imgid]
        bboxes = []
        segs = []
        for ann_id in coco.getAnnIds(imgIds=imgid):
            ann = coco.anns[ann_id]
            bbox = ann["bbox"]
            bbox = [bbox[1], bbox[0], bbox[1] + bbox[3], bbox[0] + bbox[2]]
            bboxes.append(bbox)

            seg = np.reshape(coco.anns[ann_id]["segmentation"], [-1, 2])
            segs.append(seg)

        filepath = glob.glob(join(image_path, "**", imginfo["file_name"]))
        assert len(filepath) == 1

        image = imageio.imread(filepath[0])

        if len(image.shape) == 2:
            image = image[:, :, None]
        image = (image / 255.0).astype("float32")

        yield {
            "id": imgid,
            "filename": imginfo["file_name"],
            "image": image,
            "bboxes": bboxes,
            "polygons": segs,
        }


def dataset_from_coco_annotations(
    annotation_file: str,
    image_path: str,
    image_shape: tuple = [None, None, 3],
    mask_shape: tuple = [48, 48],
):
    """Obtaining a tensowflow dataset from coco annotations. See [coco_generator_full()](api/lacss.data#lacss.data.coco_generator_full)

    Args:
        annotation_file: Path to coco annotation files
        image_path: Path to image directory
        image_shape: The expect image shapes. Use None to represent variable dimensions.
        mask_shape: If supplied, all the instance segmentations will be croped and resized to the specifed size. Otherwise,
            the segmentations are uncropped (in original image size)

    Returns:
        A tensorflow dataset.

    """
    if mask_shape is None:
        mask_spec = tf.TensorSpec([None] + image_shape[:2], dtype=tf.float32)
    else:
        mask_spec = tf.TensorSpec([None] + mask_shape, dtype=tf.float32)

    return tf.data.Dataset.from_generator(
        lambda: coco_generator_full(annotation_file, image_path, mask_shape=mask_shape),
        output_signature={
            "id": tf.TensorSpec([], dtype=tf.int64),
            "filename": tf.TensorSpec([], dtype=tf.string),
            "image": tf.TensorSpec(image_shape, dtype=tf.float32),
            "masks": mask_spec,
            "centroids": tf.TensorSpec([None, 2], dtype=tf.float32),
            "bboxes": tf.TensorSpec([None, 4], dtype=tf.float32),
            "label": tf.TensorSpec(image_shape[:2], dtype=tf.int32),
        },
    )


def simple_generator(annotation_file: str, image_path: str):
    """A simple generator function to produce image data labeled with points and image-level segmentaion.

    Args:
        annotation_file: Path to the json format annotation file.
        image_path: Path to the image directory.

    Yields:
        Data dictionary:
            * img_id: data id
            * image: an array [H, W, C]
            * image_mask: segmentation masks for the image. [H, W]
            * centroids: yx format.
    """

    with open(annotation_file, "r") as f:
        annotations = json.load(f)

    for k, ann in enumerate(annotations):
        image = imageio.imread(join(image_path, ann["image_file"]))
        if len(image.shape) == 2:
            image = image[:, :, None]
        image = (image / 255.0).astype("float32")

        binary_mask = imageio.imread(join(image_path, ann["mask_file"]))

        if len(binary_mask.shape) == 3:
            binary_mask = binary_mask[:, :, 0]
        binary_mask = (binary_mask > 0).astype("float32")

        locations = np.array(ann["locations"]).astype("float32")

        if "img_id" in ann:
            img_id = ann["img_id"]
        else:
            img_id = k

        yield {
            "img_id": img_id,
            "image": image,
            "image_mask": binary_mask,
            "centroids": locations,
        }


def dataset_from_simple_annotations(
    annotation_file, image_path, image_shape=[None, None, 3], **kwargs
):
    """Obtaining a tensowflow dataset from simple annotatiion. See [simple_generator()](/api/lacss.data#lacss.data.simple_generator)

    Args:
        annotation_file: Path to the json format annotation file.
        image_path: Path to the image directory.
        image_shape: The expect image shapes. Use None to represent variable dimensions.

    Returns:
        A tensorflow dataset object

    """
    return tf.data.Dataset.from_generator(
        lambda: simple_generator(annotation_file, image_path, **kwargs),
        output_signature={
            "img_id": tf.TensorSpec([], dtype=tf.int64),
            "image": tf.TensorSpec(image_shape, dtype=tf.float32),
            "image_mask": tf.TensorSpec(image_shape[:2], dtype=tf.float32),
            "centroids": tf.TensorSpec([None, 2], dtype=tf.float32),
        },
    )


def img_mask_pair_generator(ds_files):
    """A generator function to produce image data labeled with segmentation labels.
        In this case, one has paired input images and label images as files on disk.

    Args:
        ds_file: A tuple of (image_list, label_list).
            The image_list are pathes to images. The label_list are pathes to labels.

    Yields:
        Data dictionary:
            * img_id: data id
            * image: an array [H, W, C]
            * centroids: yx format.
            * bboxes: y0x0y1x1 format.
            * label: an array [H, W] representing pixel labels of all instances.
    """
    for k, (img_file, mask_file) in enumerate(ds_files):
        img = imageio.imread(img_file).astype("float32")
        img /= 255
        if len(img.shape) == 2:
            img = img[:, :, None]

        mask = imageio.imread(mask_file)
        if len(mask.shape) == 3:
            mask = mask[:, :, 0]

        bboxes = []
        locs = []
        for prop in regionprops(mask):
            bboxes.append(prop["bbox"])
            locs.append(prop["centroid"])

        yield {
            "img_id": k,
            "image": img.astype("float32"),
            "centroids": np.asarray(locs, dtype="float32") + 0.5,
            "bboxes": np.asarray(bboxes),
            "label": mask,
        }


def dataset_from_img_mask_pairs(
    imgfiles, maskfiles, image_shape=[None, None, 3], **kwargs
):
    """Obtaining a tensowflow dataset from image/label pairs.
            See [img_mask_pair_generator()](/api/lacss.data#lacss.data.img_mask_pair_generator)

    Args:
        imgfiles: List of file pathes to input image file.
        maskfiles: List of file pathes to label image file.
        image_shape: The expect image shapes. Use None to represent variable dimensions.

    Returns:
        A tensorflow dataset object
    """
    return tf.data.Dataset.from_generator(
        lambda: img_mask_pair_generator(zip(imgfiles, maskfiles), **kwargs),
        output_signature={
            "img_id": tf.TensorSpec([], dtype=tf.int64),
            "image": tf.TensorSpec(image_shape, dtype=tf.float32),
            "centroids": tf.TensorSpec([None, 2], dtype=tf.float32),
            "bboxes": tf.TensorSpec([None, 4], dtype=tf.float32),
            "label": tf.TensorSpec(image_shape[:2], dtype=tf.int32),
        },
    )
