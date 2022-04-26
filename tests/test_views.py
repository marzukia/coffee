from django.test import RequestFactory, TestCase, override_settings
from django.urls import include, path
from django.contrib.auth.models import User
from django.contrib import admin

from coffee.views import (
    delete_model_instance,
    get_model_form,
    get_model_list,
    post_model_form,
)

import json


urlpatterns = [path("coffee/", include("coffee.urls")), path("admin/", admin.site.urls)]


@override_settings(ROOT_URLCONF="tests.test_views")
class ModelFormViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="dog", is_staff=True)
        self.non_staff_user = User.objects.create(username="cat", is_staff=False)
        self.url = "/coffee/form/?app_name=tests&model_name=SimpleModel"

    def test_model_form_view_with_staff_user(self):
        request = self.factory.get(self.url)
        request.user = self.user
        response = get_model_form(request)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        self.assertEqual(type(content), str)
        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(content)

    def test_model_form_view_with_non_staff_user(self):
        request = self.factory.get(self.url)
        request.user = self.non_staff_user
        response = get_model_form(request)
        self.assertEqual(response.status_code, 302)

        redirect = str(response["Location"])
        expected = "/admin/login/"
        self.assertEqual(expected in redirect, True)

    def test_model_form_view_with_post(self):
        request = self.factory.post(self.url)
        request.user = self.user
        response = get_model_form(request)
        self.assertEqual(response.status_code, 405)

    def test_model_form_view_with_json(self):
        request = self.factory.get(self.url + "&json=true")
        request.user = self.user
        response = get_model_form(request)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        data = json.loads(content)

        self.assertEqual(type(content), str)
        self.assertEqual(type(data), dict)
        self.assertIn("html", data.keys())
        self.assertIn("post", data.keys())
        self.assertIn("delete", data.keys())

    def test_model_form_view_does_not_render_pk(self):
        request = self.factory.get(self.url)
        request.user = self.user
        response = get_model_form(request)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        self.assertAlmostEqual('name="id"' not in content, True)

    def test_model_form_view_returns_correct_post(self):
        request = self.factory.get(self.url + "&json=true")
        request.user = self.user
        response = get_model_form(request)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        data = json.loads(content)

        post = data["post"]
        delete = data["delete"]

        self.assertEqual(
            post,
            "/coffee/form/submit/?app_name=tests&model_name=SimpleModel&pk=None",
        )

        self.assertEqual(
            delete,
            None,
        )

    def test_model_form_with_form_only(self):
        request = self.factory.get(self.url + "&form_only=true")
        request.user = self.user
        response = get_model_form(request)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")

        self.assertEqual("button" not in content, True)


@override_settings(ROOT_URLCONF="tests.test_views")
class ModelListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="dog", is_staff=True)
        self.non_staff_user = User.objects.create(username="cat", is_staff=False)
        self.url = "/coffee/list/?app_name=tests&model_name=SimpleModel"

    def test_model_list_view_with_staff_user(self):
        request = self.factory.get(self.url)
        request.user = self.user
        response = get_model_list(request)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        self.assertEqual(type(content), str)
        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(content)

    def test_model_list_view_with_non_staff_user(self):
        request = self.factory.get(self.url)
        request.user = self.non_staff_user
        response = get_model_list(request)
        self.assertEqual(response.status_code, 302)

        redirect = str(response["Location"])
        expected = "/admin/login/"
        self.assertEqual(expected in redirect, True)


@override_settings(ROOT_URLCONF="tests.test_views")
class PostModelFormViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="dog", is_staff=True)
        self.non_staff_user = User.objects.create(username="cat", is_staff=False)
        self.url = "/coffee/form/submit/?app_name=tests&model_name=SimpleModel"

    def test_model_list_view_with_staff_user(self):
        request = self.factory.post(self.url)
        request.user = self.user
        response = post_model_form(request)

        self.assertEqual(response.status_code, 302)

        content = response.content.decode("utf-8")
        self.assertEqual(type(content), str)
        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(content)

    def test_model_list_view_with_non_staff_user(self):
        request = self.factory.post(self.url)
        request.user = self.non_staff_user
        response = post_model_form(request)

        self.assertEqual(response.status_code, 302)

        redirect = str(response["Location"])
        expected = "/admin/login/"
        self.assertEqual(expected in redirect, True)


@override_settings(ROOT_URLCONF="tests.test_views")
class DeleteModelInstanceViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="dog", is_staff=True)
        self.non_staff_user = User.objects.create(username="cat", is_staff=False)
        self.url = "/coffee/delete/?app_name=tests&model_name=SimpleModel"

    def test_model_list_view_with_staff_user(self):
        request = self.factory.post(self.url)
        request.user = self.user
        response = delete_model_instance(request)

        self.assertEqual(response.status_code, 302)

        content = response.content.decode("utf-8")
        self.assertEqual(type(content), str)
        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(content)

    def test_model_list_view_with_non_staff_user(self):
        request = self.factory.post(self.url)
        request.user = self.non_staff_user
        response = delete_model_instance(request)

        self.assertEqual(response.status_code, 302)

        redirect = str(response["Location"])
        expected = "/admin/login/"
        self.assertEqual(expected in redirect, True)
