import os
import sys
import yaml
import logging
import pandas as pd
from datetime import datetime

# 自动将 src 目录加入路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

# 导入核心函数
from src.keyword_analysis.run_market_analysis import analyze_market
from src.utils.save_product_folders import save_product_folders

# 日志配置
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format, encoding='utf-8')


def main():
    # 加载配置文件
    config_path = os.path.join(PROJECT_ROOT, "config", "run_config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 获取要处理的国家列表
    if config.get("country_list"):
        country_list = config["country_list"]
    else:
        country_list = [m.get("code") for m in config.get("markets", [])]

    # 解析 base 配置
    base_cfg = config.get("base", {})
    common_tpl = base_cfg.get("common_path_template", {})
    input_dir_tpl = common_tpl.get("input_dir", "input/raw_data_{code}")
    output_base_dir = base_cfg.get("output_dir", config.get("output_base_dir", "output"))
    trend_keywords_tpl = common_tpl.get("trend_keywords_file", "")

    # 同义词/关键词文件所在目录
    synonym_path = os.path.dirname(trend_keywords_tpl) if trend_keywords_tpl else None

    # 确保输出目录存在
    os.makedirs(output_base_dir, exist_ok=True)

    logging.info("=" * 60)
    logging.info(f"📦 开始处理国家列表：{country_list}")
    success_countries = []
    skipped_countries = []

    for country_code in country_list:
        input_path = input_dir_tpl.format(code=country_code)
        if not os.path.exists(input_path):
            logging.warning(f"[{country_code}] 未找到目录: {input_path}")
            skipped_countries.append(country_code)
            continue

        try:
            # 调用市场关键词分析
            analyze_market(input_path, output_base_dir, country_code, synonym_path=synonym_path)

            # ←—— 在这里，先确保 sales_reports 目录存在
            sales_reports_dir = os.path.join(output_base_dir, "sales_reports")
            os.makedirs(sales_reports_dir, exist_ok=True)

            # 排序后文件路径（改成从 sales_reports 里读取）
            sorted_csv_path = os.path.join(
                sales_reports_dir,
                f"priority_products_sorted_{country_code}.csv"
            )
            if not os.path.exists(sorted_csv_path):
                logging.error(f"[{country_code}] 未找到排序后文件: {sorted_csv_path}")
                skipped_countries.append(country_code)
                continue

            # 读取排序结果，创建产品文件夹
            df_sorted = pd.read_csv(sorted_csv_path, encoding="utf-8-sig")
            save_product_folders(df_sorted, output_base_dir, country_code)
            success_countries.append(country_code)

        except Exception as e:
            logging.error(f"[{country_code}] ❌ 分析失败: {e}")
            skipped_countries.append(country_code)

    logging.info("\n" + "=" * 60)
    logging.info(f"✅ 成功国家数：{len(success_countries)}，分别为：{success_countries}")
    logging.info(f"❌ 跳过国家数：{len(skipped_countries)}，分别为：{skipped_countries}")
    logging.info("=" * 60)


if __name__ == "__main__":
    main()
