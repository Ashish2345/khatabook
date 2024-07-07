from difflib import SequenceMatcher

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm

from .models import User


def is_password_too_similar_to_user_attributes(
    username, first_name, email, last_name, password, threshold=0.8
):
    """
    Check if the password is too similar to user attributes based on similarity ratio.
    """
    user_attributes = [username, first_name, email, last_name]
    for attribute in user_attributes:
        similarity_ratio = SequenceMatcher(
            None, attribute.lower(), password.lower()
        ).ratio()
        if similarity_ratio >= threshold:
            return True
    return False


class SignupForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"type": "email"})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control p-right"}),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control p-right"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username:
            raise forms.ValidationError("Username cannot be empty")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        username = self.cleaned_data.get("username", "")
        first_name = self.cleaned_data.get("first_name", "")
        email = self.cleaned_data.get("email", "")
        last_name = self.cleaned_data.get("last_name", "")

        if is_password_too_similar_to_user_attributes(
            username, first_name, email, last_name, password1
        ):
            raise forms.ValidationError("New password is too similar to user details")

        return password1


class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"readonly": True})

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class LoginForm(forms.Form):
    email = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"type": "email"})
    )
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control empty"})

    def clean_username(self):
        data = self.cleaned_data["email"]
        if not data:
            raise forms.ValidationError("Email cannot be Empty")
        return data

    def clean_password(self):
        data = self.cleaned_data["password"]
        if not data:
            raise forms.ValidationError("Password cannot be Empty")
        return data


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Current Password"}
        ),
    )
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )

    def set_user(self, user):
        self.user = user

    def clean(self):
        current_password = self.cleaned_data.get("current_password")
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")

        if not self.user.check_password(current_password):
            raise forms.ValidationError(
                {"current_password": "Incorrect current password"}
            )

        if password and confirm_password:
            if password and confirm_password:
                # Validate new password using Django's password validation framework
                try:
                    password_validation.validate_password(password)
                except forms.ValidationError as error:
                    self.add_error("password1", error)
                if password != confirm_password:
                    raise forms.ValidationError("Password confirmation failed")


class NewPasswordform(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control p-right", "type": "password"}
        ),
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control p-right", "type": "password"}
        ),
    )

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password:
            # Validate new password using Django's password validation framework
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error("password", error)
            if password != confirm_password:
                raise forms.ValidationError("Password confirmation failed")
        return self.cleaned_data


class UserCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not username:
            raise forms.ValidationError("Username cannot be Empty")

        if self.instance.pk is None:
            # Creating a new user, check if username already exists
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already exists")
        else:
            # Updating an existing user, check if username already exists and is different from current value
            if (
                User.objects.filter(username=username)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise forms.ValidationError("Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not email:
            raise forms.ValidationError("Email cannot be Empty")

        if self.instance.pk is None:
            email_qs = User.objects.filter(email=email).exists()
            if email_qs:
                raise forms.ValidationError("Email already exists")
            else:
                if (
                    User.objects.filter(email=email)
                    .exclude(pk=self.instance.pk)
                    .exists()
                ):
                    raise forms.ValidationError("Email already exists")

        return email
