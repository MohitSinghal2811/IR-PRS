from django.contrib import admin

from .models import Train, ReleasedTrain, BookingAgent, Seat, Berth, Coach, Books , Pnr, Passenger

admin.site.register(Train)
admin.site.register(ReleasedTrain)
admin.site.register(BookingAgent)
admin.site.register(Seat)
admin.site.register(Berth)
admin.site.register(Coach)
admin.site.register(Books)
admin.site.register(Pnr)
admin.site.register(Passenger)