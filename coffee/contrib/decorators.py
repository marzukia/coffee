from django.http import JsonResponse
from django.apps import apps

from functools import wraps


def render_view(func):
    """
    Decorator function to consistently package :py:class:`HttpRequest` parameters into named kwargs.

    Function sets the following kwargs:
        - :py:attr:`app_name`: name of the application, case sensitive.
        - :py:attr:`model_name`: name of the application, case sensitive.
        - :py:attr:`pk`: pk of the model class
        - :py:attr:`json`: ``json=true``, return pure rendered html or return html in a json
        - :py:attr:`page_size`: default size 15 (applies to :py:class:`ModelFormList`)
        - :py:attr:`page`: default page = 1 (applies to :py:class:`ModelFormList`)
        - :py:attr:`pagination`: render pagination in form or not

    Returns:
        :py:class:`JsonResponse` or :py:meth:`view_function`.

    Usage:
        .. code-block:: python

            @get_only
            def foo(request):
                return 'bar'

    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        app_name = request.GET.get("app_name")
        model_name = request.GET.get("model_name")
        pk = request.GET.get("pk")
        json = request.GET.get("json", None)
        page_size = int(request.GET.get("page_size", 15))
        page = int(request.GET.get("page", 1))
        pagination = request.GET.get("pagination", None)
        cls = apps.get_model(app_name, model_name)

        try:
            assert app_name is not None, "'app_name' not provided"
            assert model_name is not None, "'model_name' not provided"
            apps.get_app_config(app_name)
            apps.get_model(app_name, model_name)
        except (AssertionError, LookupError) as exception:
            return JsonResponse({"error": str(exception)}, status=400)

        return func(
            request=request,
            app_name=app_name,
            model_name=model_name,
            pk=pk,
            json=json,
            page_size=page_size,
            page=page,
            pagination=pagination,
            cls=cls,
            *args,
            **kwargs,
        )

    return wrapper


def get_only(func):
    """
    Decorator function to only allow GET requests, anything else will return a 405.

    Returns:
        :py:class:`JsonResponse` or :py:meth:`view_function`.

    Usage:
        .. code-block:: python

            @get_only
            def foo(request):
                return 'bar'
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

    Returns:
        :py:class:`JsonResponse` or :py:meth:`view_function`.

    Usage:
        .. code-block:: python

            @post_only
            def foo(request):
                return 'bar'
    """

    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            exception = f"'{request.method} is not valid for this endpoint."
            return JsonResponse({"error": exception}, status=405)

        return func(request=request, *args, **kwargs)

    return wrapper
