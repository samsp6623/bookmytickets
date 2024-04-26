from re import L
from typing import Any
from django.contrib.auth import login, logout
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
)
from django.db.models import QuerySet
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .models import Performance, Show, ShowUser, Theater, Multiplex, Ticket
# from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, "app/home.html")


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


class ShowUserDetailView(DetailView):
    model = ShowUser

    def get_object(self, *args, **kwargs) -> Model:
        username = self.kwargs.get("username")
        return get_object_or_404(ShowUser, username=username)


def booking(request):
    return render(request, "app/booking.html")


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
