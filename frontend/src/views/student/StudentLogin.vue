<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const studentId = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

// 真实API登录
const handleLogin = async () => {
  errorMessage.value = ''

  if (!studentId.value || !password.value) {
    errorMessage.value = '请输入学号和密码'
    return
  }

  console.log('🔐 Login attempt:', { studentId: studentId.value, password: password.value })
  isLoading.value = true

  try {
    // 调用真实API登录
    const result = await authStore.apiAuthLogin(studentId.value, password.value)

    if (result.success) {
      console.log('✅ Login successful, role:', result.role)

      // 根据角色跳转到相应的仪表板
      switch (result.role) {
        case 'student':
          router.push('/dashboard/student')
          break
        case 'teacher':
          router.push('/dashboard/teacher')
          break
        case 'admin':
          router.push('/dashboard/admin')
          break
        default:
          router.push('/dashboard/student')
      }
    }
  } catch (error: any) {
    console.error('❌ Login failed:', error)
    errorMessage.value = error.message || '登录失败，请检查用户名和密码'
  } finally {
    isLoading.value = false
  }
}

const goBack = () => {
  router.push('/')
}
</script>

<template>
  <div class="relative isolate overflow-hidden bg-gray-900 min-h-screen">
    <img src="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&crop=focalpoint&fp-y=.8&w=2830&h=1500&q=80&blend=111827&sat=-100&exp=15&blend-mode=multiply" alt="" class="absolute inset-0 -z-10 size-full object-cover object-right md:object-center" />
    <div class="hidden sm:absolute sm:-top-10 sm:right-1/2 sm:-z-10 sm:mr-10 sm:block sm:transform-gpu sm:blur-3xl" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-gradient-to-tr from-blue-500/20 to-cyan-500/20 opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" />
    </div>
    <div class="absolute -top-52 left-1/2 -z-10 -translate-x-1/2 transform-gpu blur-3xl sm:-top-112 sm:ml-16 sm:translate-x-0" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-gradient-to-tr from-blue-500/20 to-cyan-500/20 opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" />
    </div>

    <div class="mx-auto max-w-7xl px-6 lg:px-8 flex items-center justify-center min-h-screen">
      <div class="grid lg:grid-cols-2 gap-12 items-center w-full max-w-6xl">
        <!-- 左侧标题 -->
        <div class="text-center lg:text-left">
          <button
            @click="goBack"
            class="mb-6 text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-2 lg:ml-0 mx-auto lg:mx-0"
          >
            <span class="text-lg">←</span>
            <span>返回角色选择</span>
          </button>

          <div class="mb-8">
            <div class="text-6xl mb-6">👨‍🎓</div>
            <h2 class="text-5xl font-semibold tracking-tight text-white sm:text-7xl">学生登录</h2>
            <p class="mt-8 text-lg font-medium text-pretty text-gray-300 sm:text-xl/8">
              访问您的学习空间，查看课程、成绩和考试安排
            </p>
          </div>

          <!-- 功能预览 -->
          <div class="space-y-3">
            <div class="flex items-center text-gray-300">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              <span>查看个人课表和成绩</span>
            </div>
            <div class="flex items-center text-gray-300">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              <span>在线选课和退课</span>
            </div>
            <div class="flex items-center text-gray-300">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              <span>考试安排查询</span>
            </div>
            <div class="flex items-center text-gray-300">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              <span>个人信息管理</span>
            </div>
          </div>
        </div>

        <!-- 右侧登录表单 -->
        <div class="max-w-md mx-auto w-full">
          <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
            <form @submit.prevent="handleLogin" class="space-y-6">
              <!-- 错误提示 -->
              <div v-if="errorMessage" class="bg-red-500/20 border border-red-500/50 text-red-300 px-4 py-3 rounded-lg text-sm">
                {{ errorMessage }}
              </div>

              <div>
                <label for="studentId" class="block text-xl font-semibold text-white mb-3">学号</label>
                <input
                  id="studentId"
                  v-model="studentId"
                  type="text"
                  placeholder="请输入学号"
                  class="w-full px-4 py-3 text-lg bg-white/20 border border-white/30 rounded-lg text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-400 transition-all"
                  :disabled="isLoading"
                />
              </div>

              <div>
                <label for="password" class="block text-xl font-semibold text-white mb-3">密码</label>
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  placeholder="请输入密码"
                  class="w-full px-4 py-3 text-lg bg-white/20 border border-white/30 rounded-lg text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-400 transition-all"
                  :disabled="isLoading"
                />
              </div>

              <button
                type="submit"
                :disabled="isLoading"
                class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800/50 text-white text-lg font-semibold py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <span v-if="isLoading" class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>{{ isLoading ? '登录中...' : '登录' }}</span>
              </button>
            </form>

            <!-- 测试账号提示 -->
            <div class="mt-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
              <p class="text-blue-300 text-sm">
                <strong>测试账号：</strong><br>
                学生：<br>
                &nbsp;&nbsp;学号：2023001<br>
                &nbsp;&nbsp;密码：student123<br>
                教师：<br>
                &nbsp;&nbsp;工号：teacher001<br>
                &nbsp;&nbsp;密码：teacher123<br>
                管理员：<br>
                &nbsp;&nbsp;用户名：admin<br>
                &nbsp;&nbsp;密码：admin123
              </p>
            </div>
          </div>
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