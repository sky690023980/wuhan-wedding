#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
武汉婚庆商家数据收集工具
=====================================
使用方法:
  1. 打开 vendors_template.csv，按格式填入真实商家数据
  2. 运行本脚本:
       python convert_to_json.py
  3. 自动生成 ../data/vendors.json，直接上传到网站即可

字段说明见 vendors_template.csv 第一行注释
"""

import csv
import json
import os
import re
import sys
from datetime import datetime

# ===== 配置 =====
INPUT_FILE  = os.path.join(os.path.dirname(__file__), 'vendors_template.csv')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'vendors.json')

CATEGORY_MAP = {
    '婚庆摄影': 'photography',
    '婚纱摄影': 'photography',
    '摄影':     'photography',
    '婚礼化妆': 'make-up',
    '新娘化妆': 'make-up',
    '化妆':     'make-up',
    '婚礼场地': 'venue',
    '婚宴酒店': 'venue',
    '场地':     'venue',
    '婚庆策划': 'planner',
    '婚礼策划': 'planner',
    '策划':     'planner',
    '婚礼主持': 'host',
    '司仪':     'host',
    '婚纱礼服': 'dress',
    '礼服':     'dress',
    '婚礼花艺': 'flower',
    '花艺':     'flower',
}

def extract_price_num(price_str: str) -> int:
    """从价格字符串中提取最小数字，例如 '¥3999起' -> 3999"""
    if not price_str:
        return 0
    nums = re.findall(r'\d+', price_str.replace(',', ''))
    return int(nums[0]) if nums else 0

def normalize_category(raw: str) -> str:
    raw = raw.strip()
    return CATEGORY_MAP.get(raw, raw)

def parse_tags(raw: str) -> list:
    """将 '韩式风格, 旅拍, 底片全送' 解析成列表"""
    if not raw:
        return []
    return [t.strip() for t in re.split(r'[,，、\s]+', raw) if t.strip()][:5]

def validate_row(row: dict, idx: int) -> list:
    """返回该行的错误列表"""
    errors = []
    required = ['name', 'category', 'district', 'address', 'phone', 'price']
    for f in required:
        if not row.get(f, '').strip():
            errors.append(f'第{idx}行缺少必填字段「{f}」')
    if row.get('rating') and not re.match(r'^[1-5](\.\d)?$', row['rating'].strip()):
        errors.append(f'第{idx}行评分格式错误（应为1.0-5.0，如4.8）')
    return errors

def convert(input_path=INPUT_FILE, output_path=OUTPUT_FILE):
    if not os.path.exists(input_path):
        print(f'❌ 找不到输入文件：{input_path}')
        print(f'   请先查看 vendors_template.csv 填写商家数据')
        sys.exit(1)

    vendors = []
    errors  = []

    with open(input_path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # 第1行是表头
            # 跳过示例行（name以#开头）和空行
            if not row.get('name', '').strip() or row['name'].strip().startswith('#'):
                continue

            row_errors = validate_row(row, idx)
            if row_errors:
                errors.extend(row_errors)
                continue

            vendor = {
                'id':        len(vendors) + 1,
                'name':      row['name'].strip(),
                'category':  normalize_category(row.get('category', '')),
                'district':  row.get('district', '').strip(),
                'address':   row.get('address', '').strip(),
                'phone':     row.get('phone', '').strip(),
                'price':     row.get('price', '').strip(),
                'priceNum':  extract_price_num(row.get('price', '')),
                'rating':    float(row['rating'].strip()) if row.get('rating', '').strip() else 4.5,
                'reviews':   int(row['reviews'].strip()) if row.get('reviews', '').strip().isdigit() else 0,
                'tags':      parse_tags(row.get('tags', '')),
                'featured':  row.get('featured', '').strip().lower() in ('是', 'yes', '1', 'true'),
                'verified':  True,
                'desc':      row.get('desc', '').strip(),
                'wechat':    row.get('wechat', '').strip(),
                'website':   row.get('website', '').strip(),
                'years':     row.get('years', '').strip(),
            }
            # 去掉值为空字符串的可选字段，保持 JSON 整洁
            vendor = {k: v for k, v in vendor.items() if v != '' and v is not None}
            vendors.append(vendor)

    if errors:
        print('⚠️  发现以下错误，请修正后重新运行：')
        for e in errors:
            print(f'   • {e}')
        print()

    if not vendors:
        print('❌ 没有有效的商家数据，请检查 CSV 文件')
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vendors, f, ensure_ascii=False, indent=2)

    print(f'✅ 转换完成！共处理 {len(vendors)} 家商家')
    print(f'   输出文件：{os.path.abspath(output_path)}')
    print()
    print('分类统计：')
    from collections import Counter
    counts = Counter(v['category'] for v in vendors)
    labels = {v: k for k, v in CATEGORY_MAP.items()}
    for cat, n in counts.most_common():
        label = labels.get(cat, cat)
        print(f'   {label:10s}  {n} 家')

    print()
    print('下一步：将 data/vendors.json 上传到网站，刷新页面即可看到新数据！')
    return vendors

if __name__ == '__main__':
    convert()
