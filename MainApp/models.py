from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    passcode = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname + " " + self.email


class Agency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Destination(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    From = models.CharField(max_length=30)
    To = models.CharField(max_length=30)
    price = models.FloatField()

    def __str__(self):
        return self.agency.name + " " + self.From + "-" + self.To


class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    departure_time = models.CharField(max_length=10)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    status = models.CharField(max_length=20, default="Pending Payment")
    timestamp = models.DateTimeField(auto_now_add=True)
    ticket_id = models.CharField(max_length=20, default="0")
    transaction_id = models.CharField(max_length=25, null=True)
    proof = models.ImageField(upload_to="proofs/", null=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return (
            self.user.fullname
            + " "
            + self.destination.agency.name
            + " "
            + self.destination.From
            + "-"
            + self.destination.To
        )
