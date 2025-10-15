<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full text-center">
      <div class="mb-8">
        <div class="text-8xl mb-4">😕</div>
        <h1 class="text-3xl font-bold text-gray-900 mb-4">页面未找到</h1>
        <p class="text-gray-600 mb-8">抱歉，您访问的页面不存在</p>
      </div>

      <div class="space-y-4">
        <router-link
          to="/"
          class="w-full inline-block bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200"
        >
          返回首页
        </router-link>
      </div>
    </div>
  </div>
</template>