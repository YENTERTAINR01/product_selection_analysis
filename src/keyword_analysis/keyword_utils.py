# 文件：src/keyword_analysis/keyword_utils.py

import os
import jieba

def load_keywords(country_code, synonym_path=None):
    """
    加载指定国家的关键词列表与同义词扩展表
    """
    keyword_file = os.path.join(synonym_path, f"trend_keywords_{country_code}.txt")
    synonym_file = os.path.join(synonym_path, f"synonyms_{country_code}.txt")

    with open(keyword_file, "r", encoding="utf-8") as f:
        keywords = set(line.strip() for line in f if line.strip())

    synonyms = {}
    if os.path.exists(synonym_file):
        with open(synonym_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    main, *alts = parts
                    synonyms[main] = alts

    return keywords, synonyms


def extract_keywords(text):
    """
    使用 jieba 分词，返回关键词列表
    """
    if not isinstance(text, str):
        return []
    words = jieba.lcut(text)
    return [w.strip() for w in words if w.strip()]


def calculate_match_score(words, keywords, synonyms=None):
    """
    计算当前词语列表的关键词匹配分数
    """
    score = 0
    for word in words:
        if word in keywords:
            score += 1
        elif synonyms:
            for k, syns in synonyms.items():
                if word in syns and k in keywords:
                    score += 1
                    break
    return score
