from django.contrib import admin

from .models import Train, ReleasedTrain

admin.site.register(Train)
admin.site.register(ReleasedTrain)

