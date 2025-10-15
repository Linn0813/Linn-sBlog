---
title: 测试工具平台搭建实现 🚧
date: 2025-05-14 14:18:19
updated: {{current_date_time}} 
categories:
  - 自动化测试 & 工具开发（Test Automation & Tool Development）
  - 平台开发
  - 自动化工具
tags:
  - 技术选型
  - 测试工具平台
  - 前端开发
  - 后端开发
keywords: 测试工具平台, 技术选型, 前端技术, 后端技术
description: '结合最新技术，详细介绍前后端分离测试工具平台搭建全流程，包含前端和后端的技术选型与实现步骤。'
top_img: /img/testplatform-implementation.png
comments: true  
cover: /img/testplatform-implementation.png
toc: true  
toc_number: true  
toc_style_simple: false  
copyright: true  
copyright_author: yuxiaoling  
copyright_info: 版权所有，转载请注明出处。  
mathjax: false  
katex: false  
aplayer: false  
highlight_shrink: false  
aside: true  
abcjs: false  
noticeOutdate: false 
---
# 测试工具平台搭建实现 🚧

## 承接选型，开启搭建之旅
在上一篇博客中，我们像一群精明的“技术探险家”🧐，经过一番深入的调研和分析，为测试工具平台选好了前端的 Vue 3、Element Plus 和 Vue Router，以及后端的 Flask 和 MySQL 这些“得力助手”🤝。现在，我们就像拿到了“宝藏地图”，要开始按照地图上的指引，一步一步搭建这个测试工具平台啦🚀！

## 项目初始化
### 前端项目初始化
首先，我们要使用 Vite 这个“超级魔法师”🧙‍♂️，快速创建一个 Vue 3 项目。Vite 就像一辆“超级快车”🚄，基于 ES Modules 的前端构建工具，有着快速冷启动、即时热更新等神奇技能，能大大提高我们的开发效率。具体的“魔法咒语”（初始化命令）如下：
```bash
npm init vite@latest test - platform - frontend -- --template vue
cd test - platform - frontend
npm install
```
接着，我们要给这个项目配上 Element Plus 和 Vue Router 这两件“法宝”🔮。安装命令就像给“法宝”注入魔力的咒语：
```bash
npm install element - plus @element - plus/icons - vue vue - router
```
### 后端项目初始化
我们还要创建一个新的 Python 项目目录，就像建造一个新的“基地”🏭。然后初始化虚拟环境，这个虚拟环境就像一个“隔离舱”，能把不同项目的依赖隔离开，避免它们“打架”😜。具体的“建造步骤”（初始化命令）如下：
```bash
mkdir test - platform - backend
cd test - platform - backend
python -m venv venv
.\venv\Scripts\activate
```
之后，我们要给这个“基地”装上 Flask 和 MySQL 驱动这两个“发动机”🚗。安装命令就像启动“发动机”的钥匙：
```bash
pip install flask flask - sqlalchemy pymysql
```

## 项目结构设计
### 后端项目结构
后端项目的结构就像一座精心设计的“大厦”🏢，主要分为以下几个部分：
- **__init__.py**：这就像是“大厦”的“门牌”🏷️，是 Python 包初始化文件，能把目录标记成 Python 包。
- **apis 目录**：这里面放的是 API 相关代码，就像“大厦”里的“通信室”📞。其中，`binding_number_api.py` 提供了 `BindingNumberApi` 类，专门处理绑定数量的 API 请求。
- **app.py**：它是 Flask 应用的入口文件，就像“大厦”的“大门”🚪，负责注册蓝图和启动服务。
- **config.py**：这是项目的配置文件，里面有数据库和服务器的配置信息，就像“大厦”的“设计图纸”📄。
- **extension.py**：它是项目的扩展配置文件，可能会包含跨域处理这些功能，就像给“大厦”加了一些“秘密通道”🧙。
- **models 目录**：这里面放的是数据模型相关代码，就像“大厦”里的“档案室”📁。比如 `binding_number.py` 能根据 `ring_id` 从数据库里读取绑定数量。
- **utils 目录**：这里面是工具类代码，就像“大厦”里的“工具间”🛠️。`logger_config.py` 是日志配置文件，能设置日志输出格式和处理器；`request.py` 是请求类，把 GET 和 POST 请求方法封装起来了。

### 前端项目结构
前端项目的结构就像一个温馨的“家园”🏡，主要是这样的：
- **index.html**：它是项目的入口 HTML 文件，就像“家园”的“大门”🚪。
- **src 目录**：这里面放的是前端源代码，就像“家园”里的“各个房间”🏠。
  - **App.vue**：它是 Vue 项目的根组件，包含顶部栏、侧边栏和主内容区，就像“家园”的“客厅”，是整个项目的核心区域。
  - **api 目录**：这里面放的是 API 请求相关代码，就像“家园”里的“快递收发室”📦。像 `binding_number.js` 就封装了查询指定 `ring_id` 绑定数量的 API 请求。
  - **assets 目录**：这里面放的是静态资源，比如图片、样式这些，就像“家园”里的“装饰品”🎨。
  - **components 目录**：这里面放的是 Vue 组件，每个组件都有自己的小任务，就像“家园”里的“家庭成员”，各司其职。
  - **main.js**：它是 Vue 项目的入口文件，负责初始化 Vue 应用和注册插件，就像“家园”的“管家”🧑‍管家，把一切安排得井井有条。
  - **router 目录**：这里面放的是路由配置文件，就像“家园”里的“导航地图”🗺️。`index.js` 配置了 Vue 路由，定义了页面跳转规则。
  - **style.css**：这是全局样式文件，能让项目变得更漂亮，就像给“家园”涂上了一层“漂亮的油漆”🎨。
  - **views 目录**：这里面放的是页面视图组件，就像“家园”里的“各个房间”，每个房间都有不同的功能。像 `BindingNumber.vue` 就是工具绑定用户数据总数查询页面组件。
- **vite.config.js**：它是 Vite 构建工具的配置文件，能让 Vite 更好地工作，就像给“家园”的“智能系统”设置参数。 

## 前端界面搭建
### 整体布局
在 `src/App.vue` 里，我们要像一位“室内设计师”🎨，搭建平台的整体布局，包含顶部栏、侧边栏和主内容区。顶部栏就像“家园”的“招牌”🏢，能显示平台的名称和设置按钮；侧边栏就像“家园”的“走廊”🚶，能显示导航菜单；主内容区就像“家园”的“客厅”🛋️，用来显示具体的页面内容。具体的“设计图纸”（代码）如下：
```vue
<template>
  <div class="layout - root">
    <!-- 顶部栏 -->
    <header class="layout - header">
      <div class="header - left">
        <span class="logo">&lt;&lt; 测试平台</span>
      </div>
      <div class="header - right">
        <el - icon style="margin - right: 8px;"><Setting /></el - icon>
        <span style="margin - right: 16px;">设置</span>
        <el - avatar size="small">A</el - avatar>
      </div>
    </header>
    <div class="layout - main">
      <!-- 侧边栏 -->
      <aside class="layout - sider">
        <el - menu
          :default - active="activeMenu"
          class="el - menu - vertical - demo"
          router
          background - color="#f8f9fb"
          text - color="#333"
          active - text - color="#1976ed"
        >
          <el - menu - item index="/case">
            <el - icon><Document /></el - icon>
            <span>测试用例管理</span>
          </el - menu - item>
          <el - sub - menu index="tools">
            <template #title>
              <el - icon><Tools /></el - icon>
              <span>测试工具集成</span>
            </template>
            <el - menu - item index="/binding_number">数量查询</el - menu - item>
          </el - sub - menu>
        </el - menu>
      </aside>
      <!-- 主内容区 -->
      <main class="layout - content">
        <router - view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue - router'
import { Setting, Document, Tools } from '@element - plus/icons - vue'

const route = useRoute()
const activeMenu = ref(route.path)
watch(route, (val) => {
  activeMenu.value = val.path
})
</script>

<style scoped>
.layout - root {
  height: 100vh;
  display: flex;
  flex - direction: column;
  background: #f8f9fb;
}
.layout - header {
  height: 56px;
  background: #fff;
  display: flex;
  align - items: center;
  justify - content: space - between;
  border - bottom: 1px solid #f0f0f0;
  padding: 0 32px;
}
.header - left .logo {
  font - size: 22px;
  font - weight: bold;
  color: #1976ed;
  letter - spacing: 2px;
}
.header - right {
  display: flex;
  align - items: center;
  font - size: 16px;
  color: #1976ed;
}
.layout - main {
  flex: 1;
  display: flex;
  min - height: 0;
}
.layout - sider {
  width: 220px;
  background: #f8f9fb;
  border - right: 1px solid #f0f0f0;
  padding - top: 12px;
}
.layout - content {
  flex: 1;
  padding: 32px 24px;
  min - width: 0;
  background: #f8f9fb;
  overflow: auto;
}
.el - menu {
  border - right: none;
  background: #f8f9fb;
}
.el - menu - item span,
.el - sub - menu__title span {
  font - size: 16px;
  height: 48px;
  line - height: 48px;
}
</style>
```
### 页面组件
在 `src/views/BindingNumber.vue` 里，我们要像一位“工匠”🧑‍🔧，实现输入框、查询按钮和结果展示。用户可以在输入框里输入 `ring_id`，然后点击查询按钮，就像按下“魔法按钮”🔘，就能查到该 `ring_id` 的绑定数量啦。具体的“制作工艺”（代码）如下：
```vue
<template>
    <div style="padding: 24px;">
      <el - card shadow="never" style="border - radius: 12px;">
        <div style="font - size: 24px; font - weight: bold; display: flex; align - items: center; margin - bottom: 16px;">
          <el - icon style="margin - right: 8px;"><Search /></el - icon>
          工具绑定用户数据总数查询
        </div>
        <div style="display: flex; align - items: center; margin - bottom: 16px;">
          <el - icon style="margin - right: 8px; color: #409EFF;"><Filter /></el - icon>
          <span style="font - size: 16px; font - weight: 500; margin - right: 16px;">选择工具类型</span>
          <el - button - group>
            <el - button
              v - for="item in options"
              :key="item.value"
              :type="selectedValue === item.value ? 'primary' : 'default'"
              :disabled="item.disabled"
              @click="selectType(item.value)"
              style="min - width: 120px; display: flex; align - items: center;"
            >
              <el - icon style="margin - right: 4px;">
                <component :is="item.icon" />
              </el - icon>
              {{ item.label }}
            </el - button>
          </el - button - group>
        </div>
        <el - button
          type="primary"
          size="large"
          style="width: 100%; font - size: 20px; border - radius: 10px; margin - bottom: 24px;"
          @click="queryBindingNumber"
          :disabled="!selectedValue"
        >
          查询
        </el - button>
      </el - card>
  
      <el - card shadow="never" style="margin - top: 32px; border - radius: 12px;">
        <div style="font - size: 20px; font - weight: bold; margin - bottom: 16px;">查询结果</div>
        <div v - if="result === null" style="color: #888; font - size: 16px; min - height: 40px;">
          请选择工具类型进行查询
        </div>
        <div v - else - if="error" style="color: red;">{{ error }}</div>
        <div v - else>绑定数量：{{ result }}</div>
      </el - card>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { fetchBindingNumber } from '../../api/binding_number'
  import { Search, Filter, Cpu, Download, Upload } from '@element - plus/icons - vue'
  
  const options = [
    { value: '1', label: '工具一', icon: Cpu },
    { value: '2', label: '工具二', icon: Download },
    { value: '0', label: 'ALL', icon: Upload }
  ]
  
  const selectedValue = ref('')
  const result = ref(null)
  const error = ref('')
  
  function selectType(val) {
    if (options.find(o => o.value === val && !o.disabled)) {
      selectedValue.value = val
    }
  }
  
  async function queryBindingNumber() {
    result.value = null
    error.value = ''
    if (!selectedValue.value) {
      error.value = '请选择工具类型'
      return
    }
    try {
      const res = await fetchBindingNumber(selectedValue.value)
      if (res.data.status === 'success') {
        result.value = res.data.count
      } else {
        error.value = res.data.message || '查询失败'
      }
    } catch (e) {
      error.value = '请求失败'
    }
  }
  </script>
```
### 路由配置
在 `src/router/index.js` 里，我们要像一位“交通规划师”🚥，配置路由，定义页面跳转规则。具体的“规划方案”（代码）如下：
```javascript
import { createRouter, createWebHistory } from 'vue - router'
import BindingNumber from '../views/tools/BindingNumber.vue'
// 其它页面组件...

const routes = [
  { path: '/', redirect: '/tools/binding_number' },
  { path: '/tools/binding_number', component: BindingNumber },
  // 其它页面...
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

## 后端接口开发
### 路由配置
在 `backend/app.py` 里，我们要像一位“指挥官”👨‍✈️，注册 API 的蓝图，把 API 接口挂载到 Flask 应用上。具体的“指挥命令”（代码）如下：
```python
from flask import Flask
from apis.binding_number_api import binding_number_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(binding_number_bp)

if __name__ == '__main__':
    app.run(debug = True)
```
### API 实现
`backend/apis/binding_number_api.py` 就像一位“情报员”🕵️，实现了处理绑定数量查询请求的 API。具体的“情报传递方式”（代码）如下：
```python
from flask import Blueprint, request, jsonify
from flask.views import MethodView
import logging

log = logging.getLogger(__name__)

binding_number_bp = Blueprint('binding_number', __name__, url_prefix='/api/binding_number')

class BindingNumberApi(MethodView):
    def post(self):
        try:
            form = request.json
            if not form:
                return jsonify({'status': 'error', 'message': '无效的 JSON 数据'}), 400

            ring_id = int(form.get('ring_id'))
            log.info(f'ring_id: {ring_id}')

            if ring_id is None:
                return jsonify({'status': 'error', 'message': '缺少 ring_id 参数'}), 400

            count = BN.get_binding_number(ring_id)

            if count is None:
                return jsonify({'status': 'error', 'message': '无效的 ring_id 或查询结果为空'}), 400

            return jsonify({'status': 'success', 'count': count})

        except Exception as e:
            log.error(f'异常: {str(e)}')
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

# 注册视图函数
binding_number_bp.add_url_rule('', view_func=BindingNumberApi.as_view('binding_number'))
```
### 数据模型
`backend/models/binding_number.py` 就像一位“数据管理员”📁，实现了从数据库查询绑定数量的功能。具体的“管理方法”（代码）如下：
```python
import pymysql
from config import MySqlConfig

class BindingNumber:

    def get_binding_number (self, ring_id):
        # 查数据库的操作内容
        pass

BN = BindingNumber()
```

## 前后端交互
1. 用户在前端 `BindingNumber.vue` 页面输入 `ring_id`，点击“查询绑定数量”按钮，就像按下了“启动开关”🔛。
2. 触发 `queryBindingNumber` 方法，调用 `fetchBindingNumber` 函数向后端发送 Post 请求，请求地址为 `http://localhost:5000/api/binding_number`，并携带 `ring_id` 参数，就像派出了一位“信使”📨。
3. 后端 `binding_number` 路由接收到请求，获取 `ring_id` 参数，就像“信使”把消息送到了目的地📬。
4. 调用 `get_binding_number` 函数从数据库中查询对应 `ring_id` 的绑定数量，就像在“档案室”里查找资料📖。
5. 后端将查询结果封装成 JSON 格式返回给前端，就像把资料整理好打包送回📦。
6. 前端根据返回结果更新页面，显示绑定数量或错误信息，就像把资料展示给用户看👀。