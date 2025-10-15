<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue'

const hasError = ref(false)
const errorMessage = ref('')

// 捕获子组件的错误
onErrorCaptured((err, instance, info) => {
  console.error('Error captured by boundary:', err, info)
  hasError.value = true
  errorMessage.value = err.message || '发生了一个错误'

  // 返回false阻止错误继续传播
  return false
})

const retry = () => {
  hasError.value = false
  errorMessage.value = ''
}
</script>

<template>
  <div v-if="hasError" class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full bg-white p-8 rounded-lg shadow-lg">
      <div class="text-center">
        <div class="text-6xl mb-4">⚠️</div>
        <h2 class="text-2xl font-bold text-gray-900 mb-4">出现了一个错误</h2>
        <p class="text-gray-600 mb-6">{{ errorMessage }}</p>
        <div class="space-y-3">
          <button
            @click="retry"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            重试
          </button>
          <button
            @click="() => window.location.reload()"
            class="w-full bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            刷新页面
          </button>
          <button
            @click="() => window.location.href = '/'"
            class="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            返回首页
          </button>
        </div>
      </div>
    </div>
  </div>
  <slot v-else />
</template>

<style scoped>
/* 自定义样式 */
</style>