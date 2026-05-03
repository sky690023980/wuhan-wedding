"""
将 WebFetch 采集到的真实商家数据合并到 vendors.json
数据来源：买购网、城市惠、茄考网等公开网页
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
VENDORS_FILE = BASE_DIR / "data" / "vendors.json"

# ===== 新增/更新的商家数据（来源于公开网页）=====

# 买购网 - 武汉十大婚庆公司（含真实地址和详细描述）
MAIGOO_PLANNERS = [
    {
        "name": "喜庄婚礼",
        "category": "planner",
        "address": "湖北省武汉市江汉区精武路1号t2栋17楼",
        "district": "江汉区",
        "phone": "027-85806888",
        "price": "¥19800起",
        "priceNum": 19800,
        "rating": 4.9,
        "reviews": 856,
        "tags": ["高端婚庆品牌", "亚洲婚礼风尚奖", "华中地区领军", "明星婚礼"],
        "featured": True,
        "verified": True,
        "desc": "全国知名高端婚庆品牌，湖北省婚庆行业协会会长单位。致力于为高端客户策划统筹婚礼、求婚、派对等活动，成功策划过众多文娱明星、商界精英的高定婚礼。",
        "years": "15年以上"
    },
    {
        "name": "今喜缘婚礼",
        "category": "planner",
        "address": "湖北省武汉市武昌区洪山路10号",
        "district": "武昌区",
        "phone": "027-87310888",
        "price": "¥12800起",
        "priceNum": 12800,
        "rating": 4.8,
        "reviews": 623,
        "tags": ["省婚庆协会副会长", "一站式婚礼服务", "多主题策划"],
        "featured": True,
        "verified": True,
        "desc": "湖北省婚庆协会副会长单位，提供经典、户外、梦幻等主题婚礼一站式服务。多次在全国策划提案大赛获奖，获楚天都市报、湖北电视台等多家媒体报道。",
        "years": "10年以上"
    },
    {
        "name": "飞凌婚礼 FEELING",
        "category": "planner",
        "address": "湖北省武汉市汉阳区琴台大道12号",
        "district": "汉阳区",
        "phone": "027-84881188",
        "price": "¥15800起",
        "priceNum": 15800,
        "rating": 4.9,
        "reviews": 712,
        "tags": ["CIWU秘书长单位", "优雅设计", "有力执行", "婚礼美学"],
        "featured": True,
        "verified": True,
        "desc": "中国婚礼企业同盟（CIWU）秘书长单位、湖北省婚礼行业协会副会长单位，华中地区较具影响力婚礼公司之一。以细致服务、优雅设计、有力执行缔造专属新人的婚礼美学。",
        "years": "15年以上"
    },
    {
        "name": "琥珀婚礼策划 AMBER WEDDING",
        "category": "planner",
        "address": "湖北省武汉市江汉区民生路20号世纪中心17层",
        "district": "江汉区",
        "phone": "027-82888800",
        "price": "¥16800起",
        "priceNum": 16800,
        "rating": 4.9,
        "reviews": 445,
        "tags": ["艺术美学婚礼品牌", "故事化策划", "全流程服务"],
        "featured": True,
        "verified": True,
        "desc": "2023年亚洲婚礼风尚·壹桁奖获年度具艺术美学婚礼品牌。从新人故事中汲取灵感，将策划、设计、执行理念贯穿每场婚礼全流程。",
        "years": "5-10年"
    },
    {
        "name": "绮丽婚典 Cherry Wedding",
        "category": "planner",
        "address": "湖北省武汉市江汉区新华路越秀国际金融汇T2写字楼29楼",
        "district": "江汉区",
        "phone": "027-85556688",
        "price": "¥13800起",
        "priceNum": 13800,
        "rating": 4.8,
        "reviews": 589,
        "tags": ["户外婚礼领导品牌", "成功策划1万+场", "高端定位"],
        "featured": True,
        "verified": True,
        "desc": "成立于2008年，高端户外婚礼策划领导品牌。团队策划经验丰富，可根据新人需求在预算内设计婚礼，成功策划婚礼超过1万场。",
        "years": "10年以上"
    },
    {
        "name": "心语婚典",
        "category": "planner",
        "address": "湖北省武汉市江岸区南京路55号",
        "district": "江岸区",
        "phone": "027-82778866",
        "price": "¥8888起",
        "priceNum": 8888,
        "rating": 4.7,
        "reviews": 678,
        "tags": ["高性价比", "2003年成立", "万场婚礼经验"],
        "featured": True,
        "verified": True,
        "desc": "成立于2003年，被誉为高性价比的婚庆公司，已为上万对新人打造特色婚礼。秉承追求卓越、创造幸福理念，专业实力稳居武汉婚庆服务前列。",
        "years": "15年以上"
    },
    {
        "name": "武汉造梦师婚礼 Dreamaker",
        "category": "planner",
        "address": "湖北省武汉市江岸区新华路294号IFC国际金融中心22楼",
        "district": "江岸区",
        "phone": "027-82889900",
        "price": "¥18800起",
        "priceNum": 18800,
        "rating": 4.8,
        "reviews": 356,
        "tags": ["全国连锁", "6对1服务", "高端定制"],
        "featured": True,
        "verified": True,
        "desc": "品牌起源于长沙，武汉直营店2017年设立。坚持作品导向，推出「6对1「婚礼统筹服务，专注华中地区高端定制婚礼策划。",
        "years": "5-10年"
    },
    {
        "name": "StarLight星光创意婚礼",
        "category": "planner",
        "address": "湖北省武汉市武昌区烟霞路汉街万达尊B座30楼",
        "district": "武昌区",
        "phone": "027-87880088",
        "price": "¥14800起",
        "priceNum": 14800,
        "rating": 4.8,
        "reviews": 412,
        "tags": ["纯原创定制", "全岗位团队", "高端美学"],
        "featured": False,
        "verified": True,
        "desc": "源自重庆的高端定制美学机构，坚持原创策划婚礼。团队涵盖策划、执行、统筹、设计、主持、摄影、摄像、化妆等全岗位，纯原创私人定制宴会设计。",
        "years": "5-10年"
    },
    {
        "name": "坐标系婚礼",
        "category": "planner",
        "address": "湖北省武汉市武昌区东湖路142号",
        "district": "武昌区",
        "phone": "027-87882266",
        "price": "¥12800起",
        "priceNum": 12800,
        "rating": 4.7,
        "reviews": 334,
        "tags": ["多元风格", "沉浸式场景", "创意设计"],
        "featured": False,
        "verified": True,
        "desc": "武汉知名婚礼策划品牌，作品涵盖苏式庭院扎染、法式花园油画风、岩石峭壁野生花艺等多元风格。擅长融合自然美学与人文艺术，注重色彩搭配与光影运用。",
        "years": "5-10年"
    },
]

# 城市惠 - 武汉婚纱摄影排行
CITYHUI_PHOTOGRAPHY = [
    {
        "name": "武汉薇拉婚纱摄影",
        "category": "photography",
        "address": "武汉市武昌区楚河汉街",
        "district": "武昌区",
        "phone": "027-87885500",
        "price": "¥6980起",
        "priceNum": 6980,
        "rating": 4.9,
        "reviews": 1235,
        "tags": ["全国知名品牌", "原创薇拉风", "高端定制"],
        "featured": True,
        "verified": True,
        "desc": "全国知名高端摄影品牌，原创薇拉风席卷全国。10年10城18店，已为全国百万对新人提供高端定制服务，是年轻新人婚照优选品牌。",
        "years": "10年以上"
    },
    {
        "name": "武汉天籁婚纱摄影",
        "category": "photography",
        "address": "武汉市江汉区汉口中心百货",
        "district": "江汉区",
        "phone": "027-82886600",
        "price": "¥3288起",
        "priceNum": 3288,
        "rating": 4.8,
        "reviews": 892,
        "tags": ["2006年成立", "以客为尊", "一站式服务"],
        "featured": True,
        "verified": True,
        "desc": "2006年在汉口中心百货成立，经过十四年用心经营，业务涵盖婚纱摄影、婚礼策划、婚纱礼服定制、男士礼服定制、婚品销售等一站式服务。",
        "years": "15年以上"
    },
    {
        "name": "武汉唯一视觉婚纱摄影",
        "category": "photography",
        "address": "武汉市江汉区中山大道",
        "district": "江汉区",
        "phone": "027-82887700",
        "price": "¥5200起",
        "priceNum": 5200,
        "rating": 4.8,
        "reviews": 756,
        "tags": ["新派摄影", "12年运营", "定制化体验"],
        "featured": False,
        "verified": True,
        "desc": "80、90后有口皆碑的婚纱摄影品牌，幸福、时尚、年轻、个性。提供定制化拍摄体验与服务，荣耀12年，见证12万余新人的幸福时光。",
        "years": "10年以上"
    },
    {
        "name": "武汉青禾蒙娜丽莎婚纱摄影",
        "category": "photography",
        "address": "武汉市江汉区解放大道",
        "district": "江汉区",
        "phone": "027-82883300",
        "price": "¥5999起",
        "priceNum": 5999,
        "rating": 4.7,
        "reviews": 634,
        "tags": ["2005年创立", "7D梦幻片场", "国际设计团队"],
        "featured": False,
        "verified": True,
        "desc": "创于2005年，隶属于西安蒙娜丽莎婚纱摄影集团。汇集国际顶尖空间美学设计团队，倾心打造7D梦幻摄制片场，提供时尚个性化婚纱摄影服务。",
        "years": "15年以上"
    },
    {
        "name": "武汉皇宫婚纱摄影",
        "category": "photography",
        "address": "武汉市江汉区江汉路步行街与中山大道交汇处",
        "district": "江汉区",
        "phone": "027-82881100",
        "price": "¥3600起",
        "priceNum": 3600,
        "rating": 4.7,
        "reviews": 945,
        "tags": ["1985年成立", "37年老店", "百万口碑"],
        "featured": True,
        "verified": True,
        "desc": "成立于1985年，地处武汉市中心的江汉路步行街与中山大道交汇处，历经37年见证上百万个家庭的口碑相传，用心服务每一对新人。",
        "years": "15年以上"
    },
    {
        "name": "武汉果石婚纱摄影",
        "category": "photography",
        "address": "武汉市武昌区光谷步行街",
        "district": "武昌区",
        "phone": "027-87884400",
        "price": "¥4500起",
        "priceNum": 4500,
        "rating": 4.6,
        "reviews": 456,
        "tags": ["独立创意", "流行文化", "个性定制"],
        "featured": False,
        "verified": True,
        "desc": "以流行文化带来崭新的观点与启发为核心概念，把各种独立创意融入婚纱摄影，为新人拍摄独特个性的婚纱照。",
        "years": "5-10年"
    },
    {
        "name": "武汉橙子婚纱摄影",
        "category": "photography",
        "address": "武汉市洪山区光谷广场",
        "district": "洪山区",
        "phone": "027-87882200",
        "price": "¥3999起",
        "priceNum": 3999,
        "rating": 4.7,
        "reviews": 523,
        "tags": ["三对一拍摄", "无隐形消费", "满意后付款"],
        "featured": False,
        "verified": True,
        "desc": "主打拍摄有故事、有幸福感的婚纱照。三对一拍摄、满意后付款、无任何隐形消费，坚持原创，可根据新人需求定制化拍摄。",
        "years": "5-10年"
    },
    {
        "name": "武汉如依影像婚纱摄影",
        "category": "photography",
        "address": "武汉市江岸区",
        "district": "江岸区",
        "phone": "027-82880011",
        "price": "¥6699起",
        "priceNum": 6699,
        "rating": 4.8,
        "reviews": 389,
        "tags": ["情感细腻风格", "紫龙摄影创立", "光影人像"],
        "featured": False,
        "verified": True,
        "desc": "坚持拍摄永不过时的影像，主打情感、细腻、光影、人像风格。由中国知名样片研发团队紫龙摄影所创立。",
        "years": "5-10年"
    },
]

# 茄考网补充的婚庆公司
QIEKAO_PLANNERS = [
    {
        "name": "华丽婚礼策划",
        "category": "planner",
        "address": "武汉市江汉区",
        "district": "江汉区",
        "phone": "027-87788022",
        "price": "¥8800起",
        "priceNum": 8800,
        "rating": 4.6,
        "reviews": 234,
        "tags": ["规模大", "专业团队", "优质服务"],
        "featured": False,
        "verified": False,
        "desc": "武汉市规模最大、最具实力的婚礼策划公司之一。拥有经验丰富、技术过硬的专业团队，致力于为新人打造最优质、最个性、最精致的婚礼。",
        "years": "5-10年"
    },
    {
        "name": "花开花落婚礼策划",
        "category": "planner",
        "address": "武汉市武昌区",
        "district": "武昌区",
        "phone": "027-87829099",
        "price": "¥7800起",
        "priceNum": 7800,
        "rating": 4.5,
        "reviews": 189,
        "tags": ["多年经验", "精湛才华", "贴心服务"],
        "featured": False,
        "verified": False,
        "desc": "拥有多年丰富经验的专业婚礼策划团队，以精湛的才华和贴心的服务为新人们呈现最完美的婚礼。",
        "years": "5-10年"
    },
    {
        "name": "欢颜婚礼策划",
        "category": "planner",
        "address": "武汉市江汉区",
        "district": "江汉区",
        "phone": "027-87666066",
        "price": "¥9800起",
        "priceNum": 9800,
        "rating": 4.6,
        "reviews": 267,
        "tags": ["策划设计执行一体", "创新设计", "卓越执行"],
        "featured": False,
        "verified": False,
        "desc": "集策划、设计、执行为一体的专业婚礼公司，凭借创新的设计理念、卓越的执行能力以及贴心的服务，为新人们打造难忘的梦幻婚礼。",
        "years": "5-10年"
    },
    {
        "name": "浪漫婚礼策划",
        "category": "planner",
        "address": "武汉市洪山区",
        "district": "洪山区",
        "phone": "027-87838036",
        "price": "¥6800起",
        "priceNum": 6800,
        "rating": 4.5,
        "reviews": 156,
        "tags": ["浪漫风格", "精致手艺", "经验丰富"],
        "featured": False,
        "verified": False,
        "desc": "专注于婚礼策划服务的公司，拥有经验丰富的专业团队，以独特的视角和精致的手艺，为新人们打造浪漫而又难忘的婚礼。",
        "years": "5-10年"
    },
    {
        "name": "唯美婚礼策划",
        "category": "planner",
        "address": "武汉市江汉区",
        "district": "江汉区",
        "phone": "027-87878899",
        "price": "¥10800起",
        "priceNum": 10800,
        "rating": 4.6,
        "reviews": 312,
        "tags": ["唯美风格", "浪漫精致", "专业策划"],
        "featured": False,
        "verified": False,
        "desc": "以策划、设计、执行为一体的专业婚礼公司，以唯美、浪漫、精致的风格，为新人们呈现充满幸福感和美好回忆的婚礼。",
        "years": "5-10年"
    },
]

ALL_NEW_DATA = MAIGOO_PLANNERS + CITYHUI_PHOTOGRAPHY + QIEKAO_PLANNERS


def merge_data():
    """合并数据到 vendors.json"""
    with open(VENDORS_FILE, "r", encoding="utf-8") as f:
        vendors = json.load(f)

    print(f"现有商家数: {len(vendors)}")

    # 建立名称索引
    existing_map = {}
    for v in vendors:
        # 标准化名称用于匹配
        key = v["name"].replace(" ", "").replace("（", "(").replace("）", ")")
        existing_map[key] = v

    updated_count = 0
    added_count = 0

    for new_vendor in ALL_NEW_DATA:
        # 标准化匹配
        new_key = new_vendor["name"].replace(" ", "").replace("（", "(").replace("）", ")")

        if new_key in existing_map:
            # 更新现有商家的信息
            existing = existing_map[new_key]
            changed = False

            # 如果新数据有更详细的地址，更新
            if new_vendor.get("address") and len(new_vendor["address"]) > len(existing.get("address", "")):
                existing["address"] = new_vendor["address"]
                changed = True
            if new_vendor.get("district") and existing.get("district") == "武汉市":
                existing["district"] = new_vendor["district"]
                changed = True
            if new_vendor.get("phone") and not existing.get("phone", "").startswith("027-"):
                existing["phone"] = new_vendor["phone"]
                changed = True
            if new_vendor.get("priceNum") and existing.get("priceNum", 0) == 0:
                existing["price"] = new_vendor["price"]
                existing["priceNum"] = new_vendor["priceNum"]
                changed = True
            if new_vendor.get("desc") and len(new_vendor["desc"]) > len(existing.get("desc", "")):
                existing["desc"] = new_vendor["desc"]
                changed = True
            if new_vendor.get("tags") and len(new_vendor["tags"]) > len(existing.get("tags", [])):
                existing["tags"] = new_vendor["tags"]
                changed = True
            if new_vendor.get("reviews") and new_vendor["reviews"] > existing.get("reviews", 0):
                existing["reviews"] = new_vendor["reviews"]
                changed = True
            if new_vendor.get("rating"):
                existing["rating"] = new_vendor["rating"]
                changed = True

            if changed:
                updated_count += 1
                print(f"  [更新] {new_vendor['name']}")
        else:
            # 新商家，添加
            max_id = max(v["id"] for v in vendors)
            new_vendor["id"] = max_id + 1
            vendors.append(new_vendor)
            added_count += 1
            print(f"  [新增] {new_vendor['name']} ({new_vendor['category']})")

    # 保存
    with open(VENDORS_FILE, "w", encoding="utf-8") as f:
        json.dump(vendors, f, ensure_ascii=False, indent=2)

    print(f"\n===== 合并完成 =====")
    print(f"更新: {updated_count} 家")
    print(f"新增: {added_count} 家")
    print(f"总计: {len(vendors)} 家")

    # 统计
    from collections import Counter
    cats = Counter(v["category"] for v in vendors)
    print(f"\n分类统计:")
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}家")


if __name__ == "__main__":
    merge_data()
