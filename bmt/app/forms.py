import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SCategory, ShowUser, Ticket
from django.forms import ModelForm, ValidationError


def is_valid_str(value):
    if re.search("[<>!`\%\+\-\\(\)\|\.\^\*]", value) is not None:
        raise ValidationError(
            "Reserved Characters are not allowed. %(value)s", params={"value": value}
        )
    return value


def is_valid_loylty_num(value):
    if len(value) != 16:
        raise ValidationError(
            "Please enter 16 digit long Loylty Number. %(value)s",
            params={"value": value},
        )
    return value


def is_non_zero_int(value):
    if int(value) < 0:
        raise ValidationError(
            "The number of ticket must be >= to zero. %(value)s",
            params={"value": value},
        )
    return value


class ShowUserForms(ModelForm):
    class Meta:
        model = ShowUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "loyalty_number",
            "email_consent",
        ]


class MyUserCreationForm(UserCreationForm):
    def clean_username(self):
        return is_valid_str(self["username"].value())

    class Meta:
        model = ShowUser
        fields = ["username", "password1", "password2"]


opts = SCategory.opts


class SeatNosField(forms.IntegerField):
    def __init__(self, **kwargs):
        super().__init__(initial=0, min_value=0, **kwargs, validators=[is_non_zero_int])


class BookTicketForm(ModelForm):
    gen_seat = SeatNosField()
    sen_seat = SeatNosField()
    cld_seat = SeatNosField()
    seat = forms.CharField(widget=forms.TextInput(attrs={"id": "selected-seat"}))

    class Meta:
        model = Ticket
        fields = ["seat", "gen_seat", "sen_seat", "cld_seat"]
