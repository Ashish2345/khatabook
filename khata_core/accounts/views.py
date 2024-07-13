from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View

from .forms import LoginForm, PasswordChangeForm
from general.mixins import NonLoginRequiredMixin
from general.utils import store_audit


class LoginView(NonLoginRequiredMixin, View):
    template_name = "authentication/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": LoginForm()})

    def post(self, request, *args, **kwargs):
        post_dict = self.request.POST.dict()
        form = LoginForm(data={**post_dict})
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request=request, username=email, password=password)
            if user is not None:
                if user.is_verified_email:
                    login(request, user)
                    store_audit(
                        request=self.request,
                        instance=user,
                        action="Logged in Successfully",
                    )
                    if not request.POST.get("remember_me"):
                        request.session.set_expiry(0)
                    return redirect("accounts:dashboard")
                else:
                    request.session["email"] = user.email
                    return redirect("accounts:verify-email")
            else:
                return render(
                    request,
                    self.template_name,
                    {"form": LoginForm(), "msg_error": "Invalid Email and/or Password"},
                )
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:login")


class PasswordChangeView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "change_password.html"
        usr_id = kwargs.get("pk")
        form = PasswordChangeForm()
        self.args = {
            "form": form,
            "user_id": usr_id,
        }
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.args)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.POST)
        form.set_user(request.user)
        if form.is_valid():
            new_password = form.cleaned_data.get("password1")
            user = request.user
            user.set_password(new_password)
            user.save()
            context = {"title": "Password", "message": "Password Changed Successfully"}
            store_audit(request=self.request, instance=user, action=context["title"])
            messages.success(request, "Password changed successfully!")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            self.args = {
                "form": form,
                "user_id": self.args["user_id"],
            }
            return render(request, self.template_name, self.args)


class DashboardView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "index.html"
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
