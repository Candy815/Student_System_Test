from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# 初始化智谱AI客户端
try:
    Zhipu_API_Key = os.getenv("Zhipu_API_Key")
    if not Zhipu_API_Key:
        raise ValueError("Zhipu_API_Key environment variable not set")

    client = ZhipuAI(api_key=Zhipu_API_Key)
except Exception as e:
    print(f"初始化AI客户端失败: {e}")
    client = None

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

def get_ai_response(user_message: str) -> str:
    """获取AI回复"""
    if not client:
        return "抱歉，AI服务暂时不可用，请稍后再试。"

    try:
        # 构建系统提示词，专注于学习相关内容
        system_prompt = """你是一个专业的学习助手，专门帮助大学生解答学习相关的问题。
你的回答应该：
1. 专业、准确、有条理
2. 针对学生的学习问题提供实用的建议
3. 鼓励学生主动学习，培养良好的学习习惯
4. 回答要简洁明了，重点突出
5. 如果遇到不适当的问题，礼貌地引导回学习主题

请用中文回答，语气友好且专业。"""

        # 调用智谱AI API
        response = client.chat.completions.create(
            model="glm-4.5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            thinking={
                "type": "enabled",  # 启用深度思考模式
            },
            stream=False,  # 不使用流式输出
            max_tokens=2048,  # 限制输出长度
            temperature=0.7  # 控制输出的随机性
        )

        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "抱歉，我暂时无法理解您的问题，请换个方式询问。"

    except Exception as e:
        print(f"AI API调用失败: {e}")
        return "抱歉，AI服务出现错误，请稍后再试。"

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """AI聊天接口"""
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="消息内容不能为空")

        # 获取AI回复
        ai_response = get_ai_response(request.message.strip())

        return ChatResponse(
            response=ai_response,
            session_id=request.session_id or "default"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"聊天接口错误: {e}")
        raise HTTPException(status_code=500, detail="服务器内部错误")

@router.get("/health")
async def ai_health_check():
    """AI服务健康检查"""
    try:
        is_available = client is not None
        return {
            "status": "healthy" if is_available else "unavailable",
            "ai_service": "Zhipu GLM-4.5",
            "available": is_available
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }