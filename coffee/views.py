from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
)
from django.shortcuts import redirect

from coffee.util.decorators import has_sufficient_params
from coffee.util.functions import (
    get_delete_button_html,
    render_model_form_html,
)


@staff_member_required
@has_sufficient_params
def get_model_form(request):
    app_name = request.GET.get("app_name")
    model_name = request.GET.get("model_name")
    pk = request.GET.get("pk")

    instance = None

    if pk:
        try:
            cls = apps.get_model(app_name, model_name)
            instance = cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            exception = f"pk '{pk}' for '{app_name}.{model_name}' not found"
            return HttpResponseBadRequest(exception)

    html = "<div class='Wrapper'>\n"
    html += "<div class='Header'>\n"
    if instance:
        html += get_delete_button_html(request, app_name, model_name) % instance.pk
    html += "</div>"
    html += render_model_form_html(request, app_name, model_name, instance)
    html += "</div>"

    return HttpResponse(html)


@staff_member_required
@has_sufficient_params
def post_model_form(request):
    app_name = request.GET.get("app_name")
    model_name = request.GET.get("model_name")

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
def delete_model_instance(request, pk=None):
    app_name = request.GET.get("app_name")
    model_name = request.GET.get("model_name")

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
