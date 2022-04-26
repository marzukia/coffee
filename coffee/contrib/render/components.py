from typing import List


class InputTemplate:
    type: str
    tag: str
    implemented: bool
    disabled: bool

    def __init__(self, type="text", tag="input", implemented=True, disabled=False):
        self.tag = tag
        self.type = type
        self.implemented = implemented
        self.disabled = disabled


class HTMLComponent:
    tag = None
    value = None
    children = []
    properties = {}
    class_name = None

    def __init__(self, value=None, children=None, class_name=None):
        self.value = value
        if children:
            self.value = "".join([str(i) for i in children])

        if class_name:
            self.class_name = class_name

    def get_template(self):
        self.properties["class"] = self.class_name
        props = " ".join([f"{k}='{v}'" for k, v in self.properties.items() if v])
        return f"<{self.tag} {props}>{self.value or ''}</{self.tag}>"

    def __str__(self):
        return self.get_template()


class Div(HTMLComponent):
    tag = "div"


class InputLabel(HTMLComponent):
    tag = "label"
    field_name: str = None
    class_name = "coffee-form-item-label"

    def get_template(self):
        return f"<label class={self.class_name} for='{self.value}'>{self.value}</label>"


class Input(HTMLComponent):
    template: InputTemplate
    field_name: str
    class_name = "coffee-form-item-input"

    def __init__(self, template, field_name, value=None):
        self.field_name = field_name
        self.value = value
        self.tag = template.tag
        self.type = template.type

    def get_template(self):
        value = self.value or ""
        if self.type == "datetime-local" and self.value:
            value = self.value.strftime("%Y-%m-%dT%H:%M")

        self.properties = {
            "value": value or "",
            "name": self.field_name,
            "id": self.field_name,
            "type": self.type,
            "class": self.class_name,
        }
        props = " ".join([f"{k}='{v}'" for k, v in self.properties.items() if v])

        label_html = str(InputLabel(value=self.field_name))
        if self.type == "hidden" or self.tag == "button":
            label_html = ""

        input_html = f"<{self.tag} {props}></{self.tag}>"
        if self.tag == "textarea" or self.tag == "button":
            input_html = f"<{self.tag} {props}>{value}</{self.tag}>"

        html = str(Div(children=[label_html, input_html], class_n="coffee-form-item"))

        return html


class CSRFToken(HTMLComponent):
    class_name = "coffee-form-item-input"

    def get_template(self):
        return f'<input name="csrfmiddlewaretoken" value={self.value} type="hidden"/>'


class SubmitButton(HTMLComponent):
    class_name = "coffee-form-submit"

    def get_template(self):
        return f'<button type="submit" class="{self.class_name}">{self.value}</button>'


class THead(HTMLComponent):
    tag = "thead"
    children = []
    class_name = "coffee-table-thead"


class TBody(HTMLComponent):
    tag = "tbody"
    children = []
    class_name = "coffee-table-tbody"

    def __init__(self, children):
        if children:
            self.value = "".join([str(i) for i in children])


class Td(HTMLComponent):
    tag = "td"
    class_name = "coffee-table-td"


class Th(HTMLComponent):
    tag = "td"
    class_name = "coffee-table-th"


class TRow(HTMLComponent):
    tag = "tr"
    class_name = "coffee-table-tr"


class Table(HTMLComponent):
    tag = "table"
    thead: THead
    tbody: TBody
    class_name = "coffee-table"

    def __init__(self, thead=None, tbody=None):
        self.thead = str(thead)
        self.tbody = str(tbody)
        self.value = self.thead + self.tbody

    def get_template(self):
        return super().get_template()

    def __str__(self):
        return self.get_template()


class Form(HTMLComponent):
    action: str
    children: List[Input]
    tag = "form"
    class_name = "coffee-form"

    def __init__(self, children, action, method="POST"):
        if children:
            self.value = "".join([str(i) for i in children])

        self.properties = {
            "action": action,
            "method": method,
        }


class PaginationButton(HTMLComponent):
    class_name = "coffee-pagination-button"
    tag = "a"
    href: str

    def __init__(self, href=None, value=None):
        self.value = value
        self.properties = {"href": href}

        if not href:
            self.properties["disabled"] = "true"


class PaginationText(HTMLComponent):
    class_name = "coffee-pagination-text"
    tag = "span"


class Pagination(HTMLComponent):
    class_name = "coffee-pagination"
    tag = "div"

    def __init__(self, pagination):
        previous = pagination.get("previous")
        next = pagination.get("next")
        number_of_pages = pagination.get("number_of_pages")
        current_page = pagination.get("current_page")

        children = [
            PaginationButton(href=previous, value="previous"),
            PaginationText(value=f"{current_page} / {number_of_pages}"),
            PaginationButton(href=next, value="next"),
        ]
        if children:
            self.value = "".join([str(i) for i in children])
