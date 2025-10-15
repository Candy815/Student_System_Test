<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title?: string
  subtitle?: string
  padding?: 'none' | 'sm' | 'md' | 'lg'
  shadow?: 'none' | 'sm' | 'md' | 'lg'
  rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  border?: boolean
  hover?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  padding: 'md',
  shadow: 'sm',
  rounded: 'lg',
  border: true,
  hover: false
})

const paddingClasses = computed(() => {
  switch (props.padding) {
    case 'none':
      return ''
    case 'sm':
      return 'p-4'
    case 'lg':
      return 'p-8'
    default:
      return 'p-6'
  }
})

const shadowClasses = computed(() => {
  switch (props.shadow) {
    case 'none':
      return ''
    case 'md':
      return 'shadow-md'
    case 'lg':
      return 'shadow-lg'
    default:
      return 'shadow-sm'
  }
})

const roundedClasses = computed(() => {
  switch (props.rounded) {
    case 'none':
      return ''
    case 'sm':
      return 'rounded-sm'
    case 'md':
      return 'rounded-md'
    case 'lg':
      return 'rounded-lg'
    case 'xl':
      return 'rounded-xl'
    default:
      return 'rounded-lg'
  }
})

const cardClasses = computed(() => {
  const classes = ['bg-white', roundedClasses.value, shadowClasses.value]

  if (props.border) {
    classes.push('border', 'border-gray-200')
  }

  if (props.hover) {
    classes.push('hover:shadow-md', 'transition-shadow', 'duration-200')
  }

  return classes.join(' ')
})
</script>

<template>
  <div :class="cardClasses">
    <div v-if="title || subtitle || $slots.header" class="border-b border-gray-200">
      <slot name="header">
        <div :class="paddingClasses">
          <h3 v-if="title" class="text-lg font-semibold text-gray-900">{{ title }}</h3>
          <p v-if="subtitle" class="text-sm text-gray-600 mt-1">{{ subtitle }}</p>
        </div>
      </slot>
    </div>

    <div :class="paddingClasses">
      <slot></slot>
    </div>

    <div v-if="$slots.footer" class="border-t border-gray-200">
      <div :class="paddingClasses">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>