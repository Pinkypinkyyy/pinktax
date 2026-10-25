"""Every <img> carries width and height so the browser reserves its box.

Lighthouse (25 Oct 2026) flagged the header and footer logo as unsized on
every page. The logo is shown at a fixed CSS height (34px header, 30px
footer) with the width following the file's aspect ratio (300x139), so the
attributes below are the displayed size, not the file size.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# individuals/ is being added on feat/individuals-booking-page-2026-10-25 (#16)
# with the old unsized logo tags. It is exempt so this branch cannot block
# that merge; drop the exemption once its logos carry width and height.
EXEMPT = {"individuals/index.html"}
PAGES = [
    p for p in ROOT.rglob("*.html")
    if ".git" not in p.parts and p.relative_to(ROOT).as_posix() not in EXEMPT
]
IMG = re.compile(r"<img\b[^>]*>")


def test_logo_is_sized_and_keeps_its_aspect_ratio():
    seen = 0
    for p in PAGES:
        for tag in IMG.findall(p.read_text(encoding="utf-8")):
            if "logo-white.png" not in tag:
                continue
            seen += 1
            w = int(re.search(r'width="(\d+)"', tag).group(1))
            h = int(re.search(r'height="(\d+)"', tag).group(1))
            assert abs(w / h - 300 / 139) < 0.05, f"{p.relative_to(ROOT)}: {tag}"
    assert seen >= 40


def test_every_img_has_alt_and_dimensions():
    for p in PAGES:
        for tag in IMG.findall(p.read_text(encoding="utf-8")):
            assert " alt=" in tag, f"{p.relative_to(ROOT)}: missing alt: {tag}"
            assert 'width="' in tag and 'height="' in tag, f"{p.relative_to(ROOT)}: unsized: {tag}"
