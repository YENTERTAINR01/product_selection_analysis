import os
import logging
import yaml
import glob
import pandas as pd


def load_config(path="config/run_config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def expand_market_configs(config):
    base = config.get("base", {})
    template = base.get("common_path_template", {})
    expanded = []

    for market in config.get("markets", []):
        code = market["code"]
        merged = {**base, **market}
        merged["country_code"] = code  # backward compatibility

        # 自动展开模板路径
        for k, v in template.items():
            merged[k] = v.replace("{code}", code)

        expanded.append(merged)
    return expanded


def load_trend_keywords(file_path):
    if not os.path.exists(file_path):
        logging.warning(f"趋势关键词文件不存在: {file_path}")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def apply_market_rules(df, csv_path):
    if not os.path.exists(csv_path):
        logging.warning(f"市场规则文件不存在: {csv_path}")
        return df
    rules_df = pd.read_csv(csv_path)
    return df  # TODO: 实现具体规则逻辑


def filter_by_trend_keywords(df, keywords):
    if "关键词" not in df.columns:
        return df
    return df[df["关键词"].apply(lambda x: any(k in str(x) for k in keywords))]


def run_for_market(market_config: dict):
    code = market_config["code"]
    raw_data_dir = market_config["raw_data_dir"]
    input_glob = market_config["input_glob"]
    output_dir = market_config["output_dir"]
    trend_keywords_file = market_config["trend_keywords_file"]
    market_rule_csv = market_config["market_rule_table_csv"]

    os.makedirs(output_dir, exist_ok=True)

    files = glob.glob(os.path.join(raw_data_dir, input_glob))
    if not files:
        logging.warning(f"[{code}] 未找到匹配文件: {input_glob}")
        return

    input_file = max(files, key=os.path.getmtime)
    logging.info(f"[{code}] 加载数据文件: {input_file}")

    df = pd.read_csv(input_file, encoding="utf-8")
    df = apply_market_rules(df, market_rule_csv)

    trend_keywords = load_trend_keywords(trend_keywords_file)
    df = filter_by_trend_keywords(df, trend_keywords)

    output_path = os.path.join(output_dir, f"filtered_{code}.xlsx")
    df.to_excel(output_path, index=False)
    logging.info(f"[{code}] 已保存筛选结果: {output_path}")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    config = load_config()
    markets = expand_market_configs(config)

    for market in markets:
        try:
            run_for_market(market)
        except Exception as e:
            logging.exception(f"[{market.get('code', '?')}] 分析失败: {e}")


if __name__ == "__main__":
    main()
