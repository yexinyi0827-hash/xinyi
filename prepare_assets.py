from pathlib import Path
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

SOURCE = Path("C:/Users/Y/Desktop/\u8bbe\u8ba1\u4f5c\u54c1\u96c6")
OUT = Path("C:/Users/Y/Documents/\u957f\u56fe\u6d77\u62a5/portfolio-site/assets/portfolio")

ASSETS = {
    "ui-dashboard.jpg": "UI\u8bbe\u8ba1/\u7f51\u9875\u8bbe\u8ba1/\u770b\u677f/\u91d1\u534e\u770b\u677f_\u753b\u677f 1 \u526f\u672c 3.png",
    "ui-payment.jpg": "UI\u8bbe\u8ba1/\u7f51\u9875\u8bbe\u8ba1/\u770b\u677f/\u56de\u6b3e\u5206\u67901.png",
    "ui-classic.jpg": "UI\u8bbe\u8ba1/\u7f51\u9875\u8bbe\u8ba1/\u7ecf\u5178\u84dd.png",
    "ui-change.jpg": "UI\u8bbe\u8ba1/\u7f51\u9875\u8bbe\u8ba1/\u53d8\u66f4.png",
    "ui-contract.jpg": "UI\u8bbe\u8ba1/\u7f51\u9875\u8bbe\u8ba1/\u7eed\u7b7e\u5408\u540c.png",
    "ui-ai.jpg": "UI\u8bbe\u8ba1/\u7f51\u9875\u8bbe\u8ba1/\u5b98\u7f51/\u5b98\u7f51-AI \u4ea7\u54c1.png",
    "ui-park.jpg": "UI\u8bbe\u8ba1/\u7f51\u9875\u8bbe\u8ba1/\u5b98\u7f51/\u5b98\u7f51-\u667a\u6167\u56ed\u533a.png",
    "ui-state.jpg": "UI\u8bbe\u8ba1/\u7f51\u9875\u8bbe\u8ba1/\u5b98\u7f51/\u5b98\u7f51-\u667a\u6167\u56fd\u8d44.png",
    "graphic-main-kv.jpg": "\u5e73\u9762/banner/\u4e3bkv2.png",
    "graphic-anniversary.jpg": "\u5e73\u9762/banner/7\u5468\u5e74.png",
    "graphic-speech.jpg": "\u5e73\u9762/banner/ai \u6f14\u8bb2\u5927\u8d5b.png",
    "graphic-cosmic.jpg": "\u5e73\u9762/banner/cosmic.png",
    "graphic-public.jpg": "\u5e73\u9762/banner/\u516c\u4f17\u53f7banner.png",
    "expo-booth.jpg": "\u5e73\u9762/\u5c55\u4f1a/\u7269\u535a\u4f1a\u5c55\u53f0\u8bbe\u8ba1.JPG",
    "expo-forum.jpg": "\u5e73\u9762/\u5c55\u4f1a/\u8bba\u575b\u6d3b\u52a8kv\u8bbe\u8ba1.jpg",
    "expo-anniversary.jpg": "\u5e73\u9762/\u5c55\u4f1a/\u5468\u5e74\u5e86\u6d3b\u52a8kv\u8bbe\u8ba1.jpg",
    "expo-invite.jpg": "\u5e73\u9762/\u5c55\u4f1a/\u6df1\u5733\u7269\u535a\u4f1a\u9080\u8bf7\u51fd.png",
    "print-calendar.jpg": "\u5e73\u9762/\u5370\u5237/\u53f0\u5386\u5c55\u793a.jpg",
    "print-fold-1.jpg": "\u5e73\u9762/\u5370\u5237/\u7269\u4e1a\u6298\u9875\uff08\u8f6c\u66f2\uff09_\u753b\u677f 1 \u526f\u672c 2.png",
    "print-fold-2.jpg": "\u5e73\u9762/\u5370\u5237/\u7269\u4e1a\u6298\u9875\uff08\u8f6c\u66f2\uff09_\u753b\u677f 1 \u526f\u672c 3.png",
    "ops-training.jpg": "\u5e73\u9762/\u8fd0\u8425/\u57f9\u8bad\u6d77\u62a5.png",
    "ops-alipay.jpg": "\u5e73\u9762/\u8fd0\u8425/\u652f\u4ed8\u5b9d\u6d3b\u52a8.png",
    "ops-startup.jpg": "\u5e73\u9762/\u8fd0\u8425/\u521b\u4e1a\u516c\u793e.png",
    "ops-flagship.jpg": "\u5e73\u9762/\u8fd0\u8425/\u65d7\u8230\u7248.png",
    "long-state.jpg": "\u5e73\u9762/\u957f\u56fe\u9875\u9762/\u56fd\u8d44\u89e3\u51b3\u65b9\u6848\u957f\u56fe.png",
    "long-pos.jpg": "\u5e73\u9762/\u957f\u56fe\u9875\u9762/pos.png",
    "long-alipay.jpg": "\u5e73\u9762/\u957f\u56fe\u9875\u9762/\u652f\u4ed8\u5b9d\u6d77\u62a5.png",
    "long-report.jpg": "\u5e73\u9762/\u957f\u56fe\u9875\u9762/\u7075\u6790\u667a\u62a5-\u957f\u56fe2.png",
    "video-01.jpg": "\u77ed\u89c6\u9891/\u7075\u6790\u667a\u62a501\u5c01\u9762.png",
    "video-02.jpg": "\u77ed\u89c6\u9891/\u7075\u6790\u667a\u62a502\u5c01\u9762.png",
    "video-release.jpg": "\u77ed\u89c6\u9891/\u7075\u6790\u667a\u62a5\u4ea7\u54c1\u53d1\u5e03\u5c01\u9762.png",
    "video-cover.jpg": "\u77ed\u89c6\u9891/\u5c01\u9762.png",
}


def save_web_image(src, dst):
    image = Image.open(src).convert("RGB")
    width, height = image.size
    max_width = 1800
    if width > max_width:
        new_height = round(height * max_width / width)
        image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
    image.save(dst, "JPEG", quality=88, optimize=True, progressive=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, source_rel in ASSETS.items():
        save_web_image(SOURCE / source_rel, OUT / name)
        print(name)


if __name__ == "__main__":
    main()
