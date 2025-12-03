import random
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from operations.models import (
    Department,
    Equipment,
    EquipmentDeployment,
    EquipmentHandover,
    EquipmentLiquidation,
    EquipmentRepair,
    ErrorType,
    HandleStatusType,
    NetworkMaintenanceLog,
    Requirement,
    RequirementType,
    Staff,
    User,
)

fake = Faker("vi_VN")


class Command(BaseCommand):
    help = "Tạo dữ liệu mẫu cho xử lý kỹ thuật với ngữ cảnh thực tế."

    def _staff_in_dept(self, staff_list, dept):
        candidates = [s for s in staff_list if s.department_id == dept.id]
        return random.choice(candidates) if candidates else None

    def handle(self, *args, **kwargs):
        departments = list(Department.objects.all())
        staff_list = list(Staff.objects.select_related("department").all())
        users = list(User.objects.all())
        request_types = {rt.name: rt for rt in RequirementType.objects.all()}
        status_list = list(HandleStatusType.objects.all())
        equipment_list = list(Equipment.objects.all())
        error_types = list(ErrorType.objects.all())

        if not all([departments, staff_list, users, request_types, status_list, equipment_list]):
            self.stdout.write(self.style.ERROR("Thiếu dữ liệu. Hãy chạy seed_data và seed_equipment trước."))
            return

        valid_departments = [d for d in departments if any(s.department_id == d.id for s in staff_list)]
        requirements_created = []

        request_type_choices = [
            request_types.get("Điều động trang bị"),
            request_types.get("Sửa chữa trang bị"),
            request_types.get("Bàn giao trang bị"),
            request_types.get("Thanh lý trang bị"),
            request_types.get("Bảo trì định kỳ"),
            request_types.get("Khắc phục sự cố mạng"),
            request_types.get("Cấu hình thiết bị mạng"),
            request_types.get("Cài đặt phần mềm"),
        ]
        request_type_choices = [rt for rt in request_type_choices if rt]

        for _ in range(60):
            dept = random.choice(valid_departments)
            requester = self._staff_in_dept(staff_list, dept)
            approver = self._staff_in_dept(staff_list, dept)
            if not requester or not approver:
                continue

            equipments = random.sample(equipment_list, k=min(len(equipment_list), random.randint(1, 3)))
            req = Requirement.objects.create(
                department=dept,
                request_type=random.choice(request_type_choices),
                received_at=fake.date_time_between(start_date="-5m", end_date="now"),
                status=random.choice(status_list),
                department_approver=approver,
                requester=requester,
                receiving_officer=random.choice(users),
                result_deliverer=random.choice(users),
                result_receiver=requester,
                delivered_at=timezone.now() - timedelta(days=random.randint(1, 10)),
                request_content=fake.sentence(nb_words=12),
                quantity=random.randint(1, 5),
                processing_content=fake.paragraph(nb_sentences=2),
                has_material_debt=random.choice([True, False, False]),
            )
            req.equipments.set(equipments)
            req.processing_staff.set(random.sample(users, k=min(len(users), 2)))
            requirements_created.append(req)

        # Điều động trang bị
        for _ in range(25):
            dept = random.choice(valid_departments)
            borrower = self._staff_in_dept(staff_list, dept)
            approver = self._staff_in_dept(staff_list, dept)
            if not borrower or not approver:
                continue

            deployment = EquipmentDeployment.objects.create(
                department=dept,
                request_type=request_types.get("Điều động trang bị"),
                received_at=fake.date_time_between(start_date="-90d", end_date="now"),
                status=random.choice(status_list),
                borrower=borrower,
                borrow_date=fake.date_between(start_date="-60d", end_date="-7d"),
                lender=random.choice(users),
                payer=approver,
                pay_date=fake.date_between(start_date="-6d", end_date="today"),
                hours=random.randint(4, 120),
                receiver=random.choice(users),
                st=random.choice([True, False]),
                notes="Mượn phục vụ đào tạo nội bộ/ hỗ trợ khách hàng.",
            )
            deployment.equipments.set(random.sample(equipment_list, k=min(len(equipment_list), random.randint(1, 2))))

        # Sửa chữa trang bị
        for _ in range(25):
            dept = random.choice(valid_departments)
            requester = self._staff_in_dept(staff_list, dept)
            approver = self._staff_in_dept(staff_list, dept)
            if not requester or not approver:
                continue

            repair = EquipmentRepair.objects.create(
                department=dept,
                request_type=request_types.get("Sửa chữa trang bị"),
                received_at=fake.date_time_between(start_date="-120d", end_date="now"),
                status=random.choice(status_list),
                requester=requester,
                department_approver=approver,
                repair_date=fake.date_between(start_date="-90d", end_date="today"),
                repair_content=random.choice(
                    [
                        "Thay ổ cứng SSD, cài đặt lại hệ điều hành và ứng dụng nghiệp vụ.",
                        "Vệ sinh, tra keo tản nhiệt và cập nhật BIOS.",
                        "Kiểm tra dây mạng, cấu hình lại VLAN và gán IP tĩnh.",
                    ]
                ),
                result_deliverer=random.choice(users),
                result_receiver=approver,
                error=random.choice(error_types) if error_types else None,
                notes={"Khuyến nghị": "Theo dõi log 7 ngày, nếu lặp lại sẽ đổi thiết bị khác."},
            )
            repair.equipments.set(random.sample(equipment_list, k=min(len(equipment_list), random.randint(1, 3))))
            repair.repair_staff.set(random.sample(users, k=min(len(users), 2)))

        # Bàn giao trang bị
        for _ in range(20):
            dept = random.choice(valid_departments)
            giver = self._staff_in_dept(staff_list, dept)
            receiver_staff = self._staff_in_dept(staff_list, dept)
            if not giver or not receiver_staff:
                continue
            handover = EquipmentHandover.objects.create(
                department=dept,
                request_type=request_types.get("Bàn giao trang bị"),
                received_at=fake.date_time_between(start_date="-45d", end_date="now"),
                status=random.choice(status_list),
                from_staff=giver,
                to_staff=receiver_staff,
                handover_date=fake.date_time_between(start_date="-30d", end_date="now"),
                notes={"Ghi chú": "Giao kèm túi chống sốc, sạc dự phòng và checklist cấu hình."},
            )
            handover.equipments.set(random.sample(equipment_list, k=min(len(equipment_list), random.randint(1, 2))))
            handover.save()

        # Thanh lý trang bị
        for _ in range(8):
            dept = random.choice(valid_departments)
            approver = self._staff_in_dept(staff_list, dept)
            if not approver:
                continue
            liquidation = EquipmentLiquidation.objects.create(
                department=dept,
                request_type=request_types.get("Thanh lý trang bị"),
                received_at=fake.date_time_between(start_date="-200d", end_date="now"),
                status=random.choice(status_list),
                liquidation_date=fake.date_between(start_date="-180d", end_date="-20d"),
                approved_by=approver,
                notes={"Lý do thanh lý": random.choice(["Hết khấu hao", "Không đáp ứng yêu cầu nghiệp vụ", "Hỏng không sửa được"])},
            )
            liquidation.equipments.set(random.sample(equipment_list, k=min(len(equipment_list), random.randint(1, 2))))
            liquidation.save()

        # Bảo trì mạng
        network_requirements = [
            req for req in requirements_created if req.request_type and req.request_type.name in ["Bảo trì định kỳ", "Khắc phục sự cố mạng", "Cấu hình thiết bị mạng"]
        ]
        for _ in range(20):
            dept = random.choice(valid_departments)
            staff_perform = [s for s in staff_list if s.department_id == dept.id]
            log = NetworkMaintenanceLog.objects.create(
                requirement=random.choice(network_requirements) if network_requirements else None,
                network=random.choice([choice[0] for choice in settings.COMPUTER_NETWORKS]),
                date=fake.date_between(start_date="-90d", end_date="today"),
                description=random.choice(
                    [
                        "Kiểm tra thiết bị mạng core, cập nhật firmware và backup cấu hình.",
                        "Đi dây lại cáp uplink, thay module SFP lỗi.",
                        "Tối ưu cấu hình Wi-Fi, tách SSID khách và nội bộ.",
                        "Kiểm tra log firewall, bổ sung rule chặn IP bất thường.",
                    ]
                ),
            )
            if staff_perform:
                log.performed_by.set(random.sample(staff_perform, k=min(len(staff_perform), 2)))

        self.stdout.write(self.style.SUCCESS("Đã tạo dữ liệu mẫu cho các nghiệp vụ xử lý kỹ thuật."))
