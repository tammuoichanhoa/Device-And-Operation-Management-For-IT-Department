from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django import forms
# ========================================================================================================================
#                                                Quản lý  nhân viên
# ========================================================================================================================

class Department(MPTTModel):
    class Meta:
        db_table = 'department'
        verbose_name = 'Phòng/Ban'
        verbose_name_plural = 'Phòng/Ban'

    id = models.CharField(max_length=10, primary_key=True, verbose_name='MS')
    name = models.CharField(max_length=100, blank=False, verbose_name='Tên Phòng/Ban')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name='Phòng/Ban cha')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
    

class StaffRole(models.Model):
    class Meta:
        db_table = 'staffrole'
        verbose_name = 'Chức vụ'
        verbose_name_plural ='Chức vụ'
    
    id = models.CharField(max_length = 10, primary_key = True,verbose_name='MS')
    name = models.CharField(max_length=100, blank=False, unique=True, verbose_name ='Chức vụ')

    def __str__(self):
        return f"{self.name}"


class Staff(models.Model):
    class Meta:
        db_table = 'staff'
        verbose_name = 'Cán bộ/Nhân viên'
        verbose_name_plural ='Cán bộ/Nhân viên'
    
    id = models.AutoField(primary_key = True,verbose_name='MS')
    name = models.CharField(max_length=100, blank=False, verbose_name ='Họ và tên')
    staffrole = models.ForeignKey(StaffRole,on_delete=models.PROTECT, blank=False, verbose_name='Chức vụ')
    department = models.ForeignKey(Department,on_delete=models.PROTECT, blank=False, verbose_name = 'Phòng/Ban', related_name="departments")
    status = models.BooleanField(default=False, verbose_name='Đã nghỉ việc')
    phonenumber = models.CharField(max_length=10, blank=True, null=True, verbose_name ='Số điện thoại')

    def __str__(self):
        return f"{self.name}" +","+ self.staffrole.id + " " + self.department.name
    

# ========================================================================================================================
#                                                Quản lý công văn
# ========================================================================================================================

class DocumentTypes(models.Model):
    class Meta:
        db_table = 'document_types'
        verbose_name = 'Loại văn bản'
        verbose_name_plural = 'Loại văn bản'
    
    id = models.CharField(max_length=10, primary_key=True, verbose_name='MS')
    name = models.CharField(max_length=100, blank=False, unique=True, verbose_name='Loại văn bản')

    def __str__(self):
        return self.name

class BaseDocument(models.Model):
    """Lớp cơ sở cho cả văn bản đi và đến, tránh lặp mã nguồn"""
    class Meta:
        abstract = True
    
    id = models.AutoField(primary_key=True, verbose_name='id')
    ms = models.CharField(max_length=20, verbose_name='Số văn bản')
    document_type = models.ForeignKey(DocumentTypes, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Loại văn bản')
    date = models.DateField(verbose_name='Ngày')
    title = models.CharField(max_length=2000, verbose_name="Trích yếu")
    quantity = models.IntegerField(verbose_name="Số lượng bản")
    pages = models.IntegerField(verbose_name="Số lượng tờ")
    security = models.CharField(max_length=20, choices=settings.SECURITY_LEVELS, verbose_name='Độ mật', null=True, blank=True, default='BT')
    note = models.TextField(verbose_name="Ghi chú", null=True, blank=True)

    def __str__(self):
        return self.ms

# ========================================================================================================================
#                                                Quản lý khác
# ========================================================================================================================
# class UsagePurpose(models.Model):
#     """Danh mục mục đích sử dụng trang bị."""
#     class Meta:
#         db_table = 'usage_purpose'
#         verbose_name = 'Mục đích sử dụng'
#         verbose_name_plural = 'Mục đích sử dụng'

#     id = models.CharField(max_length=50, primary_key=True, verbose_name='MS')
#     name = models.CharField(max_length=255, unique=True, verbose_name='Tên mục đích')

#     def __str__(self):
#         return self.name

class ErrorType(models.Model):
    class Meta:
        db_table = 'errortype'
        verbose_name = 'Hỏng hóc'
        verbose_name_plural ='Hỏng hóc'
    
    id = models.CharField( max_length=10, primary_key = True,verbose_name='MS')
    name = models.CharField(max_length=100, blank=False, unique=True, verbose_name='Hỏng hóc')
    
    def __str__(self):
        return self.name
    
class HandleStatusType(models.Model):
    class Meta:
        db_table = 'handlestatustype'
        verbose_name = 'Trạng thái xử lý'
        verbose_name_plural ='Trạng thái xử lý'
    
    id = models.CharField( max_length=10, primary_key = True,verbose_name='MS')
    name = models.CharField(max_length=100, blank=False, unique=True, verbose_name='Trạng thái')
    
    def __str__(self):
        return self.name

class ConnectionType(models.Model):
    class Meta:
        db_table = 'connectiontype'
        verbose_name = 'Kiểu cáp kết nối'
        verbose_name_plural ='Kiểu cáp kết nối'
    
    id = models.CharField(max_length = 50, primary_key = True,verbose_name='MS')
    name = models.CharField(max_length = 100, verbose_name ='Kiểu kết nối', null = True, blank = True)

    def __str__(self):
        return self.name
    
class Manufacturer(models.Model):
    class Meta:
        db_table = 'manufacturer'
        verbose_name = 'Hãng sản xuất'
        verbose_name_plural = 'Hãng sản xuất'
    
    id = models.CharField(max_length = 20, verbose_name='MS', primary_key=True)
    name = models.CharField(max_length = 50, verbose_name='Hãng sản xuất', default='')

    def __str__(self):
        return self.name
    
class StaffUser(models.Model):
    class Meta:
        db_table = "staff_user"
        verbose_name = "Tài khoản"
        verbose_name_plural = "Tài khoản"
        unique_together = ('user', 'staff')  # Đảm bảo một cặp user-staff là duy nhất

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Tài khoản", related_name="staff_user")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="Nhân viên", related_name="user_accounts")

    def __str__(self):
        return f"{self.user.username} - {self.staff.name}"


# ========================================================================================================================
#                                                Quản lý mạng máy tính
# ========================================================================================================================
class NetworkAddress(models.Model):
    class Meta:
        db_table = 'networkaddress'
        verbose_name = 'Địa chỉ mạng'
        verbose_name_plural = 'Địa chỉ mạng'

    id = models.AutoField(primary_key=True, verbose_name='Ms')
    mac_address = models.CharField(max_length=17, verbose_name='Địa chỉ MAC', blank=False, null=False, unique=True, default="FF:FF:FF:FF:FF:FF")
    ip_address = models.GenericIPAddressField(verbose_name='Địa chỉ IP', blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address}"
    

# class ComputerNetwork(models.Model):
#     """Danh mục mạng máy tính."""
#     class Meta:
#         db_table = 'computer_networks'
#         verbose_name = 'Mạng máy tính'
#         verbose_name_plural = 'Mạng máy tính'

#     id = models.AutoField(primary_key=True, verbose_name='Ms')
#     name = models.CharField(max_length=255, unique=True, verbose_name='Tên mạng')
#     description = models.TextField(verbose_name='Mô tả', blank=True, null=True)

#     def __str__(self):
#         return self.name

# ========================================================================================================================
#                                                Xử lý kỹ thuật
# ========================================================================================================================
class RequirementType(MPTTModel):
    class Meta:
        db_table = 'requirementtype'
        verbose_name = 'Loại Yêu cầu XLKT'
        verbose_name_plural ='Loại yêu cầu XLKT'

    id = models.AutoField(primary_key = True,verbose_name='MS')
    name = models.CharField(max_length=100, blank=False, unique=True,verbose_name= 'Tên yêu cầu')
    unit = models.CharField(max_length=100, blank=False, verbose_name = 'Đơn vị tính')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name='Parent')
    # is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
# ========================================================================================================================
#                                                Quản lý thiết bị 
# ========================================================================================================================

class EquipmentType(MPTTModel):
    """Quản lý danh mục nhóm loại trang bị."""
    class Meta:
        db_table = 'equipment_type'
        verbose_name = 'Loại trang bị'
        verbose_name_plural = 'Loại trang bị'

    id = models.CharField(max_length=50, primary_key=True, verbose_name='MS')
    name = models.CharField(max_length=255, unique=True, verbose_name='Loại trang bị')
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Loại trang bị cha'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
    

class EquipmentModel(models.Model):
    class Meta:
        db_table = 'equipmentmodel'
        verbose_name = 'Model trang bị'
        verbose_name_plural ='Model trang bị'

    id = models.AutoField(primary_key=True, verbose_name='MS')
    name = models.CharField(max_length = 200,verbose_name='Trang bị')
    battery = models.BooleanField(verbose_name='Tích hợp pin sạc', default= False)
    needdriver = models.BooleanField(verbose_name='Cần driver riêng', default= False)
    cable = models.ForeignKey(ConnectionType, on_delete=models.PROTECT, verbose_name = 'Kiểu kết nối', null = True, blank = True)
    features = models.TextField(verbose_name='Tính năng trang bị',null = True, blank = True)
    specifications = models.JSONField(verbose_name='Thông số kỹ thuật', null=True, blank=True,  default=dict)
    type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT, verbose_name='Loại trang bị', null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Không xác định"
