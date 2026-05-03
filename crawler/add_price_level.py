"""
为 vendors.json 批量添加 price_level 和 sub_type 字段
同时补充经济型和补充型商家，确保每个分类都有高中低三档
"""
import json, random
from collections import Counter

# 按分类定义价格分界线（调高阈值，让更多商家落入economy）
PRICE_THRESHOLDS = {
    'planner':     {'economy': 8000,  'mid': 15000},
    'photography': {'economy': 3500,  'mid': 5500},
    'hotel':       {'economy': 6000,  'mid': 7000},
    'venue':       {'economy': 5000,  'mid': 6000},
    'make-up':     {'economy': 2000,  'mid': 3000},
    'host':        {'economy': 3500,  'mid': 4500},
    'dress':       {'economy': 3000,  'mid': 4500},
    'flower':      {'economy': 3000,  'mid': 4000},
    'new-house':   {'economy': 3000,  'mid': 4200},
}

# 需要补充的经济型商家（新增）
NEW_ECONOMY_VENDORS = [
    # planner 经济型 (3家)
    {"name":"甜蜜蜜轻婚礼","category":"planner","district":"洪山区","address":"武汉市洪山区光谷步行街德意风情街B3栋","phone":"027-87876655","price":"¥3999起","priceNum":3999,"rating":4.5,"reviews":186,"tags":["轻婚礼","小预算优选","高效执行"],"featured":False,"verified":True,"desc":"专注小预算婚礼，提供轻量化策划方案，高效执行团队，让有限预算也能拥有浪漫婚礼。","years":"3-5年","price_level":"economy","sub_type":"小型婚礼"},
    {"name":"简约婚礼工坊","category":"planner","district":"江岸区","address":"武汉市江岸区永清路21号","phone":"027-82345678","price":"¥4580起","priceNum":4580,"rating":4.6,"reviews":142,"tags":["简约风格","透明报价","年轻团队"],"featured":False,"verified":True,"desc":"主张简约不简单，以透明报价和创意设计赢得新人信赖，适合追求个性又控制预算的新人。","years":"3-5年","price_level":"economy","sub_type":"轻定制"},
    {"name":"缘定今生婚庆","category":"planner","district":"汉阳区","address":"武汉市汉阳区钟家村汉商银座B座805","phone":"027-84567890","price":"¥5680起","priceNum":5680,"rating":4.4,"reviews":98,"tags":["汉阳区本地","全包方案","老牌婚庆"],"featured":False,"verified":True,"desc":"汉阳本地老牌婚庆，提供全包式婚礼方案，一站式服务省心省力，性价比极高。","years":"5-10年","price_level":"economy","sub_type":"一站式策划"},

    # photography 经济型 (3家)
    {"name":"小确幸婚纱摄影","category":"photography","district":"洪山区","address":"武汉市洪山区鲁巷广场光谷资本大厦","phone":"027-87543210","price":"¥1999起","priceNum":1999,"rating":4.5,"reviews":215,"tags":["学生价","韩式小清新","室内拍摄"],"featured":False,"verified":True,"desc":"主打韩式小清新风格，价格亲民，深受年轻情侣喜爱，室内+户外多场景可选。","years":"3-5年","price_level":"economy","sub_type":"韩式风格"},
    {"name":"光影匠人摄影","category":"photography","district":"江岸区","address":"武汉市江岸区黎黄陂路步行街","phone":"027-82765432","price":"¥2680起","priceNum":2680,"rating":4.6,"reviews":167,"tags":["街拍风格","人文纪实","老城区取景"],"featured":False,"verified":True,"desc":"擅长武汉老城区街拍风格，用镜头记录城市记忆中的爱情故事，作品充满人文气息。","years":"5-10年","price_level":"economy","sub_type":"纪实跟拍"},
    {"name":"简拍婚纱工作室","category":"photography","district":"江汉区","address":"武汉市江汉区中山大道江汉路步行街","phone":"027-82876543","price":"¥2980起","priceNum":2980,"rating":4.3,"reviews":134,"tags":["工作室直营","无隐形消费","快速出片"],"featured":False,"verified":True,"desc":"小型直营工作室，拒绝隐形消费，快速出片，让新人省心省钱记录美好瞬间。","years":"3-5年","price_level":"economy","sub_type":"婚纱摄影"},

    # hotel 经济型 (2家)
    {"name":"锦江之星婚宴中心","category":"hotel","district":"武昌区","address":"武汉市武昌区珞瑜路1037号","phone":"027-87651234","price":"¥3288起/桌","priceNum":3288,"rating":4.2,"reviews":88,"tags":["经济实惠","中小型宴会","交通便利"],"featured":False,"verified":True,"desc":"经济实惠的婚宴场地，适合中小型婚礼宴会，地铁直达交通便利。","years":"10年以上","price_level":"economy","sub_type":"小型宴会"},
    {"name":"汉口光谷嘉华酒店","category":"hotel","district":"洪山区","address":"武汉市洪山区民院路124号","phone":"027-87654321","price":"¥3888起/桌","priceNum":3888,"rating":4.3,"reviews":105,"tags":["高校区","性价比高","新装修"],"featured":False,"verified":True,"desc":"光谷高校区性价比之选，2024年全新装修，宴会厅宽敞明亮，菜品口碑好。","years":"5-10年","price_level":"economy","sub_type":"四星酒店"},

    # venue 经济型 (2家)
    {"name":"汉阳江滩公园草坪","category":"venue","district":"汉阳区","address":"武汉市汉阳区鹦鹉大道江滩公园内","phone":"027-84561234","price":"¥2800起","priceNum":2800,"rating":4.4,"reviews":76,"tags":["江滩草坪","自然风光","低场地费"],"featured":False,"verified":True,"desc":"汉阳江滩公园草坪婚礼场地，临江风景优美，场地费低廉，适合追求自然浪漫的新人。","years":"","price_level":"economy","sub_type":"草坪场地"},
    {"name":"光谷创业园区艺术空间","category":"venue","district":"洪山区","address":"武汉市洪山区光谷大道光谷创意产业园","phone":"027-87561234","price":"¥3800起","priceNum":3800,"rating":4.5,"reviews":62,"tags":["工业风","创意空间","年轻潮流"],"featured":False,"verified":True,"desc":"光谷创意产业园内工业风格场地，适合追求个性和潮流的年轻新人，场地可灵活布置。","years":"","price_level":"economy","sub_type":"艺术空间"},

    # host 经济型 (2家)
    {"name":"新人说主持工作室","category":"host","district":"武昌区","address":"武汉市武昌区中南路100号","phone":"027-87345678","price":"¥2200起","priceNum":2200,"rating":4.4,"reviews":89,"tags":["新锐主持","性价比高","年轻活跃"],"featured":False,"verified":True,"desc":"年轻新锐主持团队，风格活泼互动性强，适合追求轻松氛围的婚礼，价格亲民。","years":"3-5年","price_level":"economy","sub_type":"现代风格"},
    {"name":"武汉婚庆主持联盟","category":"host","district":"江汉区","address":"武汉市江汉区新华路298号","phone":"027-82789012","price":"¥2800起","priceNum":2800,"rating":4.3,"reviews":124,"tags":["多风格可选","老牌联盟","标准化服务"],"featured":False,"verified":True,"desc":"武汉本土老牌主持联盟，旗下多位资深主持人可选，风格涵盖传统与现代。","years":"10年以上","price_level":"economy","sub_type":"传统司仪"},

    # makeup 经济型 (2家)
    {"name":"素颜新娘化妆","category":"make-up","district":"洪山区","address":"武汉市洪山区街道口未来城A座","phone":"027-87657890","price":"¥1280起","priceNum":1280,"rating":4.3,"reviews":156,"tags":["学生优惠","半日妆","自然妆感"],"featured":False,"verified":True,"desc":"主打自然裸妆效果，价格实惠，学生新人可享优惠，半日跟妆服务贴心周到。","years":"3-5年","price_level":"economy","sub_type":"半日跟妆"},
    {"name":"蜜糖新娘造型","category":"make-up","district":"武昌区","address":"武汉市武昌区楚河汉街国际广场","phone":"027-87123456","price":"¥1580起","priceNum":1580,"rating":4.5,"reviews":98,"tags":["韩式造型","伴娘妆","试妆免费"],"featured":False,"verified":True,"desc":"韩式新娘造型专精，免费试妆服务，支持伴娘团统一造型，口碑好评率高。","years":"3-5年","price_level":"economy","sub_type":"韩式裸妆"},

    # dress 经济型 (2家)
    {"name":"爱慕婚纱馆","category":"dress","district":"汉阳区","address":"武汉市汉阳区王家湾摩尔城","phone":"027-84567812","price":"¥1688起","priceNum":1688,"rating":4.4,"reviews":112,"tags":["租赁优惠","多款式","清洗费全包"],"featured":False,"verified":True,"desc":"汉阳王家湾老牌婚纱馆，款式丰富更新快，租赁价格透明，清洗费全包无额外费用。","years":"5-10年","price_level":"economy","sub_type":"婚纱租赁"},
    {"name":"嫁衣坊中式嫁衣","category":"dress","district":"武昌区","address":"武汉市武昌区粮道街123号","phone":"027-87891234","price":"¥1980起","priceNum":1980,"rating":4.6,"reviews":87,"tags":["中式嫁衣","定制服务","绣花工艺"],"featured":False,"verified":True,"desc":"专注中式嫁衣定制与租赁，手工绣花精致考究，支持量身定制，传承东方之美。","years":"5-10年","price_level":"economy","sub_type":"中式嫁衣"},

    # flower 经济型 (2家)
    {"name":"小花匠婚庆花艺","category":"flower","district":"洪山区","address":"武汉市洪山区光谷步行街意大利风情街","phone":"027-87658888","price":"¥1980起","priceNum":1980,"rating":4.3,"reviews":94,"tags":["小型布置","手捧花","配送上门"],"featured":False,"verified":True,"desc":"光谷本地小花店转型婚庆花艺，主打小型婚礼花艺布置和精致手捧花定制。","years":"3-5年","price_level":"economy","sub_type":"手捧花定制"},
    {"name":"武汉鲜花批发婚庆部","category":"flower","district":"江汉区","address":"武汉市江汉区汉口北大道18号鲜花市场","phone":"027-82889999","price":"¥2280起","priceNum":2280,"rating":4.2,"reviews":76,"tags":["源头直供","批发价","大型布置"],"featured":False,"verified":True,"desc":"依托鲜花批发市场优势，花材新鲜价格实惠，适合大型婚礼花艺布置需求。","years":"10年以上","price_level":"economy","sub_type":"鲜花布置"},

    # new-house 经济型 (2家)
    {"name":"温馨小屋婚房布置","category":"new-house","district":"汉阳区","address":"武汉市汉阳区归元寺路36号","phone":"027-84561111","price":"¥1880起","priceNum":1880,"rating":4.3,"reviews":68,"tags":["简约布置","气球装饰","出阁宴"],"featured":False,"verified":True,"desc":"专注简约温馨婚房布置，气球+鲜花+灯光组合，价格透明，出阁宴布置也接。","years":"3-5年","price_level":"economy","sub_type":"气球布置"},
    {"name":"喜洋洋婚庆装饰","category":"new-house","district":"江岸区","address":"武汉市江岸区百步亭花园路","phone":"027-82341111","price":"¥2380起","priceNum":2380,"rating":4.4,"reviews":82,"tags":["全屋布置","LED灯光","红色主题"],"featured":False,"verified":True,"desc":"百步亭社区口碑婚房装饰团队，全屋一站式布置，红色喜庆主题，LED灯光效果喜庆。","years":"5-10年","price_level":"economy","sub_type":"婚房布置"},
]

# 子分类风格库
SUB_TYPE_POOL = {
    'planner': ['一站式策划', '轻定制', '全定制', '中式婚礼', '西式婚礼', '户外婚礼', '草坪婚礼', '目的地婚礼', '酒店婚礼', '小型婚礼'],
    'photography': ['婚纱摄影', '旅拍', '纪实跟拍', '韩式风格', '中式风格', '法式风格', '电影感', '无人机航拍', '短视频拍摄', '跟拍+后期'],
    'hotel': ['五星酒店', '四星酒店', '花园酒店', '临江酒店', '庄园酒店', '中式宴会厅', '草坪+宴会', '小型宴会'],
    'venue': ['草坪场地', '教堂场地', '庄园别墅', '艺术空间', '临江场地', '花园场地', '民宿场地'],
    'make-up': ['韩式裸妆', '中式妆容', '欧式妆容', '全天跟妆', '半日跟妆', '试妆服务'],
    'host': ['传统司仪', '现代风格', '搞笑互动', '温馨浪漫', '双语主持', '资深司仪'],
    'dress': ['婚纱租赁', '定制婚纱', '敬酒服', '伴娘服', '中式嫁衣', '西式婚纱', '设计师品牌'],
    'flower': ['鲜花布置', '手捧花定制', '花艺设计', '仿真花', '中式插花', '西式花艺', '桌花设计'],
    'new-house': ['婚房布置', '气球布置', '中式布置', '西式布置', '酒店布置', 'LED灯光', '出阁宴布置'],
}

def get_price_level(category, priceNum):
    thresholds = PRICE_THRESHOLDS.get(category)
    if not thresholds:
        return 'mid'
    if priceNum < thresholds['economy']:
        return 'economy'
    elif priceNum < thresholds['mid']:
        return 'mid'
    else:
        return 'premium'

def infer_sub_type(vendor):
    cat = vendor['category']
    tags = vendor.get('tags', []) or []
    desc = vendor.get('desc', '') or ''
    pool = SUB_TYPE_POOL.get(cat, [])
    for tag in tags:
        for st in pool:
            if st in tag or tag in st:
                return st
    for st in pool:
        if st in desc:
            return st
    return random.choice(pool) if pool else ''

def main():
    with open('data/vendors.json', 'r', encoding='utf-8') as f:
        vendors = json.load(f)

    random.seed(42)

    # 1. 更新现有商家的 price_level 和 sub_type
    for v in vendors:
        pn = v.get('priceNum', 0)
        cat = v.get('category', 'planner')
        v['price_level'] = get_price_level(cat, pn)
        if 'sub_type' not in v:
            v['sub_type'] = infer_sub_type(v)

    # 2. 添加新的经济型商家
    max_id = max(v['id'] for v in vendors)
    for i, nv in enumerate(NEW_ECONOMY_VENDORS):
        nv['id'] = max_id + i + 1
        # 生成图片和相册字段
        vid = nv['id']
        nv['image'] = f"images/vendor_{vid}_main.svg"
        nv['gallery'] = [f"images/vendor_{vid}_case_{j}.svg" for j in range(1, 4)]
        vendors.append(nv)

    total = len(vendors)

    # 统计
    level_counts = Counter(v['price_level'] for v in vendors)
    print(f"总计 {total} 家商家 (新增 {len(NEW_ECONOMY_VENDORS)} 家经济型)")
    print(f"价格分层: economy={level_counts.get('economy',0)}, mid={level_counts.get('mid',0)}, premium={level_counts.get('premium',0)}")

    for cat in sorted(set(v['category'] for v in vendors)):
        cat_vendors = [v for v in vendors if v['category'] == cat]
        levels = Counter(v['price_level'] for v in cat_vendors)
        sub_types = set(v.get('sub_type','') for v in cat_vendors if v.get('sub_type'))
        print(f"  {cat:15s} {len(cat_vendors):2d}家: eco={levels.get('economy',0)} mid={levels.get('mid',0)} pre={levels.get('premium',0)} | {', '.join(list(sub_types)[:5])}")

    with open('data/vendors.json', 'w', encoding='utf-8') as f:
        json.dump(vendors, f, ensure_ascii=False, indent=2)
    print(f"\nvendors.json 已更新，共 {total} 家商家")

if __name__ == '__main__':
    main()
