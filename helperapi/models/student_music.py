from django.db import models

class StudentMusic(models.Model):

    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    music = models.ForeignKey("Music", on_delete=models.CASCADE)