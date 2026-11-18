#!/usr/bin/env python3
"""Build civil-war collective portraits by replacing only the flag in an approved base."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "DESIGN/source_assets/collective_portraits/accepted_kir_council_base.png"
OUT = ROOT / "gfx/leaders/NW14/collective"
SIZE = (156, 210)
FLAG_SIZE = (742, 465)

FLAGS = {
    "NCR": "NCR_democratic.tga",
    "TCF": "TCF_democratic.tga",
    "TRP": "TRP_neutrality.tga",
    "BLF": "BLF_neutrality.tga",
    "BLW": "BLW_democratic.tga",
    "DNR": "DNR_democratic.tga",
    "AKV": "AKV_neutrality.tga",
    "KIR": "KIR_democratic.tga",
}


def polygon_mask(size: tuple[int, int], points: list[tuple[int, int]]) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    return mask


def make_flag_panel_mask(size: tuple[int, int]) -> Image.Image:
    # Trace the visible flag hem in the accepted 1081x1455 source.
    return polygon_mask(
        size,
        [
            (0, 0),
            (742, 0),
            (742, 451),
            (710, 453),
            (680, 457),
            (650, 459),
            (620, 461),
            (590, 462),
            (560, 463),
            (530, 464),
            (500, 464),
            (470, 464),
            (440, 463),
            (410, 463),
            (380, 462),
            (350, 462),
            (320, 462),
            (290, 461),
            (260, 461),
            (230, 461),
            (200, 462),
            (170, 462),
            (140, 463),
            (110, 463),
            (80, 463),
            (50, 463),
            (20, 463),
            (0, 463),
        ],
    )


def make_foreground_restore_mask(base: Image.Image) -> Image.Image:
    width, height = base.size
    hsv = np.asarray(base.convert("HSV"))
    hue = hsv[:, :, 0]
    saturation = hsv[:, :, 1]

    # The standing officer overlaps the flag. Restore his original pixels;
    # within this bounded area, identify the old red and yellow flag colors
    # so that only those pixels receive the replacement flag.
    overlap = np.zeros((height, width), dtype=bool)
    overlap[250:470, 555:744] = True
    rows = np.arange(height)[:, None]
    old_flag_color = (
        ((rows >= 166) & (rows < 311) & (hue < 10) & (saturation > 150))
        | ((rows >= 311) & (rows < 466) & (hue >= 24) & (hue <= 40) & (saturation > 150))
    )
    restore = overlap & ~old_flag_color

    # The seated officer's cap crosses the flag hem. Restore its full traced
    # silhouette, including metallic insignia whose color can resemble a flag.
    cap = polygon_mask(
        base.size,
        [
            (344, 389),
            (355, 385),
            (365, 385),
            (377, 389),
            (387, 396),
            (395, 404),
            (402, 415),
            (409, 428),
            (415, 440),
            (419, 450),
            (420, 457),
            (416, 463),
            (409, 466),
            (400, 469),
            (391, 472),
            (380, 473),
            (369, 472),
            (358, 469),
            (347, 467),
            (337, 464),
            (326, 462),
            (316, 460),
            (307, 458),
            (298, 457),
            (290, 455),
            (283, 452),
            (278, 449),
            (276, 444),
            (278, 438),
            (282, 432),
            (287, 425),
            (294, 418),
            (302, 411),
            (310, 403),
            (319, 397),
            (330, 392),
        ],
    )
    restore |= (np.asarray(cap) > 0) & ~old_flag_color
    return Image.fromarray(restore.astype(np.uint8) * 255)


def make_cloth_shading(base: Image.Image) -> np.ndarray:
    rgb = np.asarray(base.convert("RGB")).astype(np.float32)
    flag = rgb[: FLAG_SIZE[1], : FLAG_SIZE[0]]
    luma = 0.2126 * flag[:, :, 0] + 0.7152 * flag[:, :, 1] + 0.0722 * flag[:, :, 2]
    row_median = np.median(luma[:, 270:560], axis=1)
    shading = np.clip(luma / np.maximum(row_median[:, None], 1.0), 0.50, 1.45)

    # Recover the original cloth folds across the whole flag, including the top
    # band. Mask only the old pale crescent/star so they cannot appear on new flags.
    hsv = np.asarray(base.convert("HSV"))
    saturation = hsv[: FLAG_SIZE[1], : FLAG_SIZE[0], 1]
    old_emblem = np.zeros(luma.shape, dtype=bool)
    old_emblem[:165, :235] = (
        (saturation[:165, :235] < 90)
        & (luma[:165, :235] > row_median[:165, None] + 12)
    )
    shading[old_emblem] = 1.0
    return shading


def build() -> None:
    base = Image.open(BASE).convert("RGB")
    if base.size != (1081, 1455):
        raise ValueError(f"Unexpected accepted base dimensions: {base.size}")

    panel_mask = make_flag_panel_mask(base.size)
    restore_mask = make_foreground_restore_mask(base)
    shading = make_cloth_shading(base)
    panel_array = np.asarray(panel_mask) > 0
    restore_array = np.asarray(restore_mask) > 0
    base_array = np.asarray(base)

    OUT.mkdir(parents=True, exist_ok=True)
    for tag, flag_name in FLAGS.items():
        flag = Image.open(ROOT / "gfx/flags" / flag_name).convert("RGB")
        flag = flag.resize(FLAG_SIZE, Image.Resampling.LANCZOS)
        target = np.asarray(flag).astype(np.float32)
        target = np.clip(target * (0.48 + 0.52 * shading[:, :, None]), 0, 255).astype(np.uint8)

        result = base.copy()
        result.paste(Image.fromarray(target), (0, 0), panel_mask.crop((0, 0, *FLAG_SIZE)))
        result.paste(base, (0, 0), restore_mask)

        result_array = np.asarray(result)
        changed = np.any(base_array != result_array, axis=2)
        if np.any(changed & ~panel_array):
            raise AssertionError(f"{tag}: pixels outside the flag panel changed")
        if np.any(changed & restore_array):
            raise AssertionError(f"{tag}: protected foreground pixels changed")

        result.resize(SIZE, Image.Resampling.LANCZOS).save(
            OUT / f"Portrait_CW_Collective_{tag}.png"
        )
        print(f"{tag}: flag-only edit verified at source resolution")


if __name__ == "__main__":
    build()
