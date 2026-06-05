"""SQLAlchemy models for the document storage database."""

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    BigInteger,
    DateTime,
    ForeignKey,
    Table,
    LargeBinary,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Many-to-many association table: documents <-> tags
document_tags = Table(
    "document_tags",
    Base.metadata,
    Column(
        "document_id",
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    """A user who can upload documents."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(128), unique=True, nullable=False, index=True)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    documents = relationship(
        "Document", back_populates="owner", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username!r})>"


class Document(Base):
    """Metadata and optional binary content for an uploaded document."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    filename = Column(String(255), nullable=False)
    file_extension = Column(String(20), nullable=False)
    mime_type = Column(String(128), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_path = Column(String(512), nullable=True)
    file_data = Column(LargeBinary, nullable=True)
    description = Column(Text, nullable=True)
    uploaded_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    owner = relationship("User", back_populates="documents")
    tags = relationship("Tag", secondary=document_tags, back_populates="documents")

    def __repr__(self):
        return (
            f"<Document(id={self.id}, filename={self.filename!r}, "
            f"type={self.file_extension!r})>"
        )


class Tag(Base):
    """A label that can be attached to documents."""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False, index=True)

    documents = relationship(
        "Document", secondary=document_tags, back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name!r})>"
