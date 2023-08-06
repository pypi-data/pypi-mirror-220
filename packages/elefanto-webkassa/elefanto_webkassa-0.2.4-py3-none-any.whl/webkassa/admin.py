from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from webkassa.models import Check, WebKassaAccount, WebkassaErrorLog


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'show_ticket_url', 'check_order_number')
    list_display_links = ('id', 'date_time', 'check_order_number')

    def show_ticket_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.ticket_url)

    show_ticket_url.short_description = _('Ticket URL')

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

    readonly_fields = ('id', 'created_at', 'updated_at', 'is_encrypted', 'token')


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
