import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'

// API响应接口
export interface ApiResponse<T = any> {
  data: T
  message?: string
  status?: string
}

// API错误接口
export interface ApiError {
  message: string
  status?: number
  detail?: any
}

// 创建axios实例
const apiClient: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8001',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加认证token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers = config.headers || {}
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误和统一响应格式
apiClient.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    return response
  },
  (error) => {
    const apiError: ApiError = {
      message: error.response?.data?.detail || error.message || '请求失败',
      status: error.response?.status,
      detail: error.response?.data
    }

    // 处理401未授权错误
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_info')
      window.location.href = '/login'
    }

    return Promise.reject(apiError)
  }
)

export default apiClient