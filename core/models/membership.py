from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as  _

class Membership(models.Model):
    network = models.ForeignKey('Network', related_name="memberships", on_delete=models.CASCADE)
    organisation = models.ForeignKey('Organisation', related_name="network_requests", on_delete=models.CASCADE)
    join_date = models.DateTimeField(blank=True, null=True)


    PENDING = "pending"
    ACCEPTED = "accepted"
    DENIED = "denied"

    STATUS_OPTIONS = (
        (PENDING, "pending"),  # or Complete
        (ACCEPTED, "accepted"), # or Incomplete
        (DENIED, "denied")
    )
    status = models.CharField(max_length=100, blank=False, choices=STATUS_OPTIONS, default="pending")

    NETWORK = "network"
    ORGANISATION = "organisation"

    REQUESTER = (
        (NETWORK, "network"),  # or Complete
        (ORGANISATION, "organisation"), # or Incomplete
        # Add in more status options
    )
    requester = models.CharField(max_length=100, blank=False, choices=REQUESTER)

    def save(self, *args, **kwargs):
        # if not self._status and self.status:
        #     self.pub_date = now()
        if (self.status == 'accepted') and self.join_date is None:
            self.join_date = now()
        elif (not self.status == 'accepted') and self.join_date is not None:
            self.join_date = None
        super(Membership, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('network', 'organisation')

    def __str__(self):
        return f"{self.organisation.name} - {self.network.name}"


    # def __init__(self, *args, **kwargs):
    #     super(Membership, self).__init__(*args, **kwargs)
    #     self._status = self.status
