<script setup lang="ts">
import { RouterLink } from 'vue-router'

const roles = [
  {
    name: '学生',
    path: '/login/student',
    description: '查看课程、成绩、个人信息',
    bgColor: 'bg-blue-600',
    hoverColor: 'hover:bg-blue-700',
    icon: '👨‍🎓',
    features: ['课程查询', '成绩查看', '选课系统', '考试安排']
  },
  {
    name: '教师',
    path: '/login/teacher',
    description: '管理课程、录入成绩、考勤管理',
    bgColor: 'bg-green-600',
    hoverColor: 'hover:bg-green-700',
    icon: '👨‍🏫',
    features: ['课程管理', '成绩录入', '学生名单', '考勤管理']
  },
  {
    name: '管理员',
    path: '/login/admin',
    description: '系统管理、用户管理、数据统计',
    bgColor: 'bg-purple-600',
    hoverColor: 'hover:bg-purple-700',
    icon: '👨‍💼',
    features: ['用户管理', '权限设置', '数据统计', '系统配置']
  }
]
</script>

<template>
  <div class="relative isolate overflow-hidden bg-gray-900 min-h-screen">
    <img src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&crop=focalpoint&fp-y=.8&w=2830&h=1500&q=80&blend=111827&sat=-100&exp=15&blend-mode=multiply" alt="" class="absolute inset-0 -z-10 size-full object-cover object-right md:object-center" />
    <div class="hidden sm:absolute sm:-top-10 sm:right-1/2 sm:-z-10 sm:mr-10 sm:block sm:transform-gpu sm:blur-3xl" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-gradient-to-tr from-[#ff4694] to-[#776fff] opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" />
    </div>
    <div class="absolute -top-52 left-1/2 -z-10 -translate-x-1/2 transform-gpu blur-3xl sm:-top-112 sm:ml-16 sm:translate-x-0" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-gradient-to-tr from-[#ff4694] to-[#776fff] opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" />
    </div>

    <div class="mx-auto max-w-7xl px-6 lg:px-8 flex items-center justify-center min-h-screen">
      <div class="w-full max-w-6xl">
        <!-- 标题部分 -->
        <div class="text-center mb-16">
          <h1 class="text-5xl font-bold tracking-tight text-white sm:text-6xl mb-6">学生管理系统</h1>
          <p class="text-xl font-medium text-gray-300 max-w-2xl mx-auto">
            选择您的角色身份，开始使用高效便捷的教育管理平台
          </p>
        </div>

        <!-- 角色选择卡片 -->
        <div class="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <RouterLink
            v-for="role in roles"
            :key="role.name"
            :to="role.path"
            class="group"
          >
            <div class="relative overflow-hidden bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 transition-all duration-300 hover:scale-105 hover:bg-white/15">
              <!-- 背景渐变 -->
              <div :class="`absolute inset-0 opacity-0 group-hover:opacity-20 transition-opacity duration-300 ${role.bgColor}`"></div>

              <!-- 内容 -->
              <div class="relative z-10">
                <!-- 图标 -->
                <div class="text-6xl mb-6 text-center">{{ role.icon }}</div>

                <!-- 角色名称 -->
                <h3 class="text-2xl font-bold text-white text-center mb-4">{{ role.name }}</h3>

                <!-- 描述 -->
                <p class="text-gray-300 text-center mb-6 leading-relaxed">{{ role.description }}</p>

                <!-- 功能列表 -->
                <div class="space-y-2 mb-6">
                  <div v-for="feature in role.features" :key="feature" class="flex items-center text-gray-300 text-sm">
                    <div class="w-2 h-2 bg-current rounded-full mr-3"></div>
                    {{ feature }}
                  </div>
                </div>

                <!-- 进入按钮 -->
                <div :class="`w-full text-center py-3 px-4 rounded-lg font-semibold transition-colors duration-200 ${role.bgColor} ${role.hoverColor} text-white`">
                  进入登录
                </div>
              </div>
            </div>
          </RouterLink>
        </div>

        <!-- 底部说明 -->
        <div class="text-center mt-12">
          <p class="text-gray-400 text-sm">
            测试账号：学生(用户名2023001/密码student123) | 教师(用户名teacher001/密码teacher123) | 管理员(用户名admin/密码admin123)
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.min-h-screen {
  min-height: 100vh;
}
</style>