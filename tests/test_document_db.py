"""Tests for the document_db package."""

import os
import tempfile

import pytest

from document_db.database import init_db, get_session
from document_db.crud import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    upload_document,
    get_document_by_id,
    list_documents,
    delete_document,
    get_or_create_tag,
)


@pytest.fixture(autouse=True)
def db_session():
    """Provide a fresh in-memory database for every test."""
    init_db("sqlite:///:memory:")
    yield


@pytest.fixture()
def sample_user():
    session = get_session()
    user = create_user(session, "alice", "alice@example.com")
    session.close()
    return user


@pytest.fixture()
def sample_file():
    """Create a temporary file to simulate a document upload."""
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.write(fd, b"%PDF-1.4 fake content")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


# ---- User tests ----

def test_create_user():
    session = get_session()
    user = create_user(session, "bob", "bob@example.com")
    assert user.id is not None
    assert user.username == "bob"
    session.close()


def test_get_user_by_id(sample_user):
    session = get_session()
    user = get_user_by_id(session, sample_user.id)
    assert user is not None
    assert user.username == "alice"
    session.close()


def test_get_user_by_username(sample_user):
    session = get_session()
    user = get_user_by_username(session, "alice")
    assert user is not None
    assert user.email == "alice@example.com"
    session.close()


# ---- Document tests ----

def test_upload_document(sample_user, sample_file):
    session = get_session()
    doc = upload_document(
        session,
        sample_user.id,
        sample_file,
        description="A test PDF",
        tags=["report", "test"],
    )
    assert doc.id is not None
    assert doc.filename.endswith(".pdf")
    assert doc.file_extension == "pdf"
    assert doc.mime_type == "application/pdf"
    assert doc.file_size > 0
    assert len(doc.tags) == 2
    session.close()


def test_upload_document_with_binary(sample_user, sample_file):
    session = get_session()
    doc = upload_document(
        session,
        sample_user.id,
        sample_file,
        store_binary=True,
    )
    assert doc.file_data is not None
    assert len(doc.file_data) > 0
    session.close()


def test_list_documents_filter_by_user(sample_user, sample_file):
    session = get_session()
    upload_document(session, sample_user.id, sample_file)
    docs = list_documents(session, user_id=sample_user.id)
    assert len(docs) == 1
    session.close()


def test_list_documents_filter_by_extension(sample_user, sample_file):
    session = get_session()
    upload_document(session, sample_user.id, sample_file)
    docs = list_documents(session, file_extension="pdf")
    assert len(docs) == 1
    docs = list_documents(session, file_extension="docx")
    assert len(docs) == 0
    session.close()


def test_list_documents_filter_by_tag(sample_user, sample_file):
    session = get_session()
    upload_document(session, sample_user.id, sample_file, tags=["important"])
    docs = list_documents(session, tag_name="important")
    assert len(docs) == 1
    docs = list_documents(session, tag_name="other")
    assert len(docs) == 0
    session.close()


def test_get_document_by_id(sample_user, sample_file):
    session = get_session()
    doc = upload_document(session, sample_user.id, sample_file)
    fetched = get_document_by_id(session, doc.id)
    assert fetched is not None
    assert fetched.filename == doc.filename
    session.close()


def test_delete_document(sample_user, sample_file):
    session = get_session()
    doc = upload_document(session, sample_user.id, sample_file)
    assert delete_document(session, doc.id) is True
    assert get_document_by_id(session, doc.id) is None
    session.close()


def test_delete_nonexistent_document():
    session = get_session()
    assert delete_document(session, 9999) is False
    session.close()


# ---- Tag tests ----

def test_get_or_create_tag_creates_once():
    session = get_session()
    tag1 = get_or_create_tag(session, "finance")
    tag2 = get_or_create_tag(session, "finance")
    assert tag1.id == tag2.id
    session.close()


# ---- Database init guard ----

def test_get_session_before_init():
    """Ensure get_session raises if init_db has not been called."""
    import document_db.database as db_mod
    original_session = db_mod._SessionLocal
    db_mod._SessionLocal = None
    with pytest.raises(RuntimeError):
        get_session()
    db_mod._SessionLocal = original_session
