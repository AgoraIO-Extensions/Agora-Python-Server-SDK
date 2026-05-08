# coding=utf-8
#
# author: Yan Zhennan
# date: 2026-04-14
#
# Offline tool: merge multiple same-size I420 YUV frames into a fixed layout
# (see plan_merge_yuv.md) and save as JPEG/PNG.

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import os
import sys
from typing import Sequence

import numpy as np
from PIL import Image

# libyuv FilterMode (include/libyuv/scale.h)
LIBYUV_FILTER_NONE = 0
LIBYUV_FILTER_LINEAR = 1
LIBYUV_FILTER_BILINEAR = 2
LIBYUV_FILTER_BOX = 3

_libyuv: ctypes.CDLL | None = None
_libyuv_tried = False


def _load_libyuv() -> ctypes.CDLL | None:
    """Load libyuv shared library once; return None if not available."""
    global _libyuv, _libyuv_tried
    if _libyuv_tried:
        return _libyuv
    _libyuv_tried = True
    if os.environ.get("EXAMPLE_MERGE_YUV_NO_LIBYUV", "").strip().lower() in ("1", "true", "yes"):
        return None
    names: list[str] = []
    try:
        found = ctypes.util.find_library("yuv")
        if found:
            names.append(found)
    except Exception:
        pass
    names.extend(
        (
            "libyuv.dylib",
            "libyuv.so.0",
            "libyuv.so",
            "yuv.dll",
        )
    )
    for name in names:
        if not name:
            continue
        try:
            _libyuv = ctypes.CDLL(name)
            return _libyuv
        except OSError:
            continue
    return None


def _scale_i420_libyuv_native(
    in_yuv: bytes | bytearray,
    in_width: int,
    in_height: int,
    out_width: int,
    out_height: int,
    filter_mode: int,
) -> bytes | None:
    """Call libyuv ``I420Scale`` via ctypes; return None if libyuv is not loaded."""
    lib = _load_libyuv()
    if lib is None:
        return None

    in_y_size = in_width * in_height
    in_c_size = (in_width // 2) * (in_height // 2)
    out_y_size = out_width * out_height
    out_c_size = (out_width // 2) * (out_height // 2)

    src = np.frombuffer(memoryview(in_yuv), dtype=np.uint8, count=in_y_size + 2 * in_c_size).copy()
    out = np.empty(out_y_size + 2 * out_c_size, dtype=np.uint8)

    I420Scale = lib.I420Scale
    I420Scale.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ]
    I420Scale.restype = ctypes.c_int

    sy = src.ctypes.data
    su = src.ctypes.data + in_y_size
    sv = src.ctypes.data + in_y_size + in_c_size
    dy = out.ctypes.data
    du = out.ctypes.data + out_y_size
    dv = out.ctypes.data + out_y_size + out_c_size

    ret = I420Scale(
        ctypes.c_void_p(sy),
        ctypes.c_int(in_width),
        ctypes.c_void_p(su),
        ctypes.c_int(in_width // 2),
        ctypes.c_void_p(sv),
        ctypes.c_int(in_width // 2),
        ctypes.c_int(in_width),
        ctypes.c_int(in_height),
        ctypes.c_void_p(dy),
        ctypes.c_int(out_width),
        ctypes.c_void_p(du),
        ctypes.c_int(out_width // 2),
        ctypes.c_void_p(dv),
        ctypes.c_int(out_width // 2),
        ctypes.c_int(out_width),
        ctypes.c_int(out_height),
        ctypes.c_int(int(filter_mode)),
    )
    if ret != 0:
        return None
    return out.tobytes()


def _black_i420(width: int, height: int) -> bytes:
    """Return one I420 black frame (Y=0, U=V=128)."""
    y_size = width * height
    c_size = (width // 2) * (height // 2)
    buf = bytearray(y_size + 2 * c_size)
    buf[y_size : y_size + c_size] = bytes([128] * c_size)
    buf[y_size + c_size :] = bytes([128] * c_size)
    return bytes(buf)


def _split_i420_planes(yuv: bytes | bytearray, width: int, height: int) -> tuple[memoryview, memoryview, memoryview]:
    y_size = width * height
    c_size = (width // 2) * (height // 2)
    mv = memoryview(yuv)
    if len(mv) != y_size + 2 * c_size:
        raise ValueError(f"I420 length mismatch: got {len(mv)}, expected {y_size + 2 * c_size}")
    y_plane = mv[:y_size]
    u_plane = mv[y_size : y_size + c_size]
    v_plane = mv[y_size + c_size : y_size + 2 * c_size]
    return y_plane, u_plane, v_plane


def layout_rows_cols(n: int) -> tuple[int, int]:
    """
    Return (rows, cols) for merging N same-size I420 tiles.

    2 -> 1x2 (left-right), 3 -> 1x3, 4 -> 2x2, 5-6 -> 2x3, 7-9 -> 3x3.
    """
    if n == 2:
        return 1, 2
    if n == 3:
        return 1, 3
    if n == 4:
        return 2, 2
    if n in (5, 6):
        return 2, 3
    if 7 <= n <= 9:
        return 3, 3
    raise ValueError("Stream count must be between 2 and 9 inclusive.")


def merge_i420_grid(yuv_list: Sequence[bytes | bytearray], width: int, height: int) -> bytes:
    """
    Merge N I420 frames (same W/H) into one I420 frame.
    Layout follows ``layout_rows_cols``; unused tiles are black I420.
    """
    n = len(yuv_list)
    rows, cols = layout_rows_cols(n)

    if width % 2 or height % 2:
        raise ValueError("width and height must be even for I420.")

    expected = width * height * 3 // 2
    for i, frame in enumerate(yuv_list):
        if len(frame) != expected:
            raise ValueError(f"Frame {i}: expected {expected} bytes, got {len(frame)}")

    gw, gh = cols * width, rows * height
    cw, ch = width // 2, height // 2
    gcw, gch = cols * cw, rows * ch

    y_out = bytearray(gw * gh)
    u_out = bytearray(gcw * gch)
    v_out = bytearray(gcw * gch)

    black = _black_i420(width, height)
    tiles = rows * cols

    for idx in range(tiles):
        tr, tc = divmod(idx, cols)
        if idx < n:
            src = yuv_list[idx]
        else:
            src = black

        y_src, u_src, v_src = _split_i420_planes(src, width, height)

        # Y
        for sy in range(height):
            drow = tr * height + sy
            d0 = drow * gw + tc * width
            s0 = sy * width
            y_out[d0 : d0 + width] = y_src[s0 : s0 + width]

        # U / V (half resolution)
        for uy in range(ch):
            for ux in range(cw):
                du_row = tr * ch + uy
                du_col = tc * cw + ux
                d_uv = du_row * gcw + du_col
                s_uv = uy * cw + ux
                u_out[d_uv] = u_src[s_uv]
                v_out[d_uv] = v_src[s_uv]

    y_size = gw * gh
    c_size = gcw * gch
    return bytes(y_out) + bytes(u_out) + bytes(v_out)


def _resize_gray_bilinear(plane: np.ndarray, out_h: int, out_w: int) -> np.ndarray:
    """Resize a single-channel uint8 image (in_h, in_w) to (out_h, out_w) with bilinear sampling."""
    in_h, in_w = plane.shape
    if out_h <= 0 or out_w <= 0:
        raise ValueError("out_h and out_w must be positive.")
    if in_h <= 0 or in_w <= 0:
        raise ValueError("plane dimensions must be positive.")

    if out_h == in_h and out_w == in_w:
        return np.asarray(plane, dtype=np.uint8).copy()

    oy = np.arange(out_h, dtype=np.float32) + 0.5
    ox = np.arange(out_w, dtype=np.float32) + 0.5
    iy = oy[:, None] * (in_h / out_h) - 0.5
    ix = ox[None, :] * (in_w / out_w) - 0.5

    iy0 = np.floor(iy).astype(np.int32)
    ix0 = np.floor(ix).astype(np.int32)
    iy1 = np.clip(iy0 + 1, 0, in_h - 1)
    ix1 = np.clip(ix0 + 1, 0, in_w - 1)
    iy0 = np.clip(iy0, 0, in_h - 1)
    ix0 = np.clip(ix0, 0, in_w - 1)

    wy1 = (iy - iy0.astype(np.float32)).clip(0.0, 1.0)
    wx1 = (ix - ix0.astype(np.float32)).clip(0.0, 1.0)
    wy0 = 1.0 - wy1
    wx0 = 1.0 - wx1

    pf = plane.astype(np.float32)
    c00 = pf[iy0, ix0]
    c01 = pf[iy0, ix1]
    c10 = pf[iy1, ix0]
    c11 = pf[iy1, ix1]
    top = wx0 * c00 + wx1 * c01
    bot = wx0 * c10 + wx1 * c11
    out = wy0 * top + wy1 * bot
    return np.clip(np.rint(out), 0, 255).astype(np.uint8)


def _resize_gray_nearest(plane: np.ndarray, out_h: int, out_w: int) -> np.ndarray:
    """Nearest-neighbor resize (center-aligned sample grid)."""
    in_h, in_w = plane.shape
    if out_h == in_h and out_w == in_w:
        return np.asarray(plane, dtype=np.uint8).copy()
    iy = np.minimum(
        ((np.arange(out_h, dtype=np.float64) + 0.5) * (in_h / out_h)).astype(np.int32),
        in_h - 1,
    )
    ix = np.minimum(
        ((np.arange(out_w, dtype=np.float64) + 0.5) * (in_w / out_w)).astype(np.int32),
        in_w - 1,
    )
    return plane[iy[:, np.newaxis], ix[np.newaxis, :]]


def _integral_plane_u64(plane: np.ndarray) -> np.ndarray:
    """Prefix sums so sum of p[r0:r1, c0:c1] = I[r1,c1]-I[r0,c1]-I[r1,c0]+I[r0,c0]."""
    p = plane.astype(np.uint64)
    g = np.cumsum(np.cumsum(p, axis=0), axis=1)
    ii = np.zeros((plane.shape[0] + 1, plane.shape[1] + 1), dtype=np.uint64)
    ii[1:, 1:] = g
    return ii


def _rect_sum(ii: np.ndarray, r0: int, c0: int, r1: int, c1: int) -> int:
    """Sum of original plane over half-open rows [r0,r1), cols [c0,c1)."""
    a = int(ii[r1, c1].item())
    b = int(ii[r0, c1].item())
    c = int(ii[r1, c0].item())
    d = int(ii[r0, c0].item())
    return a - b - c + d


def _resize_gray_box_integral(plane: np.ndarray, out_h: int, out_w: int) -> np.ndarray:
    """Area-average downsample (box) using proportional source windows per output pixel."""
    in_h, in_w = plane.shape
    if out_h <= 0 or out_w <= 0:
        raise ValueError("out_h and out_w must be positive.")
    if in_h <= 0 or in_w <= 0:
        raise ValueError("plane dimensions must be positive.")
    if out_h == in_h and out_w == in_w:
        return np.asarray(plane, dtype=np.uint8).copy()

    ii = _integral_plane_u64(plane)
    out = np.empty((out_h, out_w), dtype=np.uint8)
    for yd in range(out_h):
        sy0 = yd * (in_h / out_h)
        sy1 = (yd + 1) * (in_h / out_h)
        r0 = int(np.floor(sy0))
        r1 = int(np.ceil(sy1 - 1e-12))
        r0 = max(0, min(in_h - 1, r0))
        r1 = max(r0 + 1, min(in_h, r1))
        for xd in range(out_w):
            sx0 = xd * (in_w / out_w)
            sx1 = (xd + 1) * (in_w / out_w)
            c0 = int(np.floor(sx0))
            c1 = int(np.ceil(sx1 - 1e-12))
            c0 = max(0, min(in_w - 1, c0))
            c1 = max(c0 + 1, min(in_w, c1))
            s = _rect_sum(ii, r0, c0, r1, c1)
            area = (r1 - r0) * (c1 - c0)
            v = (float(s) / float(area)) if area > 0 else 0.0
            out[yd, xd] = int(np.clip(round(v), 0, 255))
    return out


def scale_i420(
    in_yuv: bytes | bytearray,
    in_width: int,
    in_height: int,
    out_width: int,
    out_height: int,
    *,
    libyuv_filter: int = LIBYUV_FILTER_BOX,
) -> bytes:
    """
    Scale one I420 frame to ``out_width`` x ``out_height``.

    If the system ``libyuv`` library is available, uses ``I420Scale`` with
    ``libyuv_filter`` (default ``LIBYUV_FILTER_BOX``, same enum as libyuv's
    ``FilterMode``). Otherwise falls back to NumPy: box-style area average when
    both dimensions are not increased, else per-plane bilinear (not bit-identical
    to libyuv). Set env ``EXAMPLE_MERGE_YUV_NO_LIBYUV=1`` to force the fallback.

    Input and output dimensions must be even and positive.
    """
    if in_width % 2 or in_height % 2 or out_width % 2 or out_height % 2:
        raise ValueError("in_width, in_height, out_width, out_height must be even for I420.")
    if in_width <= 0 or in_height <= 0 or out_width <= 0 or out_height <= 0:
        raise ValueError("Dimensions must be positive.")

    in_y_size = in_width * in_height
    in_c_size = (in_width // 2) * (in_height // 2)
    expected = in_y_size + 2 * in_c_size
    if len(in_yuv) != expected:
        raise ValueError(f"in_yuv length mismatch: got {len(in_yuv)}, expected {expected}")

    if in_width == out_width and in_height == out_height:
        return bytes(in_yuv)

    fm = int(libyuv_filter)
    if fm < LIBYUV_FILTER_NONE or fm > LIBYUV_FILTER_BOX:
        raise ValueError("libyuv_filter must be a libyuv FilterMode value (0..3).")

    native = _scale_i420_libyuv_native(
        in_yuv, in_width, in_height, out_width, out_height, fm
    )
    if native is not None:
        return native

    mv = memoryview(in_yuv)
    Y = np.frombuffer(mv[:in_y_size], dtype=np.uint8).reshape(in_height, in_width)
    U = np.frombuffer(mv[in_y_size : in_y_size + in_c_size], dtype=np.uint8).reshape(
        in_height // 2, in_width // 2
    )
    V = np.frombuffer(
        mv[in_y_size + in_c_size : in_y_size + 2 * in_c_size],
        dtype=np.uint8,
    ).reshape(in_height // 2, in_width // 2)

    if fm == LIBYUV_FILTER_NONE:
        resizer = _resize_gray_nearest
    elif fm == LIBYUV_FILTER_BOX:
        if out_width <= in_width and out_height <= in_height:
            resizer = _resize_gray_box_integral
        else:
            resizer = _resize_gray_bilinear
    else:
        # kFilterLinear / kFilterBilinear: approximate both as full bilinear off native.
        resizer = _resize_gray_bilinear

    out_y = resizer(Y, out_height, out_width)
    out_u = resizer(U, out_height // 2, out_width // 2)
    out_v = resizer(V, out_height // 2, out_width // 2)

    return out_y.tobytes() + out_u.tobytes() + out_v.tobytes()


def i420_to_rgb_numpy(yuv: bytes | bytearray, width: int, height: int) -> np.ndarray:
    """Convert I420 to RGB uint8 array shape (height, width, 3)."""
    if width % 2 or height % 2:
        raise ValueError("width and height must be even for I420.")

    y_size = width * height
    c_size = (width // 2) * (height // 2)
    mv = memoryview(yuv)
    if len(mv) != y_size + 2 * c_size:
        raise ValueError("I420 buffer size mismatch for i420_to_rgb_numpy.")

    Y = np.frombuffer(mv[:y_size], dtype=np.uint8).reshape(height, width)
    U = np.frombuffer(mv[y_size : y_size + c_size], dtype=np.uint8).reshape(height // 2, width // 2)
    V = np.frombuffer(mv[y_size + c_size : y_size + 2 * c_size], dtype=np.uint8).reshape(height // 2, width // 2)

    U_up = np.repeat(np.repeat(U, 2, axis=0), 2, axis=1)[:height, :width]
    V_up = np.repeat(np.repeat(V, 2, axis=0), 2, axis=1)[:height, :width]

    yf = Y.astype(np.float32)
    uf = U_up.astype(np.float32) - 128.0
    vf = V_up.astype(np.float32) - 128.0

    r = yf + 1.402 * vf
    g = yf - 0.344136 * uf - 0.714136 * vf
    b = yf + 1.772 * uf
    rgb = np.stack([r, g, b], axis=-1)
    return np.clip(rgb, 0, 255).astype(np.uint8)


def save_merged_image(
    merged_i420: bytes | bytearray,
    out_width: int,
    out_height: int,
    path: str,
    image_format: str,
) -> None:
    """Save I420 frame as JPEG or PNG (same as ``i420_to_image``)."""
    fmt = image_format.lower()
    if fmt == "jpg":
        fmt = "jpeg"
    if fmt not in ("jpeg", "png"):
        raise ValueError("image_format must be jpeg, jpg, or png")

    rgb = i420_to_rgb_numpy(merged_i420, out_width, out_height)
    img = Image.fromarray(rgb, mode="RGB")
    if fmt == "jpeg":
        img.save(path, format="JPEG", quality=95)
    else:
        img.save(path, format="PNG")


def i420_to_image(
    merged_i420: bytes | bytearray,
    out_width: int,
    out_height: int,
    path: str,
    image_format: str,
) -> None:
    """Alias for :func:`save_merged_image` (plan naming)."""
    save_merged_image(merged_i420, out_width, out_height, path, image_format)


def _read_first_frame(path: str, frame_bytes: int) -> bytes:
    with open(path, "rb") as f:
        data = f.read(frame_bytes)
    if len(data) != frame_bytes:
        raise ValueError(f"{path}: expected {frame_bytes} bytes for one frame, got {len(data)}")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Merge 2–9 I420 YUV frames into a fixed grid layout and save as JPEG/PNG."
    )
    parser.add_argument("--width", type=int, required=True, help="Luma width per input frame")
    parser.add_argument("--height", type=int, required=True, help="Luma height per input frame")
    parser.add_argument("--out", required=True, help="Output image path (.jpg / .jpeg / .png)")
    parser.add_argument(
        "--format",
        choices=("jpeg", "jpg", "png"),
        default=None,
        help="Output image type (default: infer from --out extension)",
    )
    parser.add_argument(
        "--output-yuv",
        metavar="PATH",
        help="Optional path to write merged raw I420 (.yuv or any filename)",
    )
    parser.add_argument(
        "--yuv",
        nargs="+",
        metavar="FILE",
        default=None,
        help="Input YUV paths (2..9). Alternative to positional paths.",
    )
    parser.add_argument(
        "yuv_files",
        nargs="*",
        default=[],
        help="Input YUV paths when --yuv is omitted (first frame of each file).",
    )

    args = parser.parse_args(argv)

    yuv_files = list(args.yuv) if args.yuv else list(args.yuv_files)
    if not yuv_files:
        parser.error("Provide input YUV files via --yuv or as positional arguments.")
    n = len(yuv_files)
    if not 2 <= n <= 9:
        parser.error("Provide between 2 and 9 input YUV files.")

    w, h = args.width, args.height
    frame_bytes = w * h * 3 // 2

    frames = [_read_first_frame(p, frame_bytes) for p in yuv_files]
    merged = merge_i420_grid(frames, w, h)

    if args.output_yuv:
        with open(args.output_yuv, "wb") as out_yuv:
            out_yuv.write(merged)

    rows, cols = layout_rows_cols(n)
    ow, oh = cols * w, rows * h

    out_fmt = args.format
    if out_fmt is None:
        low = args.out.lower()
        if low.endswith(".png"):
            out_fmt = "png"
        elif low.endswith(".jpg") or low.endswith(".jpeg"):
            out_fmt = "jpeg"
        else:
            parser.error("Cannot infer --format from --out; pass --format explicitly.")

    i420_to_image(merged, ow, oh, args.out, out_fmt)
    print(f"Wrote {args.out} ({ow}x{oh}, {out_fmt})")
    if args.output_yuv:
        print(f"Wrote merged I420: {args.output_yuv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
