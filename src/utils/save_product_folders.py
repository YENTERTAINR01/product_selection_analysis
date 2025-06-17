import os
import logging
import re
import pandas as pd


def clean_folder_name(name: str) -> str:
    """
    清理文件夹名称中不合法的字符
    """
    # 替换非法字符为空格或下划线
    name = re.sub(r'[<>:"/\\|?*\n]', '_', name)
    # 删除首尾空格
    name = name.strip()
    # 截断太长的文件夹名，避免 Windows 超过 255 限制
    return name[:100]


def save_product_folders(df: pd.DataFrame, code: str, base_output_dir: str):
    """
    根据产品信息 DataFrame 创建子目录（产品库）

    参数:
        df: 包含产品数据的 DataFrame，要求有编号、sku、中文名称、产品类别、产品状态字段
        code: 市场代码（如 ID, TH）
        base_output_dir: 主目录，一般为 "output"
    """

    output_dir = os.path.join(base_output_dir, f"产品库_{code}")
    os.makedirs(output_dir, exist_ok=True)

    for _, row in df.iterrows():
        try:
            # 获取并格式化字段
            编号_str = str(row["编号"]).zfill(3)
            sku = clean_folder_name(str(row["sku"]))
            name = clean_folder_name(str(row["中文名称"]))
            category = clean_folder_name(str(row["产品类别"]))
            status = clean_folder_name(str(row["产品状态"]))

            # 构建文件夹名
            folder_name = f"产品库_{编号_str}_{sku}_{name}_{category}_{status}"
            folder_path = os.path.join(output_dir, folder_name)

            # 创建文件夹
            os.makedirs(folder_path, exist_ok=True)

        except Exception as e:
            logging.warning(f"❌ 产品目录创建失败: {e}")
