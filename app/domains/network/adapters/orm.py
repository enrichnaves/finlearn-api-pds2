from sqlalchemy import Column, String, Boolean, ForeignKey, TIMESTAMP
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.domains.user.domain.user import User
from app.domains.network.domain.network import (
    Post,
    Reply,
    PostValuation,
    ReplyValuation,
)
from app.core.entities.base import Base, mapper_registry

# Tabelas
post_table = sa.Table(
    "post",
    Base.metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    ),
    Column("title", String, nullable=False),
    Column("body_text", String, nullable=False),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("date_created", TIMESTAMP(timezone=True), server_default=sa.sql.func.now()),
    Column(
        "date_updated",
        TIMESTAMP(timezone=True),
        server_default=sa.sql.func.now(),
        onupdate=sa.sql.func.now(),
    ),
)

reply_table = sa.Table(
    "reply",
    Base.metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    ),
    Column("body_text", String, nullable=False),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "post_id",
        UUID(as_uuid=True),
        ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("date_created", TIMESTAMP(timezone=True), server_default=sa.sql.func.now()),
    Column(
        "date_updated",
        TIMESTAMP(timezone=True),
        server_default=sa.sql.func.now(),
        onupdate=sa.sql.func.now(),
    ),
)

post_valuation_table = sa.Table(
    "post_valuation",
    Base.metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    ),
    Column("is_up", Boolean, nullable=False),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "post_id",
        UUID(as_uuid=True),
        ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("date_created", TIMESTAMP(timezone=True), server_default=sa.sql.func.now()),
    Column(
        "date_updated",
        TIMESTAMP(timezone=True),
        server_default=sa.sql.func.now(),
        onupdate=sa.sql.func.now(),
    ),
)

reply_valuation_table = sa.Table(
    "reply_valuation",
    Base.metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    ),
    Column("is_up", Boolean, nullable=False),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "reply_id",
        UUID(as_uuid=True),
        ForeignKey("reply.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("date_created", TIMESTAMP(timezone=True), server_default=sa.sql.func.now()),
    Column(
        "date_updated",
        TIMESTAMP(timezone=True),
        server_default=sa.sql.func.now(),
        onupdate=sa.sql.func.now(),
    ),
)


# Mapeamento
def start_mappers():
    mapper_registry.map_imperatively(
        Post,
        post_table,
        properties={
            "user": relationship(User, back_populates="posts"),
            "replies": relationship(Reply, back_populates="post"),
            "valuations": relationship(PostValuation, back_populates="post"),
        },
    )

    mapper_registry.map_imperatively(
        Reply,
        reply_table,
        properties={
            "user": relationship(User, back_populates="replies"),
            "post": relationship(Post, back_populates="replies"),
            "valuations": relationship(ReplyValuation, back_populates="reply"),
        },
    )

    mapper_registry.map_imperatively(
        PostValuation,
        post_valuation_table,
        properties={
            "user": relationship(User, back_populates="posts_valuations"),
            "post": relationship(Post),
        },
    )

    mapper_registry.map_imperatively(
        ReplyValuation,
        reply_valuation_table,
        properties={
            "user": relationship(User, back_populates="replies_valuations"),
            "reply": relationship(Reply),
        },
    )
