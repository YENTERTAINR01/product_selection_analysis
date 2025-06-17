
# 🧠 Product Selection Analysis 智能选品分析系统

本项目用于基于【产品中文名称】的关键词趋势热度分析，自动筛选出最优产品，并按照热度生成资料文件夹。适用于 Shopee、Lazada 等东南亚跨境电商平台。

---

## 📂 项目结构说明

```
product_selection_analysis/
├── config/                        # 配置文件夹
│   ├── run_config.yaml           # 主运行配置
│   └── trend_keywords/           # 市场热词、停用词、同义词配置
├── input/                        # 输入数据目录（每个市场一个子目录）
│   └── raw_data_ID/              # 示例市场：印尼数据（table_*.csv）
├── output/                       # 分析输出结果（包含优先产品列表及子文件夹）
│   ├── priority_products_ID.csv
│   └── priority_products_sorted_ID.csv
├── src/
│   ├── keyword_analysis/
│   │   ├── run_market_analysis.py
│   │   └── keyword_matcher.py
│   ├── selection_analysis/
│   │   └── selection_pipeline.py
│   └── utils/
│       └── save_product_folders.py
├── run_selection_analysis.py     # 主程序入口
├── todo_map.md                   # 待办任务记录
└── README.md                     # 使用文档（当前文件）
```

---

## 🚀 使用说明

### 1. 准备输入数据

每个市场应在 `input/` 下建一个文件夹，如 `raw_data_ID`，并放入命名为 `table_1_*.csv` 的产品表格，必须包含如下字段：

| 字段名       | 示例                  |
|--------------|-----------------------|
| SKU          | 121-JLID00-001        |
| 中文名称     | 烟酰胺美白祛斑霜30g   |
| 包装形式     | 盒、袋                |
| 类型         | 通货、新品、清库存    |
| 货品状态     | 正常备货、下架等      |

---

### 2. 配置关键词热度文件

在 `config/trend_keywords/` 中为每个市场准备一份关键词文件，例如：

```
trend_keywords_ID.txt
```

内容为每行一个关键词，例如：

```
美白
祛斑
面膜
洗面奶
```

如需添加同义词匹配，可以创建同名文件：

```
synonyms_ID.txt
```

格式参考：

```
美白,亮肤,提亮肤色
祛痘,去痘,抗痘
```

---

### 3. 运行主程序

确保 Python 版本 ≥ 3.8，安装 `jieba` 和 `pandas`：

```bash
pip install jieba pandas
```

运行主程序：

```bash
python run_selection_analysis.py
```

---

## 📈 输出说明

程序运行成功后将在 `output/` 下生成：

- `priority_products_ID.csv`: 初步筛选后的产品列表
- `priority_products_sorted_ID.csv`: 按关键词热度打分后的排序列表
- `产品库_ID/`: 每个优选产品建立一个对应的子文件夹，命名示例：

```
产品库_ID/
├── 产品库_4679_烟酰胺美白祛斑霜_盒_通货_正常备货/
├── 产品库_6845_水杨酸棉片绿色_袋_通货_清库存/
```

---

## 🧩 后续优化建议（见 todo_map.md）

- 同义词自动扩展与权重融合
- 分词去除品牌名/无意义词（可选启用停用词）
- 产品评分加入销量、评论数、上新时间等维度
- 输出子文件夹内生成初始资料模板（如 info.txt）

---

## 👨‍💻 作者与贡献

此项目由 BERLOOK 团队开发维护，旨在提升运营选品效率，支持后续自动选品、自动打包推送 WhatsApp 的整体流程。

欢迎提交 issue 或 PR 进行功能建议与合作开发。
