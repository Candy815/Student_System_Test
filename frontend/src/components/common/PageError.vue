<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title?: string
  message?: string
  code?: number | string
  showHomeButton?: boolean
  showRetryButton?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '页面出错了',
  message: '抱歉，页面加载时发生了错误',
  showHomeButton: true,
  showRetryButton: false
})

const emit = defineEmits<{
  retry: []
}>()

const errorCode = computed(() => {
  if (props.code) {
    return props.code
  }

  const codes = {
    '403': '403',
    '404': '404',
    '500': '500'
  }

  return codes[props.message] || 'Error'
})

const errorIcon = computed(() => {
  if (props.code === 404) return '🔍'
  if (props.code === 403) return '🔒'
  if (props.code === 500) return '⚠️'
  return '❌'
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full text-center">
      <div class="mb-8">
        <div class="text-8xl mb-4">{{ errorIcon }}</div>
        <div v-if="code" class="text-6xl font-bold text-gray-900 mb-2">{{ errorCode }}</div>
        <h1 class="text-2xl font-bold text-gray-900 mb-4">{{ title }}</h1>
        <p class="text-gray-600 mb-8">{{ message }}</p>
      </div>

      <div class="space-y-4">
        <button
          v-if="showRetryButton"
          @click="emit('retry')"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200"
        >
          重试
        </button>

        <router-link
          v-if="showHomeButton"
          to="/"
          class="w-full inline-block bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-3 px-4 rounded-lg transition-colors duration-200"
        >
          返回首页
        </router-link>
      </div>

      <div v-if="$slots.footer" class="mt-8">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>