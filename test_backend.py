import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入必要的模块
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import time

def test_backend():
    print("=== 测试后端服务器 ===")

    # 测试健康检查
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✓ 后端服务器正常运行")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"✗ 后端服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到后端服务器 (端口8001)")
        return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_login():
    print("\n=== 测试登录功能 ===")

    login_data = {
        "username": "admin",
        "password": "admin123"
    }

    try:
        # 测试登录接口
        response = requests.post(
            "http://localhost:8001/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )

        if response.status_code == 200:
            print("✓ 登录功能正常")
            result = response.json()
            print(f"用户信息: {result.get('user', {}).get('full_name', 'Unknown')}")
            print(f"角色: {result.get('user', {}).get('role', 'Unknown')}")
            return result.get('access_token')
        else:
            print(f"✗ 登录失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"✗ 登录测试失败: {e}")
        return None

def test_admin_courses(token):
    print("\n=== 测试管理员课程功能 ===")

    if not token:
        print("✗ 没有有效的token，跳过测试")
        return

    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
            "http://localhost:8001/admin/courses",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print("✓ 管理员课程功能正常")
            data = response.json()
            print(f"课程数量: {data.get('total', 0)}")
            return True
        else:
            print(f"✗ 课程功能异常: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 课程功能测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试学生管理系统...")

    # 测试后端服务器
    if test_backend():
        # 测试登录功能
        token = test_login()

        # 测试管理员课程功能
        if token:
            test_admin_courses(token)

    print("\n测试完成！")