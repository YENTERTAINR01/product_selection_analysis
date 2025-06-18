# 文件：src/keyword_analysis/run_market_analysis.py

import os
import pandas as pd
import logging
from src.keyword_analysis.keyword_utils import extract_keywords, load_keywords, calculate_match_score

logger = logging.getLogger(__name__)

def analyze_market(input_path, output_path, country_code, synonym_path=None):
    # 加载并合并数据
    files = [f for f in os.listdir(input_path) if f.endswith(".csv")]
    if not files:
        logger.warning(f"[{country_code}] 未找到匹配文件: table_1*.csv")
        return

    df_list = [pd.read_csv(os.path.join(input_path, f), encoding='utf-8') for f in files]
    df = pd.concat(df_list, ignore_index=True).drop_duplicates()
    logger.info(f"[{country_code}] 成功读取 {len(files)} 个文件，合并后共 {len(df)} 条记录")

    # 保留关键词分析原始表
    raw_output_path = os.path.join(output_path, f"priority_products_{country_code}.csv")
    df.to_csv(raw_output_path, index=False, encoding="utf-8-sig")
    logger.info(f"[{country_code}] 分析完成，输出结果保存为: {raw_output_path}")

    # 关键词匹配分析
    try:
        keywords, synonyms = load_keywords(country_code, synonym_path)
        df["关键词"] = df["中文名称"].astype(str).apply(extract_keywords)
        df["匹配分数"] = df["关键词"].apply(lambda words: calculate_match_score(words, keywords, synonyms))

        # 排序
        df_sorted = df.sort_values(by="匹配分数", ascending=False).reset_index(drop=True)
        df_sorted.insert(0, "序号", df_sorted.index + 1)  # 添加衍生列“序号”

        sorted_output_path = os.path.join(output_path, f"priority_products_sorted_{country_code}.csv")
        df_sorted.to_csv(sorted_output_path, index=False, encoding="utf-8-sig")
        logger.info(f"[{country_code}] 排序后文件已保存至: {sorted_output_path}")

    except Exception as e:
        logger.error(f"[{country_code}] 市场关键词分析失败: {e}")
