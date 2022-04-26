from django.test import RequestFactory, TestCase, override_settings
from django.urls import include, path
from django.contrib.auth.models import User

from coffee.views import get_model_form


urlpatterns = [path("coffee/", include("coffee.urls"))]


@override_settings(ROOT_URLCONF="tests.test_views")
class ModelFormViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="dog", is_staff=True)
        self.non_staff_user = User.objects.create(username="cat", is_staff=False)

    def test_model_form_view(self):
        request = self.factory.get(
            "/coffee/form/?app_name=tests&model_name=SimpleModel"
        )
        request.user = self.user
        response = get_model_form(request)
        self.assertEqual(response.status_code, 200)
