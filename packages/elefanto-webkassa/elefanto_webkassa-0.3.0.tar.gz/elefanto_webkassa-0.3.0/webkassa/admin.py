from django.contrib import admin, messages
from django.contrib.admin.utils import unquote
from django.contrib.auth.admin import sensitive_post_parameters_m
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import escape
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from webkassa.forms import AccountChangeForm, AdminAccountPasswordChangeForm, BaseAccountCreationForm
from webkassa.models import Check, WebKassaAccount, WebkassaErrorLog


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'ticket_url', 'check_order_number')
    list_display_links = ('id', 'date_time', 'check_order_number')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(WebKassaAccount)
class WebKassaAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'cashbox_unique_number', 'updated_at')
    list_display_links = ('id', 'email', 'cashbox_unique_number', 'updated_at')

    readonly_fields = ('id', 'created_at', 'updated_at', 'token')

    add_form_template = 'admin/change_form.html'
    form = AccountChangeForm
    add_form = BaseAccountCreationForm
    change_password_form = AdminAccountPasswordChangeForm
    change_account_password_template = 'change_password_template.html'

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_urls(self):
        return [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.account_change_password),
                name='auth_user_password_change',
            ),
        ] + super().get_urls()

    @sensitive_post_parameters_m
    def account_change_password(self, request, id, form_url=''):
        instance = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, instance):
            raise PermissionDenied
        if instance is None:
            raise Http404(
                _('%(name)s object with primary key %(key)r does not exist.')
                % {
                    'name': self.opts.verbose_name,
                    'key': escape(id),
                },
            )
        if request.method == 'POST':
            form = self.change_password_form(instance, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, instance, change_message)
                msg = gettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change'
                        % (
                            self.admin_site.name,
                            instance._meta.app_label,
                            instance._meta.model_name,
                        ),
                        args=(instance.pk,),
                    ),
                )
        else:
            form = self.change_password_form(instance)
        fieldsets = [(None, {'fields': list(form.base_fields)})]
        admin_form = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(instance.email),
            'adminForm': admin_form,
            'form_url': form_url,
            'form': form,
            'is_popup': False,
            'is_popup_var': False,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.opts,
            'original': instance,
            'save_as': False,
            'show_save': True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_account_password_template
            or 'admin/auth/user/change_password.html',
            context,
        )


@admin.register(WebkassaErrorLog)
class WebkassaErrorLogAdmin(admin.ModelAdmin):
    list_display = ('check', 'code', 'text', 'created_at')
    list_display_links = ('check', 'code', 'text', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('check_obj')
