class FieldNotSupported(Exception):
    def __init__(self, field_name=None, *args, **kwargs):
        exception = f"Could not convert field '{field_name}'"
        return super().__init__(exception, *args, **kwargs)


class DefinitionNotFound(Exception):
    def __init__(self, model_name=None, *args, **kwargs):
        exception = f"Could not find model '{model_name}'"
        return super().__init__(exception, *args, **kwargs)
