# Coffee - Django Admin Tools

`django-coffee-tools` provides a ready-to-use Django plugin which provides dynamic form generation for your Django models. These forms are intended to be integrated with your admin or management dashboard to allow easy management of your application's data.

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
<!-- http://localhost:8000/coffee/form/?app_name=api&model_name=Category&pk=4 -->

<div class="Wrapper">
  <div class="Header">
    <form
      method="POST"
      action="/coffee/delete/4/?app_name=api&model_name=Category"
    >
      <input type="hidden" name="csrfmiddlewaretoken" nbvBvalue="XXX" /><button
        type="submit"
      >
        Delete
      </button>
    </form>
  </div>
  <form
    method="POST"
    class="Form"
    action="/coffee/form/submit/?app_name=api&model_name=Category"
  >
    <div class="FormItem">
      <label for="id">id</label>
      <input type="number" value="4" name="id" />
    </div>

    <div class="FormItem">
      <label for="name">name</label>
      <input type="text" value="Bakery" name="name" />
    </div>

    <div class="FormItem">
      <button type="submit" class="FormButton">Submit</button>
    </div>
    <input type="hidden" name="csrfmiddlewaretoken" value="XXX" />
  </form>
</div>
```

## How to Use

The model form can be used for existing instances of data or be used to create new instances of data.

```
/coffee/form/?app_name=&model_name=&pk=
```

- `app_name`: The name of your Django application, e.g. `api`
- `model_name`: The name of your application model, e.g. `ShoppingItem`. Note, this property is case sensitive.
- `pk`: Optional. The relevant primary key for your selected model.

## Feedback

This project won't move very fast and I've built it mostly for my own projects, if you'd like to contribute, get in touch!
