# 学生管理系统 - 前端

一个基于 Vue 3 + TypeScript + Tailwind CSS 的现代化学生管理系统前端应用。

## 🚀 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - JavaScript 的超集
- **Tailwind CSS** - 原子化 CSS 框架
- **Vue Router** - Vue.js 官方路由
- **Pinia** - Vue 状态管理库
- **Vite** - 下一代前端构建工具

## 📦 安装与运行

### 环境要求

- Node.js >= 20.19.0
- npm 或 yarn

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

应用将在 http://localhost:5173 启动

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 👥 用户角色与测试账号

### 学生登录
- **路径**: `/login/student`
- **学号**: `2023001`
- **密码**: `student123`

### 教师登录
- **路径**: `/login/teacher`
- **工号**: `T001`
- **密码**: `teacher123`

### 管理员登录
- **路径**: `/login/admin`
- **用户名**: `admin`
- **密码**: `admin123`

## 📁 项目结构

```
src/
├── components/           # 组件目录
│   ├── common/          # 公共组件
│   │   ├── Alert.vue   # 警告组件
│   │   ├── Card.vue    # 卡片组件
│   │   └── LoadingSpinner.vue  # 加载组件
│   ├── AppLoading.vue   # 应用加载组件
│   ├── Layout.vue       # 布局组件
│   └── index.ts         # 组件导出文件
├── router/              # 路由配置
│   └── index.ts
├── stores/              # 状态管理
│   └── auth.ts         # 认证状态管理
├── styles/              # 样式文件
├── views/               # 页面组件
│   ├── student/         # 学生页面
│   ├── teacher/         # 教师页面
│   ├── admin/           # 管理员页面
│   ├── RoleSelect.vue   # 角色选择页面
│   └── Login.vue        # 登录页面
├── App.vue              # 根组件
└── main.ts              # 入口文件
```

## 🎨 功能特性

### 角色选择系统
- 精美的角色选择界面
- 每个角色有独特的主题色和功能预览

### 登录系统
- 三个独立的登录页面（学生、教师、管理员）
- 模拟登录功能
- 加载状态和错误处理

### 主布局系统
- 响应式侧边栏
- 动态主题色
- 角色个性化菜单

### 仪表板页面
- **学生仪表板**: 课程表、成绩概览、考试安排
- **教师仪表板**: 今日课程、授课信息、学生出勤
- **管理员仪表板**: 系统监控、用户统计、活动日志

### 状态管理
- Pinia 状态管理
- 本地存储持久化
- 权限控制

## 🛠️ 开发指南

### 添加新页面

1. 在 `src/views/` 对应角色目录下创建 `.vue` 文件
2. 在 `src/router/index.ts` 中添加路由配置
3. 在 `src/components/Layout.vue` 中添加菜单项

### 使用公共组件

```vue
<template>
  <Card title="卡片标题">
    <Alert type="success" title="成功" description="操作成功！" />
    <LoadingSpinner size="md" color="primary" />
  </Card>
</template>

<script setup>
import { Card, Alert, LoadingSpinner } from '@/components'
</script>
```

### 状态管理

```ts
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 登录
authStore.studentLogin(userData)

// 检查权限
authStore.hasPermission('view_grades')

// 获取主题色
const theme = authStore.getThemeColors()
```

## 🔧 自定义配置

### 主题色修改

在 `src/stores/auth.ts` 中的 `getThemeColors` 方法中修改对应的颜色值。

### 路由守卫

在 `src/router/index.ts` 中的 `beforeEach` 守卫中配置访问权限。

### 组件注册

公共组件已在 `src/components/index.ts` 中导出，可直接导入使用。

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**注意**: 这是一个演示项目，所有登录数据都是模拟数据，仅用于展示功能。
