#!/usr/bin/env python3
"""
GitHub Webhook 处理示例
用于接收 GitHub webhook 并触发博客部署

使用方法：
1. 安装依赖：pip install flask hmac hashlib
2. 配置环境变量：export GITHUB_WEBHOOK_SECRET=your_secret
3. 运行：python tools/webhook-handler-example.py
4. 配置 GitHub Webhook：https://your-server.com/webhook/deploy
"""

import os
import hmac
import hashlib
import subprocess
import json
from flask import Flask, request, abort

app = Flask(__name__)

# Webhook 密钥（从环境变量读取）
WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET', '')

# 博客目录
BLOG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def verify_signature(payload_body, signature_header):
    """验证 GitHub webhook 签名"""
    if not WEBHOOK_SECRET:
        print("⚠️  警告：未设置 GITHUB_WEBHOOK_SECRET，跳过签名验证")
        return True
    
    if not signature_header:
        return False
    
    # GitHub 使用 HMAC SHA256
    hash_object = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        payload_body,
        hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)


@app.route('/webhook/deploy', methods=['POST'])
def deploy_webhook():
    """处理 GitHub webhook"""
    
    # 获取签名
    signature = request.headers.get('X-Hub-Signature-256', '')
    
    # 验证签名
    if not verify_signature(request.data, signature):
        print("❌ 签名验证失败")
        abort(401)
    
    # 解析事件
    try:
        event = request.json
    except:
        abort(400)
    
    # 只处理 push 事件
    event_type = request.headers.get('X-GitHub-Event', '')
    if event_type != 'push':
        print(f"ℹ️  忽略事件类型: {event_type}")
        return {'status': 'ignored', 'reason': f'Event type: {event_type}'}, 200
    
    # 只处理 main 分支
    ref = event.get('ref', '')
    if ref != 'refs/heads/main':
        print(f"ℹ️  忽略分支: {ref}")
        return {'status': 'ignored', 'reason': f'Branch: {ref}'}, 200
    
    print(f"✅ 收到 push 事件，触发部署...")
    print(f"   提交: {event.get('head_commit', {}).get('message', 'N/A')[:50]}")
    
    # 触发部署（异步执行，避免超时）
    try:
        # 切换到博客目录
        os.chdir(BLOG_DIR)
        
        # 执行部署脚本
        result = subprocess.run(
            ['bash', 'deploy_with_retry.sh'],
            capture_output=True,
            text=True,
            timeout=600  # 10 分钟超时
        )
        
        if result.returncode == 0:
            print("✅ 部署成功")
            return {
                'status': 'success',
                'message': 'Deployment triggered successfully'
            }, 200
        else:
            print(f"❌ 部署失败: {result.stderr}")
            return {
                'status': 'error',
                'message': result.stderr
            }, 500
            
    except subprocess.TimeoutExpired:
        print("❌ 部署超时")
        return {
            'status': 'timeout',
            'message': 'Deployment timeout'
        }, 500
    except Exception as e:
        print(f"❌ 部署异常: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }, 500


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return {'status': 'ok'}, 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Webhook 服务启动在端口 {port}")
    print(f"📁 博客目录: {BLOG_DIR}")
    print(f"🔗 Webhook URL: http://localhost:{port}/webhook/deploy")
    print(f"💚 健康检查: http://localhost:{port}/health")
    app.run(host='0.0.0.0', port=port, debug=False)
