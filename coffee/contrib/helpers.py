import re


def to_camel_case(text):
    first, *others = text.split("_")

    return "".join([first.lower(), *map(str.title, others)])


def to_snake_case(text):
    text = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    text = re.sub("__([A-Z])", r"_\1", text)
    text = re.sub("([a-z0-9])([A-Z])", r"\1_\2", text)

    return text.lower()
