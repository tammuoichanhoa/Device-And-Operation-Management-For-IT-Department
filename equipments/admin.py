from django.contrib import admin
from common.models import *
from common.admin import *
from .models import *
from mptt.admin import DraggableMPTTAdmin
from django.utils.html import format_html
from mptt.admin import TreeRelatedFieldListFilter
from django.contrib.admin import SimpleListFilter

class EquipmentForm(forms.ModelForm):
    # request_type = TreeNodeChoiceField(queryset=RequirementType.objects.all(), required=False, label="Loại yêu cầu")
    department = TreeNodeChoiceField(queryset=Department.objects.all(), required=False, label="Phòng ban")
    class Meta:
        model = Equipment
        fields = '__all__'

# Equipment Admin (hiển thị dạng cây)
@admin.register(Equipment)
class EquipmentAdmin(DraggableMPTTAdmin):
    # mptt_indent_field = "indented_serial"
    list_per_page = 20
    form = EquipmentForm
    list_display = (
        'tree_actions',
        'indented_title',
        'model',
        'department',
        'group',
        'available',
    )
    list_display_links = ('indented_title',)

    # def indented_serial(self, instance):
    #     return instance.serial
    # indented_serial.short_description = 'Số serial'

    list_filter = (
        ('department',TreeRelatedFieldListFilter),
        ('model__type',TreeRelatedFieldListFilter),
        'available',
        'group',
        'country',
       
        'manufacturer',
    )

    search_fields = (
        'serial',
        'ms',
        'model__name',
        'department__name',
        'manufacturer__name',
    )

    autocomplete_fields = (
        'model',
        'department',
        'manufacturer',
        'parent',
    )

    fieldsets = (
        ('Thông tin chung', {
            'fields': ('serial', 'ms', 'model', 'department', 'year','purpose', 'source', 'country', 'manufacturer', 'available')
        }),
        ('Cấu hình & Lưu trữ', {
            'fields': ('specification', 'storage_location', 'short_description')
        }),
        ('Thông tin bảo hành', {
            'fields': ('expiry_date', 'waranty_info')
        }),
        ('Phân loại và phân cấp', {
            'fields': ( 'group', 'parent')
        }),
    )

# Thiết bị mạng
@admin.register(NetworkDevice)
class NetworkDeviceAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'network', 'equipment',)
    list_filter = ('network',)
    search_fields = ('id', 'equipment__id',)
    filter_horizontal = ('address',)

# Vật tư tiêu hao
@admin.register(ConsumableEquipment)
class ConsumableEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipment', 'quantity')
    list_filter = ('equipment',)
    search_fields = ('equipment__serial', 'equipment__ms', 'equipment__model__type__name')
    # readonly_fields = ('id',)
    list_per_page = 20
    autocomplete_fields = ('equipment',)

    fieldsets = (
        ('Thông tin vật tư tiêu hao', {
            'fields': ('equipment', 'quantity')
        }),
    )

