# 📦 Product Selection Analysis

A flexible, extensible product selection analysis system designed for e-commerce multi-market environments. Supports keyword trend matching, SKU scoring, and market-specific rule enforcement with YAML-driven configuration.

---

## ✅ Features

- Multi-market support (Shopee / Lazada; SG, MY, ID, VN, PH, TH, TW, HK, MO)
- Trend keyword mapping per country
- SKU scoring system: matching degree, margin, new product bonus
- Configurable output filters and scoring weights
- Modular YAML configuration with Git versioning

---

## 📁 Directory Structure

```bash
product_selection_analysis/
├── config/                         # All configuration files
│   ├── run_config.yaml             # Main execution config
│   ├── version_info.yaml           # Version and update log
│   ├── status_config.yaml          # Status filtering rules
│   ├── trend_keywords_mapping.yaml # Market to keyword file map
│   ├── trend_keywords_*.txt        # Country-specific keywords
│   ├── market_rule_config_*.csv    # Country-specific rule configs
│   └── archive/                    # Archived markets
├── raw_data_xxxx/                  # Raw input (not tracked by Git)
├── output/                         # Analysis results
├── run_selection_analysis.py       # Main entry
├── push_flow.md                    # Git operation guide
└── README.md                       # This file
```

---

## 🌍 Supported Markets

| Code | Market       | Platform | Status  |
|------|--------------|----------|---------|
| ID   | Indonesia    | Shopee   | ✅ Active |
| TH   | Thailand     | Lazada   | ⏸️ Archived |
| TW   | Taiwan       | Shopee   | 🚧 Planned |
| SG   | Singapore    | Both     | ✅ Active |
| MY   | Malaysia     | Both     | ✅ Active |
| PH   | Philippines  | Both     | ✅ Active |
| VN   | Vietnam      | Both     | ✅ Active |
| HK   | Hong Kong    | Both     | ✅ Active |
| MO   | Macau        | Both     | ✅ Active |

---

## 🚀 How to Use

1. Update `run_config.yaml`:
```yaml
country_code: "ID"
platform: "shopee"
raw_data_dir: "input/raw_data_ID/"
rule_config: "config/market_rule_config_ID.csv"
trend_keywords_file: "config/trend_keywords_ID.txt"
```

2. Place raw data in the specified folder, such as `input/raw_data_ID/`.

3. Run the enhanced version:
```bash
```

4. Results will be exported to:
```
output/product_manage_ID/
```

---

## 📌 Versioning & Update Log

- Version: 1.5.0
- Last Updated: 2025-06-14

### Update Highlights:
- Multi-market config via YAML
- Keyword file auto-mapping
- SKU scoring improvements
- Market rule integration (per-country)
- Raw data/output folder refactoring
- Versioning recorded in `version_info.yaml`

---

## 🔖 Git Usage Tips

- ✅ Only track configuration and scripts
- ❌ Do not push `raw_data_xxxx` and `output/`
- 🧊 Archive inactive markets in `config/archive/`
- 📄 See `push_flow.md` for commit guidance

---

## 🛠️ Future Roadmap

- [ ] Add tag-based SKU classification
- [ ] Automatically infer "上架建议" from rule config
- [ ] Integrate trend modeling (optional ML component)
- [ ] Add reporting dashboard (e.g., Excel or Streamlit)

---

# 📦 产品选品分析系统

本项目是一套灵活、模块化的电商选品分析系统，适用于多个国家市场。支持趋势关键词匹配、SKU 打分系统、市场特定规则控制，并采用 YAML 文件集中配置，方便维护与协作。

---

## ✅ 功能亮点

- ✅ 多国家多平台支持（Shopee / Lazada，覆盖东南亚各国）
- ✅ 趋势关键词匹配（按国家配置）
- ✅ SKU 优选打分（匹配度、毛利率、新品权重）
- ✅ 输出格式及过滤条件可配
- ✅ 采用 YAML 文件集中配置，支持 Git 管理与版本记录

---

## 📁 项目结构说明

```bash
product_selection_analysis/
├── config/                         # 所有配置文件
│   ├── run_config.yaml             # 主配置文件
│   ├── version_info.yaml           # 版本号与更新记录
│   ├── status_config.yaml          # 状态筛选条件
│   ├── trend_keywords_mapping.yaml # 国家关键词映射
│   ├── trend_keywords_*.txt        # 各国家关键词
│   ├── market_rule_config_*.csv    # 各国家规则
│   └── archive/                    # 暂未启用市场归档
├── raw_data_xxxx/                  # 原始数据目录（不建议 Git 管理）
├── output/                         # 结果输出
├── run_selection_analysis.py       # 脚本入口
├── push_flow.md                    # Git 操作指南
└── README.md                       # 当前说明文档
```

---

## 🌍 当前支持市场

| 代码 | 国家       | 平台     | 启用状态 |
|------|------------|----------|----------|
| ID   | 印尼       | Shopee   | ✅ 启用中 |
| TH   | 泰国       | Lazada   | ⏸️ 已归档 |
| TW   | 台湾       | Shopee   | 🚧 计划中 |
| SG   | 新加坡     | 全部     | ✅ 启用中 |
| MY   | 马来西亚   | 全部     | ✅ 启用中 |
| PH   | 菲律宾     | 全部     | ✅ 启用中 |
| VN   | 越南       | 全部     | ✅ 启用中 |
| HK   | 中国香港   | 全部     | ✅ 启用中 |
| MO   | 中国澳门   | 全部     | ✅ 启用中 |

---

## 🚀 使用方式

1. 编辑 `run_config.yaml` 文件：
```yaml
country_code: "ID"
platform: "shopee"
raw_data_dir: "input/raw_data_ID/"
rule_config: "config/market_rule_config_ID.csv"
trend_keywords_file: "config/trend_keywords_ID.txt"
```

2. 把原始数据放入对应国家目录，如 `input/raw_data_ID/`。

3. 执行分析脚本：
```bash

```

4. 结果将保存在：
```
output/product_manage_ID/
```

---

## 📌 版本记录

- 当前版本：1.5.0
- 更新时间：2025-06-14

### 更新日志摘要：
- 支持多国家配置结构
- 自动映射趋势关键词文件
- 打分逻辑调整
- 市场规则支持按国家配置
- 输出结构标准化
- 版本号和更新记录写入 `version_info.yaml`

---

## ✅ Git 使用建议

- ✅ 仅提交配置和脚本文件
- ❌ 不要推送 `raw_data/` 和 `output/` 内容
- 🧊 暂未启用的国家放入 `config/archive/`
- 📄 参考 `push_flow.md` 获取 Git 操作说明

---

🚀 Every product choice is an iteration toward better strategy.
每一次选品，都是一次战略优化的开始。
