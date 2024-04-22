from django.contrib import admin
from .models import Show, ShowUser, Multiplex, Theater, Tarrif, Performance, Ticket
# Register your models here.
admin.site.register(Show)
admin.site.register(ShowUser)
admin.site.register(Multiplex)
admin.site.register(Theater)
admin.site.register(Tarrif)
admin.site.register(Performance)
admin.site.register(Ticket)

