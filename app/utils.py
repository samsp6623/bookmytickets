from django.http import HttpResponse
from functools import wraps
from app.models import Order
from django.shortcuts import redirect
from django.contrib import messages
from django.db import IntegrityError, transaction


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
    pcode = form.cleaned_data["postalcode"] == "380001"
    if all([cc, secc, expd, pcode]):
        return True
    else:
        return False


def book_seat(request, form, show, tarrif):
    """Books ticket in show, creates the Order object for ShowUser in DB"""
    general = form.cleaned_data["general"]
    senior = form.cleaned_data["senior"]
    children = form.cleaned_data["children"]
    booked_seat = form.cleaned_data["seat"].split(" ")
    bticket = ""
    for seat in booked_seat:
        if seat in show.seats_occupied["seats"]:
            bticket += seat + " "
    if bticket:
        messages.error(
            request,
            "Sorry tickets {bticket}are booked! Please choose some other seats.",
        )
        return redirect("book")
    total_b4_tax = 0
    for tar in tarrif.values_list():
        if tar[2] == 1:
            total_b4_tax += int(tar[3] * general)
        elif tar[2] == 2:
            total_b4_tax += int(tar[3] * senior)
        elif tar[2] == 3:
            total_b4_tax += int(tar[3] * children)
    total_tax = round((total_b4_tax * 0.135), 2)
    net_total = round((total_b4_tax + total_tax), 2)
    try:
        with transaction.atomic():
            Order.objects.create(
                user=request.user,
                seat=form.cleaned_data["seat"],
                show=show,
                general=general,
                senior=senior,
                children=children,
                total_b4_tax=round(total_b4_tax, 2),
                total_tax=total_tax,
                net_total=net_total,
            )
            for st in booked_seat:
                show.seats_occupied["seats"].append(st)
            show.save()
        messages.success(request, "You have Successfully booked your ticket.")
        return redirect("home")
    except IntegrityError as e:
        print(f"Error {e} occured!")
        messages.error(
            request,
            "Sorry your tickets are not booked! Please choose some other seats.",
        )
        return redirect("book")
