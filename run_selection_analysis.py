# run_selection_analysis.py
<<<<<<< HEAD
# 产品选品分析增强版 V1.4.1
# 🚀 更新点：
# - 新增 trend_keywords_file 配置，支持多市场趋势词文件
# - run_config.yaml 配置 trend_keywords_file + market_code
# - 优化 logging + 版本结构
=======
# 产品选品分析增强版 V1.4.0
# 🚀 更新点：
# - 新增 market_rule_config_TH.yaml 规范配置支持
# - run_selection_analysis.py 增加市场规则加载 stub
# - 维持版本信息 / 结构清晰定位
>>>>>>> 13c0f29f4588310ec1ec962f7b6a40d8c4f31b53

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
LOG_FILE = os.path.join(LOG_DIR, 'selection_analysis.log')

<<<<<<< HEAD
=======
# utf-8 handler
>>>>>>> 13c0f29f4588310ec1ec962f7b6a40d8c4f31b53
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# === [2] 读取 version_info.yaml ===
with open('config/version_info.yaml', 'r', encoding='utf-8') as f:
    version_info = yaml.safe_load(f)

version = version_info.get('version', 'unknown')
compatibility = version_info.get('compatibility', 'unknown')
update_date = version_info.get('update_date', 'unknown')
update_log = version_info.get('update_log', [])

# 打印版本信息
print(f"\n==== 当前版本信息 ====")
print(f"版本号：{version} ({compatibility})")
print(f"描述：{version_info.get('description', 'No description')}")
print(f"更新日期：{update_date}")
print("更新日志：")
for log_entry in update_log:
    print(f" - {log_entry}")
print("=" * 40)

# logging 版本信息
logging.info(f"Version: {version} | Compatibility: {compatibility} | Update Date: {update_date}")
logging.info("Update Log:")
for log_entry in update_log:
    logging.info(f"- {log_entry}")
<<<<<<< HEAD
=======

>>>>>>> 13c0f29f4588310ec1ec962f7b6a40d8c4f31b53
# === [3] 读取 run_config.yaml ===
with open('config/run_config.yaml', 'r', encoding='utf-8') as f:
    run_config = yaml.safe_load(f)

BASE_DIR = os.getcwd()
RAW_DATA_DIR = os.path.join(BASE_DIR, run_config['raw_data_dir'])
INPUT_GLOB = os.path.join(RAW_DATA_DIR, run_config['input_glob'])
OUTPUT_DIR = os.path.join(BASE_DIR, run_config['output_dir'])
NUMERIC_COLS = run_config['numeric_cols']

<<<<<<< HEAD
# 新增
MARKET_CODE = run_config.get('market_code', 'TH')
market_rule_config_path = run_config.get('market_rule_config_path', f'config/market_rule_config_{MARKET_CODE}.yaml')
trend_keywords_file = run_config.get('trend_keywords_file', f'config/trend_keywords_{MARKET_CODE}.txt')

=======
>>>>>>> 13c0f29f4588310ec1ec962f7b6a40d8c4f31b53
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === [4] 读取 status_config.yaml ===
with open('config/status_config.yaml', 'r', encoding='utf-8') as f:
    status_config = yaml.safe_load(f)

status_keep = status_config['status_keep']

<<<<<<< HEAD
# === [5] 读取 trend_keywords_file ===
if not os.path.exists(trend_keywords_file):
    logging.warning(f"未找到趋势词文件 {trend_keywords_file}，使用 fallback 通用趋势词 trend_keywords.txt")
    trend_keywords_file = 'config/trend_keywords.txt'

with open(trend_keywords_file, 'r', encoding='utf-8') as f:
    trend_keywords = [line.strip() for line in f if line.strip()]

logging.info(f"趋势关键词已加载: {trend_keywords_file} （共 {len(trend_keywords)} 个词）")

# === [6] 读取 market_rule_config.yaml ===
with open(market_rule_config_path, 'r', encoding='utf-8') as f:
    market_rule_config = yaml.safe_load(f)

logging.info(f"市场规则配置已加载: {market_rule_config_path}")
=======
# === [5] 读取 trend_keywords.txt ===
with open('config/trend_keywords.txt', 'r', encoding='utf-8') as f:
    trend_keywords = [line.strip() for line in f if line.strip()]

# === [6] 读取 market_rule_config_TH.yaml ===
with open('config/market_rule_config_TH.yaml', 'r', encoding='utf-8') as f:
    market_rule_config = yaml.safe_load(f)

logging.info("市场规则配置已加载 (market_rule_config_TH.yaml)")
>>>>>>> 13c0f29f4588310ec1ec962f7b6a40d8c4f31b53
logging.info(f"当前平台规则更新日期: {market_rule_config['market_rule']['meta']['update_date']}")

# === [7] 数据加载 ===
all_files = glob.glob(INPUT_GLOB)
df_list = [pd.read_csv(f, encoding='utf-8') for f in all_files]
store_data = pd.concat(df_list, ignore_index=True)
store_data = store_data.drop_duplicates(subset=['编号'])

print(f"\n共加载 {len(all_files)} 个文件，去重后总行数：{store_data.shape[0]}")
logging.info(f"共加载 {len(all_files)} 个文件，去重后总行数：{store_data.shape[0]}")

# === [8] 缺失值处理 & 字段处理 ===
drop_cols = ['图片', '包材sku', '套餐', '已上架店铺', '最近调价', '是否为新品', '是否上架店铺', '店铺', '产品素材包']
store_data.drop(columns=[c for c in drop_cols if c in store_data.columns], inplace=True, errors='ignore')

fill_cols = ['体积', '重量', '体积重', '合作商活动最低售价外币', '箱子规格', '关键词', '主推方向']
for col in fill_cols:
    if col in store_data.columns:
        if store_data[col].dtype == 'O':
            store_data[col] = store_data[col].fillna('')
        else:
            store_data[col] = pd.to_numeric(store_data[col], errors='coerce').fillna(0)

# === [9] 提取平台售价 ===
def extract_price(val, platform='Shopee'):
    if pd.isnull(val):
        return np.nan
    m = re.search(fr'{platform}[：:]\s*(\d+(\.\d+)?)', str(val), re.IGNORECASE)
    if m:
        return float(m.group(1))
    return np.nan

store_data['Shopee价格'] = store_data['合作商最低售价外币'].apply(lambda x: extract_price(x, 'Shopee'))
store_data['Lazada价格'] = store_data['合作商最低售价外币'].apply(lambda x: extract_price(x, 'Lazada'))

# === [10] 成本&毛利率 ===
for col in NUMERIC_COLS + ['Shopee价格', 'Lazada价格']:
    store_data[col] = pd.to_numeric(store_data[col], errors='coerce').fillna(0)

store_data['总成本'] = (
    store_data['本期采购价'] +
    store_data['国内运费'] +
    store_data['国际运费'] +
    store_data['仓库操作费']
)

store_data['Shopee毛利率'] = np.where(
    store_data['Shopee价格'] > 0,
    (store_data['Shopee价格'] - store_data['总成本']) / store_data['Shopee价格'],
    np.nan
)

# === [11] 异常 Shopee毛利率 行剔除 ===
abnormal_mask = store_data['Shopee毛利率'] < -0.1
removed_rows = store_data[abnormal_mask]
store_data = store_data[~abnormal_mask]
removed_rows.to_csv(os.path.join(OUTPUT_DIR, 'removed_rows.csv'), index=False, encoding='utf_8_sig')

logging.info(f"剔除异常 Shopee毛利率 行数：{removed_rows.shape[0]}")

# === 活跃产品筛选 ===
active = store_data[store_data['产品状态'].isin(status_keep)].copy()
print("活跃产品数量：", active.shape[0])
logging.info(f"活跃产品数量：{active.shape[0]}")

# === 匹配度计算 ===
def calculate_match(text, keywords):
    if pd.isnull(text):
        return 0
    text = str(text)
    words = list(jieba.cut(text))
    return sum(1 for word in words if word in keywords)

active['关键词'] = active['关键词'].fillna(active['中文名称'])
active['匹配度'] = active['关键词'].apply(lambda x: calculate_match(x, trend_keywords))

# === [12] SKU评分 修正 ===
active['SKU评分'] = 100

# === [13] 产品状态分类 ===
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

# === [13] 运营上架建议 ===
def gen_ope_advice(row):
    if row['产品状态'] == '正常备货':
        return '推荐上架（上架价 ≥ 最低价，禁止低价违规）'
    elif row['产品状态'] == '清库存':
        return '暂不推荐上架（当前阶段不做礼包促销）'
    else:
        return '可上架（需手动确认最低价合规）'

active['运营上架建议'] = active.apply(gen_ope_advice, axis=1)

# === [14] 上新优先级计算 ===
active['Shopee毛利率_clip'] = active['Shopee毛利率'].clip(lower=0, upper=1)
active['新品优先权重'] = active['编号'] / active['编号'].max()

active['上新优先级'] = (
    active['匹配度'] * 5 +
    active['Shopee毛利率_clip'] * 100 +
    active['新品优先权重'] * 10
)

# === 排序&导出 ===
priority_products = active.sort_values(
    by='上新优先级',
    ascending=False
<<<<<<< HEAD
)[['编号', 'sku', '中文名称', '产品类别', '规格', 'Shopee价格', '产品状态', '产品状态分类', '运营上架建议',
=======
)[['编号', 'sku', '中文名称', '产品类别', '产品状态', '产品状态分类', '运营上架建议',
>>>>>>> 13c0f29f4588310ec1ec962f7b6a40d8c4f31b53
   '匹配度', 'Shopee毛利率', 'SKU评分', '新品优先权重', '上新优先级']]

priority_products.to_csv(
    os.path.join(OUTPUT_DIR, 'priority_products.csv'),
    index=False,
    encoding='utf_8_sig'
)

<<<<<<< HEAD
# === [15] 生成 SKU 文件夹结构 ===
EXPORT_DIR = os.path.join(BASE_DIR, f'output/product_manage_{MARKET_CODE}')
os.makedirs(EXPORT_DIR, exist_ok=True)

# 清理非法字符函数（用于文件夹名）
def sanitize_filename(name):
    return re.sub(r'[\/:*?"<>|]', '_', str(name)).strip()

for idx, row in priority_products.reset_index(drop=True).iterrows():
    sku_index = f"{idx + 1:03d}"  # 三位数编号
    folder_name = f"{sku_index}_{row['编号']}_{sanitize_filename(row['sku'])}_" \
                  f"{sanitize_filename(row['产品状态'])}_{sanitize_filename(row['产品类别'])}_" \
                  f"{sanitize_filename(row['中文名称'])}"

    folder_path = os.path.join(EXPORT_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

logging.info(f"已生成 {len(priority_products)} 个 SKU 文件夹至：{EXPORT_DIR}")
print(f"已生成 {len(priority_products)} 个 SKU 文件夹至：{EXPORT_DIR}")
=======
with pd.ExcelWriter(os.path.join(OUTPUT_DIR, 'product_selection_analysis_result.xlsx'), engine='openpyxl') as writer:
    priority_products.to_excel(writer, sheet_name='优先上新产品', index=False)
    active.to_excel(writer, sheet_name='活跃产品全表', index=False)
>>>>>>> 13c0f29f4588310ec1ec962f7b6a40d8c4f31b53

# === version_info.yaml 更新 ===
try:
    version_info['last_run_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('config/version_info.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(version_info, f, allow_unicode=True)
    logging.info(f"已更新 version_info.yaml last_run_date → {version_info['last_run_date']}")
except Exception as e:
    logging.error(f"⚠️ 更新 version_info.yaml 失败：{e}")

# === 结束 ===
print("\n✅ 数据处理完毕，增强版结果已输出到：", OUTPUT_DIR)
logging.info("✅ 数据处理完毕，增强版结果已输出")
