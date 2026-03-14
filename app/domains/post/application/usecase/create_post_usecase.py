from app.domains.post.application.port.post_repository_port import PostRepositoryPort
from app.domains.post.application.request.create_post_request import CreatePostRequest
from app.domains.post.application.response.create_post_response import CreatePostResponse
from app.domains.post.domain.entity.post import Post


class CreatePostUseCase:
    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    async def execute(self, request: CreatePostRequest) -> CreatePostResponse:
        post = Post(title=request.title, content=request.content)
        saved = await self.post_repository.save(post)
        return CreatePostResponse(id=saved.id, created_at=saved.created_at)
