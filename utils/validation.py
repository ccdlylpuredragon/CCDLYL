"""Shared data validation utilities."""


class FieldValidator:
    """Declarative field validator that collects errors.

    Usage:
        validator = FieldValidator(data)
        validator.require("name", type_=str, max_length=100)
        validator.require("email", type_=str, pattern="@")
        validator.optional("age", type_=int, min_val=0, max_val=150)
        errors = validator.errors
    """

    def __init__(self, data):
        self.data = data
        self.errors = []

    def require(self, field, type_=None, max_length=None, min_val=None,
                max_val=None, pattern=None, choices=None, min_length=None):
        """Validate a required field.

        Args:
            field: The field name in the data dict.
            type_: Expected type (e.g., str, int, float) or tuple of types.
            max_length: Maximum string length.
            min_length: Minimum string length (e.g., exact length when min==max).
            min_val: Minimum numeric value.
            max_val: Maximum numeric value.
            pattern: Substring that must be present in the value.
            choices: Allowed values (iterable).
        """
        value = self.data.get(field)
        if not value and value != 0:
            self.errors.append(f"{field} is required")
            return

        self._check_type_and_constraints(
            field, value, type_, max_length, min_val, max_val, pattern,
            choices, min_length
        )

    def optional(self, field, type_=None, max_length=None, min_val=None,
                 max_val=None, pattern=None, choices=None, min_length=None):
        """Validate an optional field (skip if None/missing).

        Args:
            Same as require().
        """
        value = self.data.get(field)
        if value is None:
            return

        self._check_type_and_constraints(
            field, value, type_, max_length, min_val, max_val, pattern,
            choices, min_length
        )

    def _check_type_and_constraints(self, field, value, type_, max_length,
                                    min_val, max_val, pattern, choices,
                                    min_length):
        if type_ is not None and not isinstance(value, type_):
            type_name = type_.__name__ if hasattr(type_, '__name__') else str(type_)
            self.errors.append(f"{field} must be a {type_name}")
            return

        if max_length is not None and hasattr(value, '__len__') and len(value) > max_length:
            self.errors.append(f"{field} must be at most {max_length} characters")

        if min_length is not None and hasattr(value, '__len__') and len(value) < min_length:
            self.errors.append(f"{field} must be at least {min_length} characters")

        if min_val is not None and value < min_val:
            self.errors.append(f"{field} must be at least {min_val}")

        if max_val is not None and value > max_val:
            self.errors.append(f"{field} must be at most {max_val}")

        if pattern is not None and isinstance(value, str) and pattern not in value:
            self.errors.append(f"{field} must contain '{pattern}'")

        if choices is not None and value not in choices:
            self.errors.append(f"{field} must be one of: {', '.join(str(c) for c in choices)}")
