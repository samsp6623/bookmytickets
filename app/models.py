from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils.text import slugify


# Create your models here.
class ShowUser(AbstractBaseUser, PermissionsMixin):
    username = models.SlugField(max_length=32, unique=True)
    email = models.EmailField()
    first_name = models.SlugField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    cell_number = models.CharField(max_length=10, blank=True, null=True)
    loyalty_number = models.IntegerField(blank=True, null=True)
    email_consent = models.BooleanField(blank=True, null=True, default=False)

    is_active = models.BooleanField(blank=True, null=True, default=True)
    is_staff = models.BooleanField(blank=True, null=True, default=False)
    is_superuser = models.BooleanField(blank=True, null=True, default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return f"/profile/{self.username}/"

    def get_full_name(self):
        return (self.first_name + self.last_name).title()

    def save(self, *args, **kwargs):
        self.username = slugify(self.username)
        super().save(*args, **kwargs)


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
        return (
            (self.theater_no + " ")
            if self.theater_no
            else "" + self.kind + " " + str(self.multiplex)
        )


class Performance(models.Model):
    name = models.CharField(max_length=128)
    artist = models.CharField(max_length=256)
    runtime = models.CharField(max_length=16)
    language = models.CharField(max_length=16)
    slugfield = models.SlugField(max_length=32, blank=True, null=True)
    cover_picture = models.ImageField(
        upload_to="media/", max_length=128, blank=True, null=True
    )

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        self.slugfield = slugify(self.name)[0:10]
        super().save(*args, **kwargs)


class SCategory(models.Model):
    opts = {
        "GEN": "General",
        "SEN": "Senior",
        "CLD": "Children",
    }
    scat = models.CharField(max_length=8, choices=opts)

    def __str__(self):
        return self.opts[self.scat]


def init_json():
    return {"seats": []}


class Show(models.Model):
    date_time = models.DateTimeField()
    performance = models.ForeignKey(
        Performance,
        on_delete=models.DO_NOTHING,
    )
    theater = models.ForeignKey(Theater, on_delete=models.DO_NOTHING)
    seats_occupied = models.JSONField(null=False, blank=True, default=init_json)
    seat_category = models.ManyToManyField(SCategory, through="Tarrif")

    def __str__(self):
        return (
            self.date_time.strftime("%a, %d %b %Y, %I:%M%p")
            + " | "
            + str(self.performance)
        )


class Tarrif(models.Model):
    show = models.ForeignKey(Show, on_delete=models.DO_NOTHING)
    seat_category = models.ForeignKey(SCategory, on_delete=models.DO_NOTHING)
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return (
            "$" + str(self.rate) + " " + str(self.seat_category) + " " + str(self.show)
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["show", "seat_category"],
                name="uni_to_show_seatcategory",
                violation_error_message="""The tarrif rate for selected Show 
                has been defined already.""",
            )
        ]


class Ticket(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(ShowUser, on_delete=models.DO_NOTHING)
    seat = models.CharField(max_length=256)
    show = models.ForeignKey(Show, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.show) + " " + self.seat + " " + str(self.show.theater)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["show", "seat"],
                name="uni_seat_for_ticket",
                violation_error_message="""This seat has already been sold. 
                Please select other seat.""",
            )
        ]


class Order(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ShowUser, on_delete=models.DO_NOTHING)
    seat = models.CharField(max_length=256)
    show = models.ForeignKey(Show, on_delete=models.DO_NOTHING)
    general = models.IntegerField(default=0)
    senior = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    total_b4_tax = models.FloatField(default=0.00)
    total_tax = models.FloatField(default=0.00)
    net_total = models.FloatField(default=0.00)

    def __str__(self):
        return str(self.show) + " " + self.seat + " " + str(self.show.theater)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["show", "seat"],
                name="unique_seat_for_ticket",
                violation_error_message="""This seat has already been sold. 
                Please select another seat.""",
            )
        ]
