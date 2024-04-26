from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("locations/", views.MultiplexListView.as_view()),
    path("performances/", views.PerformanceListView.as_view()),
    path("multiplex/<int:pk>", views.ShowListView.as_view(), name="show-running"),
    path("shows/<slug:slugfield>", views.ShowListView.as_view(), name="show-detail"),
    path("booking/", views.booking),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("pastorders/", views.PastTicketListsViews.as_view(), name="past-orders"),
    path(
        "profile/<slug:username>/", views.ShowUserDetailView.as_view(), name="profile"
    ),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
