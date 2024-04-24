import pdb
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ShowUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    loyalty_number =models.CharField(max_length=16, blank=True, null=True)
    email_consent = models.BooleanField()

    def __str__(self):
        return self.user.username

class Multiplex(models.Model):
    parking_spots = models.IntegerField()
    washrooms = models.IntegerField()
    drinking_water_stations = models.IntegerField(blank=True, null=True)
    accessibility_features = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=128)

    def __str__(self):
        return self.address
    
class Theater(models.Model):
    theater_no = models.CharField(max_length=3, blank=True, null=True)
    screen_size = models.CharField(max_length=128)
    audio_features = models.CharField(max_length=256)
    accessibility_features = models.CharField(max_length=512)
    multiplex = models.ForeignKey(Multiplex, on_delete=models.DO_NOTHING)
    opts = {
        "UAVX": "UltraAVX",
        "IMAX": "IMAX",
        "SX": "ScreenX",
        "DB": "D-Box",
        "4DX": "4DX",
        "SF": "Sensory-Friendly",
    }
    kind = models.CharField(max_length=4, choices=opts)
    seats_available = models.JSONField()

    def __str__(self):
        return self.theater_no + " " if self.theater_no else "" + self.screen_size + " " + self.kind + " " + str(self.multiplex)

class Performance(models.Model):
    name = models.CharField(max_length=128)
    artist = models.CharField(max_length=256)
    runtime = models.CharField(max_length=16)
    language = models.CharField(max_length=16)
    cover_picture = models.ImageField(upload_to="media/", max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name.title()

class SCategory(models.Model):
    opts = {
        "GEN": "General",
        "SEN": "Senior",
        "CLD": "Children",
    }
    scat = models.CharField(max_length=8, choices=opts)

    def __str__(self):
        return self.opts[self.scat]

class Show(models.Model):
    date_time = models.DateTimeField()
    performance = models.ForeignKey(Performance, on_delete=models.DO_NOTHING, )
    theater = models.ForeignKey(Theater, on_delete=models.DO_NOTHING)
    seats_occupied = models.JSONField(null=True)
    seat_category = models.ManyToManyField(SCategory, through="Tarrif")

    def __str__(self):
        return self.date_time.strftime('%a %d %b %Y, %I:%M%p') +  " | " + str(self.performance)

class Tarrif(models.Model):
    show = models.ForeignKey(Show, on_delete=models.DO_NOTHING)
    seat_cateogry = models.ForeignKey(SCategory, on_delete=models.DO_NOTHING)
    theater = models.ForeignKey(Theater, on_delete=models.DO_NOTHING)
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.show) + " | " + str(self.seat_cateogry) + " | $" + str(self.rate)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["show", "theater", "seat_cateogry"], name="uni_to_theater_show",
                                    violation_error_message="The tarrif rate for selected Show and Theater has been defined already.")

        ]

class Ticket(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(ShowUser, on_delete=models.DO_NOTHING)
    tarrif = models.ForeignKey(Tarrif, on_delete=models.DO_NOTHING)
    seat = models.CharField(max_length=4)
    show = models.ForeignKey(Show, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.tarrif) +  " | " + self.seat + " | " + str(self.show.theater)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["show", "seat"], name="uni_seat_for_ticket",
                                    violation_error_message="This seat has already been sold. Please select other seat.")
        ]