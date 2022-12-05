from django.db import models

class Music(models.Model):

    school = models.ForeignKey("School", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    part = models.CharField(max_length=30)
    assigned = models.BooleanField(default=False)