from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from pydantic import BaseModel
from database import get_db
from models import User, FriendRequest, Friendship, UserRole
from routers.auth import get_current_active_user

router = APIRouter()

# Pydantic models
class FriendRequestCreate(BaseModel):
    receiver_id: int
    message: Optional[str] = None

class FriendRequestResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    status: str
    message: Optional[str]
    created_at: str
    sender_name: str
    sender_role: str
    receiver_name: str

class FriendResponse(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    role: str
    student_id: Optional[str] = None
    teacher_id: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    class_name: Optional[str] = None
    friendship_since: str

class UserSearchResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    student_id: Optional[str] = None
    teacher_id: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    class_name: Optional[str] = None

@router.get("/search", response_model=List[UserSearchResponse])
async def search_users(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """搜索用户（用于添加好友）"""
    try:
        # 搜索用户名、姓名、邮箱
        users = db.query(User).filter(
            and_(
                User.id != current_user.id,  # 排除自己
                or_(
                    User.username.contains(q),
                    User.full_name.contains(q),
                    User.email.contains(q)
                )
            )
        ).limit(20).all()

        result = []
        for user in users:
            user_data = {
                "id": user.id,
                "name": user.full_name,
                "email": user.email,
                "role": user.role.value
            }

            # 根据角色添加额外信息
            if user.role == UserRole.STUDENT and hasattr(user, 'student_profile') and user.student_profile:
                user_data.update({
                    "student_id": user.student_profile.student_id,
                    "class_name": user.student_profile.class_name
                })
            elif user.role == UserRole.TEACHER and hasattr(user, 'teacher_profile') and user.teacher_profile:
                user_data.update({
                    "teacher_id": user.teacher_profile.teacher_id,
                    "department": user.teacher_profile.department,
                    "title": user.teacher_profile.title
                })

            result.append(user_data)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索用户失败: {str(e)}")

@router.post("/request", response_model=dict)
async def send_friend_request(
    request_data: FriendRequestCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """发送好友请求"""
    try:
        # 检查是否是自己
        if request_data.receiver_id == current_user.id:
            raise HTTPException(status_code=400, detail="不能添加自己为好友")

        # 检查用户是否存在
        receiver = db.query(User).filter(User.id == request_data.receiver_id).first()
        if not receiver:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 检查是否已经是好友
        existing_friendship = db.query(Friendship).filter(
            or_(
                and_(Friendship.user1_id == current_user.id, Friendship.user2_id == request_data.receiver_id),
                and_(Friendship.user1_id == request_data.receiver_id, Friendship.user2_id == current_user.id)
            )
        ).first()
        if existing_friendship:
            raise HTTPException(status_code=400, detail="你们已经是好友了")

        # 检查是否有待处理的好友请求
        existing_request = db.query(FriendRequest).filter(
            or_(
                and_(FriendRequest.sender_id == current_user.id, FriendRequest.receiver_id == request_data.receiver_id, FriendRequest.status == "pending"),
                and_(FriendRequest.sender_id == request_data.receiver_id, FriendRequest.receiver_id == current_user.id, FriendRequest.status == "pending")
            )
        ).first()
        if existing_request:
            raise HTTPException(status_code=400, detail="已经有一个待处理的好友请求")

        # 创建好友请求
        friend_request = FriendRequest(
            sender_id=current_user.id,
            receiver_id=request_data.receiver_id,
            message=request_data.message,
            status="pending"
        )
        db.add(friend_request)
        db.commit()

        return {"message": "好友请求已发送", "request_id": friend_request.id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发送好友请求失败: {str(e)}")

@router.get("/requests/sent", response_model=List[FriendRequestResponse])
async def get_sent_requests(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取我发送的好友请求"""
    try:
        requests = db.query(FriendRequest).filter(
            FriendRequest.sender_id == current_user.id
        ).order_by(FriendRequest.created_at.desc()).all()

        result = []
        for req in requests:
            result.append({
                "id": req.id,
                "sender_id": req.sender_id,
                "receiver_id": req.receiver_id,
                "status": req.status,
                "message": req.message,
                "created_at": req.created_at.isoformat(),
                "sender_name": req.sender.full_name,
                "sender_role": req.sender.role.value,
                "receiver_name": req.receiver.full_name
            })

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取发送的好友请求失败: {str(e)}")

@router.get("/requests/received", response_model=List[FriendRequestResponse])
async def get_received_requests(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取收到的好友请求"""
    try:
        requests = db.query(FriendRequest).filter(
            FriendRequest.receiver_id == current_user.id,
            FriendRequest.status == "pending"
        ).order_by(FriendRequest.created_at.desc()).all()

        result = []
        for req in requests:
            result.append({
                "id": req.id,
                "sender_id": req.sender_id,
                "receiver_id": req.receiver_id,
                "status": req.status,
                "message": req.message,
                "created_at": req.created_at.isoformat(),
                "sender_name": req.sender.full_name,
                "sender_role": req.sender.role.value,
                "receiver_name": req.receiver.full_name
            })

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取收到的好友请求失败: {str(e)}")

@router.post("/requests/{request_id}/accept")
async def accept_friend_request(
    request_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """接受好友请求"""
    try:
        friend_request = db.query(FriendRequest).filter(
            FriendRequest.id == request_id,
            FriendRequest.receiver_id == current_user.id,
            FriendRequest.status == "pending"
        ).first()

        if not friend_request:
            raise HTTPException(status_code=404, detail="好友请求不存在或已被处理")

        # 创建好友关系
        friendship = Friendship(
            user1_id=friend_request.sender_id,
            user2_id=friend_request.receiver_id,
            status="active"
        )
        db.add(friendship)

        # 更新请求状态
        friend_request.status = "accepted"
        db.commit()

        return {"message": "已接受好友请求"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"接受好友请求失败: {str(e)}")

@router.post("/requests/{request_id}/reject")
async def reject_friend_request(
    request_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """拒绝好友请求"""
    try:
        friend_request = db.query(FriendRequest).filter(
            FriendRequest.id == request_id,
            FriendRequest.receiver_id == current_user.id,
            FriendRequest.status == "pending"
        ).first()

        if not friend_request:
            raise HTTPException(status_code=404, detail="好友请求不存在或已被处理")

        # 更新请求状态
        friend_request.status = "rejected"
        db.commit()

        return {"message": "已拒绝好友请求"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"拒绝好友请求失败: {str(e)}")

@router.get("/list", response_model=List[FriendResponse])
async def get_friends(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取好友列表"""
    try:
        # 查询所有好友关系
        friendships = db.query(Friendship).filter(
            or_(
                Friendship.user1_id == current_user.id,
                Friendship.user2_id == current_user.id
            ),
            Friendship.status == "active"
        ).all()

        result = []
        for friendship in friendships:
            # 确定好友是哪个用户
            friend_id = friendship.user2_id if friendship.user1_id == current_user.id else friendship.user1_id
            friend = db.query(User).filter(User.id == friend_id).first()

            if friend:
                friend_data = {
                    "id": friendship.id,
                    "user_id": friend.id,
                    "name": friend.full_name,
                    "email": friend.email,
                    "role": friend.role.value,
                    "friendship_since": friendship.created_at.isoformat()
                }

                # 根据角色添加额外信息
                if friend.role == UserRole.STUDENT and hasattr(friend, 'student_profile') and friend.student_profile:
                    friend_data.update({
                        "student_id": friend.student_profile.student_id,
                        "class_name": friend.student_profile.class_name
                    })
                elif friend.role == UserRole.TEACHER and hasattr(friend, 'teacher_profile') and friend.teacher_profile:
                    friend_data.update({
                        "teacher_id": friend.teacher_profile.teacher_id,
                        "department": friend.teacher_profile.department,
                        "title": friend.teacher_profile.title
                    })

                result.append(friend_data)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取好友列表失败: {str(e)}")

@router.delete("/remove/{friend_id}")
async def remove_friend(
    friend_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除好友"""
    try:
        # 查找好友关系
        friendship = db.query(Friendship).filter(
            or_(
                and_(Friendship.user1_id == current_user.id, Friendship.user2_id == friend_id),
                and_(Friendship.user1_id == friend_id, Friendship.user2_id == current_user.id)
            ),
            Friendship.status == "active"
        ).first()

        if not friendship:
            raise HTTPException(status_code=404, detail="好友关系不存在")

        # 删除好友关系
        db.delete(friendship)
        db.commit()

        return {"message": "好友已删除"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除好友失败: {str(e)}")