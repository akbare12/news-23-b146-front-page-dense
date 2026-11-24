#!/usr/bin/env python3
"""news-23 b146 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Validates the PNG header with struct, checks chunk CRCs,
and refuses to write next to main.py or into the repo.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "52b27bb981ecc5541bbfb5c3f98119df35507932300c7a9cd05f1ea2ce19526f"
EXPECTED_SIZE = 197508
SRC_NAME = "entry.png"
MIN_SIZE = 10000
MAX_SIZE = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.isfile(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if out_dir_abs == here or out_dir_abs.startswith(here + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    dst = os.path.join(out_dir_abs, SRC_NAME)
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source")

    with open(src, "rb") as f:
        data = f.read()
    if len(data) < MIN_SIZE:
        return fail("source too small: %d bytes" % len(data))
    if len(data) > MAX_SIZE:
        return fail("source over 1 MiB: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("bad PNG signature")
    # First chunk must be IHDR, 13 bytes: width, height, bit depth, colour type,
    # compression, filter, interlace. CRC covers type+data, not length.
    if len(data) < 33:
        return fail("file truncated before IHDR")
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        return fail("first chunk is not a 13-byte IHDR")
    w, h, depth, ctype_b, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        return fail("expected 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype_b not in (2, 6):
        return fail("expected 8-bit RGB/RGBA, got depth %d type %d" % (depth, ctype_b))
    if comp != 0 or filt != 0 or inter != 0:
        return fail("unexpected compression/filter/interlace flags")
    crc_stored = struct.unpack(">I", data[29:33])[0]
    crc_calc = zlib.crc32(data[12:29]) & 0xFFFFFFFF
    if crc_stored != crc_calc:
        return fail("IHDR CRC mismatch")
    # Walk remaining chunks: CRC each, IDAT payload non-empty, IEND last.
    pos = 33
    idat_total = 0
    seen_iend = False
    while pos + 8 <= len(data):
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        cname = data[pos + 4:pos + 8]
        end = pos + 8 + clen + 4
        if end > len(data):
            return fail("truncated chunk %r" % cname)
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:end])[0]
        crc_calc = zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF
        if crc_stored != crc_calc:
            return fail("CRC mismatch in chunk %r" % cname)
        if cname == b"IDAT":
            if clen == 0:
                return fail("empty IDAT chunk")
            idat_total += clen
        if cname == b"IEND":
            if clen != 0:
                return fail("IEND must be 0 bytes")
            if end != len(data):
                return fail("trailing data after IEND")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        return fail("no IEND chunk found")
    if idat_total < 1000:
        return fail("IDAT payload too small: %d bytes" % idat_total)

    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        return fail("size mismatch: expected %d, got %d" % (EXPECTED_SIZE, len(data)))
    if EXPECTED_SHA256 != "0" * 64 and sha != EXPECTED_SHA256:
        return fail("sha256 mismatch: expected %s, got %s" % (EXPECTED_SHA256, sha))

    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        out = f.read()
    if out != data:
        return fail("output not byte-identical to source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
