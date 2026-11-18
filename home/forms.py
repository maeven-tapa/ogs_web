from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class StaffAuthenticationForm(AuthenticationForm):
    """Django's normal password authentication, restricted to active staff."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "autocomplete": "username",
            "placeholder": "Enter your staff username",
            "autocapitalize": "none",
            "spellcheck": "false",
        })
        self.fields["password"].widget.attrs.update({
            "autocomplete": "current-password",
            "placeholder": "Enter your password",
        })

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            # Keep account type and existence private on failed sign-in.
            raise ValidationError(self.error_messages["invalid_login"], code="invalid_login", params={"username": self.username_field.verbose_name})
