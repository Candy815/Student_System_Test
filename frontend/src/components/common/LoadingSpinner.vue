<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'sm' | 'md' | 'lg'
  color?: 'white' | 'primary'
  text?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  color: 'white',
  text: ''
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-4 h-4'
    case 'lg':
      return 'w-8 h-8'
    default:
      return 'w-6 h-6'
  }
})

const colorClasses = computed(() => {
  switch (props.color) {
    case 'primary':
      return 'border-blue-600 border-t-transparent'
    default:
      return 'border-white border-t-transparent'
  }
})
</script>

<template>
  <div class="flex items-center justify-center space-x-2">
    <div
      :class="[
        'animate-spin rounded-full border-2',
        sizeClasses,
        colorClasses
      ]"
    ></div>
    <span v-if="text" class="text-white">{{ text }}</span>
  </div>
</template>