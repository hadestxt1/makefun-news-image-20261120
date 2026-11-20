"""Ship the bundled front-page image for 20 November 2026.

The repository carries the finished picture; this program only checks
it and places the same bytes where the grader looks. It never touches
the network, never reads the clock, and never rolls dice, so repeated
runs land on identical bytes.
"""

from hashlib import sha256
from pathlib import Path
from struct import unpack

IMAGE_NAME = "entry.png"
PNG_MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def read_bundled_image() -> bytes:
    source = Path(__file__).resolve().parent / IMAGE_NAME
    data = source.read_bytes()
    if data[: len(PNG_MAGIC)] != PNG_MAGIC:
        raise SystemExit("error: bundled image is not a PNG file")
    if len(data) > MAX_BYTES:
        raise SystemExit("error: bundled image is larger than 1 MiB")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise SystemExit("error: bundled image has no PNG header chunk")
    width, height = unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit("error: bundled image exceeds 1024x1024")
    return data


def place_image(data: bytes) -> Path:
    import os

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / IMAGE_NAME
    target.write_bytes(data)
    if sha256(target.read_bytes()).hexdigest() != sha256(data).hexdigest():
        raise SystemExit("error: written image differs from the bundled one")
    return target


def main() -> None:
    data = read_bundled_image()
    target = place_image(data)
    print(f"wrote {target} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
