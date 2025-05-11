from django.core.management.base import BaseCommand
from equipments.models import *
from common.models import *
from django.utils import timezone
import random
from faker import Faker
import string
from django.conf import settings
from datetime import timedelta

fake = Faker()
# Tạo ngày hết hạn ngẫu nhiên từ năm 2025 đến 2030
def random_expiry_date(start_year=2025, end_year=2030):
    start_date = timezone.now().replace(year=start_year).date()
    end_date = timezone.now().replace(year=end_year).date()
    delta_days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, delta_days))

class Command(BaseCommand):
    help = "Seed sample data for Equipment, ConsumableEquipment, NetworkDevice"

    def handle(self, *args, **options):
        models = list(EquipmentModel.objects.all())
        departments = list(Department.objects.all())
        manufacturers = list(Manufacturer.objects.all())
        networks = settings.COMPUTER_NETWORKS
        addresses = list(NetworkAddress.objects.all())

        if not all([models, departments, manufacturers, addresses]):
            self.stdout.write(self.style.ERROR("Thiếu dữ liệu liên quan! Hãy seed đầy đủ trước."))
            return

        # Seed Equipment
        equipment_list = []
        for i in range(1000):
            serial = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            equip = Equipment.objects.create(
                serial=serial,
                ms=f"MS{i+1:03}",
                model=random.choice(models),
                year=random.randint(2000, 2024),
                source=random.choice(['NS', 'DA', 'KH']),
                specification="CPU: Intel i5, RAM: 8GB",
                storage_location=fake.address(),
                department=random.choice(departments),
                manufacturer=random.choice(manufacturers),
                country=random.choice(['VN', 'US', 'JP', 'CN', 'FR']),
                group=random.choice(['1', '2']),
                expiry_date=random_expiry_date(),
                waranty_info="Bảo hành 3 năm",
                short_description="Trang bị dùng cho văn phòng",
                available=True,
            )
            equipment_list.append(equip)

        # self.stdout.write(self.style.SUCCESS(f"Đã tạo {len(equipment_list)} Equipment"))
        # Phân loại thiết bị theo group
        # Phân loại thiết bị theo group
        group1_equipment = [e for e in equipment_list if e.group == '1']
        group2_equipment = [e for e in equipment_list if e.group == '2']

        # Gán thiết bị nhóm 2 làm con của thiết bị nhóm 1
        for child in group2_equipment:
            if group1_equipment:
                parent = random.choice(group1_equipment)
                child.parent = parent  # Gán thiết bị nhóm 2 làm con của thiết bị nhóm 1
                child.save()

                # Sau khi gán thiết bị con, có thể xóa thiết bị cha khỏi danh sách nhóm 1
                # để tránh thiết bị cha bị gán làm con của thiết bị nhóm 2 khác nữa.
                group1_equipment.remove(parent)


        # Seed ConsumableEquipment
        for equip in equipment_list[:50]:  # chỉ seed 5 cái
            ConsumableEquipment.objects.create(
                equipment=equip,
                quantity=random.randint(10, 100)
            )
        # self.stdout.write(self.style.SUCCESS("Đã tạo 5 ConsumableEquipment"))

        # Seed NetworkDevice
        for equip in equipment_list[50:120]:
            net_dev = NetworkDevice.objects.create(
                equipment=equip,
                network=random.choice(networks)
            )
            net_dev.address.set(random.sample(addresses, k=1))
        # self.stdout.write(self.style.SUCCESS("Đã tạo 5 NetworkDevice"))

        self.stdout.write(self.style.SUCCESS("✅ Hoàn tất tạo dữ liệu mẫu Equipments"))
