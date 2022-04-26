from django.urls import path

from coffee.views import (
    delete_model_instance,
    get_model_form,
    get_model_list,
    post_model_form,
)


urlpatterns = [
    path("form/", get_model_form, name="coffee_form"),
    path("form/submit/", post_model_form, name="coffee_post"),
    path("delete/", delete_model_instance, name="coffee_delete"),
    path("list/", get_model_list, name="coffee_list"),
]
