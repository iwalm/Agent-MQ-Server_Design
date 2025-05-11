# 医院管理APP项目运行与使用详解

## 项目运行指南

### 1. 环境准备

#### 开发环境要求：
- **操作系统**：Windows 10/11, macOS 10.15+, 或 Linux (Ubuntu 20.04+推荐)
- **Node.js**：v14.x 或更高版本
- **npm**：v6.x 或更高版本 (或使用yarn)
- **MongoDB**：社区版4.4+
- **移动开发环境**：
  - Android开发：Android Studio + Android SDK
  - iOS开发：Xcode 12+

#### 工具安装：
```bash
# 检查Node.js是否安装
node -v
npm -v

# 如果没有安装，从官网下载安装：
# https://nodejs.org/

# MongoDB安装指南：
# https://docs.mongodb.com/manual/installation/
```

### 2. 项目获取与初始化

```bash
# 克隆项目仓库
git clone https://github.com/yazdanhaider/Hospital-Management.git

# 进入项目目录
cd Hospital-Management

# 安装后端依赖
cd server
npm install

# 安装前端依赖
cd ../client
npm install
```

### 3. 数据库配置

1. 启动MongoDB服务：
   ```bash
   mongod
   ```
   (Windows用户可能需要使用管理员权限运行)

2. 创建数据库和初始数据：
   ```bash
   cd server
   npm run seed
   ```
   这将创建：
   - 一个管理员账户 (admin/admin123)
   - 几个测试医生账户
   - 基础科室设置
   - 初始药品库存

### 4. 配置环境变量

在`server`目录下创建`.env`文件：

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/hospital_management
JWT_SECRET=your_strong_secret_key_here
NODE_ENV=development
```

### 5. 启动项目

#### 启动后端服务：
```bash
cd server
npm start
```
成功启动后，控制台会显示：
```
Server is running on port 5000
MongoDB Connected...
```

#### 启动前端应用：

**方式1：使用模拟器**
```bash
cd client
npm run android  # 或 npm run ios
```

**方式2：开发模式**
```bash
cd client
npm start
```
然后在浏览器打开Expo开发工具，或使用Expo Go APP扫描二维码

### 6. 测试账号

- 管理员：admin / admin123
- 医生：doctor1 / doctor123
- 患者：patient1 / patient123

## 项目架构解析

### 前端结构 (client/)
```
src/
├── assets/            # 静态资源
├── components/        # 可复用组件
├── navigation/        # 路由配置
├── screens/           # 各功能页面
├── services/          # API服务
├── store/             # Redux状态管理
├── utils/             # 工具函数
└── App.js             # 主入口文件
```

### 后端结构 (server/)
```
src/
├── config/            # 配置文件
├── controllers/       # 业务逻辑
├── models/            # 数据库模型
├── routes/            # API路由
├── middleware/        # 中间件
├── utils/             # 工具函数
└── server.js          # 主入口文件
```

## 核心功能使用说明

### 1. 患者管理流程

**患者注册：**
1. 打开APP选择"注册"
2. 填写基本信息(姓名、手机号、身份证号等)
3. 设置登录密码
4. 完成验证后登录系统

**预约挂号：**
1. 登录后点击"预约挂号"
2. 选择科室(如内科、外科)
3. 选择医生(显示医生简介和排班时间)
4. 选择可用时间段
5. 确认预约并支付挂号费

### 2. 医生工作流程

**接诊患者：**
1. 登录医生账户
2. 查看"今日排班"列表
3. 选择已签到患者
4. 查看患者历史病历
5. 录入诊断信息和处方

**开具处方：**
1. 在诊断页面点击"开处方"
2. 搜索药品名称
3. 设置用法用量
4. 添加医嘱说明
5. 提交处方(自动扣除库存)

### 3. 管理员功能

**用户管理：**
1. 登录管理员账户
2. 进入"系统管理" > "用户管理"
3. 可添加/编辑/禁用用户账户
4. 设置用户角色(医生、护士、药师等)

**药品库存管理：**
1. 进入"药房管理"
2. 查看当前库存和预警药品
3. 点击"入库"添加新药品
4. 设置药品信息(名称、规格、价格等)
5. 设置库存预警阈值

## API接口文档

后端提供RESTful API，主要端点包括：

| 端点 | 方法 | 描述 |
|------|------|------|
| /api/auth/login | POST | 用户

