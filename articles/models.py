from unittest.mock import NonCallableMagicMock
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from articles.utils import slugify_instance_title

# Create your models here.

class Article(models.Model):
    # put CharField() for title to set max_character length
    # head to the Django Model-field-types
    title = models.CharField(max_length = 100) 
    # add a Slug, to use instead of the model id in the url
    slug = models.SlugField(unique=True,blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # auto_now: whenever the model is saved is going to be saved
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add: whenever the model is added is going to be added
    # now that we added new fields to the Article Model, Django asks what to do with the already existing articles
    # as you know, their new added fields are empty
    # add defualt from shell when shows the warning, timezone.now
    publish = models.DateField(auto_now=False, auto_now_add=False, default = timezone.now) # DateField just has the calender, no time
    # null=True: in the databse it can be empty
    # blank=True: in django forms or django admin in can be empty
    '''why is it showing in the /admin/<article_id> ?'''
    ''' how to delete a field? or how to reset a mistaken field?'''
    # just comment the field commmand and makemigrations and migrate > it is deleted!
    '''for changing a field, simply remove it (by commenting) and re add the altered one'''
    
    def get_absolute_url(self):
        return f'/articles/{self.slug}/'

    def save(self, *args, **kwargs):
        # let's change somethings and change the properties of the .save()

        # with this if, slug can be changes regardless of the title
        # if self.slug is None:
        #     self.slug = slugify(self.title)
        super().save(*args, **kwargs)
   

def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(sender, instance, created, *args, **kwargs):
    # we write this if to prevent recursion
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)