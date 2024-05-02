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


class BookTicketForm(ModelForm):
    general = forms.IntegerField()
    senior = forms.IntegerField()
    children = forms.IntegerField()
    seat = forms.CharField(widget=forms.TextInput(attrs={"id": "selected-seat"}))
    creditcard = forms.CharField()
    seccode = forms.CharField()
    expdate = forms.DateTimeField(input_formats="%Y-%m")
    postalcode = forms.CharField()

    def clean_creditcard(self):
        if self.cleaned_data["creditcard"] == "9999888877776666":
            return self.cleaned_data["creditcard"]
        raise ValidationError("Payment Failed")

    def clean_expdate(self):
        if self.cleaned_data["expdate"] == "2029-06":
            return self.cleaned_data["expdate"]
        raise ValidationError("Payment Failed")

    def clean_seccode(self):
        if self.cleaned_data["seccode"] == "999":
            return self.cleaned_data["seccode"]
        raise ValidationError("Payment Failed")

    def clean_postalcode(self):
        if self.cleaned_data["postalcode"] == "M9Z1P4":
            return self.cleaned_data["postalcode"]
        raise ValidationError("Payment Failed")

    class Meta:
        model = Ticket
        fields = [
            "seat",
            "general",
            "senior",
            "children",
            "creditcard",
            "seccode",
            "expdate",
            "postalcode",
        ]
