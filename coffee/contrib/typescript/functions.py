from coffee.exceptions import FieldNotSupported
from coffee.contrib.render.definitions import TYPESCRIPT_TRANSLATION


def get_typescript_type(db_type):
    if db_type not in TYPESCRIPT_TRANSLATION:
        raise FieldNotSupported(db_type)

    return TYPESCRIPT_TRANSLATION[db_type]
