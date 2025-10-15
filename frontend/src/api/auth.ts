import apiClient, { type ApiResponse } from './index'

// 用户信息接口
export interface UserInfo {
  id: number
  username: string
  email: string
  full_name: string
  role: 'guest' | 'student' | 'teacher' | 'admin'
  student_id?: string
  class_name?: string
  teacher_id?: string
  department?: string
  title?: string
}

// 登录请求参数
export interface LoginRequest {
  username: string
  password: string
}

// 登录响应
export interface LoginResponse {
  access_token: string
  token_type: string
  user: UserInfo
}

// 注册请求参数
export interface RegisterRequest {
  username: string
  email: string
  password: string
  full_name: string
  role: string
}

// 登录API
export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('password', data.password)

  const response = await apiClient.post<LoginResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
  return response.data
}

// 注册API
export const register = async (data: RegisterRequest): Promise<{ message: string; user_id: number }> => {
  const response = await apiClient.post<ApiResponse<{ message: string; user_id: number }>>('/auth/register', data)
  return response.data.data
}

// 获取当前用户信息
export const getCurrentUser = async (): Promise<UserInfo> => {
  const response = await apiClient.get<UserInfo>('/auth/me')
  return response.data
}

// 升级角色请求参数
export interface UpgradeRequest {
  target_role: string
  student_id?: string
  teacher_id?: string
  class_name?: string
  department?: string
  title?: string
}

// 升级角色响应
export interface UpgradeResponse {
  message: string
  request_id: number
}

// 升级角色API
export const upgradeRole = async (data: UpgradeRequest): Promise<UpgradeResponse> => {
  const response = await apiClient.post<ApiResponse<UpgradeResponse>>('/auth/upgrade-role', data)
  return response.data.data
}

// 获取我的升级请求
export const getMyUpgradeRequest = async (): Promise<{ has_request: boolean; request?: any }> => {
  const response = await apiClient.get<ApiResponse<{ has_request: boolean; request?: any }>>('/auth/my-upgrade-request')
  return response.data.data
}

// 管理员获取所有升级请求
export const getUpgradeRequests = async (): Promise<any[]> => {
  const response = await apiClient.get<ApiResponse<any[]>>('/auth/upgrade-requests')
  return response.data.data
}

// 管理员批准升级请求
export const approveUpgrade = async (requestId: number): Promise<{ message: string }> => {
  const response = await apiClient.post<ApiResponse<{ message: string }>>(`/auth/approve-upgrade/${requestId}`)
  return response.data.data
}

// 管理员拒绝升级请求
export const rejectUpgrade = async (requestId: number, rejectionReason: string): Promise<{ message: string }> => {
  const response = await apiClient.post<ApiResponse<{ message: string }>>(`/auth/reject-upgrade/${requestId}`, {
    rejection_reason: rejectionReason
  })
  return response.data.data
}