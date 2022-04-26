import json
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    JsonResponse,
)
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
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
    json = request.GET.get("json", None)
    pagination = request.GET.get("pagination", None)

    offset = (page - 1) * page_size

    cls = apps.get_model(app_name, model_name)
    queryset = cls.objects.all()[offset : offset + page_size]

    pagination_json = get_pagination(request, cls, page_size, page)

    html = render_model_table(
        cls, queryset, None if not pagination else pagination_json
    )

    if json:
        return JsonResponse({"html": html, "pagination": pagination_json})

    return HttpResponse(html)


@staff_member_required
@has_sufficient_params
def get_model_form(request, app_name=None, model_name=None, pk=None):
    instance = None

    json = request.GET.get("json", None)
    form_only = request.GET.get("form_only", None)

    cls = None
    if pk:
        try:
            cls = apps.get_model(app_name, model_name)
            instance = cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            exception = f"pk '{pk}' for '{app_name}.{model_name}' not found"
            return HttpResponseBadRequest(exception)

    html = render_model_form(
        request=request,
        app_name=app_name,
        model_name=model_name,
        instance=instance,
        form_only=form_only,
    )

    if json:
        params = f"?app_name={app_name}&model_name={model_name}&pk={pk}"
        post_url = reverse("coffee_post") + params
        delete_url = reverse("coffee_delete") + params
        return JsonResponse({"html": html, "post": post_url, "delete": delete_url})

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

    data = request.POST.copy()
    if data.keys() == 0:
        data = json.loads(request.body.decode("utf-8"))

    data = {
        k: None if v == "" else v for k, v in data.items() if k != "csrfmiddlewaretoken"
    }
    pk = data.get(pk_field)

    if not pk:
        for key, value in data.items():
            field = cls._meta.get_field(key)
            if hasattr(field, "auto_now_add"):
                if not value:
                    data[key] = timezone.now()
            fk_cls = field.related_model
            if fk_cls:
                data[key] = fk_cls.objects.get(pk=value)
        instance, _ = cls.objects.get_or_create(**data)
        pk = instance.pk

    if pk:
        instance = cls.objects.get(pk=pk)
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()

    base_url = reverse("coffee_form")
    url = base_url + f"?app_name={app_name}&model_name={model_name}&pk={pk}"

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

    base_url = reverse("coffee_form")
    url = base_url + f"?app_name={app_name}&model_name={model_name}"

    return redirect(url)
