"""Tests for the shared validation utility."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validation import FieldValidator


def test_require_missing_field():
    v = FieldValidator({})
    v.require("name", type_=str)
    assert v.errors == ["name is required"]


def test_require_wrong_type():
    v = FieldValidator({"name": 123})
    v.require("name", type_=str)
    assert v.errors == ["name must be a str"]


def test_require_max_length_exceeded():
    v = FieldValidator({"name": "a" * 101})
    v.require("name", type_=str, max_length=100)
    assert v.errors == ["name must be at most 100 characters"]


def test_require_min_val():
    v = FieldValidator({"age": -1})
    v.require("age", type_=int, min_val=0, max_val=150)
    assert v.errors == ["age must be at least 0"]


def test_require_max_val():
    v = FieldValidator({"age": 200})
    v.require("age", type_=int, min_val=0, max_val=150)
    assert v.errors == ["age must be at most 150"]


def test_require_pattern():
    v = FieldValidator({"email": "notanemail"})
    v.require("email", type_=str, pattern="@")
    assert v.errors == ["email must contain '@'"]


def test_require_choices():
    v = FieldValidator({"method": "cash"})
    v.require("method", type_=str, choices=("credit_card", "debit_card"))
    assert v.errors == ["method must be one of: credit_card, debit_card"]


def test_optional_missing_is_ok():
    v = FieldValidator({})
    v.optional("notes", type_=str, max_length=500)
    assert v.errors == []


def test_optional_present_invalid():
    v = FieldValidator({"notes": 123})
    v.optional("notes", type_=str)
    assert v.errors == ["notes must be a str"]


def test_valid_data_no_errors():
    v = FieldValidator({"name": "Alice", "email": "alice@example.com", "age": 30})
    v.require("name", type_=str, max_length=100)
    v.require("email", type_=str, pattern="@")
    v.optional("age", type_=int, min_val=0, max_val=150)
    assert v.errors == []


def test_multiple_errors():
    v = FieldValidator({})
    v.require("name", type_=str)
    v.require("email", type_=str)
    assert len(v.errors) == 2


def test_min_length():
    v = FieldValidator({"code": "US"})
    v.require("code", type_=str, min_length=3, max_length=3)
    assert v.errors == ["code must be at least 3 characters"]
