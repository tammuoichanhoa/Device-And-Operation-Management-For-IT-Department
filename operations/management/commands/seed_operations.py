from django.core.management.base import BaseCommand
from django.utils import timezone
from random import choice, randint, sample
from faker import Faker
from operations.models import (
    Requirement, EquipmentDeployment, EquipmentRepair, EquipmentHandover, EquipmentLiquidation,
    Department, Equipment, Staff, User, RequirementType, HandleStatusType, ErrorType
)

fake = Faker()

class Command(BaseCommand):
    help = "Tạo dữ liệu mẫu cho xử lý kỹ thuật"

    def handle(self, *args, **kwargs):
        departments = list(Department.objects.all())
        staff_list = list(Staff.objects.all())
        users = list(User.objects.all())
        request_types = list(RequirementType.objects.all())
        status_list = list(HandleStatusType.objects.all())
        equipment_list = list(Equipment.objects.all())
        error_types = list(ErrorType.objects.all())

        def random_staff(dept):
            return choice([s for s in staff_list if s.department == dept])

        for _ in range(300):
            
            valid_departments = [d for d in departments if any(s.department == d for s in staff_list)]
            dept = choice(valid_departments)
            requester = random_staff(dept)
            approver = random_staff(dept)

            equipments = sample(equipment_list, randint(1, 3))

            # Requirement
            req = Requirement.objects.create(
                department=dept,
                request_type=choice(request_types),
                received_at=fake.date_time_between(start_date='-1y', end_date='now'),
                status=choice(status_list),
                department_approver=approver,
                requester=requester,
                receiving_officer=choice(users),
                result_deliverer=choice(users),
                result_receiver=requester,
                delivered_at=timezone.now(),
                request_content=fake.text(100),
                quantity=randint(1, 5),
                processing_content=fake.text(100),
                has_material_debt=choice([True, False]),
            )
            req.equipments.set(equipments)

            # Equipment Deployment
            deployment = EquipmentDeployment.objects.create(
                department=dept,
                request_type=choice(request_types),
                received_at=fake.date_time_this_year(),
                status=choice(status_list),
                borrower=requester,
                borrow_date=fake.date_between(start_date='-60d', end_date='-10d'),
                lender=choice(users),
                payer=approver,
                pay_date=fake.date_between(start_date='-9d', end_date='now'),
                hours=randint(1, 100),
                receiver=choice(users),
                st=choice([True, False]),
            )
            deployment.equipments.set(sample(equipment_list, randint(1, 2)))

            # Equipment Repair
            repair = EquipmentRepair.objects.create(
                department=dept,
                request_type=choice(request_types),
                received_at=fake.date_time_this_year(),
                status=choice(status_list),
                requester=requester,
                department_approver=approver,
                repair_date=fake.date_between(start_date='-90d', end_date='now'),
                repair_content=fake.text(80),
                result_deliverer=choice(users),
                result_receiver=approver,
                error=choice(error_types) if error_types else None,
            )

            # Gán ManyToMany sau khi đã có ID
            repair.equipments.set(sample(equipment_list, randint(1, 3)))
            repair.repair_staff.set(sample(users, randint(1, 2)))

            # Equipment Handover
            from_staff = requester
            to_staff = approver
            handover = EquipmentHandover.objects.create(
                department=dept,
                request_type=choice(request_types),
                received_at=fake.date_time_this_year(),
                status=choice(status_list),
                from_staff=from_staff,
                to_staff=to_staff,
                handover_date=fake.date_time_between(start_date='-30d', end_date='now'),
            )
            handover.equipments.set(sample(equipment_list, randint(1, 3)))
            handover.save()

            # Equipment Liquidation
            liquidation = EquipmentLiquidation.objects.create(
                department=dept,
                request_type=choice(request_types),
                received_at=fake.date_time_this_year(),
                status=choice(status_list),
                liquidation_date=fake.date_between(start_date='-180d', end_date='-30d'),
                approved_by=approver
            )
            liquidation.equipments.set(sample(equipment_list, randint(1, 3)))
            liquidation.save()

        self.stdout.write(self.style.SUCCESS("✅ Đã tạo các yêu cầu xử lý kỹ thuật mẫu."))
