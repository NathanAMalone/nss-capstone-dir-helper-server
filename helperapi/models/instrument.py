from django.db import models

class Instrument(models.Model):

    school = models.ForeignKey("School", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    serial_number = models.PositiveIntegerField(null=True)
    out_for_repair = models.BooleanField(default=False)
    school_owned = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)
