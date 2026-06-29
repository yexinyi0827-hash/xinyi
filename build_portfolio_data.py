from pathlib import Path
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

SOURCE = Path("C:/Users/Y/Desktop/\u8bbe\u8ba1\u4f5c\u54c1\u96c6")
SITE = Path("C:/Users/Y/Documents/\u957f\u56fe\u6d77\u62a5/portfolio-site")
ASSET_DIR = SITE / "assets" / "portfolio"
DATA_FILE = SITE / "portfolio-data.js"

CATEGORY_LABELS = {
    "UI\u8bbe\u8ba1": ("ui", "UI"),
    "\u5e73\u9762": ("graphic", "\u5e73\u9762"),
    "\u77ed\u89c6\u9891": ("video", "\u77ed\u89c6\u9891"),
}

EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
CATEGORY_ORDER = {"ui": 0, "graphic": 1, "video": 2}


def js_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def title_from_path(path):
    stem = path.stem
    for suffix in ["_\u753b\u677f 1", " \u526f\u672c 3", " \u526f\u672c 2"]:
        stem = stem.replace(suffix, "")
    return stem


def ui_order(path):
    rel = path.relative_to(SOURCE)
    name = path.name
    if rel.parts[0] != "UI\u8bbe\u8ba1":
        return (99, str(rel))
    if "\u5b98\u7f51" in rel.parts and name.startswith("\u5b98\u7f51-"):
        return (0, str(rel))
    if "\u5b98\u7f51" in rel.parts:
        return (1, str(rel))
    if "\u770b\u677f" in rel.parts:
        return (3, str(rel))
    return (2, str(rel))


def subtype_for_path(path, category_label):
    rel = path.relative_to(SOURCE)
    if rel.parts[0] == "UI\u8bbe\u8ba1":
        if "\u5b98\u7f51" in rel.parts and path.name.startswith("\u5b98\u7f51-"):
            return "\u5b98\u7f51Banner"
        if "\u5b98\u7f51" in rel.parts:
            return "\u5b98\u7f51\u9875\u9762"
        if "\u770b\u677f" in rel.parts:
            return "\u770b\u677f"
        return "\u4ea7\u54c1\u9875\u9762"
    return rel.parts[1] if len(rel.parts) > 2 else rel.parts[-2] if len(rel.parts) > 1 else category_label


def asset_name(index, category, path):
    return f"{index:02d}-{category}.jpg"


def save_asset(src, dst):
    image = Image.open(src).convert("RGB")
    width, height = image.size
    max_width = 1800
    if width > max_width:
        new_height = round(height * max_width / width)
        image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
    image.save(dst, "JPEG", quality=88, optimize=True, progressive=True)


def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for old in ASSET_DIR.glob("*.jpg"):
        old.unlink()

    files = [p for p in SOURCE.rglob("*") if p.is_file() and p.suffix.lower() in EXTS]
    files.sort(
        key=lambda p: (
            CATEGORY_ORDER[CATEGORY_LABELS[p.relative_to(SOURCE).parts[0]][0]],
            ui_order(p),
            str(p.relative_to(SOURCE)),
        )
    )

    items = []
    counts = {"ui": 0, "graphic": 0, "video": 0}
    for index, path in enumerate(files, 1):
        top = path.relative_to(SOURCE).parts[0]
        category, label = CATEGORY_LABELS[top]
        counts[category] += 1
        name = asset_name(index, category, path)
        save_asset(path, ASSET_DIR / name)
        rel = path.relative_to(SOURCE)
        items.append(
            {
                "title": title_from_path(path),
                "category": category,
                "categoryLabel": label,
                "subtype": subtype_for_path(path, label),
                "src": f"./assets/portfolio/{name}",
                "original": str(rel).replace("\\", "/"),
            }
        )

    lines = [
        "window.portfolioItems = [",
    ]
    for item in items:
        lines.append("  {")
        for key in ["title", "category", "categoryLabel", "subtype", "src", "original"]:
            lines.append(f"    {key}: {js_string(item[key])},")
        lines.append("  },")
    lines.append("];")
    lines.append(f"window.portfolioCounts = {{ ui: {counts['ui']}, graphic: {counts['graphic']}, video: {counts['video']} }};")
    DATA_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print({"total": len(items), "counts": counts})


if __name__ == "__main__":
    main()
