# from django.db import models
# from django.utils import timezone
# from django.contrib.auth import get_user_model
# User = get_user_model()

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse # Change here

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property 
    def month_posted(self): 
        return self.date_posted.strftime('%B') # Returns the month name, e.g., "January"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self): # Change here
        return reverse('post-detail', kwargs={'pk': self.pk}) # Change here to bring the user to the post detail view