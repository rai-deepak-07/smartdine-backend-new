from djongo import models
from django.utils import timezone

class TeamMember(models.MongoModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to="team_members/", blank=True)
    linkedin = models.URLField(max_length=300, blank=True)
    github = models.URLField(max_length=300, blank=True)
    is_leader = models.BooleanField(default=False)
    skills = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
