from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .forms import StaffAuthenticationForm
from .posts import FACEBOOK_POSTS


def index(request):
    return render(request, "home/index.html", {
        "facebook_posts": FACEBOOK_POSTS,
    })


@method_decorator(never_cache, name="dispatch")
class StaffLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = StaffAuthenticationForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_enabled"] = settings.STAFF_LOGIN_ENABLED
        return context

    def post(self, request, *args, **kwargs):
        if not settings.STAFF_LOGIN_ENABLED:
            form = self.get_form_class()(request=request)
            return render(request, self.template_name, self.get_context_data(form=form), status=503)
        return super().post(request, *args, **kwargs)


@never_cache
@login_required
def portal(request):
    if not request.user.is_staff:
        raise PermissionDenied
    return render(request, "registration/portal.html")
