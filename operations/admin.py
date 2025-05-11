from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from smart_selects.form_fields import ChainedModelChoiceField
from mptt.admin import TreeRelatedFieldListFilter
from mptt.forms import TreeNodeChoiceField
from common.models import *
from common.admin import *
from equipments.models import Equipment
from .models import *


# Register BaseOperation if needed for direct access
# @admin.register(BaseOperation)
# class BaseOperationDetailAdmin(BaseOperationAdmin):
#     """Admin for viewing base operations directly if needed."""
#     pass
class BaseOperationForm(forms.ModelForm):
    request_type = TreeNodeChoiceField(queryset=RequirementType.objects.all(), required=False, label="Loại yêu cầu")
    department = TreeNodeChoiceField(queryset=Department.objects.all(), required=False, label="Phòng ban")
    class Meta:
        model = BaseOperation
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Giới hạn chỉ các thiết bị thuộc nhóm 1
        self.fields['equipments'].queryset = Equipment.objects.filter(group='1')

class BaseOperationAdmin(admin.ModelAdmin):
    """Base admin class for all operations."""
    form = BaseOperationForm
    list_display = ('id', 'received_at', 'department', 'request_type', 'status')
    list_filter = ('status', 'department', 'request_type')
    search_fields = ('id', 'department', 'department__name', 'request_type__name')
    readonly_fields = ('id',)
    filter_horizontal = ('equipments', )
    autocomplete_fields = ('equipments',)

@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'department',
        'requester',
        'status',
        'quantity',
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'id',
        'requester__name',
        'department__name',
        'request_type__name',
    )
    autocomplete_fields = (
        'department',
        'requester',
        'department_approver',
        'receiving_officer',
        'result_deliverer',
        'result_receiver',
        'request_type',
        'processing_staff',
        'equipments'
    )
    filter_horizontal = ('equipments', 'processing_staff')
    readonly_fields = ('id',)

    fieldsets = (
        ('Thông tin yêu cầu', {
            'fields': (
                'department',
                'department_approver',
                'request_type',
                'requester',
                'request_content',
                'quantity',
               
            )
        }),
        ('Tiếp nhận & xử lý', {
            'fields': (
                'receiving_officer',
                'received_at',
                'processing_staff',
                'processing_content',
                'status',
            )
        }),
        ('Trả kết quả', {
            'fields': (
                'result_deliverer',
                'delivered_at',
                'result_receiver',
                'has_material_debt',
                'notes',
            )
        })
        
    )

@admin.register(EquipmentDeployment)
class EquipmentDeploymentAdmin(BaseOperationAdmin):
    """Admin for equipment deployment."""
    list_display = ('id', 'borrower', 'department', 'borrow_date', 'st')
    list_filter = ('status', 'department', 'st', 'borrow_date')
    search_fields = ('id', 'borrower__name', 'department__name')
    
    fieldsets = (

        (_('Thông tin mượn'), {
            'fields': ('department', 'borrower', 'borrow_date', 'lender', 'equipments',)
        }),
        (_('Thông tin trả'), {
            'fields': ('payer', 'pay_date', 'receiver', 'hours', 'st', 'notes')
        })
    )


@admin.register(EquipmentRepair)
class EquipmentRepairAdmin(BaseOperationAdmin):
    """Admin for equipment repair history."""
    list_display = ('id', 'department', 'status')
    list_filter = ( 'department', 'status')
    search_fields = ('id',  'department__name')
    
    fieldsets = (
        ('Thông tin yêu cầu', {
            'fields': (
                'department',
                'department_approver',
                'requester',
                'equipments',
                'error',
            )
        }),
        ('Tiếp nhận & xử lý', {
            'fields': (
                # 'receiving_officer',
                'repair_date',
                'repair_staff',
                'repair_content',
            )
        }),
        ('Trả kết quả', {
            'fields': (
                'result_deliverer',
                'delivered_at',
                'result_receiver',
            )
        })  
    )

@admin.register(EquipmentHandover)
class EquipmentHandoverAdmin(BaseOperationAdmin):
    """Admin for equipment handover."""
    list_display = ('id', 'from_staff', 'to_staff', 'department', 'handover_date', 'status')
    list_filter = ('handover_date', 'department', 'status')
    search_fields = ('id', 'from_staff__name', 'to_staff__name', 'department__name')
    
    fieldsets = (
        (_('Thông tin bàn giao'), {
            'fields': ('department', 'from_staff', 'to_staff', 'handover_date','equipments', 'notes',)
        }),
    )


@admin.register(EquipmentLiquidation)
class EquipmentLiquidationAdmin(BaseOperationAdmin):
    """Admin for equipment liquidation."""
    list_display = ('id', 'liquidation_date', 'department', 'approved_by', 'status')
    list_filter = ('liquidation_date', 'department', 'status')
    search_fields = ('id', 'department__name', 'approved_by__name')
    
    fieldsets = (
        (_('Thông tin thanh lý'), {
            'fields': ('department', 'liquidation_date', 'approved_by', 'equipments', 'status', 'notes',)
        }),
    )


@admin.register(NetworkMaintenanceLog)
class NetworkMaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'network', 'date')
    list_filter = ('network', 'date', 'performed_by')
    autocomplete_fields = ['performed_by',] 
    search_fields = ('id', 'network__name', 'performed_by__name', 'description', 'performed_by',)
    ordering = ('-date',)
