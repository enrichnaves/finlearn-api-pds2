import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from app.core.entities.base import Base, mapper_registry
from app.domains.network.domain.network import (
    Post,
    PostValuation,
    Reply,
    ReplyValuation,
)
from app.domains.user.domain.user import User, UserRole

user_table = sa.Table(
    "user",
    Base.metadata,
    sa.Column(
        "id",
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    ),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("cpf", sa.String, nullable=False),
    sa.Column("password", sa.String, nullable=False),
    sa.Column("email", sa.String, nullable=False),
    sa.Column("telephone", sa.String, nullable=False),
    sa.Column("coins_amount", sa.Integer),
    sa.Column(
        "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.sql.func.now()
    ),
    sa.Column(
        "date_updated",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.sql.func.now(),
        onupdate=sa.sql.func.now(),
    ),
)

user_role_table = sa.Table(
    "user_role",
    Base.metadata,
    sa.Column(
        "id",
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    ),
    sa.Column("custom_role", sa.String, nullable=False),
    sa.Column(
        "user_id",
        postgresql.UUID(as_uuid=True),
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column(
        "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.sql.func.now()
    ),
    sa.Column(
        "date_updated",
        sa.TIMESTAMP(timezone=True),
        server_default=sa.sql.func.now(),
        onupdate=sa.sql.func.now(),
    ),
)


def start_mappers():
    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            "roles": relationship(UserRole, back_populates="user"),
            "posts": relationship(Post, back_populates="user"),
            "replies": relationship(Reply, back_populates="user"),
            "posts_valuations": relationship(PostValuation, back_populates="user"),
            "replies_valuations": relationship(ReplyValuation, back_populates="user"),
        },
    )

    mapper_registry.map_imperatively(
        UserRole,
        user_role_table,
        properties={"user": relationship(User, back_populates="roles")},
    )
