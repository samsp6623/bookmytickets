from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render


def cookieconsent_context(request):
    """
    This function is the skeleton to provide notification message to user for cookie consent,
    each field allows to describe what its used for.

    `if_declined` defines the behaviour if user declines such kind of cookies. In this case
    few options are available as below like, `redirect_path` and `redirection_message`.

    for `if_declined` 3 possible options are, "abort", "request" and "continue".

    "if_declined": "abort"     # will flash the `redirection_message` and redirect to
    'redirect_path' page

    "if_declined": "continue"  # this will simply ignore and continue as normal.

    from django.contrib import messages
    "if_declined": "request"   # will flash the `redirection_message` and redirects to
    `redirect_path`

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return settings.COOKIECONSENT


def cookie_if_consent_or_action(request, response, category, *args, **kwargs):
    """
    This function helps making sure if the user allowed for particular kind of
    cookie to be stored on their machine. For Cookie kwargs passed are same as
    providedd by `HttpResponse.set_cookie`.
        Args:
        request (_type_):
        response (HttpResponse):
        category : same as defined in setting.COOKIECONSENT["options"]

    Returns:
        _type_: HttpResponse
    """
    userconsent = request.COOKIES.get("userconsent", None)
    if userconsent == "" or userconsent is None:
        return
    if str(category) in str(userconsent):
        response.set_cookie(*args, **kwargs)
        return response
    else:
        for item in settings.COOKIECONSENT["options"]:
            if item["category"] == category:
                if item["if_declined"] == "abort":
                    messages.info(request, item["redirection_message"])
                    return redirect(item["redirect_path"])
                elif item["if_declined"] == "continue":
                    pass
                elif item["if_declined"] == "request":
                    messages.info(request, item["redirection_message"])
                    return redirect(item["redirect_path"])
