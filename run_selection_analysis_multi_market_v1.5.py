import os
import yaml
import glob
import pandas as pd
import numpy as np
import re
import jieba
import datetime
import logging

# === [1] logging 配置 ===
LOG_DIR = 'output'
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'selection_analysis_multi_market.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# === [2] 读取 run_config.yaml 和 version_info ===
with open('config/run_config.yaml', 'r', encoding='utf-8') as f:
    run_config = yaml.safe_load(f)

with open('config/version_info.yaml', 'r', encoding='utf-8') as f:
    version_info = yaml.safe_load(f)

version = version_info.get('version', 'unknown')
print(f"\n==== 当前版本：{version} ====\n")
BASE_DIR = os.getcwd()

for market in run_config["markets"]:
    name = market["name"]
    platform = market["platform"]
    country = market["country_code"]
    raw_data_dir = os.path.join(BASE_DIR, market["raw_data_dir"])
    input_glob = os.path.join(raw_data_dir, market["input_glob"])
    output_dir = os.path.join(BASE_DIR, market["output_dir"])
    os.makedirs(output_dir, exist_ok=True)

    market_rule_config_path = market["rule_config"]
    trend_keywords_file = market["trend_keywords_file"]

    logging.info(f"\n=== 🚀 开始处理市场：{name} ===")

    # 1. 读取数据文件
    all_files = glob.glob(input_glob)
    if not all_files:
        logging.warning(f"⚠️ 未找到数据文件：{input_glob}，跳过该市场")
        continue

    df_list = [pd.read_csv(f, encoding='utf-8') for f in all_files]
    store_data = pd.concat(df_list, ignore_index=True)
    store_data = store_data.drop_duplicates(subset=['编号'])

    logging.info(f"共加载 {len(all_files)} 个文件，合并后总行数：{store_data.shape[0]}")
    # 2. 加载趋势关键词
    if not os.path.exists(trend_keywords_file):
        logging.warning(f"未找到趋势关键词文件：{trend_keywords_file}，使用默认 fallback")
        trend_keywords_file = 'config/trend_keywords.txt'

    with open(trend_keywords_file, 'r', encoding='utf-8') as f:
        trend_keywords = [line.strip() for line in f if line.strip()]

    logging.info(f"已加载趋势关键词：{trend_keywords_file}，共 {len(trend_keywords)} 个")

    # 3. 加载市场规则（CSV）
    if os.path.exists(market_rule_config_path):
        market_rule_df = pd.read_csv(market_rule_config_path, encoding='utf-8')
        logging.info(f"已加载市场规则文件：{market_rule_config_path}")
    else:
        logging.warning(f"⚠️ 未找到市场规则文件：{market_rule_config_path}，将跳过该市场")
        continue

    # 4. 字段清洗与填充
    drop_cols = ['图片', '包材sku', '套餐', '已上架店铺', '最近调价', '是否为新品', '是否上架店铺', '店铺', '产品素材包']
    store_data.drop(columns=[c for c in drop_cols if c in store_data.columns], inplace=True, errors='ignore')

    fill_cols = ['体积', '重量', '体积重', '合作商活动最低售价外币', '箱子规格', '关键词', '主推方向']
    for col in fill_cols:
        if col in store_data.columns:
            if store_data[col].dtype == 'O':
                store_data[col] = store_data[col].fillna('')
            else:
                store_data[col] = pd.to_numeric(store_data[col], errors='coerce').fillna(0)
    # 5. 平台售价提取（Shopee 和 Lazada）
    def extract_price(val, platform_name='Shopee'):
        if pd.isnull(val):
            return np.nan
        m = re.search(fr'{platform_name}[：:]\s*(\d+(\.\d+)?)', str(val), re.IGNORECASE)
        if m:
            return float(m.group(1))
        return np.nan

    store_data['Shopee价格'] = store_data['合作商最低售价外币'].apply(lambda x: extract_price(x, 'Shopee'))
    store_data['Lazada价格'] = store_data['合作商最低售价外币'].apply(lambda x: extract_price(x, 'Lazada'))

    # 6. 成本和 Shopee 毛利率计算
    for col in run_config['numeric_cols'] + ['Shopee价格', 'Lazada价格']:
        store_data[col] = pd.to_numeric(store_data[col], errors='coerce').fillna(0)

    store_data['总成本'] = (
        store_data.get('本期采购价', 0) +
        store_data.get('国内运费', 0) +
        store_data.get('国际运费', 0) +
        store_data.get('仓库操作费', 0)
    )

    store_data['Shopee毛利率'] = np.where(
        store_data['Shopee价格'] > 0,
        (store_data['Shopee价格'] - store_data['总成本']) / store_data['Shopee价格'],
        np.nan
    )

    # 7. 剔除毛利率 < -10% 的异常行
    abnormal_mask = store_data['Shopee毛利率'] < -0.1
    removed_rows = store_data[abnormal_mask]
    store_data = store_data[~abnormal_mask]

    removed_path = os.path.join(output_dir, 'removed_rows.csv')
    removed_rows.to_csv(removed_path, index=False, encoding='utf_8_sig')
    logging.info(f"异常毛利率剔除行数：{removed_rows.shape[0]}，保存至：{removed_path}")
    # 8. 活跃产品筛选
    status_config_path = os.path.join('config', 'status_config.yaml')
    if os.path.exists(status_config_path):
        with open(status_config_path, 'r', encoding='utf-8') as f:
            status_config = yaml.safe_load(f)
        status_keep = status_config.get('status_keep', [])
    else:
        status_keep = ['正常备货', '礼品', '清库存']

    active = store_data[store_data['产品状态'].isin(status_keep)].copy()
    logging.info(f"筛选活跃产品后剩余：{active.shape[0]} 行")

    # 9. 匹配度计算
    def calculate_match(text, keywords):
        if pd.isnull(text):
            return 0
        text = str(text)
        words = list(jieba.cut(text))
        return sum(1 for word in words if word in keywords)

    active['关键词'] = active['关键词'].fillna(active['中文名称'])
    active['匹配度'] = active['关键词'].apply(lambda x: calculate_match(x, trend_keywords))

    # 10. SKU评分和分类
    active['SKU评分'] = 100

    def classify_status(row):
        if row['产品状态'] == '正常备货':
            return '主力上新'
        elif row['产品状态'] == '清库存':
            return '礼包SKU（礼品可用）'
        elif row['产品状态'] == '礼品':
            return '礼包SKU（礼品专用）'
        else:
            return '人工确认'

    active['产品状态分类'] = active.apply(classify_status, axis=1)

    def gen_ope_advice(row):
        if row['产品状态'] == '正常备货':
            return '推荐上架（上架价 ≥ 最低价，禁止低价违规）'
        elif row['产品状态'] == '清库存':
            return '暂不推荐上架（当前阶段不做礼包促销）'
        else:
            return '可上架（需手动确认最低价合规）'

    active['运营上架建议'] = active.apply(gen_ope_advice, axis=1)

    # 11. 上新优先级评分
    active['Shopee毛利率_clip'] = active['Shopee毛利率'].clip(lower=0, upper=1)
    active['新品优先权重'] = active['编号'] / active['编号'].max()

    weights = run_config['priority_weights']
    active['上新优先级'] = (
        active['匹配度'] * weights['matching_degree'] +
        active['Shopee毛利率_clip'] * weights['shopee_margin'] +
        active['新品优先权重'] * weights['new_product_weight']
    )
    # 12. 导出排序结果
    priority_products = active.sort_values(
        by='上新优先级',
        ascending=False
    )[
        ['编号', 'sku', '中文名称', '产品类别', '规格', 'Shopee价格',
         '产品状态', '产品状态分类', '运营上架建议',
         '匹配度', 'Shopee毛利率', 'SKU评分', '新品优先权重', '上新优先级']
    ]

    output_path = os.path.join(output_dir, f'priority_products_{country}.csv')
    priority_products.to_csv(output_path, index=False, encoding='utf_8_sig')
    logging.info(f"✅ 已导出排序结果：{output_path}")

    # 13. 生成 SKU 文件夹结构
    export_dir = os.path.join(BASE_DIR, f'output/product_manage_{country}')
    os.makedirs(export_dir, exist_ok=True)

    def sanitize_filename(name):
        return re.sub(r'[\\/:*?"<>|]', '_', str(name)).strip()

    for idx, row in priority_products.reset_index(drop=True).iterrows():
        sku_index = f"{idx + 1:03d}"  # 三位数编号
        folder_name = f"{sku_index}_{row['编号']}_{sanitize_filename(row['sku'])}_" \
                      f"{sanitize_filename(row['产品状态'])}_{sanitize_filename(row['产品类别'])}_" \
                      f"{sanitize_filename(row['中文名称'])}"

        folder_path = os.path.join(export_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    logging.info(f"📁 已生成 {len(priority_products)} 个 SKU 文件夹至：{export_dir}")
