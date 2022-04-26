# [Coffee - Django Admin Tools](http://django-coffee-tools.readthedocs.io/)

[![codecov](https://codecov.io/gh/marzukia/coffee/branch/main/graph/badge.svg?token=9G8LWAAQ81)](https://codecov.io/gh/marzukia/coffee)
[![Documentation Status](https://readthedocs.org/projects/django-coffee-tools/badge/?version=latest)](https://django-coffee-tools.readthedocs.io/en/latest/?badge=latest)

`django-coffee-tools` provides a ready-to-use Django plugin which provides dynamic form generation for your Django models. These forms are intended to be integrated with your admin or management dashboard to allow easy management of your application's data.

### Quicklinks

-   [Documentation](http://django-coffee-tools.readthedocs.io/)

## Why Coffee?

Plug and play - waste less time making views to manage your application's data.

### Quick Install

```py
INSTALLED_APPS = [
    # ...
    "coffee",
]
```

```py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("coffee/", include("coffee.urls")),
    path("api/", include("api.urls")),
]
```

### Ready to Go!

Generate HTML which can be integrated into your frontend.

```html
<!-- http://localhost:8008/coffee/form/?app_name=api&model_name=Category&pk=5 -->

<form
    action="/coffee/form/submit/?app_name=api&amp;model_name=Category"
    method="POST"
    class="coffee-form"
>
    <div class="coffee-form-item">
        <label class="coffee-form-item-label" for="name">name</label
        ><textarea
            value="Frozen"
            name="name"
            id="name"
            type="text"
            class="coffee-form-item-input"
        >
Frozen</textarea
        >
    </div>
    <input
        name="csrfmiddlewaretoken"
        value="lWqQXylYRShwQcRxbYCyxrTTOMci1Pv3MJ4MMYEqkK9NM8LIdNsb99AGOigpWR4t"
        type="hidden"
    /><button type="submit" class="coffee-form-submit">Update</button>
</form>
```

## How to Use

The model form can be used for existing instances of data or be used to create new instances of data.

```
/coffee/form/?app_name=&model_name=&pk=
```

-   `app_name`: The name of your Django application, e.g. `api`
-   `model_name`: The name of your application model, e.g. `ShoppingItem`. Note, this property is case sensitive.
-   `pk`: Optional. The relevant primary key for your selected model.

## Feedback

This project won't move very fast and I've built it mostly for my own projects, if you'd like to contribute, get in touch!
