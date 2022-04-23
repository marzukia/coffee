from coffee.util.contrib.render import InputTemplate


TYPESCRIPT_TRANSLATION = {
    "AutoField": "number",
    "BigAutoField": "number",
    "BigIntegerField": "number",
    "BinaryField": "number",
    "BooleanField": "boolean",
    "CharField": "text",
    "CommaSeparatedIntegerField": "number",
    "DateField": "Date",
    "DateTimeField": "Date",
    "DecimalField": "number",
    "DurationField": "number",
    "EmailField": "text",
    "FilePathField": "text",
    "FloatField": "number",
    "GenericIPAddressField": "text",
    "IPAddressField": "text",
    "IntegerField": "number",
    "NullBooleanField": "boolean | null",
    "PositiveBigIntegerField": "number",
    "PositiveIntegerField": "number",
    "PositiveSmallIntegerField": "number",
    "SlugField": "string",
    "SmallAutoField": "number",
    "SmallIntegerField": "number",
    "TextField": "string",
    "TimeField": "string",
    "URLField": "string",
    "UUIDField": "string",
    "ForeignKey": "number",
    "OneToOneField": "number",
}

FORM_TRANSLATION = {
    "AutoField": InputTemplate(type="number", tag="input"),
    "BigAutoField": InputTemplate(type="number", tag="input"),
    "BigIntegerField": InputTemplate(type="number", tag="input"),
    "BinaryField": InputTemplate(type="number", tag="input"),
    "BooleanField": InputTemplate(type="checkbox", tag="input"),
    "CharField": InputTemplate(type="text", tag="input"),
    "CommaSeparatedIntegerField": InputTemplate(type="number", tag="input"),
    "DateField": InputTemplate(type="date", tag="input"),
    "DateTimeField": InputTemplate(type="datetime-local", tag="input"),
    "DecimalField": InputTemplate(type="number", tag="input"),
    "DurationField": InputTemplate(type="number", tag="input"),
    "EmailField": InputTemplate(type="text", tag="input"),
    "FilePathField": InputTemplate(type="text", tag="input"),
    "FloatField": InputTemplate(type="number", tag="input"),
    "GenericIPAddressField": InputTemplate(type="text", tag="input"),
    "IPAddressField": InputTemplate(type="text", tag="input"),
    "IntegerField": InputTemplate(type="number", tag="input"),
    "NullBooleanField": InputTemplate(type="checkbox", tag="input"),
    "PositiveBigIntegerField": InputTemplate(type="number", tag="input"),
    "PositiveIntegerField": InputTemplate(type="number", tag="input"),
    "PositiveSmallIntegerField": InputTemplate(type="number", tag="input"),
    "SlugField": InputTemplate(type="text", tag="input"),
    "SmallAutoField": InputTemplate(type="number", tag="input"),
    "SmallIntegerField": InputTemplate(type="number", tag="input"),
    "TextField": InputTemplate(type="text", tag="textarea"),
    "TimeField": InputTemplate(type="text", tag="input"),
    "URLField": InputTemplate(type="text", tag="input"),
    "UUIDField": InputTemplate(type="text", tag="input"),
    "ForeignKey": InputTemplate(type="number", tag="input"),
    "OneToOneField": InputTemplate(type="number", tag="input"),
}
