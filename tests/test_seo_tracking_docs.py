"""docs/TRACKING.md must name the pixel track.js actually loads."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_tracking_doc_matches_the_live_tag_ids():
    track = (ROOT / "track.js").read_text(encoding="utf-8")
    doc = (ROOT / "docs" / "TRACKING.md").read_text(encoding="utf-8")
    for var in ("GA", "GT", "META"):
        value = re.search(rf'var {var} = "([^"]+)";', track).group(1)
        assert value in doc, f"docs/TRACKING.md does not mention {var} {value}"
