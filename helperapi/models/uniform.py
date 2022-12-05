from django.db import models

class Uniform(models.Model):

    school = models.ForeignKey("School", on_delete=models.CASCADE)
    uniform_number = models.PositiveIntegerField(null=True)
    size = models.CharField(max_length=30)
    assigned = models.BooleanField(default=False)
    out_for_cleaning = models.BooleanField(default=False)