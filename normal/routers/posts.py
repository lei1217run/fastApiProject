from fastapi import APIRouter, status, HTTPException


__all__ = ("router",)

from normal.database import database
from normal.schema.posts import PostCreate, PostUpdate, Post
from normal.schema.user import User

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("",
            description="Get all posts",
            response_model=list[Post],
            status_code=status.HTTP_200_OK)
async def list_posts() -> list[Post]:
    return [
        Post(
            post_id=post["post_id"],
            title=post["title"],
            created_at=post["created_at"],
            user=User(
                user_id=post["user_id"],
                email=database.users[post["user_id"]]["email"],
                created_at=database.users[post["user_id"]]["created_at"],
            )
        )
        for post in database.posts.values()
    ]


@router.get("/{post_id}",
            description="Get {post_id} post",
            response_model=Post,
            status_code=status.HTTP_200_OK)
async def get_post(post_id: int) -> Post:
    if post_id not in database.posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist",
        )
    post = database.posts[post_id]
    return Post(
        post_id=post_id,
        title=post["title"],
        created_at=post["created_at"],
        user=User(
            user_id=post["user_id"],
            email=database.users[post["user_id"]]["email"],
            created_at=database.users[post["user_id"]]["created_at"],
        )
    )


@router.post("",
             description="Create a new post",
             response_model=Post,
             status_code=status.HTTP_201_CREATED)
async def create_post(input_post: PostCreate) -> Post:
    if input_post.user_id not in database.users:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User does not exist",
        )
    post = Post(
        post_id=len(database.posts) + 1,
        title=input_post.title,
        user=User(
            user_id=input_post.user_id,
            email=database.users[input_post.user_id]["email"],
            created_at=database.users[input_post.user_id]["created_at"],
        )
    )

    database.posts[post.post_id] = {
        "post_id": post.post_id,
        "title": post.title,
        "created_at": post.created_at,
        "user_id": input_post.user_id,
    }
    return post


@router.patch("/{post_id}",
              description="Update a post",
              response_model=Post,
              status_code=status.HTTP_200_OK)
async def update_post(post_id: int, input_post: PostUpdate) -> Post:
    if post_id not in database.posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist",
        )
    post = database.posts[post_id]
    post["title"] = input_post.title

    return Post(
        post_id=post["post_id"],
        title=post["title"],
        created_at=post["created_at"],
        user=User(
            user_id=post["user_id"],
            email=database.users[post["user_id"]]["email"],
            created_at=database.users[post["user_id"]]["created_at"],
        )
    )


@router.delete("/{post_id}",
               description="Delete a post",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int) -> None:
    if post_id not in database.posts:
        return
    database.posts.pop(post_id)
    return None
