import os
import logging
import pandas as pd
from src.keyword_analysis.keyword_matcher import (
    load_stopwords, load_keywords, add_keyword_scores, load_synonyms
)

def analyze_market(csv_path, market_code, keywords_path, stopwords_path, output_dir):
    try:
        df = pd.read_csv(csv_path, encoding="utf-8", dtype=str)
        stopwords = load_stopwords(stopwords_path)
        keywords = load_keywords(keywords_path)
        synonyms_path = os.path.join("config", "trend_keywords", f"synonyms_{market_code}.txt")
        synonyms_map = load_synonyms(synonyms_path)  # 加载近义词字典

        df = add_keyword_scores(
            df,
            keyword_set=keywords,
            stopwords=stopwords,
            text_column="中文名称",
            synonyms_map=synonyms_map  # 支持扩展
        )

        sorted_df = df.sort_values(by="关键词命中数", ascending=False)
        sorted_path = os.path.join(output_dir, f"priority_products_sorted_{market_code}.csv")
        sorted_df.to_csv(sorted_path, index=False, encoding="utf-8-sig")
        logging.info(f"[{market_code}] 排序后文件已保存至: {sorted_path}")
    except Exception as e:
        logging.error(f"[{market_code}] 市场关键词分析失败: {e}")
