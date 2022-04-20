import re

from importlib import import_module
from inspect import getmembers, isclass

from coffee.exceptions import DefinitionNotFound, FieldNotSupported
from .definitions import FORM_TRANSLATION, TYPESCRIPT_TRANSLATION

from django.middleware.csrf import get_token


def get_typescript_type(db_type):
    if db_type not in TYPESCRIPT_TRANSLATION:
        raise FieldNotSupported(db_type)
    return TYPESCRIPT_TRANSLATION[db_type]


def to_camel_case(text):
    first, *others = text.split("_")
    return "".join([first.lower(), *map(str.title, others)])


def to_snake_case(text):
    text = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    text = re.sub("__([A-Z])", r"_\1", text)
    text = re.sub("([a-z0-9])([A-Z])", r"\1_\2", text)
    return text.lower()


def get_model_definitions(app_name):
    module = import_module(f"{app_name}.models")
    models = getmembers(module, predicate=isclass)

    definitions = {}

    for model_name, model in models:
        if model_name not in definitions:
            definitions[model_name] = {}

        for field in model._meta.fields:
            related_model = None

            if field.related_model:
                related_model = field.related_model.__name__

            definitions[model_name][field.name] = {
                "related_model": related_model,
                "primary_key": field.primary_key,
                "db_type": field.get_internal_type(),
                "nullable": field.null,
            }

    return definitions


def get_form_item_input_html(db_type):
    if db_type not in FORM_TRANSLATION:
        raise FieldNotSupported()

    return f"{FORM_TRANSLATION[db_type]}\n"


def get_form_item_label_html():
    return "<label for='%s'>%s</label>\n"


def get_form_item_row_html(name, db_type, value=None):
    html = '<div class="FormItem">\n'
    html += get_form_item_label_html() % (name, name)
    html += get_form_item_input_html(db_type=db_type) % (value, name)
    html += "</div>\n"
    return html


def get_form_submit_button_html():
    html = '<div class="FormItem">\n'
    html += "<button type='submit' class='FormButton'>Submit</button>"
    html += "</div>\n"
    return html


def get_csrf_token_html():
    return '<input type="hidden" name="csrfmiddlewaretoken" value="%s" />'


def get_delete_button_html(request, app_name, model_name):
    csrf_token = get_token(request)
    url = f"/coffee/delete/%s/?app_name={app_name}&model_name={model_name}"
    html = f"<form method='POST' action='{url}' >"
    html += get_csrf_token_html() % (csrf_token)
    html += "<button type='submit'>Delete</button>\n"
    html += "</form>\n"
    return html


def render_model_form_html(request, app_name, model_name, instance):
    definitions = get_model_definitions(app_name)

    csrf_token = get_token(request)

    if model_name not in definitions:
        raise DefinitionNotFound(model_name)

    definition = definitions[model_name]

    html = "<form method='POST' class='Form' action='/coffee/form/submit/"
    html += f"?app_name={app_name}&model_name={model_name}' >\n"

    for name, field in definition.items():
        db_type = field.get("db_type")
        html += get_form_item_row_html(
            name=name, db_type=db_type, value=getattr(instance, name, None)
        )

    html += get_form_submit_button_html()
    html += get_csrf_token_html() % (csrf_token)

    html += "</form>\n"

    return html
