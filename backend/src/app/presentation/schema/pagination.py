from .base import Base


class PaginationSchema(Base):
    limit: int
    offset: int
