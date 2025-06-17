import os
import pandas as pd
import glob
import logging


def run_selection_for_market(market_code, input_dir, output_csv):
    try:
        all_files = glob.glob(os.path.join(input_dir, "table_1*.csv"))
        if not all_files:
            logging.warning(f"[{market_code}] 未找到匹配文件: table_1*.csv")
            return None

        df_list = []
        for file in all_files:
            df = pd.read_csv(file, encoding='utf-8', dtype=str)
            df_list.append(df)
        df = pd.concat(df_list, ignore_index=True)
        logging.info(f"[{market_code}] 成功读取 {len(all_files)} 个文件，合并后共 {df.shape[0]} 条记录")

        if "编号" in df.columns:
            df.drop_duplicates(subset=["编号"], inplace=True)
            logging.info(f"[{market_code}] 去重后剩余 {df.shape[0]} 条（原始 {len(df_list[0])} 条）")

        df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        logging.info(f"[{market_code}] 分析完成，输出结果保存为: {output_csv}")
        return df
    except Exception as e:
        logging.error(f"[{market_code}] 数据处理失败: {e}")
        return None