from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserModel, UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.forms import forms
from django.forms.fields import CharField, EmailField
from django.forms.widgets import PasswordInput
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_variables


class AuthenticationForm(forms.Form):
    account = CharField()
    password = CharField(
        widget=PasswordInput(attrs={"autocomplete": "current-password"})
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self , request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    @sensitive_variables()
    def clean(self):
        account = self.cleaned_data.get('account')
        password = self.cleaned_data.get('password')

        if account and password:
            uq = Q(username=account) | Q(email=account)
            user = UserModel.objects.filter(uq).first()
            self.user_cache = authenticate(username=user.username if user else '', password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={'username': 'account'}
        )

class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("username", 'email')
        field_classes = {
            "username": UsernameField,
            "email": EmailField,
        }
