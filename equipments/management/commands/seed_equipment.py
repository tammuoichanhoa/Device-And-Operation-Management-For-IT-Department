from datetime import timedelta
import random

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from common.models import Department, EquipmentModel, Manufacturer, NetworkAddress
from equipments.models import ConsumableEquipment, Equipment, NetworkDevice

fake = Faker("vi_VN")


class Command(BaseCommand):
    help = "Seed dữ liệu trang bị, vật tư tiêu hao và thiết bị mạng với thông tin thực tế."

    def _spec_text(self, model):
        specs = model.specifications or {}
        return "; ".join(f"{k}: {v}" for k, v in specs.items()) if specs else "Đang cập nhật"

    def handle(self, *args, **options):
        models = list(EquipmentModel.objects.select_related("type").all())
        departments = list(Department.objects.all())
        manufacturers = list(Manufacturer.objects.all())
        addresses = list(NetworkAddress.objects.all())

        if not all([models, departments, manufacturers]):
            self.stdout.write(self.style.ERROR("Thiếu dữ liệu liên quan! Hãy chạy seed_data trước."))
            return

        sources = [c[0] for c in settings.SOURCES]
        countries = [c[0] for c in settings.COUNTRIES]
        purposes = [c[0] for c in settings.USAGE_PURPOSES]
        locations = [
            "Phòng máy chủ - Tầng 6, trụ sở HCM",
            "Tủ mạng chi nhánh Hà Nội",
            "Phòng họp lớn - Tầng 4",
            "Bàn giao dịch khách hàng - Quầy 05",
            "Khu vực vận hành trung tâm dữ liệu",
            "Kho dự phòng thiết bị, Tầng hầm B2",
        ]

        existing_count = Equipment.objects.count()
        equipment_list = []
        for idx in range(120):
            model = random.choice(models)
            serial = f"{model.name.split()[0][:3].upper()}-{timezone.now().year % 100}-{existing_count + idx:04}"
            equip, _ = Equipment.objects.get_or_create(
                serial=serial,
                defaults={
                    "ms": f"TB-{existing_count + idx + 1:04}",
                    "model": model,
                    "year": random.randint(2018, 2024),
                    "source": random.choice(sources),
                    "specification": self._spec_text(model),
                    "storage_location": random.choice(locations),
                    "department": random.choice(departments),
                    "manufacturer": random.choice(manufacturers),
                    "country": random.choice(countries),
                    "purpose": random.choice(purposes),
                    "group": "1" if model.type and model.type.id not in ["PRN"] else random.choice(["1", "2"]),
                    "available": random.choice([True, True, True, False]),
                    "expiry_date": timezone.now().date() + timedelta(days=random.randint(365, 3 * 365)),
                    "waranty_info": "Bảo hành 36 tháng, hỗ trợ on-site nội thành",
                    "short_description": f"{model.name} phục vụ {random.choice(['văn phòng', 'điểm giao dịch', 'phòng họp'])}",
                },
            )
            equipment_list.append(equip)

        parents = [e for e in equipment_list if e.group == "1"]
        children = [e for e in equipment_list if e.group == "2"]
        for child in children:
            if parents:
                parent = random.choice(parents)
                child.parent = parent
                child.save(update_fields=["parent"])

        printer_equipment = [e for e in equipment_list if e.model and e.model.type and e.model.type.id == "PRN"]
        for equip in printer_equipment[:15]:
            ConsumableEquipment.objects.update_or_create(
                equipment=equip,
                defaults={"quantity": random.randint(5, 40)},
            )

        network_types = {"ROUTER", "SWITCH", "AP", "FW"}
        network_equipments = [e for e in equipment_list if e.model and e.model.type and e.model.type.id in network_types]
        networks = [choice[0] for choice in settings.COMPUTER_NETWORKS]
        for equip in network_equipments:
            net_dev, _ = NetworkDevice.objects.get_or_create(
                equipment=equip,
                defaults={"network": random.choice(networks)},
            )
            if addresses:
                net_dev.address.set(random.sample(addresses, k=1))

        self.stdout.write(self.style.SUCCESS("Hoàn tất tạo dữ liệu mẫu cho trang bị, vật tư và thiết bị mạng."))
