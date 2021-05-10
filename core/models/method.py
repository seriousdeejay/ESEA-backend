from django.db import models


class Method(models.Model):
    created_by = models.ForeignKey('CustomUser', editable=False, on_delete=models.SET_NULL, null=True)

    ispublic = models.BooleanField(default=True) # Change to is_public
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    version = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    def __str__(self):
        return self.name
        
    def __repr__(self):
         return (
             f"<Method id='{self.id}' name='{self.name}' "
             f"description='{self.description}' is_public='{self.ispublic}' "
         )

# organisations = models.ManyToManyField('Organisation', related_name="methods", blank=True)

