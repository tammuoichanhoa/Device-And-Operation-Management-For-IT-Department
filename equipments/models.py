from django.db import models
from common.models import *
from django.utils.timezone import now
from smart_selects.db_fields import ChainedForeignKey
from current_user import get_current_user
from django.contrib.auth import get_user_model
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.
# ========================================================================================================================
#                                                Quản lý trang bị
# ========================================================================================================================


class Equipment(MPTTModel):
    class Meta:
        db_table = 'equipment'
        verbose_name = 'Trang thiết bị'
        verbose_name_plural ='Trang thiết bị'

    serial = models.CharField(max_length = 20,  primary_key = True, verbose_name ='Số seri trang thiết bị')
    ms = models.CharField(max_length = 50, verbose_name='MS', null = True, blank = True, unique=True)
    model = models.ForeignKey(EquipmentModel, on_delete=models.SET_NULL, verbose_name = 'Model trang thiết bị', null = True, blank = True)
    year = models.PositiveIntegerField(verbose_name='Năm đưa vào sử dụng', null = True, blank = True)
    source = models.CharField(max_length=10,choices=settings.SOURCES,verbose_name='Nguồn cấp trang bị KTĐB', null=True, blank=True)
    specification = models.TextField(verbose_name='Cấu hình trang bị',null = True, blank = True)
    storage_location = models.TextField(verbose_name='Vị trí lưu trữ trang bị',null = True, blank = True)
    department = models.ForeignKey(Department, verbose_name= 'Phòng/ban quản lý', on_delete=models.PROTECT, null = True, blank = True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, verbose_name='Hãng sản xuất', null = True, blank = True)
    country = models.CharField(max_length=3, choices=settings.COUNTRIES, verbose_name='Xuất xứ', null=True, blank=True)
    purpose = models.CharField(max_length=100, choices=settings.USAGE_PURPOSES, verbose_name='Mục đích sử dụng', null=True, blank=True)
    group = models.CharField(max_length=100, choices=settings.GROUPS, verbose_name='Nhóm', null=True, blank=True)
    available = models.BooleanField(verbose_name = 'Sẵn sàng đưa vào sử dụng', default=True)
    expiry_date = models.DateField(verbose_name= 'Ngày hết hạn bảo hành',  null = True, blank = True)
    waranty_info = models.TextField(verbose_name = 'Thông tin bảo hành',  null = True, blank = True)
    short_description = models.TextField(verbose_name = 'Mô tả', null = True, blank = True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Thiết bị cha'
    )

    class MPTTMeta:
            order_insertion_by = ['serial']
    def __str__(self):
        return self.model.name + '-' + self.serial if self.serial else "Không có serial"
    

class ConsumableEquipment(models.Model):
    """Quản lý danh mục vật tư tiêu hao."""
    class Meta:
        db_table = 'consumable_equipment'
        verbose_name = 'Vật tư tiêu hao'
        verbose_name_plural = 'Vật tư tiêu hao'

    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, verbose_name='Trang bị')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Số lượng')

    def __str__(self):
        return f"{self.equipment} - SL: {self.quantity}"
    
class NetworkDevice(models.Model):
    """Thiết bị trong từng mạng máy tính."""
    class Meta:
        db_table = 'network_devices'
        verbose_name = 'Thiết bị mạng'
        verbose_name_plural = 'Thiết bị mạng'

    id = models.AutoField(primary_key=True, verbose_name='ms')
    # network = models.ForeignKey(
    #     ComputerNetwork, on_delete=models.CASCADE, verbose_name='Mạng máy tính', related_name='devices'
    # )
    network = models.CharField(max_length=50, choices=settings.COMPUTER_NETWORKS, verbose_name='Mạng máy tính', null=True, blank=True)
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, verbose_name='Thiết bị', related_name='network_devices'
    )
    address = models.ManyToManyField(NetworkAddress, verbose_name='Địa chỉ mạng', blank=True, related_name="network_device_address")

    def __str__(self):
        return f"{self.equipment.serial}"

