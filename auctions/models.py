from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10, default=None, blank=False)
    image = models.URLField(null=True, default="https://st2.depositphotos.com/1561359/12101/v/950/depositphotos_121012076-stock-illustration-blank-photo-icon.jpg")
    CATEGORIES = [
        ("Home", "Home"),
        ("Electronics", "Electronics"),
        ("Books", "Books"),
        ("Toys", "Toys"),
        ("Fashion", "Fashion"),
    ]
    category = models.CharField(max_length=32, choices=CATEGORIES)
    users = models.ManyToManyField(User, null=True, related_name="watchlisted")
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"\n ID:{self.id}\n User:{self.user}\n Title:{self.title}\n Starting bid:{self.starting_bid}\n Category:{self.category}\n"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=False)
    bid = models.DecimalField(decimal_places=2, max_digits=10, null=False, verbose_name="")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return f" ID:{self.id} Price:${self.bid} Bidder:{self.user}"

class Comment(models.Model):
    comment = models.CharField(max_length=512, default=None, verbose_name="")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=False)