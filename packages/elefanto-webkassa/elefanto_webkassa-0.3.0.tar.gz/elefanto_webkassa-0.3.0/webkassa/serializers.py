from rest_framework import serializers

from webkassa.models import Check


class CheckSerializer(serializers.ModelSerializer):
    CheckNumber = serializers.CharField(source='check_number', required=False)
    DateTime = serializers.CharField(source='date_time', required=False)
    Cashbox = serializers.JSONField(source='cash_box', required=False)
    CheckOrderNumber = serializers.IntegerField(source='check_order_number', required=False)
    ShiftNumber = serializers.IntegerField(source='shift_number', required=False)
    EmployeeName = serializers.CharField(source='employee_name', required=False)
    TicketUrl = serializers.URLField(source='ticket_url', required=False)
    TicketPrintUrl = serializers.URLField(source='ticket_print_url', required=False)
    ExternalCheckNumber = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Check
        fields = ('CheckNumber', 'DateTime', 'Cashbox',
                  'CheckOrderNumber', 'ShiftNumber', 'EmployeeName', 'TicketUrl', 'TicketPrintUrl',
                  'ExternalCheckNumber')
        read_only_fields = ('external_check_number',)

    def get_ExternalCheckNumber(self, obj):
        return str(obj.id)
