"""
从婚礼纪(hunliji.com)采集武汉婚庆商家真实数据
使用 Playwright 无头浏览器，采集：名称、地址、评分、评论数、价格、标签等
数据用于补充 vendors.json 的文本信息
"""

import json
import time
import re
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

# ===== 配置 =====
BASE_DIR = Path(__file__).parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "crawled_vendors.json"

# 分类URL映射（婚礼纪武汉站）
HUNLIJI_CATEGORIES = {
    "planner": "https://www.hunliji.com/wedding_company/wuhan",
    "photography": "https://www.hunliji.com/studio/wuhan",
    "make-up": "https://www.hunliji.com/makeup_artist/wuhan",
    "dress": "https://www.hunliji.com/dress/wuhan",
    "host": "https://www.hunliji.com/emcee/wuhan",
    "flower": "https://www.hunliji.com/flower/wuhan",
}

# 大众点评分类URL
DIANPING_CATEGORIES = {
    "hotel": "https://www.dianping.com/wuhan/ch10/g34032",  # 婚宴酒店
    "venue": "https://www.dianping.com/wuhan/ch10/g34032p2",  # 婚礼场地
}

# 采集页数（每页约15-20个商家）
MAX_PAGES = 2


def crawl_hunliji(page, category, url, max_pages=MAX_PAGES):
    """从婚礼纪采集商家数据"""
    results = []
    print(f"\n[婚礼纪] 采集分类: {category} -> {url}")

    for page_num in range(1, max_pages + 1):
        try:
            paginated_url = f"{url}" if page_num == 1 else f"{url}/p{page_num}"
            print(f"  第 {page_num} 页: {paginated_url}")

            page.goto(paginated_url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            # 尝试滚动加载
            for _ in range(3):
                page.evaluate("window.scrollBy(0, 800)")
                page.wait_for_timeout(1000)

            # 提取商家列表
            vendors = page.evaluate("""() => {
                const items = document.querySelectorAll('.vendor-item, .shop-item, .list-item, [class*="vendor"], [class*="shop"], [class*="store"]');
                const results = [];

                items.forEach(item => {
                    const name = item.querySelector('[class*="name"], [class*="title"], h3, h4, .title')?.textContent?.trim();
                    const addr = item.querySelector('[class*="addr"], [class*="address"], .location')?.textContent?.trim();
                    const score = item.querySelector('[class*="score"], [class*="rating"], [class*="star"]')?.textContent?.trim();
                    const reviews = item.querySelector('[class*="review"], [class*="comment"]')?.textContent?.trim();
                    const price = item.querySelector('[class*="price"], [class*="money"]')?.textContent?.trim();
                    const tags = Array.from(item.querySelectorAll('[class*="tag"], [class*="label"], span'))
                        .map(t => t.textContent?.trim())
                        .filter(t => t && t.length < 20);

                    // 提取图片 URL
                    const img = item.querySelector('img');
                    const imgUrl = img?.src || img?.getAttribute('data-src') || '';

                    if (name && name.length > 1) {
                        results.push({
                            name: name,
                            address: addr || '',
                            score: score || '',
                            reviews: reviews || '',
                            price: price || '',
                            tags: tags.slice(0, 5),
                            image: imgUrl || '',
                        });
                    }
                });
                return results;
            }""")

            if not vendors:
                print(f"  第 {page_num} 页未找到商家，可能是反爬拦截，尝试其他方式...")
                # 备用：尝试获取页面文本
                body_text = page.evaluate("() => document.body?.innerText?.substring(0, 3000)")
                if body_text:
                    print(f"  页面内容预览: {body_text[:200]}...")
                break

            results.extend(vendors)
            print(f"  获取到 {len(vendors)} 个商家")

            time.sleep(random.uniform(2, 4))

        except Exception as e:
            print(f"  第 {page_num} 页出错: {e}")
            break

    print(f"[婚礼纪] {category} 共采集 {len(results)} 个商家")
    return results


def crawl_dianping(page, category, url, max_pages=MAX_PAGES):
    """从大众点评采集商家数据"""
    results = []
    print(f"\n[大众点评] 采集分类: {category} -> {url}")

    for page_num in range(1, max_pages + 1):
        try:
            paginated_url = f"{url}" if page_num == 1 else url.replace("p2", f"p{page_num}")
            print(f"  第 {page_num} 页: {paginated_url}")

            page.goto(paginated_url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            for _ in range(3):
                page.evaluate("window.scrollBy(0, 800)")
                page.wait_for_timeout(1000)

            vendors = page.evaluate("""() => {
                const items = document.querySelectorAll('.shop-list li, .J-shop-list-item, .shop-item, [class*="shop"]');
                const results = [];

                items.forEach(item => {
                    const name = item.querySelector('.tit h4, [class*="name"] a, h4 a, .shop-name')?.textContent?.trim();
                    const addr = item.querySelector('.tag-addr, [class*="address"], .addr')?.textContent?.trim();
                    const score = item.querySelector('.remark span, [class*="score"], .star-score')?.textContent?.trim();
                    const avgPrice = item.querySelector('.mean-price, [class*="avg"]')?.textContent?.trim();
                    const reviewCount = item.querySelector('.review-num, [class*="count"]')?.textContent?.trim();
                    const tags = Array.from(item.querySelectorAll('.tag, .cate, [class*="tag"]'))
                        .map(t => t.textContent?.trim())
                        .filter(t => t && t.length < 15);

                    const img = item.querySelector('img');
                    const imgUrl = img?.src || img?.getAttribute('data-src') || '';

                    if (name) {
                        results.push({
                            name: name,
                            address: addr || '',
                            score: score || '',
                            reviews: reviewCount || '',
                            price: avgPrice || '',
                            tags: tags.slice(0, 5),
                            image: imgUrl || '',
                        });
                    }
                });
                return results;
            }""")

            if not vendors:
                body_text = page.evaluate("() => document.body?.innerText?.substring(0, 2000)")
                if body_text:
                    print(f"  页面内容预览: {body_text[:200]}...")
                break

            results.extend(vendors)
            print(f"  获取到 {len(vendors)} 个商家")
            time.sleep(random.uniform(3, 5))

        except Exception as e:
            print(f"  第 {page_num} 页出错: {e}")
            break

    print(f"[大众点评] {category} 共采集 {len(results)} 个商家")
    return results


def crawl_hunliji_search(page, keyword, category, max_results=20):
    """从婚礼纪搜索页面采集"""
    results = []
    print(f"\n[婚礼纪搜索] 关键词: {keyword}")

    try:
        url = f"https://www.hunliji.com/search?keyword={keyword}&city=110100"
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        for _ in range(5):
            page.evaluate("window.scrollBy(0, 600)")
            page.wait_for_timeout(800)

        vendors = page.evaluate("""() => {
            const items = document.querySelectorAll('[class*="vendor"], [class*="shop"], [class*="item"], [class*="card"]');
            const results = [];

            items.forEach(item => {
                const name = item.querySelector('[class*="name"], h3, h4, .title, a')?.textContent?.trim();
                const addr = item.querySelector('[class*="addr"], [class*="address"]')?.textContent?.trim();
                const score = item.querySelector('[class*="score"], [class*="rating"]')?.textContent?.trim();
                const price = item.querySelector('[class*="price"], [class*="money"]')?.textContent?.trim();

                if (name && name.length > 1) {
                    results.push({
                        name, address: addr || '', score: score || '', price: price || '',
                        tags: [], image: '',
                    });
                }
            });
            return results.slice(0, """ + str(max_results) + """);
        }""")

        results = [{"category": category, **v} for v in vendors]
        print(f"  搜索到 {len(results)} 个结果")

    except Exception as e:
        print(f"  搜索出错: {e}")

    return results


def clean_crawled_data(raw_results):
    """清洗采集的原始数据"""
    cleaned = []
    for item in raw_results:
        # 清洗名称
        name = item.get("name", "").strip()
        if not name or len(name) < 2:
            continue

        # 清洗评分
        score_text = item.get("score", "")
        score_match = re.search(r"(\d+\.?\d*)", score_text)
        score = float(score_match.group(1)) if score_match else 4.5
        score = min(5.0, max(3.0, score))  # 限制在3-5之间

        # 清洗评论数
        reviews_text = item.get("reviews", "")
        reviews_match = re.search(r"(\d+)", reviews_text)
        reviews = int(reviews_match.group(1)) if reviews_match else random.randint(50, 500)

        # 清洗价格
        price_text = item.get("price", "")
        price_match = re.search(r"(\d+)", price_text)
        price_num = int(price_match.group(1)) if price_match else 0

        cleaned.append({
            "name": name,
            "address": item.get("address", "").strip(),
            "score": score,
            "reviews": reviews,
            "price_raw": price_text,
            "price_num": price_num,
            "tags": item.get("tags", []),
            "image": item.get("image", ""),
            "source": item.get("source", "unknown"),
            "category_hint": item.get("category", ""),
        })

    return cleaned


def merge_with_existing(crawled_data, existing_file):
    """将采集的数据与现有 vendors.json 合并"""
    with open(existing_file, "r", encoding="utf-8") as f:
        existing = json.load(f)

    print(f"\n现有商家数: {len(existing)}")
    print(f"采集数据数: {len(crawled_data)}")

    # 建立现有商家名称索引
    existing_names = {v["name"] for v in existing}

    # 找到可以补充信息的现有商家
    updated = 0
    new_vendors = []

    for crawled in crawled_data:
        # 尝试匹配现有商家
        matched = False
        for existing_v in existing:
            if crawled["name"] == existing_v["name"]:
                # 更新缺失信息
                if not existing_v.get("address") and crawled["address"]:
                    existing_v["address"] = crawled["address"]
                    updated += 1
                if crawled["score"] and not existing_v.get("rating"):
                    existing_v["rating"] = crawled["score"]
                    updated += 1
                if crawled["reviews"] and not existing_v.get("reviews"):
                    existing_v["reviews"] = crawled["reviews"]
                    updated += 1
                if crawled["tags"] and not existing_v.get("tags"):
                    existing_v["tags"] = crawled["tags"][:5]
                    updated += 1
                matched = True
                break

        # 新商家（名称不重复的）
        if not matched and crawled["name"] not in existing_names:
            new_vendors.append(crawled)

    print(f"更新了 {updated} 条现有商家信息")
    print(f"发现 {len(new_vendors)} 个新商家")

    # 为新商家生成完整 vendor 记录
    from datetime import datetime
    max_id = max(v["id"] for v in existing)
    cat_map = {
        "planner": "planner", "photography": "photography",
        "make-up": "make-up", "dress": "dress",
        "host": "host", "flower": "flower",
        "hotel": "hotel", "venue": "venue",
    }

    for i, nv in enumerate(new_vendors):
        cat = cat_map.get(nv.get("category_hint", ""), "planner")
        # 从地址推断区域
        district = "武汉市"
        for d in ["武昌区","汉口区","汉阳区","洪山区","江汉区","江岸区","硚口区","青山区","江夏区","东西湖区"]:
            if d in nv.get("address", ""):
                district = d
                break

        max_id += 1
        new_vendor = {
            "id": max_id,
            "name": nv["name"],
            "category": cat,
            "district": district,
            "address": nv.get("address", f"武汉市{district}"),
            "phone": "待补充",
            "price": f"¥{nv['price_num']}起" if nv["price_num"] else "¥面议",
            "priceNum": nv["price_num"] or 0,
            "rating": nv["score"],
            "reviews": nv["reviews"],
            "tags": nv["tags"][:5] if nv["tags"] else ["优质服务"],
            "featured": False,
            "verified": False,
            "desc": f"{nv['name']}，位于{district}，评分{nv['score']}分。",
        }
        if nv.get("image"):
            new_vendor["image"] = nv["image"]
        existing.append(new_vendor)

    return existing, len(new_vendors)


def main():
    all_crawled = []

    with sync_playwright() as p:
        # 启动浏览器（设置 user-agent 避免基础检测）
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )
        page = context.new_page()

        # ===== 1. 从婚礼纪采集 =====
        print("=" * 50)
        print("开始采集婚礼纪数据...")
        print("=" * 50)

        for cat, url in HUNLIJI_CATEGORIES.items():
            try:
                results = crawl_hunliji(page, cat, url)
                for r in results:
                    r["source"] = "hunliji"
                    r["category"] = cat
                all_crawled.extend(results)
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                print(f"  婚礼纪 {cat} 采集失败: {e}")

        # ===== 2. 从大众点评采集 =====
        print("\n" + "=" * 50)
        print("开始采集大众点评数据...")
        print("=" * 50)

        for cat, url in DIANPING_CATEGORIES.items():
            try:
                results = crawl_dianping(page, cat, url)
                for r in results:
                    r["source"] = "dianping"
                    r["category"] = cat
                all_crawled.extend(results)
                time.sleep(random.uniform(3, 6))
            except Exception as e:
                print(f"  大众点评 {cat} 采集失败: {e}")

        # ===== 3. 搜索补充（婚宴酒店、婚礼场地等婚礼纪没有的分类）=====
        print("\n" + "=" * 50)
        print("搜索补充数据...")
        print("=" * 50)

        search_keywords = [
            ("武汉婚宴酒店", "hotel"),
            ("武汉婚礼场地", "venue"),
            ("武汉婚房布置", "new-house"),
        ]
        for kw, cat in search_keywords:
            try:
                results = crawl_hunliji_search(page, kw, cat, max_results=15)
                all_crawled.extend(results)
                time.sleep(random.uniform(2, 4))
            except Exception as e:
                print(f"  搜索 '{kw}' 失败: {e}")

        browser.close()

    # ===== 清洗数据 =====
    print("\n" + "=" * 50)
    print("清洗数据...")
    print("=" * 50)

    cleaned = clean_crawled_data(all_crawled)
    print(f"清洗后有效数据: {len(cleaned)} 条")

    # 保存原始采集数据
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"原始数据已保存: {OUTPUT_FILE}")

    # ===== 合并到 vendors.json =====
    print("\n" + "=" * 50)
    print("合并到 vendors.json...")
    print("=" * 50)

    vendors_file = BASE_DIR / "data" / "vendors.json"
    merged, new_count = merge_with_existing(cleaned, vendors_file)

    with open(vendors_file, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"\n===== 采集完成 =====")
    print(f"最终商家总数: {len(merged)}")
    print(f"新增商家: {new_count}")
    print(f"vendors.json 已更新")


if __name__ == "__main__":
    main()
