<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async (e: Event) => {
  e.preventDefault()

  if (!username.value || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  error.value = ''

  try {
    // 使用auth store的登录方法
    const result = await authStore.apiAuthLogin(username.value, password.value)

    if (result.success) {
      // 根据用户角色跳转到对应的仪表板
      const dashboardPath = `/dashboard/${result.role}`
      router.push(dashboardPath)
    }

  } catch (err: any) {
    error.value = err.response?.data?.message || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="relative isolate overflow-hidden bg-gray-900 min-h-screen">
    <img src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&crop=focalpoint&fp-y=.8&w=2830&h=1500&q=80&blend=111827&sat=-100&exp=15&blend-mode=multiply" alt="" class="absolute inset-0 -z-10 size-full object-cover object-right md:object-center" />
    <div class="hidden sm:absolute sm:-top-10 sm:right-1/2 sm:-z-10 sm:mr-10 sm:block sm:transform-gpu sm:blur-3xl" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-linear-to-tr from-[#ff4694] to-[#776fff] opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" />
    </div>
    <div class="absolute -top-52 left-1/2 -z-10 -translate-x-1/2 transform-gpu blur-3xl sm:-top-112 sm:ml-16 sm:translate-x-0" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-linear-to-tr from-[#ff4694] to-[#776fff] opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" />
    </div>

    <div class="mx-auto max-w-7xl px-6 lg:px-8 flex items-center justify-center min-h-screen">
      <div class="grid lg:grid-cols-2 gap-12 items-center w-full max-w-6xl">
        <!-- 左侧标题 -->
        <div class="text-center lg:text-left">
          <h2 class="text-5xl font-semibold tracking-tight text-white sm:text-7xl">学生管理系统</h2>
          <p class="mt-8 text-lg font-medium text-pretty text-gray-300 sm:text-xl/8">
            高效管理学生信息，提供全面的教育数据支持
          </p>
        </div>

        <!-- 右侧登录表单 -->
        <div class="max-w-md mx-auto w-full">
          <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
            <!-- 错误消息 -->
            <div v-if="error" class="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
              <p class="text-red-200 text-center">{{ error }}</p>
            </div>

            <form @submit="handleLogin" class="space-y-6">
              <div>
                <label for="username" class="block text-xl font-semibold text-white mb-3">用户名</label>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  placeholder="请输入用户名"
                  class="w-full px-4 py-3 text-lg bg-white/20 border border-white/30 rounded-lg text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-400 transition-all"
                  :disabled="loading"
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
                  :disabled="loading"
                />
              </div>

              <button
                type="submit"
                class="w-full bg-blue-600 hover:bg-blue-700 text-white text-lg font-semibold py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="loading"
              >
                {{ loading ? '登录中...' : '登录' }}
              </button>
            </form>

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