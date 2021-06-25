from django.db import models

class TextFragment(models.Model):
    section = models.ForeignKey('Section', related_name='text_fragments', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    text = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.text