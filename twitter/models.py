from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create a tweet model
class Tweet(models.Model):
    class Meta:
        verbose_name_plural = 'Tweets'
    
    def __str__(self) -> str:
        return (f"{self.user.username} "
                f"({self.created_at:%d-%m-%Y %I:%M %p}): "
                f"{self.body}..."
                )
    
    # keep track of no of likes
    def number_of_likes(self):
        return self.likes.count()

    user = models.ForeignKey(
        User, related_name='tweets', on_delete=models.CASCADE
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='tweet_like', blank=True)


# Create A User Profile Model
class Profile(models.Model):
    class Meta:
        verbose_name_plural = 'Profiles'

    def __str__(self) -> str:
        return self.user.username
    
    PUBLIC = 'public'
    PRIVATE = 'private'

    ACCOUNT_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", 
        related_name="followed_by",
        symmetrical=False,
        blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='images/')
    profile_bio = models.CharField(null=True, blank=True, max_length=200)
    website_link = models.URLField(null=True, blank=True, max_length=200)
    instagram_link = models.URLField(null=True, blank=True, max_length=200)
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_CHOICES,
        default=PUBLIC,
    )
    
# Create profile when new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # user follow himself
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)
