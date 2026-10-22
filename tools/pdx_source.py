"""Small lossless-span reader for source audits, not the HOI4 engine."""

from dataclasses import dataclass
import re


TOKEN = re.compile(r'\s+|\#[^\n]*|"(?:\\.|[^"\\])*"|>=|<=|!=|[{}=<>!]|[^\s{}=<>!#"]+')


@dataclass
class Node:
    key: str | None
    op: str | None
    value: str | list
    begin: int = 0
    end: int = 0


def parse(text):
    tokens = [
        (match.group(), match.start(), match.end())
        for match in TOKEN.finditer(text)
        if not match.group().isspace() and not match.group().startswith("#")
    ]
    index = 0

    def block(nested=False):
        nonlocal index
        result = []
        while index < len(tokens):
            token, start, end = tokens[index]
            if token == "}":
                if not nested:
                    raise ValueError("Unexpected closing brace")
                index += 1
                return result, end
            if token == "{":
                index += 1
                value, finish = block(True)
                result.append(Node(None, None, value, start, finish))
                continue
            if token in ["=", "<", ">", "<=", ">=", "!=", "!"]:
                raise ValueError(f"Unexpected token {token} at {start}")
            index += 1
            if index == len(tokens) or tokens[index][0] not in ["=", "<", ">", "<=", ">=", "!="]:
                result.append(Node(None, None, token, start, end))
                continue
            operator = tokens[index][0]
            index += 1
            if index == len(tokens):
                raise ValueError(f"Missing value {token}")
            value, _, finish = tokens[index]
            index += 1
            if value == "{":
                value, finish = block(True)
            elif value == "}":
                raise ValueError(f"Missing value {token}")
            result.append(Node(token, operator, value, start, finish))
        if nested:
            raise ValueError("Unclosed block")
        return result, len(text)

    return block()[0]


def entries(sequence):
    return [item for item in sequence if isinstance(item, Node)]


def vals(sequence, key):
    return [item.value for item in entries(sequence) if item.key and item.key.lower() == key.lower()]


def val(sequence, key, default=None):
    return next(iter(vals(sequence, key)), default)


def atom(value):
    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def walk(sequence):
    for item in entries(sequence):
        yield item
        if isinstance(item.value, list):
            yield from walk(item.value)

