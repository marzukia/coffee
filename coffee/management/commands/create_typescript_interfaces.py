from coffee.util.functions import (
    get_model_definitions,
    get_typescript_type,
    to_camel_case,
)
from django.core.management.base import BaseCommand
from structlog import get_logger

logger = get_logger(__name__)

TAB_WIDTH = 4
TAB = " " * TAB_WIDTH


class Command(BaseCommand):
    help = "Converts all models of a target app into TypeScript interfaces"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)

    def handle(self, *args, **options):
        app_name = options["app_name"]
        definitions = get_model_definitions(app_name)

        file_text = ""

        for model_name, definition in definitions.items():
            file_text += f"export interface {model_name} {'{'}\n"
            for field_name, field_details in definition.items():
                db_type = field_details.get("db_type")
                typescript_type = get_typescript_type(db_type)
                camel_case_key = to_camel_case(field_name)
                if field_details.get("nullable"):
                    camel_case_key += "?"
                file_text += f"{TAB}{camel_case_key}: {typescript_type};\n"
            file_text += "}\n\n"

        print(file_text)
