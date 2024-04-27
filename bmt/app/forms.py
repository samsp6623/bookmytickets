from django.forms import ModelForm

from bmt.app.models import ShowUser


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
