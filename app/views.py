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
from django.contrib.messages.views import SuccessMessageMixin

from .utils import book_seat, get_payment, users_content_only

from .forms import BookTicketForm, MyUserCreationForm
from .models import Order, Performance, Show, ShowUser, Multiplex, Tarrif
from django.db.models import QuerySet
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, UpdateView
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, "app/home.html")


class MyPasswordResetView(PasswordResetView):
    template_name = "app/password_reset.html"
    success_message = "You have successfully reset your password."


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
        if self.kwargs.get("slugfield", False):
            return (
                super()
                .get_queryset()
                .filter(performance__slugfield=self.kwargs.get("slugfield", None))
                .order_by("theater")
            )
        elif self.kwargs.get("pk", False):
            return (
                super()
                .get_queryset()
                .filter(theater=self.kwargs["pk"])
                .order_by("performance")
            )


class ShowUserUpdateView(SuccessMessageMixin, UpdateView):
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
    success_message = "You have successfully updated your account information."
    success_url = "/"

    @users_content_only
    def get_object(self, *args, **kwargs) -> Model:
        username = self.kwargs.get("username")
        return get_object_or_404(ShowUser, username=username)


@login_required
def booking(request, *args, **kwargs):
    form = BookTicketForm()
    tarrif = Tarrif.objects.filter(show_id=kwargs["pk"])
    show = Show.objects.get(id=kwargs["pk"])
    if request.method == "POST":
        form = BookTicketForm(request.POST)
        if form.is_valid() and get_payment(form):
            return book_seat(request, form, show, tarrif)
        return render(
            request, "app/booking.html", {"form": form, "show": show, "tarrif": tarrif}
        )
    return render(
        request, "app/booking.html", {"form": form, "show": show, "tarrif": tarrif}
    )


class PastTicketListsViews(ListView):
    model = Order
    template_name = "app/order_list.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(user=self.request.user).order_by("-date_time")


def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(
                request,
                "You have Successfully logged into your account.",
            )
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
        messages.success(
            request,
            "You have Successfully logged out of your account.",
        )
        return redirect(to="home")
    return render(request, "app/logout.html")


def signup(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if not form.is_valid():
            return render(request, "app/signup.html", {"form": form})
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        u = ShowUser.objects.create_user(
            username,
            password=password,
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        messages.success(
            request,
            "You have Successfully created your account with us.",
        )
        return redirect("login")
    form = MyUserCreationForm()
    return render(request, "app/signup.html", context={"form": form})


def p400(request, exception=None):
    return render(request, "app/400.html")


def p403(request, exception=None):
    return render(request, "app/404.html")


def p404(request, exception=None):
    return render(request, "app/404.html")


def p500(request, exception=None):
    return render(request, "app/500.html")


def test(request):
    data = dict()
    data["HTTP_X_FORWARDED_FOR"] = request.META.get("HTTP_X_FORWARDED_FOR", "test")
    return render(request, "app/test.html", {"data": data})


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def cookie_policy(request):
    return render(request, "cookie_policy.html")
