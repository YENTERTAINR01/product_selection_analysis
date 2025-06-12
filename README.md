## 🏷️ Version

- Version: v1.4.0
- Compatibility: v1.x
- Last Updated: 2025-06-13

## 🚀 Major Updates

- Added full support for `market_rule_config.yaml` (market rules per product status)
- Improved `version_info.yaml` auto update (last_run_date)
- Improved log format (Chinese supported)
- Unified file structure for GitHub compatibility
- Selection formula optimized: `Matching Degree * 5 + Shopee Margin * 100 + New Product Weight * 10`
- Cleaned unvaluable column: SKU评分
- Automatically remove abnormal Shopee Margin rows
- New `priority_products.csv` and `product_selection_analysis_result.xlsx` output

## 🗂️ Config Files

config/
├── version_info.yaml
├── run_config.yaml
├── status_config.yaml
├── trend_keywords.txt
├── market_rule_config_TH.yaml <-- ✅ NEW

## ⚙️ Usage

```bash
# 1️⃣ Configure your run_config.yaml (raw_data_dir + market_rule_config)
# 2️⃣ Place raw_data files into raw_data_xxx/
# 3️⃣ Run:
python run_selection_analysis.py
# 4️⃣ Check output folder



🏷️ Future Roadmap
# - Support dynamic mapping of "运营上架建议" from market_rule_config.yaml

Support market_rule_config auto mapping to 运营上架建议 (currently manual mapping in gen_ope_advice)

Support advanced product tagging (e.g. 买赠适用 / 礼品包适用 / 满赠适用 / 新品强推)

Support multi-market configurations (SG / MY / VN)

Integrate product trend mining model (可选）