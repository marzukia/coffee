Introduction to django-coffee-tools
===============================================

``django-coffee-tools`` provides a ready-to-use Django plugin which provides dynamic form generation for your Django models. These forms are intended to be integrated with your admin or management dashboard to allow easy management of your application's data.

The idea behind this package is to provide a plug and play so that you waste less time, and get your admin dashboards up and running quicker.



Installation
************

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


Examples
********

Generate HTML which can be integrated into your frontend.

Model Form
######################################

.. code-block:: html

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

Model List
######################################

.. code-block:: html

   <!-- http://localhost:8008/coffee/list/?app_name=api&model_name=Category&page=1 -->
   <table class="coffee-table">
      <thead class="coffee-table-thead">
         <tr class="coffee-table-tr">
               <th class="coffee-table-th">id</th>
               <th class="coffee-table-th">name</th>
         </tr>
      </thead>
      <tbody class="coffee-table-tbody">
         <tr class="coffee-table-tr" id="1">
               <td class="coffee-table-td">1</td>
               <td class="coffee-table-td">Fruit &amp; Veg</td>
         </tr>
         <tr class="coffee-table-tr" id="3">
               <td class="coffee-table-td">3</td>
               <td class="coffee-table-td">Fridge &amp; Deli</td>
         </tr>
         <tr class="coffee-table-tr" id="4">
               <td class="coffee-table-td">4</td>
               <td class="coffee-table-td">Bakery</td>
         </tr>
         <tr class="coffee-table-tr" id="5">
               <td class="coffee-table-td">5</td>
               <td class="coffee-table-td">Frozen</td>
         </tr>
         <tr class="coffee-table-tr" id="6">
               <td class="coffee-table-td">6</td>
               <td class="coffee-table-td">Pantry</td>
         </tr>
         <tr class="coffee-table-tr" id="7">
               <td class="coffee-table-td">7</td>
               <td class="coffee-table-td">Beer &amp; Wine</td>
         </tr>
         <tr class="coffee-table-tr" id="8">
               <td class="coffee-table-td">8</td>
               <td class="coffee-table-td">Drinks</td>
         </tr>
         <tr class="coffee-table-tr" id="9">
               <td class="coffee-table-td">9</td>
               <td class="coffee-table-td">Health &amp; Body</td>
         </tr>
         <tr class="coffee-table-tr" id="10">
               <td class="coffee-table-td">10</td>
               <td class="coffee-table-td">Household</td>
         </tr>
         <tr class="coffee-table-tr" id="11">
               <td class="coffee-table-td">11</td>
               <td class="coffee-table-td">Baby &amp; Child</td>
         </tr>
         <tr class="coffee-table-tr" id="12">
               <td class="coffee-table-td">12</td>
               <td class="coffee-table-td">Pet</td>
         </tr>
         <tr class="coffee-table-tr" id="15">
               <td class="coffee-table-td">15</td>
               <td class="coffee-table-td">Meat &amp; Seafood</td>
         </tr>
      </tbody>
   </table>

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   source/coffee

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
