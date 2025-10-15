<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isLoading = ref(true)

onMounted(() => {
  // 模拟应用加载时间
  setTimeout(() => {
    isLoading.value = false
  }, 1500)
})
</script>

<template>
  <Transition
    enter-active-class="transition-opacity duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity duration-300"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="isLoading"
      class="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600"
    >
      <div class="text-center">
        <div class="mb-8">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-white/20 backdrop-blur-sm rounded-full mb-6">
            <div class="text-4xl">🎓</div>
          </div>
          <h1 class="text-3xl font-bold text-white mb-2">学生管理系统</h1>
          <p class="text-white/80">正在加载中...</p>
        </div>

        <div class="flex justify-center space-x-2">
          <div class="w-3 h-3 bg-white/80 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
          <div class="w-3 h-3 bg-white/80 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
          <div class="w-3 h-3 bg-white/80 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.animate-bounce {
  animation: bounce 1.4s infinite;
}
</style>