<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

// 模拟登录
const handleLogin = async () => {
  errorMessage.value = ''

  if (!username.value || !password.value) {
    errorMessage.value = '请输入用户名和密码'
    return
  }

  isLoading.value = true

  // 模拟API调用延迟
  setTimeout(() => {
    // 模拟验证
    if (username.value === 'admin' && password.value === 'admin123') {
      // 登录成功，使用store管理状态
      authStore.adminLogin({
        username: username.value,
        name: '系统管理员',
        avatar: '',
        email: 'admin@university.edu.cn'
      })
      router.push('/dashboard/admin')
    } else {
      errorMessage.value = '用户名或密码错误'
    }
    isLoading.value = false
  }, 1000)
}

const goBack = () => {
  router.push('/')
}
</script>

<template>
  <div class="relative isolate overflow-hidden bg-gray-900 min-h-screen">
    <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&crop=focalpoint&fp-y=.8&w=2830&h=1500&q=80&blend=111827&sat=-100&exp=15&blend-mode=multiply" alt="" class="absolute inset-0 -z-10 size-full object-cover object-right md:object-center" />
    <div class="hidden sm:absolute sm:-top-10 sm:right-1/2 sm:-z-10 sm:mr-10 sm:block sm:transform-gpu sm:blur-3xl" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-gradient-to-tr from-purple-500/20 to-pink-500/20 opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" />
    </div>
    <div class="absolute -top-52 left-1/2 -z-10 -translate-x-1/2 transform-gpu blur-3xl sm:-top-112 sm:ml-16 sm:translate-x-0" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-gradient-to-tr from-purple-500/20 to-pink-500/20 opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" />
    </div>

    <div class="mx-auto max-w-7xl px-6 lg:px-8 flex items-center justify-center min-h-screen">
      <div class="grid lg:grid-cols-2 gap-12 items-center w-full max-w-6xl">
        <!-- 左侧标题 -->
        <div class="text-center lg:text-left">
          <button
            @click="goBack"
            class="mb-6 text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-2 lg:ml-0 mx-auto lg:mx-0"
          >
            <span class="text-lg">←</span>
            <span>返回角色选择</span>
          </button>

          <div class="mb-8">
            <div class="text-6xl mb-6">👨‍💼</div>
            <h2 class="text-5xl font-semibold tracking-tight text-white sm:text-7xl">管理员登录</h2>
            <p class="mt-8 text-lg font-medium text-pretty text-gray-300 sm:text-xl/8">
              系统管理和配置，确保平台正常运行
            </p>
          </div>

          <!-- 功能预览 -->
          <div class="space-y-3">
            <div class="flex items-center text-gray-300">
              <div class="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
              <span>用户权限管理</span>
            </div>
            <div class="flex items-center text-gray-300">
              <div class="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
              <span>系统配置管理</span>
            </div>
            <div class="flex items-center text-gray-300">
              <div class="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
              <span>数据统计分析</span>
            </div>
            <div class="flex items-center text-gray-300">
              <div class="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
              <span>系统监控和维护</span>
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
                <label for="username" class="block text-xl font-semibold text-white mb-3">用户名</label>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  placeholder="请输入用户名"
                  class="w-full px-4 py-3 text-lg bg-white/20 border border-white/30 rounded-lg text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-400 transition-all"
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
                  class="w-full px-4 py-3 text-lg bg-white/20 border border-white/30 rounded-lg text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-400 transition-all"
                  :disabled="isLoading"
                />
              </div>

              <button
                type="submit"
                :disabled="isLoading"
                class="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-purple-800/50 text-white text-lg font-semibold py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-purple-500/50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <span v-if="isLoading" class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>{{ isLoading ? '登录中...' : '登录' }}</span>
              </button>
            </form>

            <!-- 测试账号提示 -->
            <div class="mt-6 p-4 bg-purple-500/10 border border-purple-500/30 rounded-lg">
              <p class="text-purple-300 text-sm">
                <strong>测试账号：</strong><br>
                用户名：admin<br>
                密码：admin123
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