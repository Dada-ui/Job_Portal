from django.contrib import admin
from app.models import *

from .models import User

# Register your models here.

admin.site.register(User)
admin.site.register(Job)
admin.site.register(Contact)
admin.site.register(Applicant)
admin.site.register(Profile)
admin.site.register(ProfileRating)