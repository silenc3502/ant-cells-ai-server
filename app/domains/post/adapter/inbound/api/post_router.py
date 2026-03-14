from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.post.adapter.outbound.persistence.post_repository_impl import PostRepositoryImpl
from app.domains.post.application.request.create_post_request import CreatePostRequest
from app.domains.post.application.response.create_post_response import CreatePostResponse
from app.domains.post.application.usecase.create_authenticated_post_usecase import CreateAuthenticatedPostUseCase
from app.domains.post.application.usecase.create_post_usecase import CreatePostUseCase
from app.infrastructure.auth.current_user import get_current_user_id
from app.infrastructure.database.database import get_db_session

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    request: CreatePostRequest,
    session: AsyncSession = Depends(get_db_session),
):
    repository = PostRepositoryImpl(session)
    usecase = CreatePostUseCase(repository)
    return await usecase.execute(request)


@router.post("/me", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED)
async def create_authenticated_post(
    request: CreatePostRequest,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
):
    repository = PostRepositoryImpl(session)
    usecase = CreateAuthenticatedPostUseCase(repository)
    return await usecase.execute(request, user_id)
