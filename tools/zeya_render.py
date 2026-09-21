#!/usr/bin/env python3
"""
ZEYA Curtains & Blinds - rendering primitives for the placeholder image set.

These are GENERATED artwork placeholders, not photographs. They exist so the
layout renders at the correct aspect ratios, with the correct filenames, while
the real ZEYA photography is being produced. Drop real photos in using the same
filenames (and the same -640/-1024/-1600 responsive variants) and no markup
change is needed.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "zeya-website", "assets", "images"))
VARIANTS = (640, 1024, 1600)


# ---------------------------------------------------------------- palette ---
def hexc(s):
    s = s.lstrip("#")
    return np.array([int(s[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


IVORY = hexc("#F7F4EE")
CREAM = hexc("#EFE9DF")
BEIGE = hexc("#D6C4A5")
GOLD = hexc("#B89458")
ESPRESSO = hexc("#211B16")
CHARCOAL = hexc("#292622")
TAUPE = hexc("#6E6054")
SAND = hexc("#C9B79B")
MOCHA = hexc("#8A7561")
DAYLIGHT = hexc("#FFF7E8")
DUSK = hexc("#F2CBA1")
SKY = hexc("#CBD9E2")
NIGHT = hexc("#171310")


def gaussian_rgb(arr, sigma):
    if sigma <= 0:
        return arr
    src = (np.clip(arr, 0, 1) * 255).astype(np.uint8)
    im = Image.fromarray(src, "RGB").filter(ImageFilter.GaussianBlur(sigma))
    return np.asarray(im).astype(np.float32) / 255.0


def gaussian_signed(arr, sigma):
    """Blur a signed [-1,1] field."""
    if sigma <= 0:
        return arr
    a = arr - arr.min()
    a = a / (a.max() + 1e-6)
    im = Image.fromarray((a * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(sigma))
    return (np.asarray(im).astype(np.float32) / 255.0) * 2.0 - 1.0


class Scene:
    """A small painterly renderer: gradients, light, fabric, glass, silhouettes."""

    def __init__(self, w, h, top, bottom, seed=7):
        self.w, self.h = w, h
        self.rng = random.Random(seed)
        self.nrng = np.random.default_rng(seed)
        t = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]
        self.img = (top[None, None, :] * (1.0 - t) + bottom[None, None, :] * t)
        self.img = np.repeat(self.img, w, axis=1).astype(np.float32)
        gy, gx = np.mgrid[0:h, 0:w]
        self.gx = gx.astype(np.float32)
        self.gy = gy.astype(np.float32)

    # -- masks --------------------------------------------------------------
    def mask(self, draw_fn, blur_px=0.0):
        im = Image.new("L", (self.w, self.h), 0)
        draw_fn(ImageDraw.Draw(im))
        if blur_px:
            im = im.filter(ImageFilter.GaussianBlur(blur_px))
        return np.asarray(im).astype(np.float32) / 255.0

    def rect_mask(self, box, radius=0, blur_px=0.0):
        def d(dr):
            if radius:
                dr.rounded_rectangle(box, radius=radius, fill=255)
            else:
                dr.rectangle(box, fill=255)
        return self.mask(d, blur_px)

    def poly_mask(self, pts, blur_px=0.0):
        return self.mask(lambda dr: dr.polygon(pts, fill=255), blur_px)

    def ellipse_mask(self, box, blur_px=0.0):
        return self.mask(lambda dr: dr.ellipse(box, fill=255), blur_px)

    # -- compositing --------------------------------------------------------
    def paint(self, mask, color, alpha=1.0):
        a = (mask * alpha)[..., None]
        self.img = self.img * (1.0 - a) + color[None, None, :] * a

    def glow(self, cx, cy, rx, ry, color, strength=0.6, power=1.6):
        d = ((self.gx - cx) / max(rx, 1.0)) ** 2 + ((self.gy - cy) / max(ry, 1.0)) ** 2
        m = np.exp(-d * power)[..., None]
        self.img = self.img + (1.0 - self.img) * m * strength * color[None, None, :]

    def shadow(self, cx, cy, rx, ry, strength=0.35, power=1.5):
        d = ((self.gx - cx) / max(rx, 1.0)) ** 2 + ((self.gy - cy) / max(ry, 1.0)) ** 2
        m = np.exp(-d * power)
        self.img = self.img * (1.0 - strength * m)[..., None]

    def shade(self, mask, factor):
        f = factor if np.ndim(factor) else np.full((self.h, self.w), float(factor), np.float32)
        f = 1.0 + (f - 1.0) * mask
        self.img = self.img * f[..., None]

    def blur_region(self, mask, sigma):
        b = gaussian_rgb(self.img, sigma)
        m = mask[..., None]
        self.img = self.img * (1.0 - m) + b * m

    # -- textures -----------------------------------------------------------
    def folds(self, box, count=14, depth=0.26, phase=0.0, drop=0.18, edge=6, soften=1.6):
        """Vertical curtain folds inside `box`."""
        x0, y0, x1, y1 = box
        m = self.rect_mask(box, blur_px=edge)
        t = (self.gx - x0) / max(1.0, (x1 - x0))
        s = 0.66 * np.sin(t * math.pi * 2 * count + phase)
        s += 0.23 * np.sin(t * math.pi * 2 * count * 0.5 + phase * 1.7 + 0.9)
        s += 0.11 * np.sin(t * math.pi * 2 * count * 2.13 + 2.2)
        v = np.clip((self.gy - y0) / max(1.0, (y1 - y0)), 0.0, 1.0)
        # folds gather slightly toward the floor, so drift the phase with height
        f = (1.0 + depth * s * (1.0 - 0.18 * v)) * (1.0 - drop * v * v)
        self.shade(m, f)
        if soften:
            self.blur_region(m, soften)

    def slats(self, box, period=26, depth=0.20, gap=0.16, edge=4, tilt=0.0):
        """Horizontal blind slats inside `box`."""
        x0, y0, x1, y1 = box
        m = self.rect_mask(box, blur_px=edge)
        p = (self.gy - y0 + (self.gx - x0) * tilt) / float(period)
        f = 1.0 + depth * np.sin(p * math.pi * 2)
        line = np.clip(1.0 - np.abs(((p % 1.0) - 0.5) * 2.0) * 3.4, 0.0, 1.0)
        self.shade(m, f * (1.0 - gap * line))

    def weave(self, box, scale=2.2, amount=0.05, radius=0):
        m = self.rect_mask(box, radius=radius, blur_px=2)
        n = gaussian_signed(self.nrng.normal(0.0, 1.0, (self.h, self.w)).astype(np.float32), scale)
        self.shade(m, 1.0 + amount * n)

    def skyline(self, x0, x1, base_y, max_h, color, alpha=0.5, seed=3, spire_at=None):
        rng = random.Random(seed)

        def d(dr):
            x = x0
            while x < x1:
                bw = rng.randint(max(6, int(max_h * 0.09)), max(12, int(max_h * 0.26)))
                bh = rng.randint(int(max_h * 0.18), max_h)
                dr.rectangle([x, base_y - bh, x + bw, base_y], fill=255)
                x += bw + rng.randint(3, 16)
            if spire_at is not None:
                sx, sw = spire_at, max(9, int(max_h * 0.07))
                dr.polygon([(sx - sw, base_y),
                            (sx - sw * 0.5, base_y - max_h * 1.5),
                            (sx, base_y - max_h * 2.0),
                            (sx + sw * 0.5, base_y - max_h * 1.5),
                            (sx + sw, base_y)], fill=255)
        self.paint(self.mask(d, blur_px=1.1), color, alpha)

    def window_frame(self, box, cols=3, rows=1, frame=ESPRESSO, frame_px=7, alpha=0.8):
        x0, y0, x1, y1 = box

        def d(dr):
            dr.rectangle(box, outline=255, width=frame_px)
            for i in range(1, cols):
                x = x0 + (x1 - x0) * i / cols
                dr.rectangle([x - frame_px / 2, y0, x + frame_px / 2, y1], fill=255)
            for j in range(1, rows):
                y = y0 + (y1 - y0) * j / rows
                dr.rectangle([x0, y - frame_px / 2, x1, y + frame_px / 2], fill=255)
        self.paint(self.mask(d, blur_px=0.7), frame, alpha)

    def soft_shape(self, box, color, alpha=0.9, radius=40, blur_px=8):
        self.paint(self.rect_mask(box, radius=radius, blur_px=blur_px), color, alpha)

    def figure(self, cx, base_y, height, color=ESPRESSO, alpha=0.74, lean=0.0, arms=None):
        """A soft, out-of-focus person: head, neck, shoulders, tapering torso."""
        head_r = height * 0.056
        head_cy = base_y - height + head_r
        shoulder = height * 0.105
        hip = height * 0.082
        top = base_y - height * 0.82
        waist = base_y - height * 0.44

        def d(dr):
            dr.ellipse([cx - head_r + lean, head_cy - head_r,
                        cx + head_r + lean, head_cy + head_r], fill=255)
            dr.line([(cx + lean, head_cy), (cx, top)],
                    fill=255, width=max(3, int(height * 0.036)))
            dr.polygon([(cx - shoulder, top), (cx + shoulder, top),
                        (cx + hip, waist), (cx + hip * 0.94, base_y),
                        (cx - hip * 0.94, base_y), (cx - hip, waist)], fill=255)
            if arms:
                ax, ay = arms
                dr.line([(cx, top + height * 0.05), (ax, ay)],
                        fill=255, width=max(4, int(height * 0.038)))
        self.paint(self.mask(d, blur_px=max(2.0, height * 0.026)), color, alpha)

    def plant(self, cx, base_y, height, color=ESPRESSO, alpha=0.55, seed=11):
        rng = random.Random(seed)

        def d(dr):
            pot_w = height * 0.17
            dr.rounded_rectangle([cx - pot_w, base_y - height * 0.22, cx + pot_w, base_y],
                                 radius=int(pot_w * 0.35), fill=255)
            for _ in range(16):
                ang = rng.uniform(-1.25, 1.25)
                ln = height * rng.uniform(0.42, 0.82)
                ex = cx + math.sin(ang) * ln
                ey = base_y - height * 0.22 - math.cos(ang) * ln
                dr.line([(cx, base_y - height * 0.22), (ex, ey)],
                        fill=255, width=max(2, int(height * 0.012)))
                dr.ellipse([ex - height * 0.045, ey - height * 0.03,
                            ex + height * 0.045, ey + height * 0.03], fill=255)
        self.paint(self.mask(d, blur_px=max(1.0, height * 0.01)), color, alpha)

    # -- finishing ----------------------------------------------------------
    def vignette(self, strength=0.34, power=1.25):
        nx = (self.gx / self.w - 0.5) * 2.0
        ny = (self.gy / self.h - 0.5) * 2.0
        r = np.clip(np.sqrt(nx ** 2 + ny ** 2) / math.sqrt(2.0), 0, 1)
        self.img = self.img * (1.0 - strength * r ** power)[..., None]

    def grain(self, amount=0.015):
        self.img = self.img + self.nrng.normal(0.0, amount, (self.h, self.w, 1)).astype(np.float32)

    def grade(self, lift=0.015, contrast=1.06, warmth=0.028):
        x = np.clip(self.img, 0.0, 1.0)
        x = (x - 0.5) * contrast + 0.5 + lift
        x = np.clip(x, 0.0, 1.2)
        x = x * 0.86 + 0.14 * (x ** 0.88)          # gentle filmic shoulder
        x[..., 0] = x[..., 0] + warmth
        x[..., 2] = x[..., 2] - warmth * 0.85
        self.img = x

    def finish(self, vignette=0.32, grain=0.014, **grade_kw):
        self.grade(**grade_kw)
        self.vignette(vignette)
        self.grain(grain)
        return Image.fromarray((np.clip(self.img, 0, 1) * 255).astype(np.uint8), "RGB")


def save(im, name, variants=True):
    os.makedirs(OUT, exist_ok=True)
    im.save(os.path.join(OUT, name + ".webp"), "WEBP", quality=80, method=6)
    written = [name + ".webp"]
    if variants:
        for wv in VARIANTS:
            if wv < im.width:
                h = max(1, round(im.height * wv / im.width))
                v = im.resize((wv, h), Image.LANCZOS)
                v.save(os.path.join(OUT, "%s-%d.webp" % (name, wv)), "WEBP", quality=78, method=6)
                written.append("%s-%d.webp" % (name, wv))
    print("  " + ", ".join(written))
