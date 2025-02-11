from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.urls import reverse

# Models


class Post(models.Model):
    title = models.CharField(max_length=150, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=210)
    body = models.TextField()
    image = models.ImageField(upload_to="images", blank=True, null=True)
    image_alt = models.CharField(max_length=500,
                                 default="No alt text given because I only think about myself.")
    is_published = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    published_on = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)

    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class ContactMethod(models.Model):
    source = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.source


# Signals


@receiver(pre_save, sender=Post)
def publish_post(sender, instance, ** kwargs):
    if instance.id is None:
        if instance.is_published == True:
            instance.published_on = now()
    else:
        current = instance
        previous = Post.objects.get(id=instance.id)
        if previous.is_published == False and current.is_published == True:
            instance.published_on = now()
