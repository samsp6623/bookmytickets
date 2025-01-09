from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("locations/", views.MultiplexListView.as_view(), name="locations"),
    path("performances/", views.PerformanceListView.as_view(), name="performances"),
    path("multiplex/<int:pk>", views.ShowListView.as_view(), name="show-running"),
    path("shows/<slug:slugfield>", views.ShowListView.as_view(), name="show-detail"),
    path("shows/book/<int:pk>", views.booking, name="book"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("cookie-policy/", views.cookie_policy, name="cookie_policy"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("signup/", views.signup, name="signup"),
    path("pastorders/", views.PastTicketListsViews.as_view(), name="past-orders"),
    path(
        "profile/<slug:username>/", views.ShowUserUpdateView.as_view(), name="profile"
    ),
    path("password_reset/", views.MyPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.MyPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.MyPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.MyPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("mytest/", views.test),
]
