<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  isTyping?: boolean
}

const messages = ref<ChatMessage[]>([])
const userInput = ref('')
const isLoading = ref(false)
const chatContainer = ref<HTMLElement>()
const showColorPicker = ref(false)
const currentTheme = ref('default')
const backgroundColor = ref('#1a1a2e')
const textColor = ref('#ffffff')
const accentColor = ref('#16213e')

const themes = computed(() => [
  { id: 'default', name: '经典蓝色', bgColor: '#1a1a2e', textColor: '#ffffff', accentColor: '#16213e' },
  { id: 'green', name: '护眼绿色', bgColor: '#0f3443', textColor: '#e8e8e8', accentColor: '#34e89e' },
  { id: 'purple', name: '优雅紫色', bgColor: '#2d1b69', textColor: '#ffffff', accentColor: '#9d50bb' },
  { id: 'warm', name: '暖色护眼', bgColor: '#3e2723', textColor: '#fff3e0', accentColor: '#ff8a65' },
  { id: 'minimal', name: '简约白色', bgColor: '#f5f5f5', textColor: '#333333', accentColor: '#2196f3' }
])

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const handleSendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  // 添加用户消息
  const userMessage: ChatMessage = {
    id: Date.now().toString(),
    role: 'user',
    content: userInput.value,
    timestamp: new Date()
  }
  messages.value.push(userMessage)

  const userQuestion = userInput.value
  userInput.value = ''
  isLoading.value = true

  // 添加AI回复消息（占位）
  const aiMessage: ChatMessage = {
    id: (Date.now() + 1).toString(),
    role: 'assistant',
    content: '',
    timestamp: new Date(),
    isTyping: true
  }
  messages.value.push(aiMessage)

  await scrollToBottom()

  try {
    // 调用AI服务
    const response = await fetch('http://localhost:8000/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userQuestion }),
    })

    if (!response.ok) {
      throw new Error('网络请求失败')
    }

    const data = await response.json()

    // 更新AI回复
    const aiMessageIndex = messages.value.findIndex(msg => msg.id === aiMessage.id)
    if (aiMessageIndex !== -1) {
      messages.value[aiMessageIndex].content = data.response
      messages.value[aiMessageIndex].isTyping = false
    }
  } catch (error) {
    console.error('AI回复失败:', error)
    const aiMessageIndex = messages.value.findIndex(msg => msg.id === aiMessage.id)
    if (aiMessageIndex !== -1) {
      messages.value[aiMessageIndex].content = '抱歉，AI助手暂时无法回复，请稍后再试。'
      messages.value[aiMessageIndex].isTyping = false
    }
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

const handleKeyPress = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSendMessage()
  }
}

const applyTheme = (theme: any) => {
  backgroundColor.value = theme.bgColor
  textColor.value = theme.textColor
  accentColor.value = theme.accentColor
  currentTheme.value = theme.id
  showColorPicker.value = false
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 初始化主题
applyTheme(themes.value[0])
</script>

<template>
  <div
    class="flex flex-col h-full rounded-xl shadow-xl overflow-hidden transition-all duration-300"
    :style="{ backgroundColor: backgroundColor, color: textColor }"
  >
    <!-- 头部 -->
    <div class="p-4 border-b flex items-center justify-between" :style="{ borderColor: accentColor }">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full flex items-center justify-center animate-pulse" :style="{ backgroundColor: accentColor }">
          <span class="text-xl">🤖</span>
        </div>
        <div>
          <h3 class="font-semibold text-lg">AI学习助手</h3>
          <p class="text-sm opacity-75">随时为您解答学习问题</p>
        </div>
      </div>

      <!-- 颜色模式切换按钮 -->
      <div class="relative">
        <button
          @click="showColorPicker = !showColorPicker"
          class="p-2 rounded-lg hover:bg-white/10 transition-colors"
          :style="{ backgroundColor: accentColor }"
        >
          <span class="text-lg">🎨</span>
        </button>

        <!-- 颜色选择器 -->
        <div
          v-if="showColorPicker"
          class="absolute right-0 top-full mt-2 bg-white/95 backdrop-blur-sm rounded-lg shadow-xl p-3 z-50 border"
          :style="{ borderColor: accentColor }"
        >
          <div class="grid grid-cols-2 gap-2 min-w-[200px]">
            <button
              v-for="theme in themes"
              :key="theme.id"
              @click="applyTheme(theme)"
              class="p-2 rounded-lg text-xs font-medium transition-all hover:scale-105 border"
              :class="{ 'ring-2 ring-white': currentTheme === theme.id }"
              :style="{
                backgroundColor: theme.bgColor,
                color: theme.textColor,
                borderColor: theme.accentColor
              }"
            >
              {{ theme.name }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 聊天内容区域 -->
    <div
      ref="chatContainer"
      class="flex-1 overflow-y-auto p-4 space-y-4"
      :style="{ backgroundColor: backgroundColor + '20' }"
    >
      <!-- 欢迎消息 -->
      <div v-if="messages.length === 0" class="text-center py-8">
        <div class="text-6xl mb-4">👋</div>
        <h4 class="text-xl font-semibold mb-2">欢迎使用AI学习助手！</h4>
        <p class="opacity-75">您可以向我询问任何学习相关的问题，我会尽力为您解答。</p>
        <div class="mt-4 space-y-2 text-sm opacity-60">
          <p>💡 您可以尝试询问：</p>
          <p>• 课程相关的问题</p>
          <p>• 学习方法和建议</p>
          <p>• 考试准备技巧</p>
        </div>
      </div>

      <!-- 消息列表 -->
      <div
        v-for="message in messages"
        :key="message.id"
        class="flex gap-3 animate-fade-in"
        :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <!-- AI头像 -->
        <div
          v-if="message.role === 'assistant'"
          class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0"
          :style="{ backgroundColor: accentColor }"
        >
          <span class="text-sm">🤖</span>
        </div>

        <!-- 消息内容 -->
        <div
          class="max-w-[80%] rounded-2xl px-4 py-3 break-words"
          :class="[
            message.role === 'user'
              ? 'rounded-br-sm'
              : 'rounded-bl-sm',
          ]"
          :style="{
            backgroundColor: message.role === 'user' ? accentColor : (backgroundColor + '40'),
            color: message.role === 'user' ? '#ffffff' : textColor
          }"
        >
          <div class="whitespace-pre-wrap text-sm leading-relaxed">
            <span v-if="message.isTyping" class="flex items-center space-x-1">
              <span class="w-2 h-2 bg-current rounded-full animate-bounce"></span>
              <span class="w-2 h-2 bg-current rounded-full animate-bounce" style="animation-delay: 0.1s"></span>
              <span class="w-2 h-2 bg-current rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
            </span>
            <span v-else>{{ message.content }}</span>
          </div>
          <div class="text-xs mt-2 opacity-60">
            {{ formatTime(message.timestamp) }}
          </div>
        </div>

        <!-- 用户头像 -->
        <div
          v-if="message.role === 'user'"
          class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 bg-blue-500"
        >
          <span class="text-sm">👤</span>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="p-4 border-t" :style="{ borderColor: accentColor }">
      <div class="flex gap-2">
        <textarea
          v-model="userInput"
          @keydown="handleKeyPress"
          :disabled="isLoading"
          placeholder="输入您的问题..."
          class="flex-1 resize-none rounded-lg px-4 py-3 text-sm leading-relaxed focus:outline-none focus:ring-2 transition-all"
          :style="{
            backgroundColor: backgroundColor + '60',
            color: textColor,
            borderColor: accentColor,
            borderWidth: '1px'
          }"
          rows="1"
        ></textarea>
        <button
          @click="handleSendMessage"
          :disabled="isLoading || !userInput.trim()"
          class="px-6 py-3 rounded-lg font-medium transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
          :style="{ backgroundColor: accentColor, color: textColor }"
        >
          <span v-if="isLoading" class="flex items-center space-x-1">
            <span class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <span>发送中</span>
          </span>
          <span v-else>发送</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}

textarea:focus {
  box-shadow: 0 0 0 3px v-bind('accentColor + "40"');
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>