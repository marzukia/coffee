from django.http import JsonResponse


def render_view(func):
    def wrapper(request, *args, **kwargs):
        app_name = request.GET.get("app_name")
        model_name = request.GET.get("model_name")
        pk = request.GET.get("pk")
        json = request.GET.get("json", None)
        page_size = int(request.GET.get("page_size", 15))
        page = int(request.GET.get("page", 1))
        pagination = request.GET.get("pagination", None)

        assert app_name is not None, "'app_name' not provided"
        assert model_name is not None, "'model_name' not provided"

        return func(
            request=request,
            app_name=app_name,
            model_name=model_name,
            pk=pk,
            json=json,
            page_size=page_size,
            page=page,
            pagination=pagination,
            *args,
            **kwargs,
        )

    return wrapper


def get_only(func):
    def wrapper(request, *args, **kwargs):
        if request.method not in ["GET", "OPTIONS"]:
            exception = f"'{request.method} is not valid for this endpoint."
            return JsonResponse({"error": exception}, status=405)

        return func(request=request, *args, **kwargs)

    return wrapper


def post_only(func):
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            exception = f"'{request.method} is not valid for this endpoint."
            return JsonResponse({"error": exception}, status=405)

        return func(request=request, *args, **kwargs)

    return wrapper
