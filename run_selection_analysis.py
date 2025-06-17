# 文件：run_selection_analysis.py
import os
import logging
import yaml  # ✅ 替换 ConfigParser

from src.selection_analysis.selection_pipeline import run_selection_for_market
from src.keyword_analysis.run_market_analysis import analyze_market
from src.utils.save_product_folders import save_product_folders


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    # ✅ 使用 PyYAML 读取配置文件
    with open("config/run_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    markets = ["ID", "TH", "MY", "VN", "SG", "PH", "HK", "MO", "TW"]
    processed = []
    missing = []

    for market_code in markets:
        input_dir = os.path.join("input", f"raw_data_{market_code}")
        output_dir = os.path.join("output")
        output_csv = os.path.join(output_dir, f"priority_products_{market_code}.csv")
        keyword_output_dir = output_dir

        if not os.path.exists(input_dir):
            logging.warning(f"[{market_code}] 未找到匹配文件: table_1*.csv")
            missing.append(market_code)
            continue

        logging.info(f"[{market_code}] 使用输入路径: {input_dir}")
        df = run_selection_for_market(market_code, input_dir, output_csv)

        if df is not None:
            processed.append(market_code)

            # 关键词分析
            keywords_path = os.path.join("config", "trend_keywords", f"trend_keywords_{market_code}.txt")
            stopwords_path = os.path.join("config", "trend_keywords", "stopwords.txt")
            analyze_market(output_csv, market_code, keywords_path, stopwords_path, output_dir)

            # ✅ 新增：创建产品文件夹
            try:
                save_product_folders(df, market_code, base_output_dir=output_dir)
                logging.info(f"[{market_code}] 产品资料目录创建成功")
            except Exception as e:
                logging.error(f"[{market_code}] 产品资料目录生成失败: {e}")

    # 总结
    logging.info("\n" + "=" * 60)
    logging.info(f"✅ 处理国家数：{len(markets)}")
    logging.info(f"📦 有数据国家：{processed}")
    logging.info(f"❌ 无数据国家：{missing}")
    logging.info("=" * 60)


if __name__ == "__main__":
    main()
