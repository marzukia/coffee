from django.urls import path

from coffee.views import delete_model_instance, get_model_form, post_model_form


urlpatterns = [
    path("form/", get_model_form, name="form"),
    path("form/submit/", post_model_form, name="submit_form"),
    path("delete/<int:pk>/", delete_model_instance, name="delete"),
]
