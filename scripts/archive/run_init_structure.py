# run_init_structure.py

import os

# === 配置区（主路径只改这里！）
BASE_DIR = r"/"
RAW_DATA_DIR = os.path.join(BASE_DIR, 'raw_data_20250612')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

TREND_KEYWORDS_FILE = os.path.join(CONFIG_DIR, 'trend_keywords.txt')
STATUS_CONFIG_FILE = os.path.join(CONFIG_DIR, 'status_config.yaml')
RUN_CONFIG_FILE = os.path.join(CONFIG_DIR, 'run_config.yaml')

import yaml

# === trend_keywords.txt 模板内容 ===
trend_keywords_content = """美白
保湿
补水
控油
祛痘
祛斑
防晒
修复
抗皱
抗衰
去角质
紧致
提亮
去黑头
去粉刺
舒缓
抗敏
去暗沉
抗氧化
滋润
嫩肤
洁面
爽肤水
化妆水
精华
精华液
面霜
眼霜
眼部精华
乳液
喷雾
面膜
贴
身体乳
香皂
皂
护手霜
沐浴露
洗发水
护发素
洗面奶
牙膏
牙粉
牙贴
儿童
婴儿
宝宝
亲子
无泪
低敏
无香
柔护
孕妇可用
瘦身
瘦脸
瘦腿
瘦臂
燃脂
纤体
香氛
香味
淡香
清香
持香
美白牙齿
牙粉
牙膏
口腔喷雾
漱口水
去牙垢
去牙渍
去烟渍
脱毛
止痒
灰指甲
脚气
美甲
护甲
手足护理
夜间修复
日常护理
早晚通用
随身携带
出行必备
医美修复
学生党
敏感肌
孕妇可用
男士专用
女士专用
情侣款
家庭装
50ml
100ml
200ml
300ml
500ml
g
ml
片
日本
韩国
泰国
澳洲
欧洲
进口
"""

# === status_config.yaml 模板内容 ===
status_config_content = """STATUS_KEEP:
  - 正常备货
  - 清库存

STATUS_CATEGORY_MAPPING:
  正常备货: 主力上新
  清库存: 礼包SKU（礼品可用）
  礼品: 礼包SKU（礼品专用）
  自由定价: 人工确认
  下架: 人工确认

OPERATE_ADVICE_MAPPING:
  正常备货: 推荐上架（上架价 ≥ 最低价，禁止低价违规）
  清库存: 暂不推荐上架（当前阶段不做礼包促销）
  礼品: 暂不推荐上架（当前阶段不做礼包促销）
  自由定价: 可上架（需手动确认最低价合规）
  下架: 暂不推荐上架
"""

# === run_config.yaml 模板内容 ===
run_config_content = """DATA_VERSION: raw_data_20250612

NUMERIC_COLS:
  - 本期采购价
  - 国内运费
  - 国际运费
  - 仓库操作费

TOP_N: 10
"""

# === 创建目录
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# === 写 trend_keywords.txt
with open(TREND_KEYWORDS_FILE, 'w', encoding='utf-8') as f:
    f.write(trend_keywords_content)
print(f"✅ 已创建文件: {TREND_KEYWORDS_FILE}")

# === 写 status_config.yaml
with open(STATUS_CONFIG_FILE, 'w', encoding='utf-8') as f:
    f.write(status_config_content)
print(f"✅ 已创建文件: {STATUS_CONFIG_FILE}")

# === 写 run_config.yaml
with open(RUN_CONFIG_FILE, 'w', encoding='utf-8') as f:
    f.write(run_config_content)
print(f"✅ 已创建文件: {RUN_CONFIG_FILE}")

print("\n🚀 初始化完成！现在你可以切换到 run_selection_analysis.py 喽 🚀")
