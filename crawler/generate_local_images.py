#!/usr/bin/env python3
"""
使用 SVG + Python Pillow 生成婚庆主题配图
无需外网，本地生成，每张图都有差异化设计
"""

import json
import os
import random
from pathlib import Path

# 纯 Python 实现，不依赖 Pillow（用 SVG）

# ===== 配色方案（婚庆风格）=====
PALETTES = [
    # (主色, 辅色, 点缀色, 描述)
    ("#f8b4c8", "#fce4ec", "#e91e63", "粉色浪漫"),
    ("#d4a574", "#fdf5e6", "#8b4513", "优雅金棕"),
    ("#b8c7d6", "#e8f0fa", "#4a6fa5", "清新蓝调"),
    ("#e8d5c4", "#faf0e6", "#8b6f47", "温暖裸色"),
    ("#c8e6c9", "#f1f8e9", "#4caf50", "自然绿意"),
    ("#ffccbc", "#fbe9e7", "#ff5722", "活力橙红"),
    ("#d1c4e9", "#ede7f6", "#673ab7", "高贵紫韵"),
    ("#fff9c4", "#fffde7", "#fbc02d", "阳光明黄"),
    ("#b2dfdb", "#e0f2f1", "#009688", "清新薄荷"),
    ("#ffcdd2", "#ffebee", "#f44336", "经典中国红"),
]

# 分类图标（SVG path 简化版）
CATEGORY_ICONS = {
    "photography": ("📷", "摄影"),
    "make-up": ("💄", "化妆"),
    "venue": ("🏨", "场地"),
    "hotel": ("🥂", "酒店"),
    "planner": ("📋", "策划"),
    "host": ("🎤", "主持"),
    "dress": ("👗", "礼服"),
    "flower": ("💐", "花艺"),
    "new-house": ("🏠", "婚房"),
}

# 武汉区域关键词
WH_DISTRICTS = ["武昌", "江汉", "江岸", "洪山", "硚口", "汉阳", "江夏", "青山"]


def make_vendor_image_svg(vendor, img_type="main", index=0):
    """
    生成单个商家配图的 SVG 内容
    img_type: "main" | "case_1" | "case_2" | "case_3"
    """
    vid = vendor["id"]
    name = vendor.get("name", "商家")
    category = vendor.get("category", "planner")
    district = vendor.get("district", "武汉")

    # 选择配色（基于商家 id 确定，保证一致性）
    palette = PALETTES[(vid + index) % len(PALETTES)]
    c1, c2, c_accent, palette_name = palette

    cat_info = CATEGORY_ICONS.get(category, ("💍", "婚庆"))
    cat_icon, cat_label = cat_info

    # ===== 根据 img_type 确定内容 =====
    if img_type == "main":
        # 主图：商家名称 + 分类标识
        title_text = name[:12]  # 限制长度
        sub_text = f"{cat_label} · {district}"
        show_icon = True
        show_rating = True
        decoration = "elegant"  # 优雅装饰
    else:
        # 案例图：场景化展示
        case_themes = [
            ("婚礼现场", "Wedding Scene"),
            ("布置细节", "Details"),
            ("幸福瞬间", "Happy Moment"),
            ("浪漫场景", "Romantic View"),
        ]
        theme_idx = index % len(case_themes)
        title_text = case_themes[theme_idx][0]
        sub_text = case_themes[theme_idx][1]
        show_icon = False
        show_rating = False
        decoration = ["warm", "fresh", "elegant", "dreamy"][index % 4]

    # ===== SVG 背景 =====
    # 渐变背景
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">',
        '<defs>',
        f'<linearGradient id="bg_{vid}_{index}" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'<stop offset="0%" stop-color="{c1}"/>',
        f'<stop offset="100%" stop-color="{c2}"/>',
        '</linearGradient>',
        f'<radialGradient id="circle_{vid}_{index}" cx="50%" cy="50%">',
        f'<stop offset="0%" stop-color="{c_accent}" stop-opacity="0.3"/>',
        f'<stop offset="100%" stop-color="{c_accent}" stop-opacity="0"/>',
        '</radialGradient>',
    ]

    # 装饰性形状
    if decoration == "elegant":
        svg_parts.append(f'<filter id="shadow_{vid}_{index}"><feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.2"/></filter>')

    svg_parts.append('</defs>')

    # 背景矩形
    svg_parts.append(f'<rect width="800" height="600" fill="url(#bg_{vid}_{index})"/>')

    # 装饰性圆形
    circles = [
        (650, 100, 180, 0.08),
        (100, 500, 120, 0.06),
        (400, 300, 200, 0.04),
        (750, 500, 100, 0.07),
    ]
    for cx, cy, r, opacity in circles:
        svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c_accent}" opacity="{opacity}"/>')

    # 装饰性线条（优雅感）
    if decoration in ("elegant", "dreamy"):
        svg_parts.append(f'<line x1="50" y1="150" x2="250" y2="150" stroke="{c_accent}" stroke-width="1" opacity="0.3"/>')
        svg_parts.append(f'<line x1="550" y1="450" x2="750" y2="450" stroke="{c_accent}" stroke-width="1" opacity="0.3"/>')

    # ===== 主内容 =====
    # 中心装饰圆
    svg_parts.append(f'<circle cx="400" cy="240" r="80" fill="rgba(255,255,255,0.25)"/>')
    svg_parts.append(f'<circle cx="400" cy="240" r="60" fill="rgba(255,255,255,0.35)"/>')

    # 图标或文字
    if show_icon:
        # 用 icon 占位（SVG 中可以用 text 显示 emoji）
        svg_parts.append(
            f'<text x="400" y="255" font-size="50" text-anchor="middle" '
            f'fill="white" font-weight="bold" font-family="serif">{cat_icon}</text>'
        )
    else:
        # 案例图：纯装饰图案
        svg_parts.append(f'<rect x="370" y="210" width="60" height="60" rx="10" fill="rgba(255,255,255,0.3)"/>')
        svg_parts.append(
            f'<text x="400" y="248" font-size="28" text-anchor="middle" '
            f'fill="white" font-weight="bold">✦</text>'
        )

    # 主标题
    svg_parts.append(
        f'<text x="400" y="370" font-size="36" text-anchor="middle" '
        f'fill="white" font-weight="bold" font-family="PingFang SC, Microsoft YaHei, sans-serif">'
        f'{title_text}</text>'
    )

    # 副标题
    svg_parts.append(
        f'<text x="400" y="415" font-size="18" text-anchor="middle" '
        f'fill="white" opacity="0.85" font-family="PingFang SC, Microsoft YaHei, sans-serif">'
        f'{sub_text}</text>'
    )

    # 评分星级（仅主图）
    if show_rating:
        rating = vendor.get("rating", 4.8)
        stars_text = "★ " * int(rating) + ("☆" if rating % 1 >= 0.5 else "")
        svg_parts.append(
            f'<text x="400" y="460" font-size="22" text-anchor="middle" '
            f'fill="#FFD700" font-family="sans-serif">{stars_text}</text>'
        )
        svg_parts.append(
            f'<text x="400" y="490" font-size="16" text-anchor="middle" '
            f'fill="white" opacity="0.8" font-family="sans-serif">{rating} 分</text>'
        )

    # 底部标签
    if img_type == "main" and vendor.get("tags"):
        tags = vendor["tags"][:3]
        tag_x = 400 - len(tags) * 50
        for i, tag in enumerate(tags):
            tx = tag_x + i * 100
            svg_parts.append(
                f'<rect x="{tx-35}" y="520" width="70" height="28" rx="14" '
                f'fill="rgba(255,255,255,0.3)"/>'
            )
            svg_parts.append(
                f'<text x="{tx}" y="538" font-size="13" text-anchor="middle" '
                f'fill="white" font-family="PingFang SC, sans-serif">{tag}</text>'
            )

    # 底部水印
    svg_parts.append(
        f'<text x="400" y="580" font-size="12" text-anchor="middle" '
        f'fill="white" opacity="0.4" font-family="sans-serif">武汉婚庆目录 · 武汉婚庆服务商</text>'
    )

    svg_parts.append('</svg>')

    return "\n".join(svg_parts)


def generate_images_for_all_vendors():
    """为所有商家生成配图"""
    base_dir = Path(__file__).parent.parent
    images_dir = base_dir / "images"
    vendors_file = base_dir / "data" / "vendors.json"

    images_dir.mkdir(exist_ok=True)

    # 加载商家数据
    with open(vendors_file, "r", encoding="utf-8") as f:
        vendors = json.load(f)

    print(f"共 {len(vendors)} 个商家需要生成配图")
    print(f"图片保存到: {images_dir}")

    generated = {"main": 0, "gallery": 0}
    updated_vendors = 0

    for vendor in vendors:
        vid = vendor["id"]
        vendor["image"] = f"images/vendor_{vid}_main.svg"

        # 生成主图
        main_svg = make_vendor_image_svg(vendor, "main", 0)
        main_path = images_dir / f"vendor_{vid}_main.svg"
        if not main_path.exists():
            with open(main_path, "w", encoding="utf-8") as f:
                f.write(main_svg)
        generated["main"] += 1

        # 生成3张案例图
        gallery = []
        for i in range(1, 4):
            case_svg = make_vendor_image_svg(vendor, f"case_{i}", i)
            case_path = images_dir / f"vendor_{vid}_case_{i}.svg"
            if not case_path.exists():
                with open(case_path, "w", encoding="utf-8") as f:
                    f.write(case_svg)
            gallery.append(f"images/vendor_{vid}_case_{i}.svg")
            generated["gallery"] += 1

        vendor["gallery"] = gallery
        updated_vendors += 1

        if updated_vendors % 10 == 0:
            print(f"  已处理 {updated_vendors}/{len(vendors)}")

    # 保存更新后的 vendors.json
    with open(vendors_file, "w", encoding="utf-8") as f:
        json.dump(vendors, f, ensure_ascii=False, indent=2)

    print(f"\n===== 完成 =====")
    print(f"主图: {generated['main']} 张")
    print(f"案例图: {generated['gallery']} 张")
    print(f"已更新 {updated_vendors} 个商家的图片字段")
    print(f"vendors.json 已更新，图片路径为 SVG 文件")


def generate_preview_html():
    """生成预览 HTML，在浏览器中查看所有图片效果"""
    base_dir = Path(__file__).parent.parent
    images_dir = base_dir / "images"
    vendors_file = base_dir / "data" / "vendors.json"

    with open(vendors_file, "r", encoding="utf-8") as f:
        vendors = json.load(f)

    html_parts = [
        "<!DOCTYPE html>",
        "<html lang='zh-CN'><head><meta charset='UTF-8'><title>商家配图预览</title>",
        "<style>",
        "body { font-family: sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }",
        ".vendor-card { background: white; border-radius: 12px; padding: 16px; margin: 16px; display: inline-block; width: 220px; vertical-align: top; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }",
        ".vendor-card img, .vendor-card object { width: 100%; height: 160px; object-fit: cover; border-radius: 8px; }",
        ".vendor-name { font-weight: bold; margin-top: 8px; font-size: 14px; }",
        ".vendor-cat { color: #999; font-size: 12px; }",
        ".gallery { display: flex; gap: 4px; margin-top: 8px; }",
        ".gallery object { width: 70px; height: 50px; border-radius: 4px; }",
        "</style></head><body>",
        "<h1>商家配图预览（SVG 本地生成）</h1>",
    ]

    for vendor in vendors[:20]:  # 预览前20个
        vid = vendor["id"]
        main_svg = f"images/vendor_{vid}_main.svg"
        html_parts.append(f"<div class='vendor-card'>")
        html_parts.append(f"<object data='{main_svg}' type='image/svg+xml' width='200' height='160'></object>")
        html_parts.append(f"<div class='vendor-name'>{vendor['name']}</div>")
        html_parts.append(f"<div class='vendor-cat'>{vendor.get('category','')}</div>")
        html_parts.append("<div class='gallery'>")
        for i in range(1, 4):
            case_svg = f"images/vendor_{vid}_case_{i}.svg"
            html_parts.append(f"<object data='{case_svg}' type='image/svg+xml' width='70' height='50'></object>")
        html_parts.append("</div></div>")

    html_parts.append("</body></html>")

    preview_file = base_dir / "preview_images.html"
    with open(preview_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    print(f"\n预览文件已生成: {preview_file}")
    return str(preview_file)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        generate_preview_html()
    else:
        generate_images_for_all_vendors()
        generate_preview_html()
