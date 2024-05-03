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
    general = forms.IntegerField(required=False, min_value=0)
    senior = forms.IntegerField(required=False, min_value=0)
    children = forms.IntegerField(required=False, min_value=0)
    seat = forms.CharField(widget=forms.TextInput(attrs={"id": "selected-seat"}))
    creditcard = forms.CharField()
    seccode = forms.CharField()
    expdate = forms.DateField(
        initial="2029-06",
        widget=forms.DateInput(format="%Y-%m"),
        input_formats=["%Y-%m"],
    )
    postalcode = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["expdate"].widget.input_type = "month"

    def clean_expdate(self):
        data = self.cleaned_data.get("expdate").strftime("%Y-%m")
        if data == "2029-06":
            self.cleaned_data["expdate"] = data
            return data
        raise ValidationError("Enter Expiry date in `YYYY-MM` format.")

    def clean_seccode(self):
        if re.fullmatch("[0-9]{3}", self.cleaned_data.get("seccode", "1234")) != None:
            return self.cleaned_data["seccode"]
        raise ValidationError("Numbers of 3 digit are only allowed.")

    def clean_postalcode(self):
        if (
            re.fullmatch("([A-Z][0-9]){3}", self.cleaned_data.get("postalcode", "L2K"))
            is not None
        ):
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
