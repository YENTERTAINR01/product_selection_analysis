#!/bin/bash

# 一键切换 master -> main
echo "🚀 Switching branch from master to main ..."

# 1️⃣ 改名本地分支
git branch -m master main

# 2️⃣ 推送 main 分支到远程
git push -u origin main

# 3️⃣ 提示用户去 GitHub 设置 default branch
echo "✅ main branch pushed!"
echo "👉 Please go to GitHub → Settings → Branches → Change default branch to 'main'!"

# 4️⃣ 可选：删除远程 master 分支
echo "❓ Do you want to delete remote 'master' branch? (y/n)"
read answer

if [ "$answer" == "y" ]; then
    git push origin --delete master
    echo "🗑️ Remote 'master' branch deleted!"
else
    echo "Skipped deleting remote 'master' branch."
fi

echo "🎉 Done!"
