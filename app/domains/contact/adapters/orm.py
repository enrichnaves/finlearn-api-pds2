import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from app.core.entities.base import Base, mapper_registry
from app.domains.contact.domain.contact import Contact

contact_table = sa.Table(
    "contact",
    Base.metadata,
    sa.Column(
        "id",
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    ),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("email", sa.String, nullable=False),
    sa.Column("subject", sa.String, nullable=False),
    sa.Column("doubt", sa.String, nullable=False),
    sa.Column(
        "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.sql.func.now()
    ),
)


def start_mappers():
    mapper_registry.map_imperatively(
        Contact,
        contact_table,
    )
