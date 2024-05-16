from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    agree = models.IntegerField(default = 0)
    disagree = models.IntegerField(default = 0)
    agreeRate = models.DecimalField(max_digits=5,decimal_places=4,default = 0.0000)
    disagreeRate = models.DecimalField(max_digits=5,decimal_places=4,default = 0.0000)
    createAt = models.DateTimeField(auto_now_add=True)

