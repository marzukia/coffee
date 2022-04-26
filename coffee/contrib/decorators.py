from django.http import JsonResponse


def render_view(func):
    """
    Decorator function to consistently package :py:class:`HttpRequest` parameters into named kwargs.

    Function sets :py:attr:`app_name`, :py:attr:`model_name`, :py:attr:`pk`, :py:attr:`json`, :py:attr:`page_size`, :py:attr:`page`, :py:attr:`pagination`.

    Args:
        func ({ :py:meth:`view_function` }): :py:class:`JsonResponse` or :py:meth:`view_function` output.
    """

    def wrapper(request, *args, **kwargs):
        app_name = request.GET.get("app_name")
        model_name = request.GET.get("model_name")
        pk = request.GET.get("pk")
        json = request.GET.get("json", None)
        page_size = int(request.GET.get("page_size", 15))
        page = int(request.GET.get("page", 1))
        pagination = request.GET.get("pagination", None)

        try:
            assert app_name is not None, "'app_name' not provided"
            assert model_name is not None, "'model_name' not provided"
        except AssertionError as exception:
            return JsonResponse({"error": repr(exception)}, status=400)

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
    """
    Decorator function to only allow GET requests, anything else will return a 405.

    Args:
        func ({ :py:meth:`view_function` }): :py:class:`JsonResponse` or :py:meth:`view_function` output.
    """

    def wrapper(request, *args, **kwargs):
        if request.method not in ["GET", "OPTIONS"]:
            exception = f"'{request.method} is not valid for this endpoint."
            return JsonResponse({"error": exception}, status=405)

        return func(request=request, *args, **kwargs)

    return wrapper


def post_only(func):
    """
    Decorator function to only allow POST requests, anything else will return a 405.

    Args:
        func ({ :py:meth:`view_function` }): :py:class:`JsonResponse` or :py:meth:`view_function` output.
    """

    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            exception = f"'{request.method} is not valid for this endpoint."
            return JsonResponse({"error": exception}, status=405)

        return func(request=request, *args, **kwargs)

    return wrapper
