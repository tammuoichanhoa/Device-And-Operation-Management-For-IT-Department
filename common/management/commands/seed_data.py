from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker
import random

from common.models import (
    ConnectionType,
    Department,
    DocumentTypes,
    EquipmentModel,
    EquipmentType,
    ErrorType,
    HandleStatusType,
    Manufacturer,
    NetworkAddress,
    RequirementType,
    Staff,
    StaffRole,
    StaffUser,
)

fake = Faker("vi_VN")


class Command(BaseCommand):
    help = "Khởi tạo dữ liệu dùng chung bằng tiếng Việt với thông tin sát thực tế."

    def _unique_phone(self, used):
        phone = None
        while not phone or phone in used:
            phone = f"09{random.randint(1000000, 9999999)}"
        used.add(phone)
        return phone

    def _create_departments(self):
        structure = [
            {
                "id": "TS-HCM",
                "name": "Trụ sở TP. Hồ Chí Minh",
                "children": [
                    {
                        "id": "CNTT-HCM",
                        "name": "Khối Công nghệ thông tin",
                        "children": [
                            {"id": "HTKT-HCM", "name": "Phòng Hạ tầng kỹ thuật"},
                            {"id": "UDPM-HCM", "name": "Phòng Ứng dụng phần mềm"},
                            {"id": "ATTT-HCM", "name": "Phòng An toàn thông tin"},
                        ],
                    },
                    {
                        "id": "KD-HCM",
                        "name": "Khối Kinh doanh",
                        "children": [
                            {"id": "QLKH-HCM", "name": "Phòng Quản lý khách hàng"},
                            {"id": "DVKH-HCM", "name": "Phòng Dịch vụ khách hàng"},
                        ],
                    },
                    {"id": "HCNS-HCM", "name": "Phòng Hành chính - Nhân sự"},
                ],
            },
            {
                "id": "CN-HN",
                "name": "Chi nhánh Hà Nội",
                "children": [
                    {"id": "CNTT-HN", "name": "Tổ CNTT"},
                    {"id": "KD-HN", "name": "Tổ Kinh doanh"},
                    {"id": "HC-HN", "name": "Tổ Hành chính"},
                ],
            },
            {
                "id": "CN-DN",
                "name": "Chi nhánh Đà Nẵng",
                "children": [
                    {"id": "CNTT-DN", "name": "Tổ CNTT"},
                    {"id": "KD-DN", "name": "Tổ Kinh doanh"},
                ],
            },
        ]

        created = []

        def build(nodes, parent=None):
            for node in nodes:
                dept, _ = Department.objects.get_or_create(
                    id=node["id"], defaults={"name": node["name"], "parent": parent}
                )
                updated = False
                if dept.name != node["name"]:
                    dept.name = node["name"]
                    updated = True
                if dept.parent_id != (parent.id if parent else None):
                    dept.parent = parent
                    updated = True
                if updated:
                    dept.save(update_fields=["name", "parent"])
                created.append(dept)
                build(node.get("children", []), dept)

        build(structure)
        return created

    def _seed_roles(self):
        roles_data = [
            ("CV01", "Giám đốc CNTT"),
            ("CV02", "Trưởng phòng/ban"),
            ("CV03", "Chuyên viên hệ thống"),
            ("CV04", "Kỹ thuật viên hiện trường"),
            ("CV05", "Nhân viên vận hành"),
        ]
        return {
            code: StaffRole.objects.update_or_create(id=code, defaults={"name": name})[0]
            for code, name in roles_data
        }

    def _seed_staff(self, departments, roles):
        leaves = [d for d in departments if not Department.objects.filter(parent=d).exists()]
        used_phone = set()
        staff_members = []

        for dept in leaves:
            head, _ = Staff.objects.get_or_create(
                name=fake.name(),
                staffrole=roles["CV02"],
                department=dept,
                defaults={"phonenumber": self._unique_phone(used_phone), "status": False},
            )
            staff_members.append(head)

            for _ in range(random.randint(3, 6)):
                role = random.choice([roles["CV03"], roles["CV04"], roles["CV05"]])
                staff, _ = Staff.objects.get_or_create(
                    name=fake.name(),
                    staffrole=role,
                    department=dept,
                    defaults={"phonenumber": self._unique_phone(used_phone), "status": False},
                )
                staff_members.append(staff)

        return staff_members

    def _seed_document_types(self):
        doc_types = [
            ("DT01", "Quyết định điều động thiết bị"),
            ("DT02", "Biên bản bàn giao"),
            ("DT03", "Thông báo bảo trì hệ thống"),
            ("DT04", "Báo cáo sự cố"),
            ("DT05", "Đề nghị mua sắm/ nâng cấp"),
            ("DT06", "Công văn phối hợp với chi nhánh"),
            ("DT07", "Biên bản nghiệm thu"),
        ]
        for code, name in doc_types:
            DocumentTypes.objects.update_or_create(id=code, defaults={"name": name})

    def _seed_error_types(self):
        errors = [
            ("ERR001", "Mất kết nối VPN"),
            ("ERR002", "Switch quá nhiệt/treo cổng"),
            ("ERR003", "Ổ cứng báo bad sector"),
            ("ERR004", "Màn hình nhấp nháy"),
            ("ERR005", "Không nhận USB/Driver"),
            ("ERR006", "Máy in kẹt giấy liên tục"),
            ("ERR007", "Máy tính không boot được"),
            ("ERR008", "Ứng dụng nội bộ không đăng nhập"),
            ("ERR009", "Wi-Fi chập chờn tại khu làm việc"),
            ("ERR010", "Firewall cảnh báo lưu lượng bất thường"),
        ]
        for code, name in errors:
            ErrorType.objects.update_or_create(id=code, defaults={"name": name})

    def _seed_handle_statuses(self):
        statuses = [
            ("TN", "Đã tiếp nhận"),
            ("XL", "Đang xử lý"),
            ("HT", "Hoàn thành"),
            ("TD", "Tạm dừng"),
        ]
        return [
            HandleStatusType.objects.update_or_create(id=code, defaults={"name": name})[0]
            for code, name in statuses
        ]

    def _seed_connection_types(self):
        connections = [
            ("USBA", "USB-A 3.0"),
            ("USBC", "USB-C"),
            ("HDMI", "HDMI 2.0"),
            ("RJ45", "RJ45 Cat6"),
            ("TB4", "Thunderbolt 4"),
            ("SFP", "SFP+"),
        ]
        return {
            code: ConnectionType.objects.update_or_create(id=code, defaults={"name": name})[0]
            for code, name in connections
        }

    def _seed_manufacturers(self):
        makers = [
            ("DELL", "Dell"),
            ("HP", "HP"),
            ("LNV", "Lenovo"),
            ("ASUS", "Asus"),
            ("CSCO", "Cisco"),
            ("UBNT", "Ubiquiti"),
        ]
        return [
            Manufacturer.objects.update_or_create(id=code, defaults={"name": name})[0]
            for code, name in makers
        ]

    def _seed_network_addresses(self):
        addresses = []
        subnets = [("00:1A:11", "10.0.1."), ("00:1A:22", "10.0.2."), ("00:1B:33", "10.1.10.")]
        for subnet_idx, (mac_prefix, ip_prefix) in enumerate(subnets):
            for host in range(10, 25):
                mac = f"{mac_prefix}:{subnet_idx:02X}:{host:02X}"
                ip = f"{ip_prefix}{host}"
                addr, _ = NetworkAddress.objects.get_or_create(mac_address=mac, defaults={"ip_address": ip})
                addresses.append(addr)
        return addresses

    def _seed_requirement_types(self):
        root, _ = RequirementType.objects.get_or_create(name="Xử lý trang bị", unit="đầu việc")
        rt_move, _ = RequirementType.objects.get_or_create(name="Điều động trang bị", unit="phiếu", parent=root)
        rt_repair, _ = RequirementType.objects.get_or_create(name="Sửa chữa trang bị", unit="phiếu", parent=root)
        rt_handover, _ = RequirementType.objects.get_or_create(name="Bàn giao trang bị", unit="phiếu", parent=root)
        rt_liquid, _ = RequirementType.objects.get_or_create(name="Thanh lý trang bị", unit="phiếu", parent=root)

        network_root, _ = RequirementType.objects.get_or_create(name="Vận hành mạng", unit="đầu việc")
        RequirementType.objects.get_or_create(name="Bảo trì định kỳ", unit="lần", parent=network_root)
        RequirementType.objects.get_or_create(name="Khắc phục sự cố mạng", unit="phiếu", parent=network_root)
        RequirementType.objects.get_or_create(name="Cấu hình thiết bị mạng", unit="phiếu", parent=network_root)

        software_root, _ = RequirementType.objects.get_or_create(name="Hỗ trợ phần mềm", unit="phiếu")
        RequirementType.objects.get_or_create(name="Cài đặt phần mềm", unit="lần", parent=software_root)
        RequirementType.objects.get_or_create(name="Cấp quyền/ tài khoản", unit="phiếu", parent=software_root)

        return {
            "move": rt_move,
            "repair": rt_repair,
            "handover": rt_handover,
            "liquidation": rt_liquid,
        }

    def _seed_equipment_types(self):
        root, _ = EquipmentType.objects.get_or_create(id="TB-CNTT", name="Thiết bị CNTT")
        pc, _ = EquipmentType.objects.get_or_create(id="PC", name="Máy tính để bàn", parent=root)
        laptop, _ = EquipmentType.objects.get_or_create(id="LAPTOP", name="Laptop", parent=root)
        printer, _ = EquipmentType.objects.get_or_create(id="PRN", name="Máy in/Scan", parent=root)

        network, _ = EquipmentType.objects.get_or_create(id="NET", name="Thiết bị mạng", parent=root)
        router, _ = EquipmentType.objects.get_or_create(id="ROUTER", name="Router", parent=network)
        switch, _ = EquipmentType.objects.get_or_create(id="SWITCH", name="Switch", parent=network)
        ap, _ = EquipmentType.objects.get_or_create(id="AP", name="Access Point", parent=network)
        firewall, _ = EquipmentType.objects.get_or_create(id="FW", name="Firewall", parent=network)

        power, _ = EquipmentType.objects.get_or_create(id="UPS", name="UPS/Thiết bị nguồn", parent=root)

        return {
            "pc": pc,
            "laptop": laptop,
            "printer": printer,
            "router": router,
            "switch": switch,
            "ap": ap,
            "firewall": firewall,
            "ups": power,
        }

    def _seed_equipment_models(self, conn_types, equip_types):
        models_data = [
            {
                "name": "Dell Latitude 5430",
                "battery": True,
                "needdriver": False,
                "cable": conn_types["USBC"],
                "features": "Laptop văn phòng 14 inch, tiêu chuẩn bền MIL-STD",
                "specs": {"CPU": "Intel Core i5-1240P", "RAM": "16GB", "SSD": "512GB", "Màn hình": '14" FHD'},
                "type": equip_types["laptop"],
            },
            {
                "name": "HP ProDesk 400 G7",
                "battery": False,
                "needdriver": False,
                "cable": conn_types["RJ45"],
                "features": "Máy tính để bàn cho nhân viên giao dịch",
                "specs": {"CPU": "Intel Core i5-10500", "RAM": "16GB", "SSD": "256GB", "OS": "Windows 11 Pro"},
                "type": equip_types["pc"],
            },
            {
                "name": "Lenovo ThinkCentre M80s",
                "battery": False,
                "needdriver": False,
                "cable": conn_types["RJ45"],
                "features": "Mini tower hiệu năng ổn định cho kế toán",
                "specs": {"CPU": "Intel Core i7-11700", "RAM": "32GB", "SSD": "1TB", "OS": "Windows 11 Pro"},
                "type": equip_types["pc"],
            },
            {
                "name": "Asus ExpertBook B5",
                "battery": True,
                "needdriver": False,
                "cable": conn_types["TB4"],
                "features": "Laptop mỏng nhẹ cho cán bộ di chuyển nhiều",
                "specs": {"CPU": "Intel Core i7-1260P", "RAM": "16GB", "SSD": "512GB", "Cân nặng": "1.25kg"},
                "type": equip_types["laptop"],
            },
            {
                "name": "HP LaserJet Pro M404dn",
                "battery": False,
                "needdriver": True,
                "cable": conn_types["RJ45"],
                "features": "Máy in A4 hỗ trợ in hai mặt tự động",
                "specs": {"Tốc độ": "38ppm", "Khay giấy": "250 tờ", "Độ phân giải": "1200dpi"},
                "type": equip_types["printer"],
            },
            {
                "name": "Canon imageRUNNER 2425",
                "battery": False,
                "needdriver": True,
                "cable": conn_types["RJ45"],
                "features": "Máy photocopy đa năng A3 cho khối văn phòng",
                "specs": {"Tốc độ": "25ppm", "ADF": "Cảm biến kép", "In mạng": "Có"},
                "type": equip_types["printer"],
            },
            {
                "name": "Cisco Catalyst 9200L-24P",
                "battery": False,
                "needdriver": True,
                "cable": conn_types["RJ45"],
                "features": "Switch Layer 3 24 port PoE+ cho core tầng",
                "specs": {"Port": "24x1G PoE+", "Uplink": "4x10G SFP+", "Throughput": "128Gbps"},
                "type": equip_types["switch"],
            },
            {
                "name": "Ubiquiti UniFi U6 Lite",
                "battery": False,
                "needdriver": True,
                "cable": conn_types["RJ45"],
                "features": "Access Point Wi-Fi 6 phủ sóng phòng họp",
                "specs": {"Chuẩn": "802.11ax", "Tốc độ": "1.5Gbps", "Nguồn": "PoE 802.3af"},
                "type": equip_types["ap"],
            },
            {
                "name": "Cisco Firepower 1010",
                "battery": False,
                "needdriver": True,
                "cable": conn_types["RJ45"],
                "features": "Firewall cho chi nhánh, tích hợp VPN/IPS",
                "specs": {"Throughput": "890Mbps", "VPN": "650Mbps", "Cổng": "8x1G RJ45"},
                "type": equip_types["firewall"],
            },
            {
                "name": "MikroTik CCR2004-1G-12S+2XS",
                "battery": False,
                "needdriver": True,
                "cable": conn_types["SFP"],
                "features": "Router lõi cho đường truyền Internet chính",
                "specs": {"CPU": "ARM 4 nhân", "Port": "12xSFP+, 2x40G QSFP+", "RAM": "4GB"},
                "type": equip_types["router"],
            },
            {
                "name": "APC Smart-UPS C 1500VA",
                "battery": True,
                "needdriver": False,
                "cable": conn_types["USBA"],
                "features": "UPS rack 2U bảo vệ thiết bị mạng",
                "specs": {"Công suất": "900W", "Thời gian lưu": "12 phút tải 50%", "Quản lý": "USB/Network card"},
                "type": equip_types["ups"],
            },
        ]

        for data in models_data:
            EquipmentModel.objects.update_or_create(
                name=data["name"],
                defaults={
                    "battery": data["battery"],
                    "needdriver": data["needdriver"],
                    "cable": data["cable"],
                    "features": data["features"],
                    "specifications": data["specs"],
                    "type": data["type"],
                },
            )

    def _seed_users(self, staff_members):
        if not staff_members:
            return []

        users_data = [
            {"username": "admin", "email": "admin@qlkt.local", "password": "Admin@123", "is_super": True},
            {"username": "ktv_hcm", "email": "ktv.hcm@qlkt.local", "password": "Password@1"},
            {"username": "ktv_hn", "email": "ktv.hn@qlkt.local", "password": "Password@1"},
            {"username": "truongphong_cntt", "email": "tp.cntt@qlkt.local", "password": "Password@1"},
            {"username": "vantai", "email": "vantai@qlkt.local", "password": "Password@1"},
        ]

        users = []
        for data in users_data:
            user, _ = User.objects.get_or_create(
                username=data["username"], defaults={"email": data["email"], "first_name": fake.first_name()}
            )
            user.set_password(data["password"])
            if data.get("is_super"):
                user.is_staff = True
                user.is_superuser = True
            user.save()

            staff_choice = random.choice(staff_members)
            StaffUser.objects.update_or_create(user=user, defaults={"staff": staff_choice})
            users.append(user)
        return users

    @transaction.atomic
    def handle(self, *args, **kwargs):
        departments = self._create_departments()
        roles = self._seed_roles()
        staff_members = self._seed_staff(departments, roles)
        self._seed_document_types()
        self._seed_error_types()
        self._seed_handle_statuses()
        conn_types = self._seed_connection_types()
        self._seed_manufacturers()
        self._seed_network_addresses()
        self._seed_requirement_types()
        equip_types = self._seed_equipment_types()
        self._seed_equipment_models(conn_types, equip_types)
        self._seed_users(staff_members)

        self.stdout.write(self.style.SUCCESS("Đã khởi tạo dữ liệu danh mục chung, nhân sự và model thiết bị."))
