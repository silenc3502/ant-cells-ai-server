from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.post.application.port.post_repository_port import PostRepositoryPort
from app.domains.post.domain.entity.post import Post
from app.domains.post.infrastructure.mapper.post_mapper import PostMapper


class PostRepositoryImpl(PostRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, post: Post) -> Post:
        orm = PostMapper.to_orm(post)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return PostMapper.to_entity(orm)
