import unicodedata

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.utils.translation import gettext, gettext_lazy as _

from webkassa.models import WebKassaAccount


class EmailField(forms.EmailField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'email',
        }


class BaseAccountCreationForm(forms.ModelForm):
    """
    A form that creates an account.
    """

    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = WebKassaAccount
        fields = '__all__'
        field_classes = {'email': EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].widget.attrs[
                'autofocus'
            ] = True


class AccountCreationForm(BaseAccountCreationForm):
    def clean_email(self):
        """Reject usernames that differ only in case."""
        return self.cleaned_data.get('email')


class AdminAccountPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a webkassa account in the admin interface.
    """
    required_css_class = 'required'
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'autofocus': True},
        ),
        strip=False,
    )

    def __init__(self, account, *args, **kwargs):
        self.account = account
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """Save the new password."""
        password = self.cleaned_data['password']
        self.account.set_password(password)
        if commit:
            self.account.save()
        return self.account


class AccountReadOnlyPasswordHashWidget(ReadOnlyPasswordHashWidget):

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value:
            summary.append({'label': gettext('No password set.')})
        else:
            summary.append({'label': value})
        context['summary'] = summary
        return context


class AccountReadOnlyPasswordHashField(forms.Field):
    widget = AccountReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault('disabled', True)
        super().__init__(*args, **kwargs)


class AccountChangeForm(forms.ModelForm):
    password = AccountReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_(
            'Raw passwords are not stored, so there is no way to see this '
            'account’s password, but you can change the password using '
            '<a href="{}">this form</a>.',
        ),
    )

    class Meta:
        model = WebKassaAccount
        fields = '__all__'
        field_classes = {'email': EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format(
                f'../../{self.instance.pk}/password/',
            )
