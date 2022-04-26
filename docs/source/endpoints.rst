Endpoints
=========

/coffee/form/
#############

Creates a model form for a specified model within an application. If a ``pk`` is passed, that particular instance is loaded.

Args:
    - request (:py:class:`HttpRequest`)
    - app_name (``string``, optional): Name of application, case-sensitive. Defaults to ``None``.
    - model_name (``string``, optional): Name of model, case-sensitive. Defaults to ``None``.
    - pk (``int``, optional): Primary key of the model instance you want to modify. Defaults to ``None``.
    - json (``true``, optional): Entered as ``json=true``, data is returned as ``json`` object instead of a ``html`` object. Defaults to ``None``.

**Returns**:

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


.. code-block:: json

    {
        "html": "<form action='/coffee/form/submit/?app_name=api&model_name=Category' method='POST' class='coffee-form'><div class='coffee-form-item'><label class=coffee-form-item-label for='name'>name</label><textarea value='Frozen' name='name' id='name' type='text' class='coffee-form-item-input'>Frozen</textarea></div><input name=\"csrfmiddlewaretoken\" value=dOE54b8mjNtBj3kWsCQ2qoGXBW3t8R2WEBi1TBrOMFlSfZe7urGF26nKBs7A3TBm type=\"hidden\"/><button type=\"submit\" class=\"coffee-form-submit\">Update</button></form><form action='/coffee/delete/?app_name=api&model_name=Category&pk=5' method='POST' class='coffee-form'><input name=\"csrfmiddlewaretoken\" value=IiJZ6OKEMVW8TRO3clFIIwN84lbmgEAn95nVVe36fNOpPNIeeavlkeuV4RftbG9N type=\"hidden\"/><button type=\"submit\" class=\"coffee-form-submit\">Delete</button></form>",
        "post": "/coffee/form/submit/?app_name=api&model_name=Category&pk=5",
        "delete": "/coffee/delete/?app_name=api&model_name=Category&pk=5"
    }


/coffee/list/
#############

Creates a paginated list for a specified model within an application.

Args:
    - request (:py:class:`HttpRequest`)
    - app_name (``string``, optional): Name of application, case-sensitive. Defaults to ``None``.
    - model_name (``string``, optional): Name of model, case-sensitive. Defaults to ``None``.
    - json (``true``, optional): Primary key of the model instance you want to modify. Defaults to ``None``.
    - page_size (``number``, optional): Number of records per page. Defaults to ``None``.
    - page (``number``, optional): Offsets the queryset by the specified page. Defaults to ``None``.
    - pagination (``true``, optional): Enables pagination to be rendered within the returned list. Defaults to ``None``.

**Returns**:

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

.. code-block:: json

    {
        "html": "<table class='coffee-table'><thead class='coffee-table-thead'><tr class='coffee-table-tr'><th class='coffee-table-th'>id</th><th class='coffee-table-th'>name</th></tr></thead><tbody class='coffee-table-tbody'><tr class='coffee-table-tr' id='1'><td class='coffee-table-td'>1</td><td class='coffee-table-td'>Fruit & Veg</td></tr><tr class='coffee-table-tr' id='3'><td class='coffee-table-td'>3</td><td class='coffee-table-td'>Fridge & Deli</td></tr><tr class='coffee-table-tr' id='4'><td class='coffee-table-td'>4</td><td class='coffee-table-td'>Bakery</td></tr><tr class='coffee-table-tr' id='5'><td class='coffee-table-td'>5</td><td class='coffee-table-td'>Frozen</td></tr><tr class='coffee-table-tr' id='6'><td class='coffee-table-td'>6</td><td class='coffee-table-td'>Pantry</td></tr><tr class='coffee-table-tr' id='7'><td class='coffee-table-td'>7</td><td class='coffee-table-td'>Beer & Wine</td></tr><tr class='coffee-table-tr' id='8'><td class='coffee-table-td'>8</td><td class='coffee-table-td'>Drinks</td></tr><tr class='coffee-table-tr' id='9'><td class='coffee-table-td'>9</td><td class='coffee-table-td'>Health & Body</td></tr><tr class='coffee-table-tr' id='10'><td class='coffee-table-td'>10</td><td class='coffee-table-td'>Household</td></tr><tr class='coffee-table-tr' id='11'><td class='coffee-table-td'>11</td><td class='coffee-table-td'>Baby & Child</td></tr><tr class='coffee-table-tr' id='12'><td class='coffee-table-td'>12</td><td class='coffee-table-td'>Pet</td></tr><tr class='coffee-table-tr' id='15'><td class='coffee-table-td'>15</td><td class='coffee-table-td'>Meat & Seafood</td></tr></tbody></table>",
        "pagination": {
            "previous": null,
            "next": null,
            "current_page": 1,
            "number_of_pages": 1,
            "count": 12
        }
    }

