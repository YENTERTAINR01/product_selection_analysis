import jieba
import pandas as pd


def load_stopwords(stopwords_path):
    try:
        with open(stopwords_path, "r", encoding="utf-8") as f:
            stopwords = set(line.strip() for line in f if line.strip())
        return stopwords
    except Exception as e:
        print(f"读取停用词失败: {e}")
        return set()


def load_keywords(keywords_path):
    try:
        with open(keywords_path, "r", encoding="utf-8") as f:
            keywords = set(line.strip() for line in f if line.strip())
        return keywords
    except Exception as e:
        print(f"读取关键词失败: {e}")
        return set()


def add_keyword_scores(df, keyword_set, stopwords, text_column="中文名称", synonyms_map=None):
    import jieba

    def calculate_keyword_score(text):
        words = [w for w in jieba.cut(text) if w.strip() and w not in stopwords]
        score = 0
        hits = []

        for word in words:
            if word in keyword_set:
                score += 1
                hits.append(word)
            elif synonyms_map:
                for k, syns in synonyms_map.items():
                    if word in syns:
                        score += 1
                        hits.append(f"{word}->{k}")
                        break

        return pd.Series({"关键词命中数": score, "命中词": "，".join(hits)})

    result = df[text_column].fillna("").apply(calculate_keyword_score)
    return pd.concat([df, result], axis=1)


# keyword_matcher.py 中添加逻辑
def load_synonyms(synonyms_path):
    synonyms_map = {}
    with open(synonyms_path, encoding="utf-8") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                words = [w.strip() for w in line.strip().split(",")]
                key = words[0]
                for w in words:
                    synonyms_map[w] = key
    return synonyms_map


def calculate_keyword_score(text, keywords_set, synonyms_map):
    import jieba
    tokens = jieba.lcut(text)
    matched_keywords = set()
    for token in tokens:
        keyword = synonyms_map.get(token, token)
        if keyword in keywords_set:
            matched_keywords.add(keyword)
    return len(matched_keywords)
