from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, status, Depends

from app.application import PostService
from app.application import DIC
from app.entrypoint.fastapi.schema.posts import Post, PostCreate, PostUpdate
from app.entrypoint.fastapi.schema.user import User

from app.domain.models.post import Post as PostModel
from app.domain.models.user import User as UserModel

"""
    1. 领域模型包含核心的业务逻辑
    2. 响应模型定义输出的数据和格式
"""

__all__ = ("router",)

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


def to_user_view_model(user: UserModel) -> User:
    return User(
        user_id=user.user_id,
        email=user.email,
        created_at=user.created_at,
    )


def to_post_view_model(post: PostModel) -> Post:
    return Post(
        title=post.title,
        post_id=post.post_id,
        created_at=post.created_at,
        user=to_user_view_model(post.user)
    )


@router.get("",
            description="Get all posts",
            response_model=list[Post],
            status_code=status.HTTP_200_OK)
@inject
async def list_posts(post_service: PostService = Depends(Provide[DIC.post_service])) -> list[Post]:
    posts: list[PostModel] = await post_service.list_posts()
    return [to_post_view_model(post) for post in posts]


@router.get("/{post_id}",
            description="Get {post_id} post",
            response_model=Post,
            status_code=status.HTTP_200_OK)
@inject
async def get_post(post_id: int,post_service: PostService = Depends(Provide[DIC.post_service])) -> Post:
    post: PostModel = await post_service.get_post(post_id)
    return to_post_view_model(post)


@router.post("",
             description="Create a new post",
             response_model=Post,
             status_code=status.HTTP_201_CREATED)
@inject
async def create_post(input_post: PostCreate,post_service: PostService = Depends(Provide[DIC.post_service])) -> Post:
    post: PostModel = await post_service.create_post(
        user_id=input_post.user_id,
        title=input_post.title)
    return to_post_view_model(post)


@router.patch("/{post_id}",
              description="Update a post",
              response_model=Post,
              status_code=status.HTTP_200_OK)
@inject
async def update_post(post_id: int, input_post: PostUpdate,post_service: PostService = Depends(Provide[DIC.post_service])) -> Post:
    post: PostModel = await post_service.update_post(
        user_id=input_post.user_id, post_id=post_id, title=input_post.title)
    return to_post_view_model(post)


@router.delete("/{post_id}",
               description="Delete a post",
               status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_post(post_id: int,post_service: PostService = Depends(Provide[DIC.post_service])) -> None:
    await post_service.delete_post(post_id=post_id)
