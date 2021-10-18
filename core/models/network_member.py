from django.db import models


class NetworkMember(models.Model):
    network = models.ForeignKey('Network', related_name='teammembers', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', related_name='teams', on_delete=models.CASCADE)
    
    PENDING = "pending"
    ACCEPTED = "accepted"
    DENIED = "denied"

    STATUS_OPTIONS = (
        (PENDING, "pending"),
        (ACCEPTED, "accepted"),
        (DENIED, "denied")
    )
    invitation = models.CharField(max_length=100, blank=False, choices=STATUS_OPTIONS, default=PENDING)

    NETWORKADMIN = 2
    GUEST = 1 

    ROLES = (
        (NETWORKADMIN, "network admin"),
        (GUEST, "guest"),
        # Add in more status options
    )
    role = models.IntegerField(blank=False, choices=ROLES, default=GUEST)

    def __str__(self):
        return f"{self.network.name} - {self.user.username} ({self.get_role_display()})"