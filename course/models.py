from django.db import models

class files(models.Model):
    filename = models.CharField(max_length=20)
    last_update = models.DateField(auto_now= True)