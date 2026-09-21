#!/usr/bin/env python3
"""
Generated artwork for the Curtain Accessories collection.

The rest of the catalogue borrows photographs; accessories have none, so these
are composed from the painterly primitives in zeya_render.py. Each scene is a
window vignette that puts one fitting — the pole, the track, the tieback — in
the foreground, because the renderer reads fabric and light far better than it
reads hardware detail.

    python tools/render_accessories.py

Writes product-<slug>.webp (plus -640/-1024 variants) straight into
zeya-website/assets/images/, so removing the matching alias from asset_map.py
is all it takes for a page to pick the render up. Drop a real photograph in at
the same filename later and nothing else changes.
"""
import math

import numpy as np

from zeya_render import (Scene, save, BEIGE, CREAM, DAYLIGHT, DUSK, ESPRESSO,
                         GOLD, IVORY, MOCHA, SAND, SKY, TAUPE, hexc)

W, H = 1122, 1402                      # the 4:5 portrait the product cards use
BRASS = hexc("#A8823F")
STEEL = hexc("#9A958D")
WALNUT = hexc("#5A4232")


def room(seed, warm=0.55, window=(0.16, 0.10, 0.84, 0.74), sky=True):
    """The shared backdrop: a warm wall, one bright window, a soft floor."""
    s = Scene(W, H, CREAM * 1.02, SAND * 0.92, seed=seed)
    x0, y0, x1, y1 = (window[0] * W, window[1] * H, window[2] * W, window[3] * H)

    # Daylight behind the glass, brightest just inside the reveal.
    s.paint(s.rect_mask((x0, y0, x1, y1), blur_px=14), DAYLIGHT, 0.92)
    if sky:
        s.paint(s.rect_mask((x0, y0, x1, y0 + (y1 - y0) * 0.46), blur_px=26), SKY, 0.30)
        s.skyline(int(x0), int(x1), int(y0 + (y1 - y0) * 0.62), int((y1 - y0) * 0.22),
                  TAUPE, alpha=0.26, seed=seed + 4)
    s.glow((x0 + x1) / 2, y0 + (y1 - y0) * 0.35, (x1 - x0) * 0.72, (y1 - y0) * 0.62,
           DAYLIGHT, strength=0.52 * warm + 0.2)

    # Floor and the shadow the window light throws back into the room.
    s.paint(s.rect_mask((0, H * 0.88, W, H), blur_px=22), MOCHA, 0.30)
    s.shadow(W * 0.5, H * 1.02, W * 0.8, H * 0.22, strength=0.22)
    return s, (x0, y0, x1, y1)


def pole(s, y, x0, x1, thickness, color=BRASS, finial=None, rings=0):
    """A horizontal pole with optional end finials and a run of rings."""
    r = thickness / 2.0
    s.paint(s.rect_mask((x0, y - r, x1, y + r), radius=int(r), blur_px=1.2), color, 0.96)
    # A highlight along the top keeps the pole reading as a cylinder.
    s.paint(s.rect_mask((x0, y - r, x1, y - r * 0.28), radius=int(r * 0.5), blur_px=2.2),
            IVORY, 0.30)
    s.shadow((x0 + x1) / 2, y + thickness * 1.5, (x1 - x0) * 0.52, thickness * 1.1,
             strength=0.16)

    if finial == "ball":
        for cx in (x0, x1):
            s.paint(s.ellipse_mask((cx - r * 2.1, y - r * 2.1, cx + r * 2.1, y + r * 2.1),
                                   blur_px=1.4), color, 0.96)
            s.paint(s.ellipse_mask((cx - r * 1.1, y - r * 1.5, cx + r * 0.2, y - r * 0.3),
                                   blur_px=2.0), IVORY, 0.34)
    elif finial == "cap":
        for cx in (x0, x1):
            s.paint(s.rect_mask((cx - r * 1.5, y - r * 1.6, cx + r * 1.5, y + r * 1.6),
                                radius=int(r * 0.6), blur_px=1.2), color, 0.94)

    for i in range(rings):
        cx = x0 + (x1 - x0) * (i + 0.5) / rings
        rr = thickness * 0.82
        # Outer ring, then the pole punched back through it, so the ring reads
        # as threaded on rather than hung in front.
        s.paint(s.ellipse_mask((cx - rr, y - rr * 0.55, cx + rr, y + rr * 1.75),
                               blur_px=1.1), color * 0.92, 0.95)
        s.paint(s.ellipse_mask((cx - rr * 0.62, y - rr * 0.12, cx + rr * 0.62,
                                y + rr * 1.32), blur_px=1.1), CREAM * 1.03, 0.95)
        s.paint(s.rect_mask((cx - rr, y - r, cx + rr, y + r * 0.55), blur_px=1.0),
                color, 0.9)
        s.paint(s.rect_mask((cx - rr * 0.5, y + rr * 1.15, cx + rr * 0.5, y + rr * 2.1),
                            radius=4, blur_px=1.2), color * 0.85, 0.8)


def bracket(s, cx, y, thickness, color=BRASS):
    """The wall fixing under a pole."""
    s.paint(s.rect_mask((cx - thickness * 0.35, y, cx + thickness * 0.35, y + thickness * 1.5),
                        radius=int(thickness * 0.3), blur_px=1.2), color, 0.9)
    s.paint(s.ellipse_mask((cx - thickness * 0.8, y + thickness * 1.2,
                            cx + thickness * 0.8, y + thickness * 2.0), blur_px=1.4),
            color, 0.88)


def panel(s, box, count=11, depth=0.27, color=None, alpha=0.0, phase=0.0):
    """A hanging curtain panel: a soft body, then folds cut into it."""
    if color is not None and alpha:
        s.paint(s.rect_mask(box, blur_px=6), color, alpha)
    s.weave(box, scale=2.0, amount=0.05)
    s.folds(box, count=count, depth=depth, phase=phase, drop=0.16)


def gathered_panel(s, left, top, bot, width_of, color, alpha=0.86,
                   count=8, depth=0.30, soften=1.8):
    """A curtain whose width varies down its drop.

    Scene.folds only works on a rectangle, so this repeats its shading with the
    fold coordinate normalised against the LOCAL width. The folds then crowd
    together where the fabric is gathered and open out where it falls free —
    which is the whole point of a tieback.
    """
    ys = np.arange(s.h, dtype=np.float32)
    widths = np.maximum(width_of(ys), 1.0)

    step = max(2, int((bot - top) / 90))
    edge_l = [(left, y) for y in np.arange(top, bot, step)]
    edge_r = [(left + widths[int(min(s.h - 1, max(0, y)))], y)
              for y in np.arange(bot, top, -step)]
    m = s.poly_mask(edge_l + edge_r, blur_px=5)
    s.paint(m, color, alpha)

    u = (s.gx - left) / widths[:, None]
    f = 0.66 * np.sin(u * math.pi * 2 * count)
    f += 0.23 * np.sin(u * math.pi * 2 * count * 0.5 + 0.9)
    f += 0.11 * np.sin(u * math.pi * 2 * count * 2.13 + 2.2)
    v = np.clip((s.gy - top) / max(1.0, bot - top), 0.0, 1.0)
    s.weave((left, top, left + float(widths.max()), bot), scale=2.0, amount=0.04)
    s.shade(m, (1.0 + depth * f * (1.0 - 0.18 * v)) * (1.0 - 0.16 * v * v))
    s.blur_region(m, soften)
    return m


# ------------------------------------------------------------------ scenes ---
def curtain_rods_poles():
    s, (x0, y0, x1, y1) = room(21)
    py = H * 0.17
    pole(s, py, W * 0.10, W * 0.90, W * 0.030, finial="ball")
    bracket(s, W * 0.22, py + W * 0.016, W * 0.030)
    bracket(s, W * 0.78, py + W * 0.016, W * 0.030)
    panel(s, (W * 0.08, py + W * 0.02, W * 0.34, H * 0.92), count=7, depth=0.30,
          color=BEIGE, alpha=0.88)
    panel(s, (W * 0.66, py + W * 0.02, W * 0.92, H * 0.92), count=7, depth=0.30,
          color=BEIGE, alpha=0.88, phase=1.3)
    panel(s, (W * 0.34, py + W * 0.02, W * 0.66, H * 0.86), count=13, depth=0.14,
          color=IVORY, alpha=0.30)
    return s.finish(vignette=0.30)


def curtain_tracks():
    s, (x0, y0, x1, y1) = room(33, window=(0.12, 0.16, 0.88, 0.80))
    # A recessed ceiling, then the track hanging clear of it in its own shadow.
    s.paint(s.rect_mask((0, 0, W, H * 0.11), blur_px=10), CREAM * 1.06, 0.95)
    s.shadow(W * 0.5, H * 0.125, W * 0.7, H * 0.035, strength=0.26)
    ty = H * 0.175
    s.shadow(W * 0.5, ty + H * 0.030, W * 0.55, H * 0.030, strength=0.22)
    s.paint(s.rect_mask((W * 0.05, ty, W * 0.95, ty + H * 0.026), radius=7, blur_px=0.8),
            STEEL * 0.78, 0.97)
    s.paint(s.rect_mask((W * 0.05, ty, W * 0.95, ty + H * 0.008), blur_px=1.4),
            IVORY, 0.45)
    # The open channel along the underside, with the glides running in it.
    s.paint(s.rect_mask((W * 0.05, ty + H * 0.017, W * 0.95, ty + H * 0.026), blur_px=0.8),
            ESPRESSO, 0.45)
    for i in range(15):
        cx = W * 0.08 + (W * 0.84) * i / 14.0
        s.paint(s.ellipse_mask((cx - 9, ty + H * 0.022, cx + 9, ty + H * 0.040),
                               blur_px=1.0), STEEL * 0.95, 0.9)
    panel(s, (W * 0.05, ty + H * 0.035, W * 0.95, H * 0.94), count=17, depth=0.21,
          color=IVORY, alpha=0.62)
    return s.finish(vignette=0.28)


def tiebacks_holdbacks():
    s, (x0, y0, x1, y1) = room(47, window=(0.24, 0.12, 0.90, 0.80))
    py = H * 0.13
    pole(s, py, W * 0.06, W * 0.94, W * 0.024, finial="ball")

    # The subject is the silhouette rather than the fitting: held back at hip
    # height, the panel pinches to a waist and flares below it.
    waist = H * 0.52
    top, bot = py, H * 0.96
    left = W * 0.05

    def width_of(ys):
        k = np.abs(ys - waist) / ((bot - top) * 0.5)
        return (0.46 + 0.54 * np.clip(k, 0.0, 1.0) ** 0.8) * W * 0.38

    gathered_panel(s, left, top, bot, width_of, MOCHA, 0.86, count=8, depth=0.30)
    s.shadow(W * 0.17, waist, W * 0.13, H * 0.045, strength=0.32)

    # The sash sits in the pinch, short and angled, with a tassel below it.
    s.paint(s.poly_mask([(W * 0.045, waist - H * 0.024), (W * 0.215, waist - H * 0.006),
                         (W * 0.215, waist + H * 0.020), (W * 0.045, waist + H * 0.002)],
                        blur_px=2.6), GOLD, 0.92)
    s.paint(s.poly_mask([(W * 0.045, waist - H * 0.024), (W * 0.215, waist - H * 0.006),
                         (W * 0.215, waist + H * 0.002), (W * 0.045, waist - H * 0.016)],
                        blur_px=3.4), IVORY, 0.24)
    s.paint(s.ellipse_mask((W * 0.196, waist - H * 0.008, W * 0.234, waist + H * 0.028),
                           blur_px=1.8), GOLD * 0.86, 0.95)
    s.paint(s.rect_mask((W * 0.208, waist + H * 0.024, W * 0.222, waist + H * 0.086),
                        radius=7, blur_px=1.8), GOLD * 0.80, 0.88)
    s.paint(s.ellipse_mask((W * 0.201, waist + H * 0.080, W * 0.229, waist + H * 0.112),
                           blur_px=2.0), GOLD * 0.74, 0.88)
    return s.finish(vignette=0.32)


def curtain_rings_hooks():
    s, (x0, y0, x1, y1) = room(59, window=(0.10, 0.22, 0.90, 0.84))
    # Sits closer in: a big pole across the upper third, rings reading clearly.
    py = H * 0.26
    pole(s, py, W * 0.02, W * 0.98, W * 0.046, finial="ball", rings=7)
    panel(s, (W * 0.02, py + W * 0.05, W * 0.98, H * 0.96), count=7, depth=0.26,
          color=BEIGE, alpha=0.72)
    s.shadow(W * 0.5, py + W * 0.10, W * 0.7, H * 0.05, strength=0.18)
    return s.finish(vignette=0.34)


def finials_end_caps():
    s, (x0, y0, x1, y1) = room(71, window=(0.30, 0.06, 1.02, 0.86))
    # A cropped view of one pole end against the bright glass.
    py = H * 0.40
    th = W * 0.075
    r = th / 2.0
    s.paint(s.rect_mask((W * 0.24, py - r, W * 1.02, py + r), radius=int(r), blur_px=1.4),
            BRASS, 0.96)
    s.paint(s.rect_mask((W * 0.24, py - r, W * 1.02, py - r * 0.30), radius=int(r * 0.5),
                        blur_px=2.6), IVORY, 0.32)
    # Collar, then the ball finial on the end.
    s.paint(s.rect_mask((W * 0.22, py - r * 1.25, W * 0.255, py + r * 1.25),
                        radius=int(r * 0.4), blur_px=1.2), BRASS * 0.9, 0.95)
    cx, cr = W * 0.145, r * 1.9
    s.paint(s.ellipse_mask((cx - cr, py - cr, cx + cr, py + cr), blur_px=1.6), BRASS, 0.97)
    s.paint(s.ellipse_mask((cx - cr * 0.55, py - cr * 0.72, cx + cr * 0.12, py - cr * 0.08),
                           blur_px=3.0), IVORY, 0.40)
    s.shadow(cx, py + cr * 1.9, cr * 2.2, cr * 0.8, strength=0.20)
    panel(s, (W * 0.34, py + r, W * 1.02, H * 0.98), count=9, depth=0.24,
          color=BEIGE, alpha=0.58)
    return s.finish(vignette=0.30)


def pelmets_valances():
    s, (x0, y0, x1, y1) = room(83, window=(0.14, 0.28, 0.86, 0.82))
    # The upholstered box that hides the track, with curtains falling below it.
    top, bot = H * 0.10, H * 0.26
    s.paint(s.rect_mask((W * 0.06, top, W * 0.94, bot), radius=10, blur_px=3.0),
            WALNUT, 0.90)
    s.weave((W * 0.06, top, W * 0.94, bot), scale=1.8, amount=0.06)
    s.paint(s.rect_mask((W * 0.06, top, W * 0.94, top + H * 0.02), blur_px=5.0),
            IVORY, 0.16)
    s.paint(s.rect_mask((W * 0.06, bot - H * 0.012, W * 0.94, bot), blur_px=2.0),
            GOLD, 0.35)
    s.shadow(W * 0.5, bot + H * 0.03, W * 0.62, H * 0.05, strength=0.30)
    panel(s, (W * 0.08, bot, W * 0.36, H * 0.95), count=6, depth=0.28,
          color=BEIGE, alpha=0.82)
    panel(s, (W * 0.64, bot, W * 0.92, H * 0.95), count=6, depth=0.28,
          color=BEIGE, alpha=0.82, phase=1.1)
    panel(s, (W * 0.36, bot, W * 0.64, H * 0.90), count=11, depth=0.13,
          color=IVORY, alpha=0.26)
    return s.finish(vignette=0.31)


def curtain_linings():
    s, (x0, y0, x1, y1) = room(97, window=(0.08, 0.10, 0.92, 0.86))
    py = H * 0.12
    pole(s, py, W * 0.04, W * 0.96, W * 0.022, finial="cap")
    # Three layers, stepped back: sheer, face fabric, and the blackout lining
    # folded open so the difference in weight and opacity is the subject.
    panel(s, (W * 0.04, py, W * 0.96, H * 0.94), count=15, depth=0.14,
          color=IVORY, alpha=0.40)
    panel(s, (W * 0.30, py, W * 0.96, H * 0.96), count=9, depth=0.24,
          color=BEIGE, alpha=0.78, phase=0.5)
    panel(s, (W * 0.52, py, W * 0.96, H * 0.98), count=6, depth=0.26,
          color=ESPRESSO, alpha=0.72, phase=1.9)
    # The blackout layer turned back along its leading edge: a wedge of pale
    # lining, its fold line dark, so the two weights read against each other.
    peel = [(W * 0.52, H * 0.30), (W * 0.74, H * 0.40),
            (W * 0.74, H * 0.80), (W * 0.52, H * 0.98)]
    s.paint(s.poly_mask(peel, blur_px=4), CREAM * 1.04, 0.92)
    s.weave((W * 0.52, H * 0.30, W * 0.74, H * 0.98), scale=1.6, amount=0.05)
    s.folds((W * 0.54, H * 0.34, W * 0.74, H * 0.94), count=4, depth=0.16, drop=0.10)
    s.paint(s.poly_mask([(W * 0.515, H * 0.30), (W * 0.535, H * 0.30),
                         (W * 0.535, H * 0.98), (W * 0.515, H * 0.98)], blur_px=3),
            ESPRESSO, 0.40)
    s.shadow(W * 0.74, H * 0.60, W * 0.03, H * 0.26, strength=0.22)
    return s.finish(vignette=0.33)


def motorized_accessories():
    s, (x0, y0, x1, y1) = room(109, window=(0.42, 0.10, 1.02, 0.84))
    panel(s, (W * 0.44, H * 0.10, W * 1.02, H * 0.96), count=11, depth=0.22,
          color=IVORY, alpha=0.52)
    # A wall plate beside the curtain: the switch and its two travel buttons.
    px0, py0, px1, py1 = W * 0.10, H * 0.34, W * 0.34, H * 0.60
    s.shadow((px0 + px1) / 2 + 14, (py0 + py1) / 2 + 18, (px1 - px0) * 0.62,
             (py1 - py0) * 0.62, strength=0.24)
    s.paint(s.rect_mask((px0, py0, px1, py1), radius=22, blur_px=2.0), IVORY, 0.94)
    s.paint(s.rect_mask((px0, py0, px1, py0 + H * 0.02), radius=16, blur_px=4.0),
            CREAM * 0.9, 0.5)
    for i, sign in enumerate((-1, 1)):
        cy = (py0 + py1) / 2 + sign * (py1 - py0) * 0.22
        s.paint(s.rect_mask((px0 + W * 0.045, cy - H * 0.028,
                             px1 - W * 0.045, cy + H * 0.028), radius=14, blur_px=1.6),
                CREAM * 0.94, 0.95)
        # The up/down chevron on each key.
        ax, ay, k = (px0 + px1) / 2, cy, H * 0.013
        s.paint(s.poly_mask([(ax, ay - sign * k), (ax + k * 1.5, ay + sign * k * 0.6),
                             (ax - k * 1.5, ay + sign * k * 0.6)], blur_px=1.2),
                TAUPE, 0.75)
    s.paint(s.ellipse_mask((px1 - W * 0.055, py1 - H * 0.042,
                            px1 - W * 0.030, py1 - H * 0.030), blur_px=1.4), GOLD, 0.85)
    return s.finish(vignette=0.32)


SCENES = {
    "product-curtain-rods-poles": curtain_rods_poles,
    "product-curtain-tracks": curtain_tracks,
    "product-tiebacks-holdbacks": tiebacks_holdbacks,
    "product-curtain-rings-hooks": curtain_rings_hooks,
    "product-finials-end-caps": finials_end_caps,
    "product-pelmets-valances": pelmets_valances,
    "product-curtain-linings": curtain_linings,
    "product-motorized-accessories": motorized_accessories,
}


def main():
    for name, fn in SCENES.items():
        save(fn(), name)
    # The collection hero is the same pole scene, cropped to a landscape band
    # low enough to sit on fabric rather than on the bright window, so the
    # hero type keeps its contrast.
    hero = curtain_rods_poles()
    top = int(hero.height * 0.40)
    save(hero.crop((0, top, hero.width, top + int(hero.width * 0.62))),
         "accessories-category")
    print("\nRendered -> zeya-website/assets/images/")


if __name__ == "__main__":
    main()
