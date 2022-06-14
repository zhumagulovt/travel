from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.models import User


class Tour(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True, null=True)


class TourHistory(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="tours_history", on_delete=models.CASCADE)


class Rating(models.Model):
    tour = models.ForeignKey(Tour, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="ratings", on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ['tour', 'user']


class Saved(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="saved", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['tour', 'user']


class Comment(models.Model):
    content = models.TextField()
    tour = models.ForeignKey(Tour, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']



    