from functools import partial

import jax
import jax.numpy as jnp
import optax

from ..ops import sub_pixel_samples
from ..train.loss import Loss

EPS = jnp.finfo("float32").eps


def _mean_over_boolean_mask(loss, mask):
    mask = mask.reshape(mask.shape[0], 1)
    n_instances = jnp.count_nonzero(mask) + EPS

    loss = loss.reshape(loss.shape[0], -1)
    loss = loss.mean(axis=1, keepdims=True).sum(where=mask)
    loss /= n_instances

    return loss


def supervised_instance_loss(preds, labels, **kwargs):
    """LACSS instance loss, supervised with segmentation label

    Args:
        preds: Model predictions
        labels: Label dictionary. Two types of segmentation labels are accepted.
            If ```labels["gt_labels"]``` is provided, its value is treated as pixel
            labels of the image. Otherwisde, one much supply both ```labels["gt_bboxes"]```
            and ```labels["gt_masks"]```. The gt_masks is a 3D array representing all
            segmentation resized to a fixed dimension.
    """

    instance_mask = preds["instance_mask"]
    instance_logit = preds["instance_logit"]
    yc = preds["instance_yc"]
    xc = preds["instance_xc"]

    if not isinstance(labels, dict):
        labels = dict(gt_labels=labels)

    if "gt_labels" in labels:  # labeled with image label
        gt_labels = labels["gt_labels"].astype("int32")

        n_patches, ps, _ = yc.shape

        gt_labels = jnp.pad(gt_labels, ps // 2)
        gt_patches = gt_labels[yc + ps // 2, xc + ps // 2] == (
            jnp.arange(n_patches)[:, None, None] + 1
        )
        gt_patches = gt_patches.astype("float32")

    else:  # labeled with bboxes and rescaled segmentation masks, ie, coco
        y0, x0, y1, x1 = jnp.swapaxes(labels["gt_bboxes"], 0, 1)
        gt_segs = labels["gt_masks"]
        if len(gt_segs.shape) == 4:  # either NxHxWx1 or NxHxW
            gt_segs = gt_segs.squeeze(-1)
        seg_size = gt_segs.shape[1]

        # pixel size of the gt mask labels
        hs = (y1 - y0) / seg_size
        ws = (x1 - x0) / seg_size

        # compute rescaled coorinats in edge indexing
        yc = (yc - y0[:, None, None] + 0.5) / hs[:, None, None]
        xc = (xc - x0[:, None, None] + 0.5) / ws[:, None, None]

        # resample the label to match model coordinates
        gt_patches = jax.vmap(sub_pixel_samples)(
            gt_segs,
            jnp.stack([yc, xc], axis=-1) - 0.5,  # default is center indexing
        )
        gt_patches = (gt_patches >= 0.5).astype("float32")

    loss = optax.sigmoid_binary_cross_entropy(instance_logit, gt_patches)

    return _mean_over_boolean_mask(loss, instance_mask)


def self_supervised_instance_loss(preds, *, soft_label: bool = True, **kwargs):
    """Unsupervised instance loss

    Args:
        preds: Model prediction dict.
        soft_label: If False, it convertes image mask prediction to hard label
            (ie. 0 or 1), before computing loss.
    """

    instance_mask = preds["instance_mask"]
    instances = preds["instance_output"]
    instance_logit = preds["instance_logit"]
    yc = preds["instance_yc"]
    xc = preds["instance_xc"]

    patch_size = instances.shape[-1]
    padding_size = patch_size // 2 + 2
    yc += padding_size
    xc += padding_size

    binary_mask = jax.lax.stop_gradient(jax.nn.sigmoid(preds["fg_pred"]))
    seg = jnp.pad(binary_mask, padding_size)

    if soft_label:
        seg_patch = seg[yc, xc]

        loss = (1.0 - seg_patch) * instances + seg_patch * (1.0 - instances)

        instance_sum = jnp.zeros_like(seg)
        instance_sum = instance_sum.at[yc, xc].add(instances)
        instance_sum_i = instance_sum[yc, xc] - instances

        loss = loss + instances * instance_sum_i

    else:
        seg = (seg > 0.5).astype(instances.dtype)
        seg_patch = seg[yc, xc]

        loss = (1.0 - seg_patch) * instances + seg_patch * (1.0 - instances)

        log_yi_sum = jnp.zeros_like(seg)
        log_yi = -jax.nn.log_sigmoid(-instance_logit)
        log_yi_sum = log_yi_sum.at[yc, xc].add(log_yi)
        log_yi = log_yi_sum[yc, xc] - log_yi

        loss = loss + (instances * log_yi)

    return _mean_over_boolean_mask(loss, instance_mask)


def weakly_supervised_instance_loss(
    preds, labels, inputs, *, ignore_mask: bool = False, **kwargs
):
    """Instance loss supervised by image mask instead of instance masks"""

    instance_mask = preds["instance_mask"]
    instances = preds["instance_output"]
    instance_logit = preds["instance_logit"]
    yc = preds["instance_yc"]
    xc = preds["instance_xc"]

    patch_size = instances.shape[-1]
    padding_size = patch_size // 2 + 2
    yc += padding_size
    xc += padding_size

    if ignore_mask:
        seg = jnp.zeros(inputs["image"].shape[:-1])
        seg = jnp.pad(seg, padding_size)
        loss = jnp.zeros_like(instances)
    else:
        if isinstance(labels, dict):
            seg = labels["gt_image_mask"].astype("float32")
        else:
            seg = labels.astype("float32")
        seg = jnp.pad(seg, padding_size)
        seg_patch = seg[yc, xc]
        loss = (1.0 - seg_patch) * instances + seg_patch * (1.0 - instances)

    log_yi_sum = jnp.zeros_like(seg)

    log_yi = -jax.nn.log_sigmoid(-instance_logit)
    log_yi_sum = log_yi_sum.at[yc, xc].add(log_yi)
    log_yi = log_yi_sum[yc, xc] - log_yi

    loss = loss + (instances * log_yi)

    return _mean_over_boolean_mask(loss, instance_mask)


class SupervisedInstanceLoss(Loss):
    def call(self, preds: dict, labels: dict, **kwargs):
        return supervised_instance_loss(preds, labels)


class SelfSupervisedInstanceLoss(Loss):
    def __init__(self, soft_label: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soft_label = soft_label

    def call(self, preds: dict, **kwargs):
        return self_supervised_instance_loss(preds, soft_label=self.soft_label)


class WeaklySupervisedInstanceLoss(Loss):
    def __init__(self, ignore_mask: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ignore_mask = ignore_mask

    def call(self, *, preds, labels, inputs):
        return weakly_supervised_instance_loss(
            preds, labels, inputs, ignore_mask=self.ignore_mask
        )
