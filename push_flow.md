# 🚀 Push Flow for product_selection_analysis 项目

> 适用版本：v1.4.0 起  
> 适用场景：**GitHub首次 Push / 版本更新 Push / 跨人协作**

---

## 1️⃣ Git 初始化 (首次 init 已完成✅)

```bash

git init

## 2️⃣ Git 分支管理
查看当前分支
git branch

切换 master -> main （如果需要）
git branch -M main


## 3️⃣ 关联 GitHub 远程仓库
设置远程 origin 地址（首次 push 时执行）
git remote add origin https://github.com/你的用户名/你的仓库名.git

如果已有 origin，改地址用：
git remote set-url origin https://github.com/你的用户名/你的仓库名.git

## 4️⃣ 提交更新内容
常规操作流程
git status           # 查看改动
git add .            # 添加所有改动（包括新文件 / 修改 / 删除）
git commit -m "v1.4.0: Add market_rule_config support + Full README.md update + Code cleanup"

5️⃣ Push 到 GitHub
首次 push：
git push -u origin main

后续 push（正常更新）：
git push

6️⃣ 本项目目录 Git 结构建议
product_selection_analysis/
├── config/                    # 配置文件 (version_info.yaml / run_config.yaml / status_config.yaml / trend_keywords.txt / market_rule_config_TH.yaml)
├── output/                    # 输出结果（.gitignore 已忽略）
├── raw_data_xxx/              # 原始数据（.gitignore 已忽略）
├── run_selection_analysis.py  # 主运行脚本
├── README.md                  # 中英文版 readme
├── push_flow.md               # 本文件（Push 流程文档）
├── .gitignore                 # Git 忽略配置


7️⃣ 版本更新建议流程
1️⃣ 修改 version_info.yaml，更新：

version

compatibility

update_date

update_log（增量更新日志）

2️⃣ 修改 README.md，同步 version & log

3️⃣ 执行：
git add .
git commit -m "v1.x.x: 更新 xxx 功能 / 修复 xxx 问题"
git push


8️⃣ 常见问题提醒
✅ 不要上传 output/
✅ 不要上传 raw_data_xxx/
✅ 配置放 config/ 文件夹 ✅
✅ 脚本主入口 run_selection_analysis.py ✅
✅ 未来 market_rule_config_xx.yaml 按市场配置即可 ✅


---

Good Luck！🚀 🚀 🚀
### 用法：

👉 你只需要新建一个：

product_selection_analysis/push_flow.md

把上面内容 copy 进去就行。  
未来任何同事 / 你自己更新这个项目 **不用问流程**，看 push_flow.md 就知道了。

---
