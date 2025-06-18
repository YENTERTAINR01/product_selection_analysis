# Product Selection Analysis

> 🔍 基于市场和规则的产品选品分析框架  
> 支持多市场（如🇮🇩印尼、🇹🇭泰国）数据处理、报告生成及产品素材文件夹创建。

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/<your-org>/product_selection_analysis.git
cd product_selection_analysis
2. 创建并激活 Conda 环境
bash
复制
编辑
conda env create -f environment.yml   # 若无 environment.yml，可手动安装依赖
conda activate cpy39quant
3. 安装依赖（如果没有 environment.yml）
bash
复制
编辑
pip install -r requirements.txt
4. 配置
打开 config/run_config.yaml，根据实际需要修改：

input_dir：原始数据存放路径（默认 input/raw_data_ID、input/raw_data_TH）。

output_dir：分析结果与产品库素材输出路径（默认 output/）。

市场规则和关键词文件都在 config/market_rules/ 与 config/trend_keywords/。

5. 运行全流程
bash
复制
编辑
python run_selection_analysis.py --config config/run_config.yaml
执行后，会生成：

报表：output/priority_products_*.csv、output/sales_reports/priority_products_sorted_ID.csv 等。

产品素材目录：

output/产品库_ID/

output/产品库_TH/

📂 项目结构
graphql
复制
编辑
.
├── .github/               # GitHub Actions、Funding 等
├── config/                # 运行与规则配置
│   ├── run_config.yaml    # 主配置
│   ├── market_rules/      # 市场规则定义
│   └── trend_keywords/    # 趋势关键词文件
├── docs/                  # 项目文档、架构与流程
├── input/                 # 原始数据
│   ├── raw_data_ID/
│   └── raw_data_TH/
├── logs/                  # 日志文件
├── output/                # 分析结果和素材输出
│   ├── *.csv              # 报表
│   ├── sales_reports/     # 销量分析输出（后续添加）
│   ├── 产品库_ID/         # 印尼市场素材目录
│   └── 产品库_TH/         # 泰国市场素材目录
├── scripts/               # 辅助脚本与归档
├── src/                   # 核心代码
│   ├── keyword_analysis/  # 市场关键词分析
│   ├── selection_analysis/ # 选品流水线
│   └── utils/             # 通用工具（如 save_product_folders）
├── generate_tree.py       # 生成目录结构树（ls_R.txt）
├── run_selection_analysis.py # 主入口脚本
├── ls_R.txt               # 上一次目录快照
├── README.md              # 本文档
└── .gitignore             # 忽略规则
🔧 模块说明
src/selection_analysis/selection_pipeline.py
主要的产品筛选逻辑，读取 priority_products_*.csv，生成报告和素材目录。

src/utils/save_product_folders.py
根据市场、状态等字段，批量创建产品文件夹，支持“新品”、“通货”、“自主品牌”等标签。

src/keyword_analysis/run_market_analysis.py
依据配置文件与关键词，做市场趋势分析，供选品策略参考。

generate_tree.py
用来把当前目录结构导出到 ls_R.txt，便于文档校对和项目审查。

📈 添加销量分析
建议在根目录下新建 notebooks/ 文件夹，存放 Jupyter 分析脚本，如 notebooks/sales_analysis.ipynb。

日常销量数据可统一放到 input/sales/，并在 notebook 中读取、可视化、导出到 output/sales_reports/。

后续可结合爬虫脚本放到 scripts/ 或 src/utils，定时采集并更新数据。

🤝 贡献
Fork 本项目

新建分支 feature/xxx

提交 & PR（请附上测试截图或样例数据）

审核通过后合并
