from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import User
import readtime
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class ProfileSettings(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    location = models.CharField(max_length=60, null=True, blank=True)
    image = models.FileField(upload_to="images/", null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Profile Setting"
        verbose_name_plural = "Profile Settings"

    def __str__(self):
        return str(self.user)


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="user"
    )
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60)
    content = RichTextField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    slug = models.SlugField(max_length=255, auto_created=True, blank=True)
    image = models.FileField(upload_to="images/", null=True, blank=True)
    like = models.ManyToManyField(User, related_name="like", blank=True)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1, blank=True, null=True
    )

    def __str__(self):
        return self.title

    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text

    def save(self, *args, **kwargs):
        """Automatically creates slug on save when you left slug empty"""
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.slug == self.title:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_details", kwargs={"slug": self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comment_user"
    )
    approve = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment: {self.body} by {self.user}"


class Notification(models.Model):
    LIKE = "like"
    COMMENT = "comment"

    CHOICES = ((LIKE, "Like"), (COMMENT, "Comment"))

    receiver_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notification_receiver",
        null=True,
    )
    provider_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_provider"
    )
    notification_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_seen = models.BooleanField(default=False)
    post_name = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="notification_like"
    )

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Post name: {self.post_name}, Post id: {self.notification_id}, Receiver: {self.receiver_user}, Provider: {self.provider_user}"
