from django.db import models

class Section(models.Model):
    order = models.IntegerField(default=1)
    title = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.title
