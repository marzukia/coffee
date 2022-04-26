from django.db import models


class CoffeeTestModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        app_label = "tests"
        abstract = True


class SimpleModel(CoffeeTestModel):
    name = models.TextField(blank=True, null=True)
