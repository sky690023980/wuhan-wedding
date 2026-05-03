"""
从 Unsplash + Pexels 批量下载免费商用婚庆配图
按商家分类匹配关键词，为每个商家下载一张主图 + 3张案例图
所有图片均可免费商用，无需担心版权问题
"""

import json
import os
import time
import random
import requests
import urllib.parse
from pathlib import Path

# ===== 配置 =====
BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "images"
VENDORS_FILE = BASE_DIR / "data" / "vendors.json"

# Pexels API (免费，需注册 https://www.pexels.com/api/)
# 如果没有 key，使用 Unsplash Source（无需 API key）
PEXELS_API_KEY = ""  # 填入 Pexels API key 或留空

# 分类 -> 搜索关键词映射（英文，图片质量更好）
CATEGORY_KEYWORDS = {
    "photography": ["wedding photography", "bride portrait", "wedding couple"],
    "make-up": ["bridal makeup", "makeup artist", "bride beauty"],
    "venue": ["wedding venue", "outdoor ceremony", "wedding arch"],
    "hotel": ["wedding banquet", "hotel ballroom", "reception hall"],
    "planner": ["wedding decoration", "wedding flowers", "wedding setup"],
    "host": ["wedding ceremony", "microphone stage", "wedding reception"],
    "dress": ["wedding dress", "bridal gown", "white dress"],
    "flower": ["wedding bouquet", "floral arrangement", "bridal flowers"],
    "new-house": ["red wedding decor", "chinese wedding room", "festive decoration"],
}

# 每个分类多准备几个关键词轮换
CATEGORY_EXTRA_KEYWORDS = {
    "photography": ["wedding photo", "marriage photography", "engagement shoot"],
    "make-up": ["bridal hair", "makeup vanity", "bridal stylist"],
    "venue": ["garden wedding", "beach wedding", "chapel wedding"],
    "hotel": ["elegant banquet", "wedding dinner", "grand ballroom"],
    "planner": ["wedding planner", "event design", "romantic setup"],
    "host": ["wedding mc", "stage lights", "celebration event"],
    "dress": ["vintage wedding dress", "princess gown", "lace dress"],
    "flower": ["rose bouquet", "table centerpiece", "flower wall"],
    "new-house": ["double happiness", "red lanterns", "bridal chamber"],
}


def get_unsplash_images(query, count=1):
    """从 Unsplash Source 下载图片（无需 API key，但质量随机）"""
    urls = []
    for i in range(count):
        # Unsplash Source API（免费，随机返回相关图片）
        url = f"https://source.unsplash.com/800x600/?{urllib.parse.quote(query)}&sig={random.randint(1,99999)}"
        urls.append(url)
    return urls


def get_pexels_images(query, count=1):
    """从 Pexels API 下载图片（需要免费 API key）"""
    if not PEXELS_API_KEY:
        return []
    headers = {"Authorization": PEXELS_API_KEY}
    try:
        resp = requests.get(
            "https://api.pexels.com/v1/search",
            params={"query": query, "per_page": count, "orientation": "landscape"},
            headers=headers,
            timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            return [photo["src"]["large"] for photo in data.get("photos", [])]
    except Exception as e:
        print(f"  Pexels API error: {e}")
    return []


def get_pixabay_images(query, count=1):
    """从 Pixabay API 下载图片（免费，无需 key 也能用基础功能）"""
    try:
        resp = requests.get(
            "https://pixabay.com/api/",
            params={
                "key": "48294571-5f58d4ba95eab3b30e0fafe62",  # 公开演示 key
                "q": query,
                "image_type": "photo",
                "orientation": "horizontal",
                "per_page": count,
                "safesearch": True,
            },
            timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            results = []
            for hit in data.get("hits", []):
                # 选大图 URL
                img_url = hit.get("largeImageURL") or hit.get("webformatURL")
                if img_url:
                    results.append(img_url)
            return results
    except Exception as e:
        print(f"  Pixabay API error: {e}")
    return []


def download_image(url, save_path, timeout=20):
    """下载单张图片"""
    try:
        resp = requests.get(url, timeout=timeout, stream=True, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if resp.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            # 检查文件大小（太小可能是错误页）
            if os.path.getsize(save_path) < 5000:
                os.remove(save_path)
                return False
            return True
    except Exception as e:
        print(f"  Download error: {e}")
        if os.path.exists(save_path):
            os.remove(save_path)
    return False


def get_image_for_vendor(vendor, image_type="main"):
    """为单个商家获取图片 URL 列表"""
    category = vendor.get("category", "planner")
    keywords = CATEGORY_KEYWORDS.get(category, ["wedding"])
    extra = CATEGORY_EXTRA_KEYWORDS.get(category, [])

    # 加入商家名中的关键词（如果有品牌感）
    name = vendor.get("name", "")

    if image_type == "main":
        # 主图用核心关键词
        kw = keywords[0]
    else:
        # 案例图用不同关键词
        kw = random.choice(keywords + extra)

    return kw


def main():
    # 加载商家数据
    with open(VENDORS_FILE, "r", encoding="utf-8") as f:
        vendors = json.load(f)

    print(f"共 {len(vendors)} 个商家需要配图")
    IMAGES_DIR.mkdir(exist_ok=True)

    # 统计
    success_count = 0
    fail_count = 0
    image_map = {}  # vendor_id -> {"main": "path", "gallery": ["path1", "path2", ...]}

    for vendor in vendors:
        vid = vendor["id"]
        vname = vendor["name"]
        category = vendor["category"]

        print(f"\n[{vid}/{len(vendors)}] {vname} ({category})")

        # 每个商家：1张主图 + 3张案例图
        vendor_images = {}

        # --- 主图 ---
        main_kw = get_image_for_vendor(vendor, "main")
        main_filename = f"vendor_{vid}_main.jpg"
        main_path = IMAGES_DIR / main_filename

        if main_path.exists():
            print(f"  主图已存在: {main_filename}")
            vendor_images["main"] = f"images/{main_filename}"
        else:
            # 尝试 Pixabay（质量较好，免费）
            img_urls = get_pixabay_images(main_kw, 1)
            if not img_urls:
                # 回退到 Pexels
                img_urls = get_pexels_images(main_kw, 1)
            if not img_urls:
                # 最后回退到 Unsplash Source
                img_urls = get_unsplash_images(main_kw, 1)

            if img_urls and download_image(img_urls[0], main_path):
                print(f"  主图下载成功: {main_filename}")
                vendor_images["main"] = f"images/{main_filename}"
                success_count += 1
            else:
                print(f"  主图下载失败: {vname}")
                fail_count += 1

            time.sleep(0.5)  # 避免频率限制

        # --- 案例图 (3张) ---
        gallery = []
        for i in range(3):
            gal_kw = get_image_for_vendor(vendor, "gallery")
            gal_filename = f"vendor_{vid}_case_{i+1}.jpg"
            gal_path = IMAGES_DIR / gal_filename

            if gal_path.exists():
                print(f"  案例图{i+1}已存在")
                gallery.append(f"images/{gal_filename}")
            else:
                img_urls = get_pixabay_images(gal_kw, 1)
                if not img_urls:
                    img_urls = get_pexels_images(gal_kw, 1)
                if not img_urls:
                    img_urls = get_unsplash_images(gal_kw, 1)

                if img_urls and download_image(img_urls[0], gal_path):
                    print(f"  案例图{i+1}下载成功")
                    gallery.append(f"images/{gal_filename}")
                else:
                    print(f"  案例图{i+1}下载失败")

                time.sleep(0.3)

        vendor_images["gallery"] = gallery
        image_map[str(vid)] = vendor_images

    # --- 保存图片映射 ---
    mapping_file = BASE_DIR / "data" / "image_mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(image_map, f, ensure_ascii=False, indent=2)

    print(f"\n===== 完成 =====")
    print(f"主图成功: {success_count}")
    print(f"主图失败: {fail_count}")
    print(f"图片映射已保存: {mapping_file}")

    # --- 更新 vendors.json，添加 image 和 gallery 字段 ---
    updated = 0
    for vendor in vendors:
        vid = str(vendor["id"])
        if vid in image_map:
            if image_map[vid].get("main"):
                vendor["image"] = image_map[vid]["main"]
                updated += 1
            if image_map[vid].get("gallery"):
                vendor["gallery"] = image_map[vid]["gallery"]

    with open(VENDORS_FILE, "w", encoding="utf-8") as f:
        json.dump(vendors, f, ensure_ascii=False, indent=2)

    print(f"已更新 {updated} 个商家的 image 字段")


if __name__ == "__main__":
    main()
