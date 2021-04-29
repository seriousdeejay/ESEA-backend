from django.db import models


class Method(models.Model):
    ispublic = models.BooleanField(default=True)
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    created_by = models.ForeignKey('CustomUser', editable=False, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
        
    def __repr__(self):
         return (
             f"<Method id='{self.id}' name='{self.name}' "
             f"description='{self.description}' is_public='{self.ispublic}' "
         )

# organisations = models.ManyToManyField('Organisation', related_name="methods", blank=True)

