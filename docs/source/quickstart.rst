Quickstart
==========

.. code-block:: bash

    pip install django-coffee-tools


.. code-block:: python

   INSTALLED_APPS = [
      # ...
      "coffee",
   ]

.. code-block:: python

   urlpatterns = [
      path("admin/", admin.site.urls),
      path("coffee/", include("coffee.urls")),
      path("api/", include("api.urls")),
   ]

