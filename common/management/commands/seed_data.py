from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from common.models import (
    Department, StaffRole, Staff,
    DocumentTypes,  HandleStatusType,
    ConnectionType, Manufacturer, StaffUser,
    NetworkAddress, RequirementType,
    EquipmentModel, EquipmentType, ErrorType
)
from django.utils.timezone import now
import random


class Command(BaseCommand):
    help = 'Seed initial data into the database'

    def handle(self, *args, **kwargs):
    
        # Department for CTY 1
        c1, _ = Department.objects.get_or_create(id='CT01', name='Công ty Tài chính A')

        d0, _ = Department.objects.get_or_create(id='PB00', name='Phòng Công nghệ Thông tin', parent=c1)
        d1, _ = Department.objects.get_or_create(id='PB01', name='Phòng Kế toán', parent=c1)
        d2, _ = Department.objects.get_or_create(id='PB02', name='Phòng Nhân sự', parent=c1)
        d3, _ = Department.objects.get_or_create(id='PB03', name='Phòng Giao dịch Khách hàng', parent=c1)
        d4, _ = Department.objects.get_or_create(id='PB04', name='Phòng Quản lý Rủi ro', parent=c1)
        d5, _ = Department.objects.get_or_create(id='PB05', name='Phòng Pháp chế', parent=c1)
        d6, _ = Department.objects.get_or_create(id='PB06', name='Phòng Đầu tư', parent=c1)

        # Department for CTY 2
        c2, _ = Department.objects.get_or_create(id='CT02', name='Công ty Tài chính B')

        e0, _ = Department.objects.get_or_create(id='PB10', name='Phòng Công nghệ Thông tin', parent=c2)
        e1, _ = Department.objects.get_or_create(id='PB11', name='Phòng Kế toán', parent=c2)
        e2, _ = Department.objects.get_or_create(id='PB12', name='Phòng Nhân sự', parent=c2)
        e3, _ = Department.objects.get_or_create(id='PB13', name='Phòng Giao dịch Khách hàng', parent=c2)
        e4, _ = Department.objects.get_or_create(id='PB14', name='Phòng Quản lý Rủi ro', parent=c2)
        e5, _ = Department.objects.get_or_create(id='PB15', name='Phòng Pháp chế', parent=c2)
        e6, _ = Department.objects.get_or_create(id='PB16', name='Phòng Hành chính', parent=c2)


        # StaffRole
        roles = ['Trưởng phòng', 'Phó phòng', 'Nhân viên', 'Trợ lý']
        for idx, name in enumerate(roles):
            StaffRole.objects.get_or_create(id=f'CV0{idx+1}', name=name)

        # Staff
        for i in range(1, 30):
            Staff.objects.get_or_create(
                name=f'Cán bộ {i}',
                staffrole=StaffRole.objects.get(id='CV03'),
                department=random.choice([d0, d1, d2, d3, d4, d5, d6, e0, e1, e2, e3, e4, e5, e6]),
                phonenumber=f'09000000{i}',
                status=False
            )
        
        for i in range(1, 30):
            Staff.objects.get_or_create(
                name=f'Cán bộ {i}',
                staffrole=StaffRole.objects.get(id='CV03'),
                department=random.choice([d0, d1, d2, d3, d4, d5, d6, e0, e1, e2, e3, e4, e5, e6]),
                phonenumber=f'09000000{i}',
                status=False
            )


        for i in range(1, 30):
            Staff.objects.get_or_create(
                name=f'Cán bộ {i}',
                staffrole=StaffRole.objects.get(id='CV04'),
                department=random.choice([d0, d1, d2, d3, d4, d5, d6, e0, e1, e2, e3, e4, e5, e6]),
                phonenumber=f'09000000{i}',
                status=False
            )
        
        for i in range(1, 30):
            Staff.objects.get_or_create(
                name=f'Cán bộ {i}',
                staffrole=StaffRole.objects.get(id='CV04'),
                department=random.choice([d0, d1, d2, d3, d4, d5, d6, e0, e1, e2, e3, e4, e5, e6]),
                phonenumber=f'09000000{i}',
                status=False
            )
        for i in range(1, 2):
            Staff.objects.get_or_create(
                name=f'Cán bộ {i}',
                staffrole=StaffRole.objects.get(id='CV01'),
                department=random.choice([d0, d1, d2, d3, d4, d5, d6, e0, e1, e2, e3, e4, e5, e6]),
                phonenumber=f'09000000{i}',
                status=False
            )
        
        for i in range(1, 6):
            Staff.objects.get_or_create(
                name=f'Cán bộ {i}',
                staffrole=StaffRole.objects.get(id='CV02'),
                department=random.choice([d0, d1, d2, d3, d4, d5, d6, e0, e1, e2, e3, e4, e5, e6]),
                phonenumber=f'09000000{i}',
                status=False
            )

        # DocumentTypes
        document_type_names = [
            'Báo cáo tài chính',
            'Công văn nội bộ',
            'Thông báo nhân sự',
            'Biên bản họp',
            'Tờ trình',
            'Hợp đồng',
            'Kế hoạch công tác',
            'Đề xuất mua sắm',
        ]

        for i, name in enumerate(document_type_names):
            DocumentTypes.objects.get_or_create(id=f'DT{i+1:02}', name=name)


        # # UsagePurpose
        # for i, name in enumerate(['Công tác', 'Dự phòng', 'Khác']):
        #     UsagePurpose.objects.get_or_create(id=f'UP{i+1}', name=name)
        base_names = [
            'Hỏng nguồn', 'Lỗi màn hình', 'Không kết nối mạng', 'Lỗi phần mềm',
            'Bàn phím hỏng', 'Ổ cứng lỗi', 'Máy không khởi động', 'Lỗi driver',
            'Máy treo', 'Lỗi hệ điều hành', 'Hỏng chuột', 'Máy nóng quá mức'
        ]
        for i in range(len(base_names)):
            name = base_names[i]
            error_id = f"ERR{i+1:03d}"

            if not ErrorType.objects.filter(name=name).exists():
                ErrorType.objects.create(
                    id=error_id,
                    name=name
                )
        # self.stdout.write(self.style.SUCCESS(f"✅ Đã tạo {len(base_names)} loại hỏng hóc."))
        # HandleStatusType
        for i, name in enumerate(['Đã tiếp nhận', 'Đang xử lý', 'Hoàn thành', 'Tạm dừng']):
            HandleStatusType.objects.get_or_create(id=f'HST{i+1}', name=name)
        
        # ConnectionType
        for i, name in enumerate(['USB', 'HDMI', 'Ethernet']):
            ConnectionType.objects.get_or_create(id=f'CT{i+1}', name=name)

        # Manufacturer
        for i, name in enumerate(['Dell', 'HP', 'Asus']):
            Manufacturer.objects.get_or_create(id=f'MF{i+1}', name=name)

        # NetworkAddress
        for i in range(10,100):
            NetworkAddress.objects.get_or_create(
                mac_address=f'00:1A:C2:7B:00:{i}',
                ip_address=f'192.168.1.{100+i}'
            )
            NetworkAddress.objects.get_or_create(
                mac_address=f'00:1A:C2:7B:55:{i}',
                ip_address=f'192.168.50.{100+i}'
            )
            NetworkAddress.objects.get_or_create(
                mac_address=f'00:1B:C5:7B:66:{i}',
                ip_address=f'192.168.100.{100+i}'
            )
           
        # ComputerNetwork
        # for i, name in enumerate(['Mạng nội bộ', 'Mạng khách']):
        #     ComputerNetwork.objects.get_or_create(name=name)

        # RequirementType (tree structure)
        rt_root, _ = RequirementType.objects.get_or_create(name='Sửa chữa', unit='lần')
        RequirementType.objects.get_or_create(name='Sửa phần mềm', unit='lần', parent=rt_root)
        RequirementType.objects.get_or_create(name='Sửa phần cứng', unit='lần', parent=rt_root)

        rt_root1, _ = RequirementType.objects.get_or_create(name='Bàn giao', unit='lần')
        rt_root2, _ = RequirementType.objects.get_or_create(name='Thanh lý', unit='lần')
        rt_root3, _ = RequirementType.objects.get_or_create(name='Điều động', unit='lần')

        # EquipmentType
        et_root, _ = EquipmentType.objects.get_or_create(id='DTTH', name='Trang bị điện tử tin học')
        EquipmentType.objects.get_or_create(id='MT', name='Máy tính', parent=et_root)
        EquipmentType.objects.get_or_create(id='DT', name='Điện thoại', parent=et_root)
        EquipmentType.objects.get_or_create(id='MI', name='Máy in', parent=et_root)

        et_root2, _ = EquipmentType.objects.get_or_create(id='KTAH', name='Trang bị âm hình')
        EquipmentType.objects.get_or_create(id='MGA', name='Máy ghi âm', parent=et_root2)
        EquipmentType.objects.get_or_create(id='MGH', name='Máy ghi hình ', parent=et_root2)

        EquipmentType.objects.get_or_create(id='Laptop', name='Laptop', parent_id='MT')
        EquipmentType.objects.get_or_create(id='Desktop', name='Desktop', parent_id='MT')
        # EquipmentModel
        conn_types = list(ConnectionType.objects.all())
        equip_types = list(EquipmentType.objects.all())

        for i in range(200):
            EquipmentModel.objects.get_or_create(
                name=f'Trang bị {i+1}',
                battery=(i % 2 == 0),
                needdriver=False,
                cable=random.choice(conn_types) if conn_types else None,
                features='Chống nước, chống sốc',
                specifications={"CPU": "i5", "RAM": "8GB"},
                type=random.choice(equip_types) if equip_types else None
            )


        # StaffUser
        
        staff_list = list(Staff.objects.all())

        # Danh sách người dùng mẫu
        users_data = [
            {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin'},
            {'username': 'staff1', 'email': 'staff1@example.com', 'password': 'staffpass1'},
            {'username': 'staff2', 'email': 'staff2@example.com', 'password': 'staffpass2'},
            {'username': 'staff3', 'email': 'staff3@example.com', 'password': 'staffpass3'},
            {'username': 'staff4', 'email': 'staff4@example.com', 'password': 'staffpass4'},
            {'username': 'staff5', 'email': 'staff4@example.com', 'password': 'staffpass5'},
            {'username': 'staff6', 'email': 'staff5@example.com', 'password': 'staffpass6'},
        ]

        for udata in users_data:
            user, _ = User.objects.get_or_create(username=udata['username'], defaults={'email': udata['email']})
            user.set_password(udata['password'])
            user.save()

            # Chọn Staff ngẫu nhiên
            random_staff = random.choice(staff_list)
            StaffUser.objects.get_or_create(user=user, staff=random_staff)

        self.stdout.write(self.style.SUCCESS('Successfully seeded common data!'))
