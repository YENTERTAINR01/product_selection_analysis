# -*- coding: utf-8 -*-
"""
Author: yang
Updated for version: v1.5.1
Main script for cross-market product selection analysis.
"""

import os
import argparse
import logging
import pandas as pd
import yaml
import glob
from datetime import datetime
from src.utils import load_config

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("selection_analysis.log", mode='w', encoding='utf-8')
        ]
    )

def parse_args():
    parser = argparse.ArgumentParser(description="Product Selection Analysis")
    parser.add_argument('--config', type=str, default='config/run_config.yaml', help='Path to the run configuration YAML file')
    return parser.parse_args()

def load_market_rule_csv(market_code):
    rule_path = f"config/market_rules/market_rule_config_{market_code}.csv"
    if os.path.exists(rule_path):
        logging.info(f"加载市场规则: {rule_path}")
        return pd.read_csv(rule_path, encoding='utf-8')
    else:
        logging.warning(f"未找到市场规则 CSV: {rule_path}")
        return None

def load_trend_keywords(market_code):
    keyword_path = f"config/trend_keywords/trend_keywords_{market_code}.txt"
    if not os.path.exists(keyword_path):
        keyword_path = "config/trend_keywords.txt"
        logging.warning(f"未找到趋势词文件 {market_code}，使用通用词表")
    with open(keyword_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_store_data(raw_data_dir, input_glob):
    all_files = glob.glob(os.path.join(raw_data_dir, input_glob))
    df_list = [pd.read_csv(f, encoding='utf-8') for f in all_files]
    df_all = pd.concat(df_list, ignore_index=True).drop_duplicates(subset=['编号'])
    logging.info(f"共加载 {len(all_files)} 个文件，合并去重后总行数：{df_all.shape[0]}")
    return df_all

def main():
    setup_logger()
    args = parse_args()
    config = load_config(args.config)

    market_code = config['market']
    raw_data_dir = config['raw_data_dir']
    input_glob = config['input_glob']
    output_dir = config['output_dir']

    os.makedirs(output_dir, exist_ok=True)

    trend_keywords = load_trend_keywords(market_code)
    market_rule_df = load_market_rule_csv(market_code)
    store_data = load_store_data(raw_data_dir, input_glob)

    # 此处为简化处理，真正选品逻辑根据 v1.4-v1.5 中逻辑模块进行扩展
    selected_data = store_data[store_data['商品名称'].str.contains('|'.join(trend_keywords), na=False)]

    output_path = os.path.join(output_dir, f"selected_products_{market_code}.xlsx")
    selected_data.to_excel(output_path, index=False)
    logging.info(f"筛选结果已保存至: {output_path}")

if __name__ == '__main__':
    main()
