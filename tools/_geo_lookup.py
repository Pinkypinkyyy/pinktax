from pathlib import Path

p = Path(
    r"C:\Users\HuongBui\AppData\Local\Temp\geotargets\third_party\devsite\developers\en\google-ads\api\data\geo\geotargets-2025-10-29.csv"
)
need = [
    "Brisbane",
    "Ipswich",
    "Logan",
    "Moreton Bay",
    "Redland",
    "Gold Coast",
    "Sunshine Coast",
    "Sydney",
    "Melbourne",
    "Perth",
    "Adelaide",
    "Canberra",
    "Hobart",
    "Darwin",
]
with p.open(encoding="utf-8", errors="replace") as f:
    header = f.readline()
    print("HDR", header.strip())
    for line in f:
        if ",AU," not in line and ',"AU",' not in line:
            continue
        if not any(n in line for n in need):
            continue
        # keep city / county / region / DMA-like
        if any(t in line for t in ("City", "County", "Region", "Municipality", "Colloquial Area", "City Region")):
            print(line.strip()[:240])
