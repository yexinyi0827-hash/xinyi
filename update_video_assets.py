from pathlib import Path
from PIL import Image
import re
import shutil
import subprocess

Image.MAX_IMAGE_PIXELS = None

ROOT = Path("C:/Users/Y/Desktop/\u8bbe\u8ba1\u4f5c\u54c1\u96c6/\u89c6\u9891\u5c01\u9762")
SITE = Path("C:/Users/Y/Documents/\u957f\u56fe\u6d77\u62a5/portfolio-site")
PORTFOLIO_DIR = SITE / "assets" / "portfolio"
VIDEO_DIR = SITE / "assets" / "videos"
DATA_FILE = SITE / "portfolio-data.js"
FFMPEG = Path("C:/Users/Y/Documents/skill/videos/lingxi-zhibao-scenario/node_modules/ffmpeg-static/ffmpeg.exe")

COVERS = [
    ("\u0034\u6b65\u5b9e\u73b0\u56fd\u4f01\u7a7f\u900f\u5f0f\u76d1\u7ba1\u5c01\u9762.png", "\u4e09\u6b65\u4e03\u573a\u666f\u56fd\u4f01\u8d44\u4ea7\u7a7f\u900f\u5f0f\u76d1\u7ba1.mp4", "\u56fd\u4f01\u7a7f\u900f\u5f0f\u76d1\u7ba1"),
    ("ai\u6536\u8d39pos\u5c01\u9762.png", "ai\u6536\u8d39pos.mp4", "AI\u6536\u8d39POS"),
    ("ai\u7f34\u8d39\u4e91\u89c6\u9891\u5c01\u9762.png", "ai\u7f34\u8d39\u4e91\u89c6\u9891.mp4", "AI\u7f34\u8d39\u4e91"),
    ("\u7075\u6790\u667a\u62a501\u5c01\u9762.png", "\u7075\u6790\u667a\u62a501.mp4", "\u7075\u6790\u667a\u62a501"),
    ("\u7075\u6790\u667a\u62a5\u4ea7\u54c1\u53d1\u5e03\u5c01\u9762.png", "\u7075\u6790\u667a\u62a5\u4ea7\u54c1\u53d1\u5e03.mp4", "\u7075\u6790\u667a\u62a5\u4ea7\u54c1\u53d1\u5e03"),
    ("\u9884\u5b58\u6709\u793c.png", "\u9884\u5b58\u6709\u793c.mp4", "\u9884\u5b58\u6709\u793c"),
]


def js_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def save_cover(src, dst):
    image = Image.open(src).convert("RGB")
    width, height = image.size
    max_width = 1400
    if width > max_width:
        image = image.resize((max_width, round(height * max_width / width)), Image.Resampling.LANCZOS)
    image.save(dst, "JPEG", quality=88, optimize=True, progressive=True)


def encode_video(src, dst):
    command = [
        str(FFMPEG),
        "-y",
        "-i",
        str(src),
        "-vf",
        "scale='min(1080,iw)':-2",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "28",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-c:a",
        "aac",
        "-b:a",
        "96k",
        str(dst),
    ]
    subprocess.run(command, check=True)


def rewrite_data(items):
    text = DATA_FILE.read_text(encoding="utf-8")
    blocks = re.findall(r"  \{\n.*?\n  \},", text, flags=re.S)
    non_video = [block for block in blocks if 'category: "video"' not in block]
    lines = ["window.portfolioItems = ["]
    lines.extend(non_video)
    for item in items:
        lines.append("  {")
        for key in ["title", "category", "categoryLabel", "subtype", "src", "video", "original"]:
            lines.append(f"    {key}: {js_string(item[key])},")
        lines.append("  },")
    lines.append("];")
    lines.append(f"window.portfolioCounts = {{ ui: 10, graphic: 29, video: {len(items)} }};")
    DATA_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    if not ROOT.exists():
        raise FileNotFoundError(ROOT)
    if not FFMPEG.exists():
        raise FileNotFoundError(FFMPEG)

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    for old_video in VIDEO_DIR.glob("*"):
        if old_video.is_file():
            old_video.unlink()
    for old_cover in PORTFOLIO_DIR.glob("*-video.jpg"):
        old_cover.unlink()

    items = []
    for offset, (cover_name, video_name, title) in enumerate(COVERS):
        cover_src = ROOT / cover_name
        video_src = ROOT / video_name
        if not cover_src.exists():
            raise FileNotFoundError(cover_src)
        if not video_src.exists():
            raise FileNotFoundError(video_src)

        cover_out = PORTFOLIO_DIR / f"{40 + offset:02d}-video.jpg"
        video_out = VIDEO_DIR / f"video-{offset + 1:02d}.mp4"
        save_cover(cover_src, cover_out)
        encode_video(video_src, video_out)
        items.append(
            {
                "title": title,
                "category": "video",
                "categoryLabel": "\u77ed\u89c6\u9891",
                "subtype": "\u89c6\u9891\u5c01\u9762",
                "src": f"./assets/portfolio/{cover_out.name}",
                "video": f"./assets/videos/{video_out.name}",
                "original": f"\u89c6\u9891\u5c01\u9762/{cover_name}",
            }
        )

    rewrite_data(items)
    print({"video_items": len(items), "videos": [p.name for p in sorted(VIDEO_DIR.glob("*.mp4"))]})


if __name__ == "__main__":
    main()
