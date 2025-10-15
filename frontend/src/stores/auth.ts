import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, getCurrentUser, type UserInfo as ApiUserInfo, type LoginResponse } from '../api/auth'

export interface UserInfo {
  studentId?: string
  teacherId?: string
  username?: string
  name?: string
  className?: string
  department?: string
  title?: string
  role?: string
  permissions?: string[]
  avatar?: string
  email?: string
}

export interface AuthState {
  userRole: 'student' | 'teacher' | 'admin' | null
  userInfo: UserInfo | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', () => {
  console.log('🏪 Auth store is being initialized')

  // 状态
  const userRole = ref<'student' | 'teacher' | 'admin' | null>(null)
  const userInfo = ref<UserInfo | null>(null)
  const isAuthenticated = ref(false)

  // 计算属性
  const isStudent = computed(() => userRole.value === 'student')
  const isTeacher = computed(() => userRole.value === 'teacher')
  const isAdmin = computed(() => userRole.value === 'admin')
  const displayName = computed(() => userInfo.value?.name || '用户')

  // 初始化状态（从localStorage读取）
  const initializeAuth = () => {
    const storedToken = localStorage.getItem('access_token')
    const storedRole = localStorage.getItem('userRole') as 'student' | 'teacher' | 'admin' | null
    const storedUserInfo = localStorage.getItem('userInfo')

    console.log('🔍 localStorage check:', {
      storedToken: storedToken ? 'exists' : 'null',
      storedRole,
      storedUserInfo: storedUserInfo ? 'exists' : 'null'
    })

    if (storedToken && storedRole && storedUserInfo) {
      userRole.value = storedRole
      userInfo.value = JSON.parse(storedUserInfo)
      isAuthenticated.value = true
      console.log('✅ Auth initialized:', { userRole: userRole.value, userInfo: userInfo.value })
    } else {
      console.log('❌ No auth data found in localStorage')
    }
  }

  // 学生登录
  const studentLogin = (studentData: Omit<UserInfo, 'role' | 'permissions'>) => {
    userRole.value = 'student'
    userInfo.value = {
      ...studentData,
      role: 'student',
      permissions: ['view_grades', 'select_courses', 'view_schedule', 'view_exams', 'edit_profile', 'access_ai']
    }
    isAuthenticated.value = true

    // 保存到localStorage
    console.log('💾 Saving to localStorage:', {
      userRole: 'student',
      userInfo: userInfo.value
    })
    localStorage.setItem('userRole', 'student')
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
    console.log('✅ localStorage save completed')
  }

  // 教师登录
  const teacherLogin = (teacherData: Omit<UserInfo, 'role' | 'permissions'>) => {
    userRole.value = 'teacher'
    userInfo.value = {
      ...teacherData,
      role: 'teacher',
      permissions: ['manage_courses', 'input_grades', 'view_students', 'manage_attendance', 'edit_profile']
    }
    isAuthenticated.value = true

    // 保存到localStorage
    localStorage.setItem('userRole', 'teacher')
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
  }

  // 管理员登录
  const adminLogin = (adminData: Omit<UserInfo, 'role' | 'permissions'>) => {
    userRole.value = 'admin'
    userInfo.value = {
      ...adminData,
      role: 'admin',
      permissions: ['all']
    }
    isAuthenticated.value = true

    // 保存到localStorage
    localStorage.setItem('userRole', 'admin')
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
  }

  // 真实API登录
  const apiAuthLogin = async (username: string, password: string) => {
    try {
      console.log('🔐 Attempting API login:', { username })

      // 调用登录API
      const response: LoginResponse = await apiLogin({ username, password })

      console.log('✅ API login successful:', response)

      // 保存token
      localStorage.setItem('access_token', response.access_token)

      // 根据角色设置用户信息
      const apiUser = response.user
      let role: 'student' | 'teacher' | 'admin' = apiUser.role

      // 转换API用户信息到本地格式
      const localUserInfo: UserInfo = {
        name: apiUser.full_name,
        email: apiUser.email,
        username: apiUser.username,
        role: apiUser.role,
        avatar: '',
      }

      // 根据角色添加特定信息
      if (role === 'student' && apiUser.student_id) {
        localUserInfo.studentId = apiUser.student_id
        localUserInfo.className = apiUser.class_name || ''
        localUserInfo.permissions = ['view_grades', 'select_courses', 'view_schedule', 'view_exams', 'edit_profile', 'access_ai']
      } else if (role === 'teacher' && apiUser.teacher_id) {
        localUserInfo.teacherId = apiUser.teacher_id
        localUserInfo.department = apiUser.department || ''
        localUserInfo.title = apiUser.title || ''
        localUserInfo.permissions = ['manage_courses', 'input_grades', 'view_students', 'manage_attendance', 'edit_profile']
      } else if (role === 'admin') {
        localUserInfo.permissions = ['all']
      }

      // 更新store状态
      userRole.value = role
      userInfo.value = localUserInfo
      isAuthenticated.value = true

      // 保存到localStorage
      localStorage.setItem('userRole', role)
      localStorage.setItem('userInfo', JSON.stringify(localUserInfo))

      console.log('✅ Auth state updated successfully')
      return { success: true, role }

    } catch (error: any) {
      console.error('❌ API login failed:', error)
      throw error
    }
  }

  // 登出
  const logout = () => {
    userRole.value = null
    userInfo.value = null
    isAuthenticated.value = false

    // 清除localStorage
    localStorage.removeItem('access_token')
    localStorage.removeItem('userRole')
    localStorage.removeItem('userInfo')
  }

  // 更新用户信息
  const updateUserInfo = (newUserInfo: Partial<UserInfo>) => {
    if (userInfo.value) {
      userInfo.value = { ...userInfo.value, ...newUserInfo }
      localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
    }
  }

  // 检查权限
  const hasPermission = (permission: string): boolean => {
    if (!userInfo.value || !userInfo.value.permissions) return false
    return userInfo.value.permissions.includes('all') || userInfo.value.permissions.includes(permission)
  }

  // 获取主题色
  const getThemeColors = () => {
    switch (userRole.value) {
      case 'student':
        return {
          primary: 'blue',
          hover: 'hover:bg-blue-700',
          bg: 'bg-blue-600',
          gradient: 'from-blue-600 to-blue-700'
        }
      case 'teacher':
        return {
          primary: 'green',
          hover: 'hover:bg-green-700',
          bg: 'bg-green-600',
          gradient: 'from-green-600 to-green-700'
        }
      case 'admin':
        return {
          primary: 'purple',
          hover: 'hover:bg-purple-700',
          bg: 'bg-purple-600',
          gradient: 'from-purple-600 to-purple-700'
        }
      default:
        return {
          primary: 'gray',
          hover: 'hover:bg-gray-700',
          bg: 'bg-gray-600',
          gradient: 'from-gray-600 to-gray-700'
        }
    }
  }

  return {
    // 状态
    userRole,
    userInfo,
    isAuthenticated,

    // 计算属性
    isStudent,
    isTeacher,
    isAdmin,
    displayName,

    // 方法
    initializeAuth,
    studentLogin,
    teacherLogin,
    adminLogin,
    apiAuthLogin,
    logout,
    updateUserInfo,
    hasPermission,
    getThemeColors
  }
})