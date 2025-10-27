from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# --- Modelo Pin (como o Pinterest) ---
class Pin(models.Model):
    user = models.ForeignKey(
        User, related_name="pins",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="pins/", null=False, blank=False)
    description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="pin_likes", blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username} ({self.created_at:%d/%m/%Y %H:%M})"


# --- Modelo Profile (usuário) ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    date_modified = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profiles/")
    bio = models.CharField(null=True, blank=True, max_length=500)
    website = models.CharField(null=True, blank=True, max_length=100)
    facebook = models.CharField(null=True, blank=True, max_length=100)
    instagram = models.CharField(null=True, blank=True, max_length=100)
    linkedin = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username


# --- Criação automática de perfil ---
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(user_profile)
        user_profile.save()

post_save.connect(create_profile, sender=User)
