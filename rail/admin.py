from django.contrib import admin

from .models import Train, ReleasedTrain, BookingAgent

admin.site.register(Train)
admin.site.register(ReleasedTrain)
admin.site.register(BookingAgent)