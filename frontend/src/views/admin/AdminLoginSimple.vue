<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('admin')
const password = ref('admin123')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  // 模拟登录验证
  setTimeout(() => {
    if (username.value === 'admin' && password.value === 'admin123') {
      try {
        // 使用auth store的adminLogin方法
        authStore.adminLogin({
          name: '系统管理员',
          username: 'admin',
          email: 'admin@system.com'
        })

        // 存储token到localStorage（用于API调用）
        localStorage.setItem('access_token', 'mock_token_' + Date.now())

        // 跳转到管理员仪表板
        router.push('/dashboard/admin')
      } catch (e) {
        console.error('登录过程中出错:', e)
        error.value = '登录过程中出错，请重试'
      }
    } else {
      error.value = '用户名或密码错误'
    }
    loading.value = false
  }, 1000)
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <span class="text-3xl">👨‍💼</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900 mb-2">管理员登录</h1>
        <p class="text-gray-600">学生管理系统</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
            placeholder="请输入用户名"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors"
            placeholder="请输入密码"
          />
        </div>

        <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
          <p class="text-red-600 text-sm">{{ error }}</p>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading">登录中...</span>
          <span v-else>登录</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-500">
          测试账号: admin / admin123
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 自定义样式 */
</style>