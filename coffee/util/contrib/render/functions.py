import re
from importlib import import_module
from inspect import getmembers, isclass

from coffee.exceptions import DefinitionNotFound, FieldNotSupported
from coffee.util.contrib.render.components import (
    Form,
    Input,
    InputTemplate,
    Pagination,
    TBody,
    THead,
    TRow,
    Table,
    Td,
)
from coffee.util.contrib.render.definitions import (
    FORM_TRANSLATION,
)
from django.db.models.base import ModelBase
from django.forms.models import model_to_dict
from django.middleware.csrf import get_token


def get_model_definitions(app_name):
    module = import_module(f"{app_name}.models")
    models = getmembers(module, predicate=isclass)

    definitions = {}

    for model_name, model in models:
        if type(model) == ModelBase and hasattr(model, "_meta"):
            rx = re.compile(r"(?:<class [\"'])(.+)(?:[\"']>)")
            match = rx.findall(repr(model))
            match = match[0].split(".")[0]

            if match == app_name:
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


def get_input_template(field):
    db_type = field.get("db_type")
    if db_type not in FORM_TRANSLATION:
        raise FieldNotSupported()
    template = FORM_TRANSLATION[db_type]

    return template


def get_csrf_token(request):
    csrf_token = get_token(request)
    template = InputTemplate(type="hidden")
    return Input(template=template, field_name="csrfmiddlewaretoken", value=csrf_token)


def get_submit_button(value="Submit"):
    template = InputTemplate(type="submit", tag="button")
    return Input(template=template, field_name="form_submit", value=value)


def render_model_form(request, app_name, model_name, instance):
    definitions = get_model_definitions(app_name)

    if model_name not in definitions:
        raise DefinitionNotFound(model_name)

    definition = definitions[model_name]

    action = f"/coffee/form/submit/?app_name={app_name}&model_name={model_name}"

    children = []
    for name, field in definition.items():
        template = get_input_template(field)
        value = getattr(instance, name, None)
        item = Input(field_name=name, template=template, value=value)
        children.append(item)

    children.append(get_csrf_token(request))

    button_text = "Submit"
    if instance:
        button_text = "Update"

    children.append(get_submit_button(button_text))

    form = Form(children=children, action=action)

    delete_button = ""
    if instance:
        delete_button = get_delete_button_html(request, app_name, model_name, instance)

    return str(form) + str(delete_button)


def render_model_table(cls, queryset, pagination):
    keys = [i.name for i in cls._meta.fields]
    headers = [Td(i) for i in keys]
    thead = THead(value=TRow(children=headers))

    trs = []
    for row in queryset:
        row_dict = model_to_dict(row)
        tds = []
        for key in keys:
            tds.append(Td(value=row_dict.get(key)))
        trs.append(TRow(children=tds))

    tbody = TBody(children=trs)
    pagination_html = Pagination(pagination=pagination)

    return str(Table(tbody=tbody, thead=thead)) + str(pagination_html)


def get_delete_button_html(request, app_name, model_name, pk):
    action = f"/coffee/delete/?app_name={app_name}&model_name={model_name}&pk={pk}"
    children = [get_csrf_token(request), get_submit_button("Delete")]
    form = Form(action=action, children=[children])
    return form
