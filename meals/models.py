from django.db import models
from django.conf import settings
from recipes.models import Recipe

'''
Meal 
- Pending
- Completed
- Expired
- Aborted

'''

User = settings.AUTH_USER_MODEL

class MealStatus(models.TextChoices):
    PENDING = 'p', 'Pending'
    COMPLETED = 'c', 'Completed'
    EXPIRED = 'e', 'Expired'
    ABORTED = 'a', 'Aborted'



class MealQuerySet(models.QuerySet):
    def by_user_id(self, user_id):
        return self.filter(user_id=user_id)

    def by_user(self, user):
        return self.filter(user=user)

    def pending(self):
        return self.filetr(status=MealStatus.PENDING)
    
    def completed(self):
        return self.filetr(status=MealStatus.COMPLETED)

    def expired(self):
        return self.filetr(status=MealStatus.EXPIRED)

    def aborted(self):
        return self.filetr(status=MealStatus.ABORTED)

class MealManager(models.Manager):
    def get_queryset(self):
        return MealQuerySet(self.model, using=self._db)

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=MealStatus.choices, default=MealStatus.PENDING)

    objects = MealManager()