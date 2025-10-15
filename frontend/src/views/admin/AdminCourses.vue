<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { mockApi } from '@/mock_api.js'

const router = useRouter()
const useMockData = ref(false) // 是否使用模拟数据

interface Course {
  id: number
  name: string
  code: string
  teacher: string
  credits: number
  classroom: string
  schedule: string
  enrolled_students: number
  max_students: number
  is_active: boolean
  created_at: string
  teacher_id?: number
  description?: string
}

const courses = ref<Course[]>([])
const loading = ref(true)
const showEditModal = ref(false)
const editingCourse = ref<Course | null>(null)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalPages = ref(1)

const editForm = ref({
  name: '',
  code: '',
  credits: 3,
  teacher_id: '',
  classroom: '',
  schedule: '',
  max_students: 50,
  description: '',
  is_active: true
})

const teachers = ref([])

// 获取课程列表
const fetchCourses = async () => {
  try {
    loading.value = true

    if (useMockData.value) {
      // 使用模拟数据
      const data = await mockApi.getCourses(currentPage.value, pageSize.value)
      courses.value = data.courses
      totalPages.value = data.total_pages
      return
    }

    const response = await fetch(`/api/admin/courses?page=${currentPage.value}&page_size=${pageSize.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      courses.value = data.courses
      totalPages.value = data.total_pages
    } else {
      console.error('获取课程列表失败')
      // 切换到模拟数据
      useMockData.value = true
      await fetchCourses()
    }
  } catch (error) {
    console.error('获取课程列表时出错:', error)
    // 网络错误时切换到模拟数据
    useMockData.value = true
    await fetchCourses()
  } finally {
    loading.value = false
  }
}

// 获取教师列表
const fetchTeachers = async () => {
  try {
    if (useMockData.value) {
      // 使用模拟数据
      const data = await mockApi.getTeachers()
      teachers.value = data.users
      return
    }

    const response = await fetch('/api/admin/users?role=teacher', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      teachers.value = data.users
    } else {
      // 切换到模拟数据
      useMockData.value = true
      await fetchTeachers()
    }
  } catch (error) {
    console.error('获取教师列表时出错:', error)
    // 网络错误时切换到模拟数据
    useMockData.value = true
    await fetchTeachers()
  }
}

// 打开编辑模态框
const openEditModal = (course: Course) => {
  editingCourse.value = course
  editForm.value = {
    name: course.name,
    code: course.code,
    credits: course.credits,
    teacher_id: course.teacher_id?.toString() || '',
    classroom: course.classroom || '',
    schedule: course.schedule || '',
    max_students: course.max_students,
    description: course.description || '',
    is_active: course.is_active
  }
  showEditModal.value = true
}

// 关闭编辑模态框
const closeEditModal = () => {
  showEditModal.value = false
  editingCourse.value = null
}

// 保存课程编辑
const saveCourseEdit = async () => {
  if (!editingCourse.value) return

  try {
    if (useMockData.value) {
      // 使用模拟数据
      await mockApi.updateCourse(editingCourse.value.id, editForm.value)
      await fetchCourses()
      closeEditModal()
      return
    }

    const response = await fetch(`/api/admin/courses/${editingCourse.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(editForm.value)
    })

    if (response.ok) {
      await fetchCourses()
      closeEditModal()
    } else {
      console.error('保存课程编辑失败')
      // 切换到模拟数据
      useMockData.value = true
      await saveCourseEdit()
    }
  } catch (error) {
    console.error('保存课程编辑时出错:', error)
    // 网络错误时切换到模拟数据
    useMockData.value = true
    await saveCourseEdit()
  }
}

// 搜索课程
const searchCourses = () => {
  currentPage.value = 1
  fetchCourses()
}

// 切换课程状态
const toggleCourseStatus = async (course: Course) => {
  try {
    if (useMockData.value) {
      // 使用模拟数据
      await mockApi.toggleCourseStatus(course.id)
      await fetchCourses()
      return
    }

    const response = await fetch(`/api/admin/courses/${course.id}/toggle-status`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })

    if (response.ok) {
      await fetchCourses()
    } else {
      console.error('切换课程状态失败')
      // 切换到模拟数据
      useMockData.value = true
      await toggleCourseStatus(course)
    }
  } catch (error) {
    console.error('切换课程状态时出错:', error)
    // 网络错误时切换到模拟数据
    useMockData.value = true
    await toggleCourseStatus(course)
  }
}

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 计算课程状态
const getCourseStatus = (course: Course) => {
  const enrollmentRate = (course.enrolled_students / course.max_students) * 100
  if (enrollmentRate >= 90) return { text: '即将满员', color: 'bg-red-100 text-red-800' }
  if (enrollmentRate >= 70) return { text: '名额紧张', color: 'bg-yellow-100 text-yellow-800' }
  return { text: '名额充足', color: 'bg-green-100 text-green-800' }
}

// 分页处理
const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchCourses()
}

onMounted(() => {
  fetchCourses()
  fetchTeachers()
})
</script>

<template>
  <div class="space-y-6">
    <!-- 页面标题和操作栏 -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">课程管理</h1>
        <p class="text-gray-600">管理系统中的所有课程信息</p>
      </div>
      <div class="flex space-x-4">
        <div class="relative">
          <input
            v-model="searchQuery"
            @keyup.enter="searchCourses"
            type="text"
            placeholder="搜索课程名称或代码..."
            class="w-64 pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
          <div class="absolute left-3 top-2.5">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 课程列表 -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="p-6 border-b border-gray-200 flex justify-between items-center">
        <h2 class="text-lg font-semibold text-gray-900">课程列表</h2>
        <div v-if="useMockData" class="flex items-center text-sm text-yellow-600 bg-yellow-50 px-3 py-1 rounded-full">
          <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
          使用模拟数据
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">课程信息</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">任课教师</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">学分/教室</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">上课时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">选课情况</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="course in courses" :key="course.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ course.name }}</div>
                  <div class="text-sm text-gray-500">{{ course.code }}</div>
                  <div class="text-xs text-gray-400 mt-1">{{ formatDate(course.created_at) }}</div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">{{ course.teacher }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">{{ course.credits }}学分</div>
                <div class="text-sm text-gray-500">{{ course.classroom || '未分配' }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">{{ course.schedule || '未安排' }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">
                  {{ course.enrolled_students }}/{{ course.max_students }}
                </div>
                <div class="mt-1">
                  <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                        :class="getCourseStatus(course).color">
                    {{ getCourseStatus(course).text }}
                  </span>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                      :class="course.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                  {{ course.is_active ? '启用' : '停用' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex space-x-2">
                  <button
                    @click="openEditModal(course)"
                    class="text-blue-600 hover:text-blue-900 text-sm font-medium"
                  >
                    编辑
                  </button>
                  <button
                    @click="toggleCourseStatus(course)"
                    class="text-purple-600 hover:text-purple-900 text-sm font-medium"
                  >
                    {{ course.is_active ? '停用' : '启用' }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
        <div class="flex-1 flex justify-between sm:hidden">
          <button
            @click="handlePageChange(currentPage - 1)"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            上一页
          </button>
          <button
            @click="handlePageChange(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            下一页
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              显示第 <span class="font-medium">{{ (currentPage - 1) * pageSize + 1 }}</span> 到
              <span class="font-medium">{{ Math.min(currentPage * pageSize, courses.length) }}</span> 条，
              共 <span class="font-medium">{{ courses.length }}</span> 条记录
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
              <button
                @click="handlePageChange(currentPage - 1)"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
              >
                <span class="sr-only">上一页</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
              <button
                v-for="page in Math.min(totalPages, 5)"
                :key="page"
                @click="handlePageChange(page)"
                :class="currentPage === page ? 'z-10 bg-purple-50 border-purple-500 text-purple-600' : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'"
                class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
              >
                {{ page }}
              </button>
              <button
                @click="handlePageChange(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
              >
                <span class="sr-only">下一页</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑课程模态框 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900">编辑课程</h3>
            <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <form @submit.prevent="saveCourseEdit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">课程名称</label>
              <input
                v-model="editForm.name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">课程代码</label>
              <input
                v-model="editForm.code"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">学分</label>
                <input
                  v-model.number="editForm.credits"
                  type="number"
                  min="1"
                  max="10"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">最大学生数</label>
                <input
                  v-model.number="editForm.max_students"
                  type="number"
                  min="1"
                  max="500"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">任课教师</label>
              <select
                v-model="editForm.teacher_id"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="">未分配</option>
                <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
                  {{ teacher.full_name }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">教室</label>
              <input
                v-model="editForm.classroom"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">上课时间</label>
              <input
                v-model="editForm.schedule"
                type="text"
                placeholder="例如：周一 9:00-11:00"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">课程描述</label>
              <textarea
                v-model="editForm.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              ></textarea>
            </div>

            <div class="flex items-center">
              <input
                v-model="editForm.is_active"
                type="checkbox"
                class="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
              />
              <label class="ml-2 block text-sm text-gray-900">启用课程</label>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeEditModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 rounded-md"
              >
                保存
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 自定义样式 */
</style>