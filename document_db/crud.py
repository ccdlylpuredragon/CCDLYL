"""CRUD helpers for documents, users, and tags."""

from __future__ import annotations

import mimetypes
import os
from typing import List, Optional

from sqlalchemy.orm import Session

from document_db.models import Document, Tag, User


# ---------------------------------------------------------------------------
# User helpers
# ---------------------------------------------------------------------------

def create_user(session: Session, username: str, email: str) -> User:
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    return session.query(User).filter(User.username == username).first()


# ---------------------------------------------------------------------------
# Tag helpers
# ---------------------------------------------------------------------------

def get_or_create_tag(session: Session, tag_name: str) -> Tag:
    with session.no_autoflush:
        tag = session.query(Tag).filter(Tag.name == tag_name).first()
    if tag is None:
        tag = Tag(name=tag_name)
        session.add(tag)
        session.flush()
    return tag


# ---------------------------------------------------------------------------
# Document helpers
# ---------------------------------------------------------------------------

def _guess_mime(filename: str) -> str:
    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"


def upload_document(
    session: Session,
    user_id: int,
    filepath: str,
    *,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    store_binary: bool = False,
) -> Document:
    """Register a document in the database.

    Args:
        session: Active DB session.
        user_id: Owner's user ID.
        filepath: Path to the file on disk.
        description: Optional description text.
        tags: Optional list of tag names to attach.
        store_binary: If ``True``, read the file bytes into ``file_data``.

    Returns:
        The newly created :class:`Document` instance.
    """
    filename = os.path.basename(filepath)
    _, ext = os.path.splitext(filename)
    ext = ext.lstrip(".").lower()
    file_size = os.path.getsize(filepath)
    mime = _guess_mime(filename)

    file_data = None
    if store_binary:
        with open(filepath, "rb") as fh:
            file_data = fh.read()

    doc = Document(
        user_id=user_id,
        filename=filename,
        file_extension=ext,
        mime_type=mime,
        file_size=file_size,
        file_path=os.path.abspath(filepath),
        file_data=file_data,
        description=description,
    )
    session.add(doc)
    session.flush()

    if tags:
        for tag_name in tags:
            tag_obj = get_or_create_tag(session, tag_name)
            doc.tags.append(tag_obj)

    session.commit()
    session.refresh(doc)
    return doc


def get_document_by_id(session: Session, doc_id: int) -> Optional[Document]:
    return session.query(Document).filter(Document.id == doc_id).first()


def list_documents(
    session: Session,
    *,
    user_id: Optional[int] = None,
    file_extension: Optional[str] = None,
    tag_name: Optional[str] = None,
) -> List[Document]:
    """List documents with optional filters."""
    query = session.query(Document)
    if user_id is not None:
        query = query.filter(Document.user_id == user_id)
    if file_extension is not None:
        query = query.filter(Document.file_extension == file_extension.lower())
    if tag_name is not None:
        query = query.join(Document.tags).filter(Tag.name == tag_name)
    return query.order_by(Document.uploaded_at.desc()).all()


def delete_document(session: Session, doc_id: int) -> bool:
    doc = get_document_by_id(session, doc_id)
    if doc is None:
        return False
    session.delete(doc)
    session.commit()
    return True
