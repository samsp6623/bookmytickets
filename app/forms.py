import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Order, SCategory, ShowUser
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


class MyUserCreationForm(ModelForm):
    username = forms.CharField()
    password1 = forms.CharField(
        label="Password", widget=forms.TextInput(attrs={"type": "password"})
    )
    password2 = forms.CharField(
        label="Confirm by Re-entering Password",
        widget=forms.TextInput(attrs={"type": "password"}),
    )

    def clean_username(self):
        return is_valid_str(self["username"].value())

    def clean_password1(self):
        data = self.cleaned_data["password1"]
        if (
            re.search("[a-zA-Z]", data)
            and re.search(r"[!@#$]", data)
            and re.search("[0-9]", data)
        ):
            return data
        raise ValidationError(
            "Make sure to use alphabetes, numbers and special character from `!@#$`"
        )

    def clean_password2(self):
        data1 = self.data["password1"]
        data2 = self.cleaned_data["password2"]
        if data1 == data2:
            return data2
        raise ValidationError("Password does not match! try again!")

    class Meta:
        model = ShowUser
        fields = ["username", "password1", "password2"]


opts = SCategory.opts


class BookTicketForm(ModelForm):
    seat = forms.CharField(
        initial="", widget=forms.TextInput(attrs={"readonly": "readonly"})
    )
    creditcard = forms.CharField(
        initial="9999888877776666", min_length=16, max_length=16
    )
    seccode = forms.CharField(
        initial="999",
        min_length=3,
        max_length=3,
        widget=forms.TextInput(attrs={"class": "fieldinput"}),
    )
    expdate = forms.DateField(
        initial="2029-06",
        widget=forms.DateInput(format="%Y-%m", attrs={"class": "fieldinput"}),
        input_formats=["%Y-%m"],
    )
    postalcode = forms.CharField(
        initial="380001",
        min_length=6,
        max_length=6,
        widget=forms.TextInput(attrs={"class": "fieldinput"}),
    )
    total_b4_tax = forms.FloatField(
        initial=0.00,
        template_name="app/cxfloat.html",
        widget=forms.TextInput(attrs={"readonly": "readonly", "id": "total_b4_tax"}),
    )
    total_tax = forms.FloatField(
        initial=0.00,
        template_name="app/cxfloat.html",
        widget=forms.TextInput(attrs={"readonly": "readonly", "id": "total_tax"}),
    )
    net_total = forms.FloatField(
        initial=0.00,
        template_name="app/cxfloat.html",
        widget=forms.TextInput(attrs={"readonly": "readonly", "id": "net_total"}),
    )
    general = forms.IntegerField(
        initial=0,
        min_value=0,
        max_value=25,
        widget=forms.NumberInput(attrs={"class": "fieldinput"}),
    )
    senior = forms.IntegerField(
        initial=0,
        min_value=0,
        max_value=25,
        widget=forms.NumberInput(attrs={"class": "fieldinput"}),
    )
    children = forms.IntegerField(
        initial=0,
        min_value=0,
        max_value=25,
        widget=forms.NumberInput(attrs={"class": "fieldinput"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["expdate"].widget.input_type = "month"
        self.fields["seccode"].widget.input_type = "password"

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
            re.fullmatch("([0-9]){6}", str(self.cleaned_data.get("postalcode", 380001)))
            is not None
        ):
            return self.cleaned_data["postalcode"]
        raise ValidationError("Payment Failed")

    class Meta:
        model = Order
        exclude = ["date_time", "user", "show"]
