def has_sufficient_params(func):
    def wrapper(request, *args, **kwargs):
        app_name = request.GET.get("app_name")
        model_name = request.GET.get("model_name")
        pk = request.GET.get("pk")

        assert app_name is not None, "'app_name' not provided"
        assert model_name is not None, "'model_name' not provided"

        return func(
            request=request,
            app_name=app_name,
            model_name=model_name,
            pk=pk,
            *args,
            **kwargs
        )

    return wrapper
