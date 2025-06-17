# src/utils.py

import os
import yaml
import logging
import pandas as pd
from datetime import datetime


def get_args_from_yaml(yaml_path: str) -> dict:
    """读取 YAML 配置文件为字典"""
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"未找到配置文件: {yaml_path}")
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def load_config(path: str) -> dict:
    """通用配置加载"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"配置文件未找到: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_trend_keywords(path: str) -> list:
    """读取趋势关键词列表"""
    if not os.path.exists(path):
        logging.warning(f"趋势关键词文件 {path} 不存在，返回空列表")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def save_results(df: pd.DataFrame, country_code: str, output_dir: str = "output") -> str:
    """保存优选产品结果并返回保存路径"""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"selected_products_{country_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logging.info(f"优选产品已保存到 {output_path}")
    return output_path
