from django.db import models
from common.models import *
from smart_selects.db_fields import ChainedForeignKey
from current_user import get_current_user
from django.contrib.auth import get_user_model
from datetime import datetime
from equipments.models import Equipment
from mptt.forms import TreeNodeChoiceField
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
# ========================================================================================================================
#                                                Xử lý kỹ thuật
# ========================================================================================================================
 
User = get_user_model()
class BaseOperation(models.Model):
    class Meta:
        db_table = 'base_operation'
        verbose_name = 'Xử lý kỹ thuật'
        verbose_name_plural = 'Xử lý kỹ thuật'

    id = models.AutoField(primary_key=True, verbose_name='MS')

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name="Đơn vị/Phòng ban"
    )

    request_type = models.ForeignKey(
        RequirementType,
        on_delete=models.PROTECT,
        verbose_name="Loại yêu cầu",
        null=True,
        blank=True
    )
    received_at = models.DateTimeField(
        verbose_name="Ngày tiếp nhận yêu cầu",
        default=datetime.now
    )
    equipments = models.ManyToManyField(Equipment, blank=True,  verbose_name="Trang bị", related_name="equipments")
    status = models.ForeignKey(
        HandleStatusType,
        on_delete=models.PROTECT,
        verbose_name="Trạng thái",
        default='TN'
    )

    notes = models.TextField(
        verbose_name='Ghi chú',
        blank=True,
        null=True,
        # default=dict
    )
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        try:
            return f"{self.id} - {self.received_at.strftime('%Y-%m-%d')} - {self.department.name} - {self.request_type.name}"
        except Exception as e:
            return f"Yêu cầu #{self.id}"
        
class Requirement(BaseOperation):
    class Meta:
        db_table = 'requirement'
        verbose_name = 'Yêu cầu xử lý'
        verbose_name_plural = 'Yêu cầu xử lý'

    department_approver = ChainedForeignKey(
        Staff,
        on_delete=models.PROTECT,
        verbose_name="Chỉ huy phòng ban phê duyệt",
        related_name='ktdb_approver',
        chained_field="department",
        chained_model_field="department",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True
    )

    requester = ChainedForeignKey(
        Staff,
        on_delete=models.PROTECT,
        verbose_name="Cán bộ yêu cầu xử lý",
        related_name='ktdb_presenter',
        chained_field="department",
        chained_model_field="department",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True
    )

    receiving_officer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Cán bộ tiếp nhận",
        related_name="receiver",
        default=get_current_user
    )

    processing_staff = models.ManyToManyField(
        User,
        blank=True,
        verbose_name="Cán bộ xử lý",
        related_name="handler"
    )

    result_deliverer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Cán bộ trả kết quả xử lý",
        related_name="giver",
        default=get_current_user
    )

    result_receiver = models.ForeignKey(
        Staff,
        on_delete=models.PROTECT,
        verbose_name="CB nhận kết quả xử lý",
        related_name="handover",
        blank=True,
        null=True
    )

    delivered_at = models.DateTimeField(
        verbose_name="Ngày trả",
        null=True,
        blank=True
    )

    request_content = models.TextField(
        verbose_name="Nội dung yêu cầu xử lý",
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        verbose_name="Số lượng"
    )

    processing_content = models.TextField(
        verbose_name="Nội dung xử lý",
        null=True,
        blank=True
    )

    has_material_debt = models.BooleanField(
        default=False,
        verbose_name='Nợ vật tư'
    )

    def __str__(self):
        try:
            return f"{self.id} - {self.received_at.strftime('%Y-%m-%d')} - {self.requester.name} - {self.department.name} - {self.request_type.name} - SL: {self.quantity}"
        except Exception as e:
            return f"Yêu cầu #{self.id}"

class EquipmentDeployment(BaseOperation):
    """Quản lý điều động trang bị."""
    class Meta:
        db_table = 'equipment_deployments'
        verbose_name = 'Điều động'
        verbose_name_plural = 'Điều động'

    borrower = models.ForeignKey(
        Staff,
        on_delete=models.PROTECT,
        verbose_name='Người mượn thiết bị',
        related_name='borrow',
        null=True
    )

    borrow_date = models.DateField(
        verbose_name='Ngày mượn',
        default=datetime.now
    )

    lender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Người cho mượn',
        default=get_current_user,
        related_name='lend'
    )

    payer = models.ForeignKey(
        Staff,
        on_delete=models.PROTECT,
        verbose_name='Người trả',
        related_name='pay',
        null=True,
        blank=True
    )

    pay_date = models.DateField(
        verbose_name='Ngày trả',
        null=True,
        blank=True
    )
    hours = models.PositiveIntegerField(verbose_name="Số giờ sử dụng", null=True, blank=True)
    receiver = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Người nhận trả',
        related_name='receive',
        null=True,
        blank=True
    )
    st = models.BooleanField(
        verbose_name='Đã trả trang bị',
        default=False
    )

    def __str__(self):
        try:
            equipment_list = ", ".join([eq.serial for eq in self.equipments.all()])
            return f"{self.borrower.department.name} mượn {equipment_list}"
        except Exception:
            return f"Điều động #{self.id}"
    def save(self, *args, **kwargs):
        if not self.request_type:
            try:
                self.request_type = RequirementType.objects.get(name='Điều động trang bị')  # hoặc name='Sửa chữa trang bị'
            except ObjectDoesNotExist:
                pass  # tránh lỗi nếu chưa có dữ liệu

        super().save(*args, **kwargs)

class EquipmentRepair(BaseOperation):
    """Lịch sử sửa chữa trang bị."""
    class Meta:
        db_table = 'equipment_repairs'
        verbose_name = 'Sửa chữa trang bị'
        verbose_name_plural = 'Sửa chữa'

    department_approver = ChainedForeignKey(
        Staff,
        on_delete=models.PROTECT,
        verbose_name="Chỉ huy phòng ban phê duyệt",
        related_name='repair_approver',
        chained_field="department",
        chained_model_field="department",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True
    )

    requester = ChainedForeignKey(
        Staff,
        on_delete=models.PROTECT,
        verbose_name="Cán bộ yêu cầu xử lý",
        related_name='repair_requester',
        chained_field="department",
        chained_model_field="department",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True
    )

    # receiving_officer = models.ForeignKey(
    #     User,
    #     on_delete=models.PROTECT,
    #     verbose_name="Cán bộ tiếp nhận & xử lý",
    #     related_name="receiver",
    #     default=get_current_user
    # )
    
    error = models.ForeignKey(
        ErrorType, 
        on_delete=models.PROTECT,
        related_name='error',
        null=True,
        blank=True,
        verbose_name='Hiện tượng hỏng hóc'
    )

    repair_staff = models.ManyToManyField(
        User,
        blank=True,
        verbose_name="Cán bộ tiếp nhận & xử lý",
        related_name="repair_staff"
    )
    repair_date = models.DateField(verbose_name="Thời gian sửa chữa")

    repair_content = models.TextField(
        verbose_name="Nội dung xử lý",
        null=True,
        blank=True
    )

    result_deliverer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Cán bộ trả kết quả xử lý",
        related_name="result_deliverer",
        default=get_current_user
    )

    result_receiver = models.ForeignKey(
        Staff,
        on_delete=models.PROTECT,
        verbose_name="CB nhận kết quả xử lý",
        related_name="result_receiver",
        blank=True,
        null=True
    )

    delivered_at = models.DateTimeField(
        verbose_name="Ngày trả",
        null=True,
        blank=True
    )
   
    def save(self, *args, **kwargs):
        """Ghi lại thông số trang bị trước sửa chữa vào trường notes (JSONField)."""
        is_new = self.pk is None

        if not self.notes:
            self.notes = {}

        if not self.request_type:
            try:
                self.request_type = RequirementType.objects.get(name='Sửa chữa trang bị')
            except ObjectDoesNotExist:
                pass

        # Lưu lần đầu để có ID
        super().save(*args, **kwargs)

        # Sau khi có ID rồi mới xử lý M2M
        if is_new and "Thông số trước sửa chữa" not in self.notes and self.equipments.exists():
            first_equipment = self.equipments.first()
            specs = getattr(first_equipment, 'specification', 'Không có thông số')
            self.notes["Thông số trước sửa chữa"] = specs
            super().save(update_fields=["notes"])


    def __str__(self):
        try:
            equipment_list = ", ".join([eq.serial for eq in self.equipments.all()])
            return f"Sửa {equipment_list} - {self.repair_date.strftime('%Y-%m-%d')}"
        except Exception:
            return f"Sửa chữa #{self.id}"

class EquipmentHandover(BaseOperation):
    """Quản lý bàn giao trang bị."""
    class Meta:
        db_table = 'equipment_handovers'
        verbose_name = 'Bàn giao trang bị'
        verbose_name_plural = 'Bàn giao'

    from_staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        verbose_name='Bên giao',
        related_name='handovers_from'
    )

    to_staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        verbose_name='Bên nhận',
        related_name='handovers_to'
    )

    handover_date = models.DateTimeField(
        verbose_name='Thời gian bàn giao'
    )

    def save(self, *args, **kwargs):
        if self.notes is None:
            self.notes = {}
        if "Ghi chú" not in self.notes:
            self.notes["Ghi chú"] = "Tình trạng trang bị mới 100%, đã được Ban D kiểm tra ATTB, cài đặt PM QL USB, bảo đảm đủ điều kiện có thể đưa vào làm việc."
        if not self.request_type:
            try:
                self.request_type = RequirementType.objects.get(name='Bàn giao trang bị')  # hoặc name='Sửa chữa trang bị'
            except ObjectDoesNotExist:
                pass  # tránh lỗi nếu chưa có dữ liệu
        
        super().save(*args, **kwargs)

    def __str__(self):
        try:
            equipment_list = ", ".join([eq.serial for eq in self.equipments.all()])
            return f"Bàn giao {equipment_list} từ {self.from_staff} đến {self.to_staff} ({self.handover_date})"
        except Exception:
            return f"Bàn giao #{self.id}"

class EquipmentLiquidation(BaseOperation):
    """Quản lý thanh lý trang bị."""
    class Meta:
        db_table = 'equipment_liquidations'
        verbose_name = 'Thanh lý trang bị'
        verbose_name_plural = 'Thanh lý'

    liquidation_date = models.DateField(
        verbose_name='Ngày thanh lý'
    )

    approved_by = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Người phê duyệt',
        related_name='approved_liquidations'
    )

    def save(self, *args, **kwargs):
        if self.notes is None:
            self.notes = {}
        if "Lý do thanh lý" not in self.notes:
            self.notes["Lý do thanh lý"] = "Không rõ lý do"
        
        if not self.request_type:
            try:
                self.request_type = RequirementType.objects.get(name='Thanh lý trang bị')  # hoặc name='Sửa chữa trang bị'
            except ObjectDoesNotExist:
                pass  # tránh lỗi nếu chưa có dữ liệu

        super().save(*args, **kwargs)

    def __str__(self):
        try:
            equipment_list = ", ".join([eq.serial for eq in self.equipments.all()])
            return f"Thanh lý {equipment_list} - {self.liquidation_date}"
        except Exception:
            return f"Thanh lý #{self.id}"


class NetworkMaintenanceLog(models.Model):
    """Lịch sử kiểm tra, bảo trì, thay đổi với mạng máy tính."""
    
    class Meta:
        db_table = 'network_maintenance_logs'
        verbose_name = 'Bảo trì mạng'
        verbose_name_plural = 'Kiểm tra, bảo trì mạng'

    id = models.AutoField(primary_key=True, verbose_name='Ms')
    requirement = models.ForeignKey(
        Requirement, on_delete=models.PROTECT, verbose_name='Yêu cầu xử lý', null=True, blank=True
    )
    # network = models.ForeignKey(
    #     ComputerNetwork, on_delete=models.CASCADE, verbose_name='Mạng máy tính', related_name='maintenance_logs'
    # )
    network = models.CharField(max_length=10, choices=settings.COMPUTER_NETWORKS, verbose_name='Mạng máy tính', null=True, blank=True)
    date = models.DateField(verbose_name='Ngày bảo trì')
    description = models.TextField(verbose_name='Nội dung bảo trì')
    performed_by = models.ManyToManyField(
        Staff,
        blank=True,
        verbose_name='Nhân viên bảo trì',
        related_name='maintenance_logs'
    )
    def __str__(self):
        return f"{self.network} - {self.date}"