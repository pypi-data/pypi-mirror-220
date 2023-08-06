from django.contrib import admin

from webkassa.models import Check, WebKassaAccount


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

    readonly_fields = ('id', 'created_at', 'updated_at', 'is_encrypted', 'token')
