#!/bin/bash

# 部署重试脚本，用于在网络不稳定时自动重试部署操作

MAX_RETRIES=3
RETRY_DELAY=5

echo "开始博客部署 (最多尝试 $MAX_RETRIES 次)"

for ((i=1; i<=$MAX_RETRIES; i++)); do
  echo "尝试第 $i 次部署..."
  
  # 先生成静态文件
  hexo generate
  
  if [ $? -ne 0 ]; then
    echo "生成静态文件失败，等待 $RETRY_DELAY 秒后重试..."
    sleep $RETRY_DELAY
    continue
  fi
  
  # 然后部署
  hexo deploy
  
  if [ $? -eq 0 ]; then
    echo "部署成功！"
    exit 0
  else
    echo "部署失败，等待 $RETRY_DELAY 秒后重试..."
    sleep $RETRY_DELAY
  fi
done

echo "达到最大重试次数，部署失败。请检查网络连接或稍后再试。"
exit 1