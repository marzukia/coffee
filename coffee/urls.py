from django.urls import path

from coffee.views import (
    delete_model_instance,
    get_model_form,
    get_model_list,
    post_model_form,
)


urlpatterns = [
    path("form/", get_model_form, name="form"),
    path("form/submit/", post_model_form, name="submit_form"),
    path("delete/", delete_model_instance, name="delete"),
    path("list/", get_model_list, name="list"),
]
