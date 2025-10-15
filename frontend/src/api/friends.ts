import apiClient from './index'

// 用户搜索响应接口
export interface UserSearchResponse {
  id: number
  name: string
  email: string
  role: string
  student_id?: string
  teacher_id?: string
  department?: string
  title?: string
  class_name?: string
}

// 好友请求接口
export interface FriendRequest {
  id: number
  sender_id: number
  receiver_id: number
  status: string
  message?: string
  created_at: string
  sender_name: string
  sender_role: string
  receiver_name: string
}

// 好友信息接口
export interface Friend {
  id: number
  user_id: number
  name: string
  email: string
  role: string
  student_id?: string
  teacher_id?: string
  department?: string
  title?: string
  class_name?: string
  friendship_since: string
}

// 发送好友请求参数
export interface FriendRequestCreate {
  receiver_id: number
  message?: string
}

// 搜索用户
export const searchUsers = async (query: string): Promise<UserSearchResponse[]> => {
  const response = await apiClient.get<UserSearchResponse[]>('/friends/search', {
    params: { q: query }
  })
  return response.data
}

// 发送好友请求
export const sendFriendRequest = async (data: FriendRequestCreate): Promise<{ message: string; request_id: number }> => {
  const response = await apiClient.post<{ message: string; request_id: number }>('/friends/request', data)
  return response.data
}

// 获取发送的好友请求
export const getSentRequests = async (): Promise<FriendRequest[]> => {
  const response = await apiClient.get<FriendRequest[]>('/friends/requests/sent')
  return response.data
}

// 获取收到的好友请求
export const getReceivedRequests = async (): Promise<FriendRequest[]> => {
  const response = await apiClient.get<FriendRequest[]>('/friends/requests/received')
  return response.data
}

// 接受好友请求
export const acceptFriendRequest = async (requestId: number): Promise<{ message: string }> => {
  const response = await apiClient.post<{ message: string }>(`/friends/requests/${requestId}/accept`)
  return response.data
}

// 拒绝好友请求
export const rejectFriendRequest = async (requestId: number): Promise<{ message: string }> => {
  const response = await apiClient.post<{ message: string }>(`/friends/requests/${requestId}/reject`)
  return response.data
}

// 获取好友列表
export const getFriends = async (): Promise<Friend[]> => {
  const response = await apiClient.get<Friend[]>('/friends/list')
  return response.data
}

// 删除好友
export const removeFriend = async (friendId: number): Promise<{ message: string }> => {
  const response = await apiClient.delete<{ message: string }>(`/friends/remove/${friendId}`)
  return response.data
}