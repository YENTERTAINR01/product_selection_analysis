# -*- coding: utf-8 -*-
"""
保存产品文件夹的工具
每个产品生成一个以 “序号_编号_产品状态_规格_中文名称_sku_产品类别” 命名的子文件夹
下架状态的产品不生成文件夹
序号自动补齐三位
"""

import os
import pandas as pd
import logging
import re

def clean_filename(name: str) -> str:
    """
    清除 Windows 非法文件名字符
    """
    # 替换 <>:"/\|?* 等字符为下划线
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    # 去掉换行回车，左右空格
    return name.replace('\n', '').replace('\r', '').strip()

def save_product_folders(df: pd.DataFrame, base_output_dir: str, country_code: str):
    """
    根据 DataFrame 创建产品文件夹，格式为：
    序号_编号_产品状态_规格_中文名称_sku_产品类别
    下架状态的产品不生成文件夹
    """
    logger = logging.getLogger()
    required_columns = ["序号", "编号", "产品状态", "规格", "中文名称", "sku", "产品类别"]

    # 校验必要列
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"[{country_code}] 缺少必要列: {col}")
            return

    # 顶层输出目录：base_output_dir/产品库_{country_code}
    folder_base = os.path.join(base_output_dir, f"产品库_{country_code}")
    os.makedirs(folder_base, exist_ok=True)

    for _, row in df.iterrows():
        status = str(row["产品状态"]).strip()
        # 下架的产品跳过
        if status == "下架":
            logger.info(f"[{country_code}] 序号 {row['序号']} 状态为下架，跳过创建")
            continue

        try:
            # 序号补零到3位
            seq = f"{int(row['序号']):03d}"
            # 组装文件夹名
            folder_name = (
                f"{seq}_{row['编号']}_{status}_"
                f"{row['规格']}_{row['中文名称']}_{row['sku']}_{row['产品类别']}"
            )
            folder_name = clean_filename(folder_name)
            # 子文件夹直接用 folder_name（不再加“产品库_”前缀）
            folder_path = os.path.join(folder_base, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"[{country_code}] 已创建文件夹: {folder_name}")
        except Exception as e:
            logger.error(f"❌ [{country_code}] 产品目录创建失败 (序号 {row['序号']}): {e}")

    logger.info(f"[{country_code}] 产品资料目录创建完成")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="生成产品资料文件夹")
    parser.add_argument("--excel", "-e", required=True, help="产品列表 Excel 文件路径")
    parser.add_argument("--output", "-o", required=True, help="生成文件夹的根目录")
    parser.add_argument("--country", "-c", required=True, help="国家编码（如 CN）")
    args = parser.parse_args()

    # 读取 Excel
    df = pd.read_excel(args.excel)
    # 调用主函数
    save_product_folders(df, args.output, args.country)
