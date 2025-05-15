---
title: testplatform-login-and-registration
tags:
---
# 自动化测试平台添加登录注册功能设计与实现 🚀

在上一篇博客中，我们详细介绍了如何使用 MySQL 搭建一个用于登录注册模块的数据库🛢️。有了这个坚实的基础，接下来我们就可以为自动化测试平台添加登录注册功能啦👏。下面，我们将从数据库表结构设计、后端代码实现和前端代码实现三个方面来详细介绍。

## 一、数据库表结构 📋
我们已经在 MySQL 中创建了 `users` 表用于存储用户信息，这个表包含了用户 ID、用户名、密码和用户角色等字段。它就像是一个“信息仓库”，为我们存储和管理用户数据提供了便利。回顾一下创建 `users` 表的 SQL 语句：
```sql
-- 创建 users 表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20)
);
```
这个表结构是登录注册功能的基础，后续的操作都将围绕它展开。

## 二、后端代码实现（Flask） 💻
### 1. 新增 `models/user.py`
在后端代码中，我们首先要新增 `models/user.py` 文件，用于处理与数据库的交互。以下是该文件的详细代码：
```python
import hashlib
import pymysql
import logging

log = logging.getLogger(__name__)

class MySqlConfig:
    TEST_PLATFORM = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': 'password',
        'db': 'test_platform',
        'charset': 'utf8'
    }

def get_connection():
    try:
        config = MySqlConfig.TEST_PLATFORM
        log.info(f"尝试连接数据库: {config['host']}:{config['port']}/{config['db']}")
        conn = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            passwd=config['passwd'],
            db=config['db'],
            charset=config['charset']
        )
        log.info("数据库连接成功")
        return conn
    except Exception as e:
        log.error(f"数据库连接失败: {str(e)}")
        raise

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        log.info("初始化用户表")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        ''')
        conn.commit()
        log.info("用户表初始化完成")
    except Exception as e:
        log.error(f"用户表初始化失败: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        log.info(f"尝试创建用户: {username}")
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed))
        conn.commit()
        log.info(f"用户 {username} 创建成功")
        return True
    except Exception as e:
        conn.rollback()
        log.error(f"用户 {username} 创建失败: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        log.info(f"尝试查询用户: {username}")
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        if user:
            log.info(f"用户 {username} 查询成功")
        else:
            log.info(f"用户 {username} 未找到")
        return user
    except Exception as e:
        log.error(f"用户 {username} 查询失败: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()
```
这段代码实现了数据库连接、用户表初始化、密码加密、用户创建和用户查询等功能。其中，`get_connection` 函数用于建立与数据库的连接，`init_db` 函数用于初始化用户表，`hash_password` 函数用于对密码进行加密，`create_user` 函数用于创建新用户，`get_user` 函数用于查询用户信息。

### 2. 新增 `apis/user_api.py`
接下来，我们要新增 `apis/user_api.py` 文件，用于处理用户注册和登录的 API 请求。以下是该文件的详细代码：
```python
from flask import Blueprint, request, jsonify
from RingConn_TestPlatform.backend.models.user import create_user, get_user, hash_password
import logging

log = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/register', methods=['POST'])
  def register():
    data = request.get_json()
    log.info(f"接收到的注册数据: {data}")  # 使用日志记录接收到的注册数据
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        log.warning("用户名和密码不能为空")  # 使用日志记录验证失败信息
        return jsonify({'status': 'error', 'message': '用户名和密码不能为空'})
    if get_user(username):
        log.warning(f"用户名 {username} 已存在")  # 使用日志记录用户名已存在信息
        return jsonify({'status': 'error', 'message': '用户名已存在'})
    if create_user(username, password):
        log.info(f"用户 {username} 注册成功")  # 使用日志记录注册成功信息
        return jsonify({'status': 'success'})
    log.error(f"用户 {username} 注册失败")  # 使用日志记录注册失败信息
    return jsonify({'status': 'error', 'message': '注册失败'})

@user_bp.route('/api/login', methods=['POST'])
  def login():
    data = request.get_json()
    log.info(f"接收到的登录数据: {data}")  # 使用日志记录接收到的登录数据
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        log.warning("用户名和密码不能为空")  # 使用日志记录验证失败信息
        return jsonify({'status': 'error', 'message': '用户名和密码不能为空'})
    user = get_user(username)
    if not user:
        log.warning(f"用户 {username} 不存在")  # 使用日志记录用户不存在信息
    else:
        log.info(f"用户 {username} 的密码哈希值: {user['password']}")  # 使用日志记录用户密码哈希值
        log.info(f"输入密码的哈希值: {hash_password(password)}")  # 使用日志记录输入密码的哈希值
    if not user or user['password'] != hash_password(password):
        log.warning("用户名或密码错误")  # 使用日志记录验证失败信息
        return jsonify({'status': 'error', 'message': '用户名或密码错误'})
    log.info(f"用户 {username} 登录成功")  # 使用日志记录登录成功信息
    return jsonify({'status': 'success', 'token': 'dummy_token'})
```
这段代码定义了两个 API 接口：`/api/register` 用于用户注册，`/api/login` 用于用户登录。在注册接口中，会先验证用户名和密码是否为空，以及用户名是否已存在，然后调用 `create_user` 函数创建新用户。在登录接口中，会先验证用户名和密码是否为空，然后查询用户信息并验证密码是否正确，若验证通过则返回登录成功信息和一个虚拟的 `token`。

### 3. 修改 `app.py`
最后，我们要修改 `app.py` 文件，将用户 API 蓝图注册到 Flask 应用中。以下是修改后的代码：
```python
from flask import Flask, jsonify
from RingConn_TestPlatform.backend.apis.binding_number_api import binding_number_bp
from RingConn_TestPlatform.backend.apis.user_api import user_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(binding_number_bp)
app.register_blueprint(user_bp)

@app.route('/', methods=['GET'])
  def get_data():
    data = {
        "message": "Hello from Flask!"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
```
通过以上修改，我们将用户 API 集成到了 Flask 应用中，使得应用能够处理用户注册和登录的请求。

## 三、前端代码实现（Vue 3 + Element Plus + Vue Router） 🖥️
### 1. 路由配置
在 `src/router/index.js` 中添加登录和注册页面的路由。以下是配置代码：
```javascript
import { createRouter, createWebHistory } from 'vue-router'
import BindingNumber from '../views/tools/BindingNumber.vue'
import Login from '../views/Login.vue'

const routes = [
    { path: '/', redirect: '/tools/binding_number' },
    { path: '/login', component: Login },
    { path: '/tools/binding_number', component: BindingNumber }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if (!token && to.path!== '/login') {
        next('/login')
    } else if (token && to.path === '/login') {
        next('/')
    } else {
        next()
    }
})

export default router
```
这段代码配置了路由规则，当用户访问根路径时会重定向到 `/tools/binding_number` 页面，当用户访问 `/login` 页面时会显示登录页面。同时，使用 `router.beforeEach` 进行路由守卫，确保未登录用户只能访问登录页面。

### 2. 登录页面（`src/views/Login.vue`）
以下是登录页面的代码：
```vue
<template>
    <div class="login-bg">
        <el-card class="login-card">
            <div class="login-icon">
                <el-icon size="40"><Lock /></el-icon>
            </div>
            <div class="login-title">{{ isLogin ? '登录' : '注册' }}</div>
            <el-form :model="form" :rules="rules" ref="formRef" class="login-form">
                <el-form-item prop="username">
                    <el-input v-model="form.username" placeholder="用户名" />
                </el-form-item>
                <el-form-item prop="password">
                    <el-input v-model="form.password" type="password" placeholder="密码" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" style="width:100%" @click="onSubmit">{{ isLogin ? '登录' : '注册' }}</el-button>
                </el-form-item>
            </el-form>
            <div class="login-switch">
                <span>{{ isLogin ? '没有账号？' : '已有账号？' }}</span>
                <el-link type="primary" @click="isLogin =!isLogin">{{ isLogin ? '立即注册' : '去登录' }}</el-link>
            </div>
        </el-card>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { login, register } from '../api/user'

const router = useRouter()
const isLogin = ref(true)
const form = ref({ username: '', password: '' })
const formRef = ref(null)
const rules = {
    username: [ { required: true, message: '请输入用户名', trigger: 'blur' } ],
    password: [ { required: true, message: '请输入密码', trigger: 'blur' } ]
}

const onSubmit = () => {
    formRef.value.validate(async (valid) => {
        if (!valid) return
        try {
            if (isLogin.value) {
                const res = await login(form.value)
                if (res.data.status === 'success') {
                    localStorage.setItem('token', res.data.token)
                    ElMessage.success('登录成功')
                    router.push('/')
                } else {
                    ElMessage.error(res.data.message || '登录失败')
                }
            } else {
                const res = await register(form.value)
                if (res.data.status === 'success') {
                    ElMessage.success('注册成功，请登录')
                    isLogin.value = true
                } else {
                    ElMessage.error(res.data.message || '注册失败')
                }
            }
        } catch (e) {
            ElMessage.error('请求失败')
        }
    })
}
</script>

<style scoped>
.login-bg {
    min-height: 100vh;
    background: #f7f8fa;
    display: flex;
    align-items: center;
    justify-content: center;
}
.login-card {
    width: 360px;
    border-radius: 12px;
    box-shadow: 0 2px 12px #0000000d;
    padding: 32px 32px 16px 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.login-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 12px;
}
.login-title {
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 18px;
}
.login-form {
    width: 100%;
}
.login-switch {
    text-align: center;
    margin-top: 8px;
    color: #888;
    font-size: 14px;
}
</style>
```
这个登录页面使用了 Vue 3 和 Element Plus 组件库，实现了登录和注册功能的切换。用户可以输入用户名和密码，点击“登录”或“注册”按钮进行相应操作。若操作成功，会给出相应的提示信息，并进行页面跳转。

### 3. 接口（`src/api/user.js`）
以下是处理登录和注册请求的接口代码：
```javascript
import axios from 'axios'

// 获取 API 基础地址
const baseUrl = import.meta.env.VITE_API_BASE_URL

// 登录接口
export const login = (data) => {
    return axios.post(`${baseUrl}/api/login`, data)
}

// 注册接口
export const register = (data) => {
    return axios.post(`${baseUrl}/api/register`, data)
}
```
这段代码使用 `axios` 库发送登录和注册请求，将用户输入的数据发送到后端 API 接口。

通过以上步骤，我们成功地为自动化测试平台添加了登录注册功能🎉。从数据库的搭建到后端接口的实现，再到前端页面的开发，每一步都紧密相连，共同构建了一个完整的登录注册系统。希望这篇博客能对你有所帮助，让我们一起在技术的道路上不断前行🚀！