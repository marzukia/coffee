from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
)
from django.shortcuts import redirect
from coffee.contrib.parse.functions import get_pagination

from coffee.contrib.decorators import has_sufficient_params
from coffee.contrib.render.functions import (
    render_model_form,
    render_model_table,
)


@staff_member_required
@has_sufficient_params
def get_model_list(request, app_name=None, model_name=None, pk=None):
    page_size = int(request.GET.get("page_size", 15))
    page = int(request.GET.get("page", 1))

    offset = (page - 1) * page_size

    cls = apps.get_model(app_name, model_name)
    queryset = cls.objects.all()[offset : offset + page_size]

    pagination = get_pagination(request, cls, page_size, page)

    html = render_model_table(cls, queryset, pagination)

    return HttpResponse(html)


@staff_member_required
@has_sufficient_params
def get_model_form(request, app_name=None, model_name=None, pk=None):
    instance = None

    cls = None
    if pk:
        try:
            cls = apps.get_model(app_name, model_name)
            instance = cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            exception = f"pk '{pk}' for '{app_name}.{model_name}' not found"
            return HttpResponseBadRequest(exception)

    html = render_model_form(request, app_name, model_name, instance)

    return HttpResponse(html)


@staff_member_required
@has_sufficient_params
def post_model_form(request, app_name=None, model_name=None, pk=None):
    cls = apps.get_model(app_name, model_name)
    pk_field = cls._meta.pk.name

    if request.method != "POST":
        return HttpResponseNotAllowed(
            f"'{request.method} is not valid for this endpoint."
        )

    data = {
        k: None if v == "" else v
        for k, v in request.POST.copy().items()
        if k != "csrfmiddlewaretoken"
    }
    pk = data.get(pk_field)

    if not pk:
        instance, _ = cls.objects.get_or_create(**data)
        pk = instance.pk

    if pk:
        instance = cls.objects.get(pk=pk)
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()

    url = f"/coffee/form/?app_name={app_name}&model_name={model_name}&pk={pk}"

    return redirect(url)


@staff_member_required
@has_sufficient_params
def delete_model_instance(request, app_name=None, model_name=None, pk=None):
    cls = apps.get_model(app_name, model_name)

    if request.method != "POST":
        return HttpResponseNotAllowed(
            f"'{request.method} is not valid for this endpoint."
        )

    if pk:
        instance = cls.objects.get(pk=pk)
        instance.delete()

    url = f"/coffee/form/?app_name={app_name}&model_name={model_name}"

    return redirect(url)
