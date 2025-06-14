
# 📦 Product Selection Analysis / 产品选品分析系统

This project provides a flexible and extensible product selection pipeline that supports **multi-market configurations**, dynamic trend keyword mapping, SKU scoring, and market-specific rule enforcement.

本项目为一套灵活可扩展的产品选品分析系统，支持多国家配置、关键词趋势匹配、SKU打分机制及市场规则加载。

---

## ✅ Features / 功能亮点

- ✅ Multi-market keyword mapping (via `trend_keywords_mapping.yaml`)
- ✅ 市场规则支持（每个国家配置单独规则）
- ✅ SKU 优选打分系统：匹配度 + 毛利率 + 新品权重
- ✅ 自动生成 SKU 文件夹命名结构
- ✅ YAML 配置结构清晰，支持版本更新与 Git 管理
- ✅ 当前启用市场：**Indonesia (ID)**；未来市场如 TH 已归档待激活

---

## 📁 Directory Structure / 项目结构

```
product_selection_analysis/
├── config/
│   ├── run_config.yaml               # 全局运行配置
│   ├── version_info.yaml             # 版本信息记录
│   ├── trend_keywords_mapping.yaml   # 国家代码 → 趋势词文件映射
│   ├── status_config.yaml            # 状态保留筛选配置
│   ├── market_rule_config_ID.yaml    # 印尼市场规则
│   ├── trend_keywords_ID.txt         # 印尼关键词文件
│   └── archive/                      # 已归档国家配置，如泰国 TH
│       ├── trend_keywords_TH.txt
│       └── market_rule_config_TH.yaml
├── output/                           # 输出结果（自动生成）
├── raw_data_xxxx/                    # 原始数据（不建议推送）
├── run_selection_analysis.py         # 主运行脚本
├── run_selection_analysis_v1.5.py    # 增强版本
├── README.md                         # 当前文档（中英文）
├── push_flow.md                      # Git 推送流程文档
└── .gitignore
```

---

## 🌍 Supported Markets / 支持市场状态

| Code | 国家 / Market | 启用状态 | 状态说明                    |
|------|----------------|----------|-----------------------------|
| ID   | 印尼           | ✅ 启用中 | 已配置关键词和规则          |
| TH   | 泰国           | ⏸️ 暂未启用 | 配置已归档到 config/archive |
| ...  | 其他市场       | ❌ 待支持 | 后续新增                    |

---

## 🚀 Usage / 使用方式

1. Edit `run_config.yaml`:
```yaml
country_code: "ID"
platform: "Shopee"
category: "通货"
```

2. Map keywords in `trend_keywords_mapping.yaml`:
```yaml
mapping:
  ID: trend_keywords_ID.txt
```

3. Run:
```bash
python run_selection_analysis_v1.5.py
```

4. Output will appear under:
```
output/product_manage_ID/
```

---

## 🔖 Versioning / 版本控制

- 查看 `config/version_info.yaml` 获取当前版本号与更新记录。
- 所有变更需更新 `update_log` 并附带时间戳。

---

## ✅ Git Tips / Git 使用建议

- ❌ 不要提交 raw_data 和 output 目录下内容
- ✅ 所有配置文件集中在 `config/`
- ⏸️ 暂不启用国家配置统一放入 `config/archive/`
- 📄 查看 `push_flow.md` 获取标准 Git 操作说明

---

🚀 Keep iterating – 每一次选品，都是一次迭代的机会。
