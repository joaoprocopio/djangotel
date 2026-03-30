import html


def sanitize_string(value: str, max_length: int | None = None) -> str:
    stripped = value.strip()
    if max_length is not None and len(stripped) > max_length:
        raise ValueError(f"Value exceeds max length of {max_length}")
    return stripped


def sanitize_email(value: str) -> str:
    return value.strip().lower()


def sanitize_html(value: str) -> str:
    return html.escape(value)


def sanitize_username(value: str, max_length: int = 50) -> str:
    sanitized = sanitize_string(value, max_length=max_length)
    if not sanitized:
        raise ValueError("Username cannot be empty")
    if not all(c.isalnum() or c == "_" for c in sanitized):
        raise ValueError(
            "Username can only contain alphanumeric characters and underscores"
        )
    return sanitized
