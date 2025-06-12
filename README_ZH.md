# 产品选品分析增强版

本项目是一个用于**跨境电商产品选品优先级分析**的增强版工具，当前应用于泰国 Shopee / Lazada 业务场景。  
支持灵活配置、市场规则加载、趋势关键词匹配、运营策略辅助判断等功能，未来可扩展至更多市场 / 业务需求。

---

## 配置结构

- `config/version_info.yaml` → 版本信息 / 更新日志 / 兼容性
- `config/run_config.yaml` → 运行配置（数据路径 / 数值列配置等）
- `config/status_config.yaml` → 产品状态筛选配置
- `config/trend_keywords.txt` → 趋势关键词列表
- `config/market_rule_config.yaml` → 市场规则映射配置（未来 roadmap 功能）

---

## 使用方法

### 运行环境

- Python >= 3.8
- 依赖库：
  - pandas
  - numpy
  - jieba
  - pyyaml
  - openpyxl

### 运行流程

```bash
# 初始化 git repo（如果首次运行）
git init

# 确认 config/ 文件夹配置正确

# 运行主分析脚本
python run_selection_analysis.py

输出结果
output/priority_products.csv → 筛选优先上新产品列表（csv）

output/product_selection_analysis_result.xlsx → 全部活跃产品 + 优先上新产品（xlsx）

output/removed_rows.csv → 剔除的异常行记录（csv）

output/selection_analysis.log → 完整日志（包含版本号 / 执行过程 / 关键事件记录）

---

## 未来扩展 Roadmap

✅ 已完成：

- 基础产品选品分析流程
- 趋势关键词匹配度计算
- 异常 Shopee 毛利率剔除机制
- 新品优先权重字段支持
- 灵活配置 trend_keywords.txt / run_config.yaml
- 市场规则配置预留 (market_rule_config.yaml)

🚀 计划支持：

- [ ] 根据市场规则自动标注礼包 / 满赠 / 促销适用产品
- [ ] 同款买赠套餐辅助判断
- [ ] Shopee / Lazada 历史销售趋势联动分析
- [ ] 结合自定义产品分组策略支持更多选品场景
- [ ] 多语言支持（README / log / 配置文件中英文自动切换）
- [ ] 选品结果一键导入上架系统 / 生成上架资料包

📝 你的建议欢迎在 Issues 中提出，我们会持续完善 🚀。

---

## License

MIT License

---

## Contributors

- Yang / 杨先生
  - 选品分析工具设计与实现
  - 跨境电商业务规则梳理
  - 配置标准设计 + README / 配置文档撰写
- GPT-4o 协助整理代码架构、优化 README 文档结构

---

## 备注

> 本项目当前为内部选品分析工具，暂未公开发行版本，如需扩展 / 企业定制可联系作者咨询。

---
