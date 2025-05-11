from django.apps import apps
from django.contrib import admin
from .models import *
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin as IEA
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from mptt.forms import TreeNodeChoiceField

# ========================================================================================================================
#                                                Quản lý cán bộ, nhân viên
# ========================================================================================================================

@admin.register(StaffRole)
class StaffRoleAdmin(IEA, admin.ModelAdmin):
    search_fields=('name',)

@admin.register(Department)
class DepartmentAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'id', 'parent')
    list_display_links = ('indented_title',)
    search_fields = ('name', 'id')

@admin.register(Staff)
class StaffAdmin(IEA, admin.ModelAdmin):
    search_fields=('name',)
    ordering = ('id',)
    list_filter= ('staffrole','department')
    list_display = ('id', 'name', 'staffrole', 'department', 'status')

# ========================================================================================================================
#                                                Quản lý công văn
# ========================================================================================================================
@admin.register(DocumentTypes)
class DocumentTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    ordering = ('id',)


class BaseDocumentsAdmin(admin.ModelAdmin):
    """Lớp cơ sở cho Admin của văn bản đi và đến"""
    date_hierarchy = 'date'
    readonly_fields = ('ms',)
    search_fields = ('ms', 'title', 'note')
    list_filter = ('document_type', 'security', 'date')
    
    def get_fieldsets(self, request, obj=None):
        """Tạo cấu trúc nhóm các trường thông tin"""
        return (
            ('Thông tin cơ bản', {
                'fields': ('ms', 'document_type', 'date', 'title', 'quantity', 'pages', 'security', 'note')
            }),
            # Các nhóm khác sẽ được thêm vào bởi lớp con
        )
    
    def get_ms_display(self, obj):
        """Format hiển thị số văn bản"""
        return format_html('<span style="font-weight: bold; color: #1a3d66;">{}</span>', obj.ms)
    
    get_ms_display.short_description = 'Số văn bản'
    get_ms_display.admin_order_field = 'ms'
    
    def get_search_results(self, request, queryset, search_term):
        """Tối ưu tìm kiếm"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        # Có thể thêm logic tìm kiếm nâng cao ở đây nếu cần
        return queryset, use_distinct

# ========================================================================================================================
#                                                Quản lý khác
# ========================================================================================================================

@admin.register(ErrorType)
class ErrorTypeAdmin(IEA, admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

@admin.register(ConnectionType)
class ConnectionTypeAdmin(IEA, admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

@admin.register(HandleStatusType)
class HandleStatusTypeAdmin(IEA, admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

class ManufacturerAdmin(IEA, admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
admin.site.register(Manufacturer, ManufacturerAdmin)

@admin.register(StaffUser)
class StaffUserAdmin(IEA, admin.ModelAdmin):
    list_display = ('user', 'staff')  
    search_fields = ('user__username', 'staff__name')  
    list_filter = ('staff__department',) 
    autocomplete_fields = ('user', 'staff') 


# ========================================================================================================================
#                                                Quản lý mạng máy tính
# ========================================================================================================================
@admin.register(NetworkAddress)
class NetworkAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'mac_address')
    search_fields = ('id', 'ip_address', 'mac_address')

# @admin.register(ComputerNetwork)
# class ComputerNetworkAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'description')
#     search_fields = ('id', 'name', 'description')


# ========================================================================================================================
#                                                Xử lý kỹ thuật
# ========================================================================================================================

@admin.register(RequirementType)
class RequirementTypeAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'unit')
    list_display_links = ('indented_title',)
    search_fields = ('name',)
    # list_filter = ('unit',)
    # ordering = ('name',)
    # list_per_page = 20


# ========================================================================================================================
#                                                Quản lý thiết bị 
# ========================================================================================================================
@admin.register(EquipmentType)
class EquipmentTypeAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'name')
    list_display_links = ('indented_title',)
    search_fields = ('name',)


from mptt.admin import TreeRelatedFieldListFilter

class EquipmentModelForm(forms.ModelForm):
    type = TreeNodeChoiceField(queryset=EquipmentType.objects.all(), required=False, label="Loại trang bị")

    class Meta:
        model = EquipmentModel
        fields = '__all__'
        
@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    form = EquipmentModelForm
    list_display = ('id', 'name', 'battery', 'needdriver', 'cable', 'features', 'specifications')
    search_fields = ('name',)
    list_filter = ('battery', 'needdriver', 'cable', ('type', TreeRelatedFieldListFilter), )
    ordering = ('name',)
    list_per_page = 20

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

    def __str__(self):
        return self.name if self.name else "Không xác định"
    
