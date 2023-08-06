from typing import Mapping
from email.utils import parseaddr


class ParseAuthorError(Exception):
    pass


def check_name(name: str) -> None:
    if any((c in name) for c in "@<>,"):
        raise ParseAuthorError(f"invalid name: {name}")


def check_email(email: str) -> None:
    if "@" not in email:
        raise ParseAuthorError(f"invalid email: {email}")


def parse_author(author: str) -> Mapping[str, str]:
    result: Mapping[str, str] = {}
    if "@" in author:
        name, email = parseaddr(author)  # https://stackoverflow.com/a/14485817/827548
    else:
        name, email = author, ""

    if name:
        check_name(name)
        result["name"] = name

    if email:
        check_email(email)
        result["email"] = email

    if not result:
        raise ParseAuthorError(f"invalid author string: {author}")
    return result
