from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey("School", on_delete=models.CASCADE)
    prop = models.ForeignKey("Prop", on_delete=models.CASCADE)
    uniform = models.ForeignKey("Uniform", on_delete=models.CASCADE)
    instrument = models.ForeignKey("Instrument", on_delete=models.CASCADE)
    music_parts = models.ManyToManyField("Music", through="StudentMusic")


    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'