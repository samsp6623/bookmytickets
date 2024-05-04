from django.http import HttpResponse
from functools import wraps
from app.models import Order


def users_content_only(func):
    @wraps(func)
    def myfunc(self):
        if self.request.user.username != self.kwargs["username"]:
            return HttpResponse(status=403)
        return func(self)

    return myfunc


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
    """Books ticket in show, creates the Order object for ShowUser in DB"""
    booked_seat = form.cleaned_data["seat"].split(" ")
    Order.objects.create(
        user=request.user,
        seat=form.cleaned_data["seat"],
        show=show,
        general=form.cleaned_data["general"],
        senior=form.cleaned_data["senior"],
        children=form.cleaned_data["children"],
        total_b4_tax=form.cleaned_data["total_b4_tax"],
        total_tax=form.cleaned_data["total_tax"],
        net_total=form.cleaned_data["net_total"],
    )
    for st in booked_seat:
        show.seats_occupied["seats"].append(st)
    show.save()
