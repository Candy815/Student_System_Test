<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const isSidebarOpen = ref(false)

// 使用store中的用户信息
const userInfo = computed(() => {
  console.log('🔍 Layout userInfo computed:', authStore.userInfo)
  return authStore.userInfo || {}
})
const userRole = computed(() => {
  console.log('🔍 Layout userRole computed:', authStore.userRole)
  return authStore.userRole || ''
})

// 角色主题色 - 使用Tailwind CSS类名
const themeClasses = computed(() => {
  switch (userRole.value) {
    case 'student':
      return {
        gradient: 'from-blue-600 to-blue-700',
        bg: 'bg-blue-600',
        hover: 'hover:bg-blue-700',
        active: 'bg-blue-600 text-white',
        border: 'border-blue-500'
      }
    case 'teacher':
      return {
        gradient: 'from-green-600 to-green-700',
        bg: 'bg-green-600',
        hover: 'hover:bg-green-700',
        active: 'bg-green-600 text-white',
        border: 'border-green-500'
      }
    case 'admin':
      return {
        gradient: 'from-purple-600 to-purple-700',
        bg: 'bg-purple-600',
        hover: 'hover:bg-purple-700',
        active: 'bg-purple-600 text-white',
        border: 'border-purple-500'
      }
    default:
      return {
        gradient: 'from-gray-600 to-gray-700',
        bg: 'bg-gray-600',
        hover: 'hover:bg-gray-700',
        active: 'bg-gray-600 text-white',
        border: 'border-gray-500'
      }
  }
})

// 侧边栏菜单项
const menuItems = computed(() => {
  console.log('🔍 Layout menuItems computed, userRole:', userRole.value)
  switch (userRole.value) {
    case 'student':
      return [
        { name: '首页', icon: '🏠', path: '/dashboard/student' },
        { name: '个人课表', icon: '📅', path: '/dashboard/student/schedule' },
        { name: '成绩查询', icon: '📊', path: '/dashboard/student/grades' },
        { name: '选课系统', icon: '📚', path: '/dashboard/student/courses' },
        { name: '考试安排', icon: '📝', path: '/dashboard/student/exams' },
        { name: 'AI助手', icon: '🤖', path: '/dashboard/student/ai-assistant' },
        { name: '个人信息', icon: '👤', path: '/dashboard/student/profile' }
      ]
    case 'teacher':
      return [
        { name: '首页', icon: '🏠', path: '/dashboard/teacher' },
        { name: '课程管理', icon: '📚', path: '/dashboard/teacher/courses' },
        { name: '成绩录入', icon: '📊', path: '/dashboard/teacher/grades' },
        { name: '学生名单', icon: '👥', path: '/dashboard/teacher/students' },
        { name: '考勤管理', icon: '✅', path: '/dashboard/teacher/attendance' },
        { name: '好友管理', icon: '👥', path: '/dashboard/teacher/friends' },
        { name: '个人中心', icon: '👤', path: '/dashboard/teacher/profile' }
      ]
    case 'admin':
      return [
        { name: '首页', icon: '🏠', path: '/dashboard/admin' },
        { name: '用户管理', icon: '👥', path: '/dashboard/admin/users' },
        { name: '课程管理', icon: '📚', path: '/dashboard/admin/courses' },
        { name: '角色权限', icon: '🔐', path: '/dashboard/admin/roles' },
        { name: '系统设置', icon: '⚙️', path: '/dashboard/admin/settings' },
        { name: '数据统计', icon: '📈', path: '/dashboard/admin/analytics' },
        { name: '系统日志', icon: '📋', path: '/dashboard/admin/logs' }
      ]
    default:
      return []
  }
})

// 退出登录
const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

// 切换侧边栏
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- 移动端遮罩 -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-black/50 z-40 lg:hidden"
      @click="toggleSidebar"
    ></div>

    <!-- 侧边栏 -->
    <div
      :class="[
        'fixed lg:static inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      ]"
    >
      <!-- 侧边栏头部 -->
      <div :class="`bg-gradient-to-r ${themeClasses.gradient} p-6`">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <span class="text-white text-xl">
                {{ userRole === 'student' ? '👨‍🎓' : userRole === 'teacher' ? '👨‍🏫' : '👨‍💼' }}
              </span>
            </div>
            <div>
              <h3 class="text-white font-semibold">{{ userInfo.name || '用户' }}</h3>
              <p class="text-white/80 text-sm">
                {{ userRole === 'student' ? '学生' : userRole === 'teacher' ? '教师' : '管理员' }}
              </p>
            </div>
          </div>
          <button
            @click="toggleSidebar"
            class="lg:hidden text-white hover:bg-white/20 p-2 rounded-lg"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- 菜单列表 -->
      <nav class="p-4 space-y-1">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          :class="[
            'flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors duration-200',
            route.path === item.path
              ? themeClasses.active
              : 'text-gray-700 hover:bg-gray-100'
          ]"
          @click="isSidebarOpen = false"
        >
          <span class="text-xl">{{ item.icon }}</span>
          <span class="font-medium">{{ item.name }}</span>
        </router-link>
      </nav>

      <!-- 退出按钮 -->
      <div class="absolute bottom-4 left-4 right-4">
        <button
          @click="handleLogout"
          class="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200"
        >
          <span>🚪</span>
          <span>退出登录</span>
        </button>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- 顶部导航栏 -->
      <header class="bg-white shadow-sm border-b border-gray-200">
        <div class="px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <!-- 移动端菜单按钮 -->
            <button
              @click="toggleSidebar"
              class="lg:hidden text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100"
            >
              ☰
            </button>

            <!-- 页面标题 -->
            <h1 class="text-xl font-semibold text-gray-900">
              {{ menuItems.find(item => item.path === route.path)?.name || '首页' }}
            </h1>
          </div>

          <!-- 用户信息 -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                <span class="text-sm">
                  {{ userRole === 'student' ? '👨‍🎓' : userRole === 'teacher' ? '👨‍🏫' : '👨‍💼' }}
                </span>
              </div>
              <span class="text-sm font-medium text-gray-700 hidden sm:block">
                {{ userInfo.name || '用户' }}
              </span>
            </div>
          </div>
        </div>
      </header>

      <!-- 主要内容 -->
      <main class="flex-1 overflow-auto p-4 sm:p-6 lg:p-8">
        <div v-if="!userRole" class="text-center py-8">
          <div class="text-xl text-gray-600">正在加载用户信息...</div>
        </div>
        <router-view v-else />
      </main>
    </div>
  </div>
</template>

<style scoped>
/* 自定义滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>