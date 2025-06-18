import os
import yaml
import pandas as pd
from datetime import datetime

# ==================== 配置与数据加载 ====================

def load_config(path: str) -> dict:
    """加载 YAML 配置，指定编码为 utf-8 防止编码错误"""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_data(source: str) -> pd.DataFrame:
    """读取历史爬虫数据，返回 DataFrame"""
    # 支持 csv、parquet 等格式
    ext = os.path.splitext(source)[1].lower()
    if ext == '.csv':
        return pd.read_csv(source, parse_dates=['date'])
    elif ext in ['.parquet', '.pq']:
        return pd.read_parquet(source)
    else:
        raise ValueError(f"不支持的数据格式: {ext}")

# ==================== 核心算法 ====================

def build_tree_from_df(df: pd.DataFrame) -> pd.DataFrame:
    """根据关键词序列构建成长树：计算环比/同比，并生成 score"""
    df = df.sort_values(['keyword', 'date'])
    # 30 天环比
    df['prev_30d'] = df.groupby('keyword')['search_volume'].shift(30)
    df['MoM_pct'] = (df['search_volume'] - df['prev_30d']) / df['prev_30d']
    # 365 天同比
    df['prev_365d'] = df.groupby('keyword')['search_volume'].shift(365)
    df['YoY_pct'] = (df['search_volume'] - df['prev_365d']) / df['prev_365d']
    # 简单加权得分
    df['score'] = 0.5 * df['MoM_pct'].fillna(0) + 0.5 * df['YoY_pct'].fillna(0)
    return df


def score_keywords(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """筛选当天排名前 N 的关键词"""
    today = datetime.now().normalize()
    today_df = df[df['date'] == pd.Timestamp(today)]
    return today_df.nlargest(top_n, 'score')

# ==================== 上架与提醒 ====================

def select_top_sku(keyword: str, mapping: dict) -> str:
    """根据关键词->SKU 映射，选择最合适的 SKU"""
    return mapping.get(keyword, '')


def upload_product(sku: str):
    """实际调用平台 API / 界面自动化，将 SKU 上架"""
    # TODO: 填充对接代码
    pass


def send_daily_report(results: pd.DataFrame):
    """发送日报：邮箱 / 企业微信 / Slack 通知"""
    # TODO: 选用 smtplib / webhook 等
    pass

# ==================== 路线图占位函数 ====================

def calculate_brand_volume(df: pd.DataFrame) -> pd.DataFrame:
    """计算品牌在社媒/论坛的声量"""
    # TODO: 抓取社媒 API，计算提及次数等指标
    raise NotImplementedError


def check_inventory_status(sku: str) -> dict:
    """查询 ERP，获取库存数量、在途量等"""
    # TODO: 对接 ERP 系统 API
    raise NotImplementedError


def optimize_ranking_algorithm(df: pd.DataFrame) -> pd.DataFrame:
    """未来可扩展：接入转化率、利润率等多维度打分"""
    # TODO: 权重学习、机器学习模型
    raise NotImplementedError

# ==================== 主流程 ====================

def main():
    cfg = load_config('config/run_cfg.yaml')
    data = load_data(cfg['data_source'])
    tree_df = build_tree_from_df(data)
    topk = score_keywords(tree_df, top_n=cfg.get('top_n', 5))

    # SKU 映射配置
    sku_map = cfg.get('sku_map', {})
    topk['sku'] = topk['keyword'].apply(lambda kw: select_top_sku(kw, sku_map))

    # 上架第一个产品
    first = topk.iloc[0]
    upload_product(first['sku'])
    print(f"已上架 SKU: {first['sku']} (关键词: {first['keyword']})")

    # 发送日报
    send_daily_report(topk)


if __name__ == '__main__':
    main()
