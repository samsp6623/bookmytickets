from django.db import models

# Create your models here.
class ShowUser(models.Model):
    first_name = models.CharField(max_length=64, blank=False, null=False)
    last_name = models.CharField(max_length=64, blank=False, null=False)
    cell_no = models.CharField(max_length=10, blank=False, null=False)
    email_address = models.EmailField(max_length=32, blank=False, null=False)
    loyalty_number =models.CharField(max_length=16, blank=True, null=True)
    email_consent = models.BooleanField()

    def __str__(self):
        return self.first_name + " " + self.last_name

class Multiplex(models.Model):
    parking_spots = models.IntegerField()
    washrooms = models.IntegerField()
    drinking_water_stations = models.IntegerField()
    accessibility_features = models.CharField(max_length=256, blank=False, null=False)
    address = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self):
        return self.address
    
class Theater(models.Model):
    screen_size = models.CharField(max_length=128, blank=False, null=False)
    audio_features = models.CharField(max_length=256, blank=False, null=False)
    accessibility_features = models.CharField(max_length=512, blank=False, null=False)
    multiplex = models.ForeignKey(Multiplex, on_delete=models.DO_NOTHING)
    opts = {
        "UAVX": "UltraAVX",
        "IMAX": "IMAX",
        "SX": "ScreenX",
        "DB": "D-Box",
        "4DX": "D-Box",
        "SF": "Sensory-Friendly",
    }
    kind = models.CharField(max_length=4, choices=opts)

    def __str__(self):
        return self.kind +  " " + str(self.multiplex)

class Performance(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    artist = models.CharField(max_length=256, blank=False, null=False)
    runtime = models.CharField(max_length=16, blank=False, null=False)
    language = models.CharField(max_length=16, blank=False, null=False)
    cover_picture = models.ImageField(upload_to="media/", max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name.title()

class Show(models.Model):
    date_time = models.DateTimeField()
    seats_occupied = models.JSONField(blank=True, null=True)
    performance = models.ForeignKey(Performance, on_delete=models.DO_NOTHING, )
    theater = models.ForeignKey(Theater, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.date_time.strftime('%a %d %b %Y, %I:%M%p') +  " " + str(self.performance)

class Tarrif(models.Model):
    opts = {
        "GEN": "General",
        "SEN": "Senior",
        "CLD": "Children",
    }
    seat_category = models.CharField(max_length=5, choices=opts)
    show = models.ForeignKey(Show, on_delete=models.DO_NOTHING)
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.seat_category + " $" + str(self.rate)

class Ticket(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(ShowUser, on_delete=models.DO_NOTHING)
    tarrif = models.ForeignKey(Tarrif, on_delete=models.DO_NOTHING)
    seat = models.CharField(max_length=4)
    show = models.ForeignKey(Show, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.show) +  " : " + self.seat