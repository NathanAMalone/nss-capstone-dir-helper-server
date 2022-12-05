from django.db import models

class Prop(models.Model):

    school = models.ForeignKey("School", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    assigned = models.BooleanField(default=False)