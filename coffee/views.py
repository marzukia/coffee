import json
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from coffee.contrib.parse.functions import get_pagination
from coffee.contrib.decorators import get_only, post_only, render_view
from coffee.contrib.render.functions import (
    render_model_form,
    render_model_table,
)


@staff_member_required
@get_only
@render_view
def get_model_list(
    request,
    app_name=None,
    model_name=None,
    pk=None,
    json=None,
    page_size=None,
    page=None,
    pagination=None,
    *args,
    **kwargs,
):
    offset = (page - 1) * page_size

    cls = apps.get_model(app_name, model_name)
    queryset = cls.objects.all()[offset : offset + page_size]

    pagination_json = get_pagination(
        request=request, cls=cls, page_size=page_size, page=page
    )

    html = render_model_table(
        cls=cls,
        queryset=queryset,
        pagination=None if not pagination else pagination_json,
    )

    if json:
        return JsonResponse({"html": html, "pagination": pagination_json})

    return HttpResponse(html)


@staff_member_required
@get_only
@render_view
def get_model_form(
    request,
    app_name=None,
    model_name=None,
    pk=None,
    json=None,
    cls=None,
    *args,
    **kwargs,
):
    instance = None
    form_only = request.GET.get("form_only", None)

    if pk:
        try:
            instance = cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            exception = f"pk '{pk}' for '{app_name}.{model_name}' not found"
            return JsonResponse({"error": exception}, status=404)

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
        delete_url = reverse("coffee_delete") + params if pk else None
        return JsonResponse({"html": html, "post": post_url, "delete": delete_url})

    return HttpResponse(html)


@staff_member_required
@post_only
@render_view
def post_model_form(
    request, app_name=None, model_name=None, pk=None, cls=None, *args, **kwargs
):
    pk_field = cls._meta.pk.name

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
@post_only
@render_view
def delete_model_instance(
    request, app_name=None, model_name=None, pk=None, cls=None, *args, **kwargs
):
    if pk:
        instance = cls.objects.get(pk=pk)
        instance.delete()

    base_url = reverse("coffee_form")
    url = base_url + f"?app_name={app_name}&model_name={model_name}"

    return redirect(url)
