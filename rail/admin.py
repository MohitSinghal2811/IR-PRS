from django.contrib import admin

from .models import Train, ReleasedTrain, BookingAgent, Seat, Berth, Coach

admin.site.register(Train)
admin.site.register(ReleasedTrain)
admin.site.register(BookingAgent)
admin.site.register(Seat)
admin.site.register(Berth)
admin.site.register(Coach)