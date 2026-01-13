# AI测试用例生成功能迁移到测试平台方案

## 📋 项目对比分析

### AI项目 (ai_demo_service)
- **后端框架**: FastAPI
- **前端框架**: Vue 3 + Element Plus + Vite
- **核心功能**: 
  - AI测试用例生成
  - 文档理解
  - 功能模块提取
  - 质量评估
- **架构**: Domain-Driven Design (DDD)
  - `domain/`: 业务逻辑层
  - `infrastructure/`: 基础设施层（LLM、向量存储）
  - `api/`: API路由层

### 测试平台 (ringconntestplatform)
- **后端框架**: Flask
- **前端框架**: Vue 3 + Element Plus + Vite ✅ (技术栈一致)
- **核心功能**: 
  - API测试管理
  - 测试用例管理
  - 测试执行
- **架构**: MVC模式
  - `controllers/`: 控制器层
  - `services/`: 服务层
  - `models/`: 数据模型层
  - `routes/`: 路由层

## 🎯 迁移策略

### 方案一：模块化集成（推荐）⭐

**优点**:
- 保持测试平台现有架构不变
- 最小化对现有代码的影响
- 易于维护和扩展

**实施步骤**:

#### 1. 后端迁移

##### 1.1 复制核心模块到测试平台

```bash
# 从AI项目复制以下目录到测试平台
ringconntestplatform/backend/
├── domain/                    # 新增：业务逻辑层
│   ├── test_case/            # 测试用例生成核心逻辑
│   │   ├── service.py        # 主服务类
│   │   ├── test_case_generator.py
│   │   ├── document_understanding.py
│   │   ├── extractors.py
│   │   ├── prompts.py
│   │   └── validators.py
│   └── task/                 # 任务管理
│       └── manager.py
├── infrastructure/           # 新增：基础设施层
│   └── llm/                  # LLM服务
│       └── service.py
└── shared/                   # 新增：共享工具
    ├── config.py
    ├── logger.py
    └── debug_recorder.py
```

##### 1.2 创建Flask路由适配器

在 `ringconntestplatform/backend/routes/` 下创建：
- `ai_test_case_routes.py` - AI测试用例生成路由

##### 1.3 创建Flask控制器适配器

在 `ringconntestplatform/backend/controllers/` 下创建：
- `ai_test_case_controller.py` - 适配FastAPI服务到Flask控制器

##### 1.4 更新依赖

在 `ringconntestplatform/backend/requirements.txt` 中添加：
```txt
# AI功能依赖
openai>=1.0.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
python-dotenv>=1.0.0
```

#### 2. 前端迁移

##### 2.1 复制Vue组件

```bash
ringconntestplatform/frontend/src/
├── views/
│   └── ai/                    # 新增：AI测试用例生成页面
│       ├── AITestCaseGenerate.vue
│       └── AiModule.vue
└── components/
    └── ai/                    # 新增：AI相关组件
        ├── AiPageLayout.vue
        ├── FunctionPointsConfirm.vue
        └── FunctionPointsContent.vue
```

##### 2.2 复制API接口

```bash
ringconntestplatform/frontend/src/apis/
└── ai.js                      # 新增：AI相关API
```

##### 2.3 更新路由

在 `ringconntestplatform/frontend/src/router/index.js` 中添加AI测试用例生成路由

#### 3. 配置迁移

##### 3.1 环境变量配置

在测试平台添加 `.env` 或更新 `config.py`:
```python
# LLM配置
LLM_BASE_URL = os.getenv('LLM_BASE_URL', '')
LLM_API_KEY = os.getenv('LLM_API_KEY', '')
LLM_DEFAULT_MODEL = os.getenv('LLM_DEFAULT_MODEL', 'gpt-4')
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')  # openai/azure
```

##### 3.2 数据目录

创建数据存储目录：
```bash
ringconntestplatform/data/
├── debug/ai_runs/            # AI运行调试记录
└── uploads/                   # 文档上传目录
```

## 🔧 具体实施步骤

### 阶段一：后端核心模块迁移（1-2天）

1. **复制核心业务逻辑**
   ```bash
   cd /Users/yuxiaoling/PycharmProjects
   # 创建domain目录
   mkdir -p ringconntestplatform/backend/domain/test_case
   mkdir -p ringconntestplatform/backend/domain/task
   mkdir -p ringconntestplatform/backend/infrastructure/llm
   mkdir -p ringconntestplatform/backend/shared
   
   # 复制文件（需要手动调整import路径）
   cp -r ai_demo_service/backend/domain/test_case/* ringconntestplatform/backend/domain/test_case/
   cp -r ai_demo_service/backend/domain/task/* ringconntestplatform/backend/domain/task/
   cp -r ai_demo_service/backend/infrastructure/llm/* ringconntestplatform/backend/infrastructure/llm/
   cp ai_demo_service/backend/shared/config.py ringconntestplatform/backend/shared/
   cp ai_demo_service/backend/shared/logger.py ringconntestplatform/backend/shared/
   cp ai_demo_service/backend/shared/debug_recorder.py ringconntestplatform/backend/shared/
   ```

2. **修复import路径**
   - 将所有 `from infrastructure.llm.service` 改为相对导入或适配Flask项目结构
   - 调整 `shared.config` 的配置读取方式以适配Flask

3. **创建Flask适配器**
   - 创建 `controllers/ai_test_case_controller.py`
   - 创建 `routes/ai_test_case_routes.py`
   - 在 `app.py` 中注册新路由

### 阶段二：前端组件迁移（1天）

1. **复制Vue组件**
   ```bash
   mkdir -p ringconntestplatform/frontend/src/views/ai
   mkdir -p ringconntestplatform/frontend/src/components/ai
   
   cp -r ai_demo_service/frontend/src/views/ai/* ringconntestplatform/frontend/src/views/ai/
   cp -r ai_demo_service/frontend/src/components/ai/* ringconntestplatform/frontend/src/components/ai/
   ```

2. **复制API接口**
   ```bash
   cp ai_demo_service/frontend/src/apis/ai.js ringconntestplatform/frontend/src/apis/
   ```

3. **更新API基础URL**
   - 修改 `ai.js` 中的API基础路径以适配Flask路由

4. **添加路由**
   - 在测试平台的路由配置中添加AI测试用例生成页面路由

### 阶段三：集成测试（1天）

1. **测试后端API**
   - 测试文档上传
   - 测试功能模块提取
   - 测试测试用例生成

2. **测试前端功能**
   - 测试页面显示
   - 测试交互流程
   - 测试数据展示

3. **修复兼容性问题**
   - 修复Flask和FastAPI的差异
   - 修复前端API调用路径
   - 修复样式问题

## 📝 关键适配点

### 1. FastAPI → Flask 适配

**FastAPI路由**:
```python
@router.post("/function-modules/extract")
def extract_function_modules(payload: ExtractModulesRequest):
    ...
```

**Flask路由**:
```python
@ai_bp.route('/function-modules/extract', methods=['POST'])
def extract_function_modules():
    payload = request.get_json()
    ...
```

### 2. 响应格式统一

FastAPI使用Pydantic模型，Flask需要手动构造响应：
```python
# FastAPI
return ExtractModulesResponse(function_points=modules)

# Flask
return jsonify({
    'code': 0,
    'message': 'success',
    'data': {
        'function_points': modules
    }
})
```

### 3. 异步任务处理

测试平台可能需要适配任务管理机制，可以：
- 复用AI项目的 `domain/task/manager.py`
- 或者集成到测试平台现有的任务系统

### 4. 数据库集成（可选）

如果需要将生成的测试用例保存到数据库：
- 在 `models/` 中创建AI测试用例相关模型
- 在控制器中调用模型保存方法

## 🚀 快速开始脚本

创建一个迁移脚本 `migrate_ai_to_platform.sh`:

```bash
#!/bin/bash

# 设置路径
AI_PROJECT="/Users/yuxiaoling/PycharmProjects/ai_demo_service"
PLATFORM_PROJECT="/Users/yuxiaoling/PycharmProjects/ringconntestplatform"

# 1. 复制后端核心模块
echo "复制后端核心模块..."
cp -r $AI_PROJECT/backend/domain $PLATFORM_PROJECT/backend/
cp -r $AI_PROJECT/backend/infrastructure $PLATFORM_PROJECT/backend/
mkdir -p $PLATFORM_PROJECT/backend/shared
cp $AI_PROJECT/backend/shared/config.py $PLATFORM_PROJECT/backend/shared/
cp $AI_PROJECT/backend/shared/logger.py $PLATFORM_PROJECT/backend/shared/
cp $AI_PROJECT/backend/shared/debug_recorder.py $PLATFORM_PROJECT/backend/shared/

# 2. 复制前端组件
echo "复制前端组件..."
cp -r $AI_PROJECT/frontend/src/views/ai $PLATFORM_PROJECT/frontend/src/views/
cp -r $AI_PROJECT/frontend/src/components/ai $PLATFORM_PROJECT/frontend/src/components/
cp $AI_PROJECT/frontend/src/apis/ai.js $PLATFORM_PROJECT/frontend/src/apis/

# 3. 创建数据目录
echo "创建数据目录..."
mkdir -p $PLATFORM_PROJECT/data/debug/ai_runs
mkdir -p $PLATFORM_PROJECT/data/uploads

echo "迁移完成！请手动修复import路径和配置。"
```

## ⚠️ 注意事项

1. **依赖冲突**: 检查两个项目的依赖是否有冲突，特别是Python版本要求
2. **配置管理**: 统一配置管理方式，建议使用环境变量
3. **日志系统**: 统一日志格式和输出方式
4. **错误处理**: 统一错误响应格式
5. **权限控制**: 如果测试平台有权限系统，需要添加AI功能的权限控制

## 📚 后续优化

1. **数据库持久化**: 将生成的测试用例保存到数据库
2. **历史记录**: 记录AI生成历史，支持查看和复用
3. **批量生成**: 支持批量文档处理
4. **模板管理**: 支持自定义prompt模板
5. **质量报告**: 集成质量评估报告到测试平台

## 🎯 推荐实施顺序

1. ✅ **第一步**: 复制核心模块，修复import路径
2. ✅ **第二步**: 创建Flask路由和控制器适配器
3. ✅ **第三步**: 测试后端API功能
4. ✅ **第四步**: 复制前端组件，更新API路径
5. ✅ **第五步**: 集成测试和修复问题
6. ✅ **第六步**: 添加数据库持久化（可选）
7. ✅ **第七步**: 优化和性能调优

