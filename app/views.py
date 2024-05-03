from typing import Any
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)

from .forms import BookTicketForm, MyUserCreationForm
from .models import Performance, Show, ShowUser, Multiplex, Tarrif, Ticket
from django.db.models import QuerySet
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, UpdateView

# from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, "app/home.html")


class MyPasswordResetView(PasswordResetView):
    template_name = "app/password_reset.html"


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = "app/password_reset_done.html"


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "app/password_reset_confirm.html"


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "app/password_reset_complete.html"


class MultiplexListView(ListView):
    model = Multiplex


class PerformanceListView(ListView):
    model = Performance


class ShowListView(ListView):
    model = Show

    def get_queryset(self) -> QuerySet[Any]:
        if self.kwargs.get("slugfield"):
            return (
                super()
                .get_queryset()
                .filter(performance__slugfield=self.kwargs.get("slugfield", None))
                .order_by("date_time")
            )
        elif self.kwargs.get("pk"):
            return (
                super()
                .get_queryset()
                .filter(theater=self.kwargs["pk"])
                .order_by("date_time")
            )


class ShowUserUpdateView(UpdateView):
    model = ShowUser
    fields: list[str] = [
        "username",
        "email",
        "first_name",
        "last_name",
        "cell_number",
        "loyalty_number",
        "email_consent",
    ]
    template_name = "app/showuser_detail.html"

    def get_object(self, *args, **kwargs) -> Model:
        username = self.kwargs.get("username")
        return get_object_or_404(ShowUser, username=username)


def get_payment(form):
    """Ideally this should be Strip like paymeny API checking for
    Payment information and transfering the fund.
    """
    cc = form.cleaned_data["creditcard"] == "9999888877776666"
    secc = form.cleaned_data["seccode"] == "999"
    expd = form.cleaned_data["expdate"] == "2029-06"
    pcode = form.cleaned_data["postalcode"] == "M9Z1P4"
    if all([cc, secc, expd, pcode]):
        return True
    else:
        return False


def book_seat(request, form, show):
    """Books ticket, creates the Ticket object in DB registers the booked seat
    in respective Show.
    """
    booked_seat = form.cleaned_data["seat"].split(" ")
    for i in [
        form.cleaned_data["general"] if not None else 0,
        form.cleaned_data["senior"] if not None else 0,
        form.cleaned_data["children"] if not None else 0,
    ]:
        for j in range(i):
            s = booked_seat.pop()
            Ticket.objects.create(user=request.user, show=show, seat=s)
            show.seats_occupied["seats"].append(s)
    show.save()


@login_required
def booking(request, *args, **kwargs):
    form = BookTicketForm()
    tarrif = Tarrif.objects.filter(show_id=kwargs["pk"])
    show = Show.objects.get(id=kwargs["pk"])
    if request.method == "POST":
        form = BookTicketForm(request.POST)
        if form.is_valid() and get_payment(form):
            book_seat(request, form, show)
            return redirect("home")
        return render(
            request, "app/booking.html", {"form": form, "show": show, "tarrif": tarrif}
        )
    return render(
        request, "app/booking.html", {"form": form, "show": show, "tarrif": tarrif}
    )


class PastTicketListsViews(ListView):
    model = Ticket

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user)


def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
        return render(
            request,
            "app/login.html",
            {"form": AuthenticationForm(request, data=request.POST)},
        )
    return render(request, "app/login.html", {"form": form})


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect(to="home")
    return render(request, "app/logout.html")


def signup(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if not form.is_valid():
            return render(request, "app/signup.html", {"form": form})
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        ShowUser.objects.create_user(username, password=password)
        return redirect("login")
    form = MyUserCreationForm()
    return render(request, "app/signup.html", context={"form": form})


def test(request):
    data = dict()
    data["addr"] = request.META["REMOTE_ADDR"]
    data["host"] = request.META["REMOTE_HOST"]
    return render(request, "app/test.html", {"data": data})
