import random

from django.conf import settings
from django.core.management.base import BaseCommand
from faker import Faker

from common.models import Department, DocumentTypes, Staff
from documents.models import IncomingDocuments, OutgoingDocuments

fake = Faker("vi_VN")


class Command(BaseCommand):
    help = "Tạo dữ liệu văn bản đi/đến bằng tiếng Việt với nội dung nghiệp vụ CNTT."

    def handle(self, *args, **options):
        doc_types = list(DocumentTypes.objects.all())
        departments = list(Department.objects.all())
        staff_members = list(Staff.objects.all())
        security_levels = [level[0] for level in settings.SECURITY_LEVELS]

        if not doc_types or not departments or not staff_members:
            self.stdout.write(self.style.ERROR("Cần seed danh mục văn bản, phòng ban và nhân sự trước."))
            return

        outgoing_titles = [
            "Thông báo lịch bảo trì hệ thống core banking",
            "Quyết định điều chuyển 05 laptop cho chi nhánh Hà Nội",
            "Biên bản nghiệm thu hạng mục nâng cấp wifi tầng 4",
            "Đề nghị mua sắm thiết bị bảo mật cho phòng ATTT",
            "Thông báo thay đổi dải IP nội bộ tại trụ sở",
            "Kế hoạch rà soát thiết bị quá hạn bảo hành",
            "Quyết định triển khai giải pháp VPN cho chi nhánh",
        ]

        incoming_titles = [
            "Công văn yêu cầu hỗ trợ kết nối Internet tại quầy giao dịch",
            "Đề nghị cấp bổ sung mực in và giấy A4",
            "Thông báo lỗi ứng dụng CRM từ chi nhánh Đà Nẵng",
            "Thư mời tham dự buổi diễn tập an toàn thông tin",
            "Công văn phối hợp kiểm kê thiết bị quý IV",
        ]

        for _ in range(60):
            doc_type = random.choice(doc_types)
            outgoing = OutgoingDocuments.objects.create(
                document_type=doc_type,
                date=fake.date_between(start_date="-6m", end_date="today"),
                title=random.choice(outgoing_titles),
                quantity=random.randint(1, 4),
                pages=random.randint(2, 12),
                security=random.choices(security_levels, weights=[80, 10, 8, 2])[0],
                note=fake.sentence(nb_words=14),
            )
            outgoing.destination.set(random.sample(departments, k=min(2, len(departments))))
            outgoing.receiver.set(random.sample(staff_members, k=min(3, len(staff_members))))
            outgoing.save()

        for _ in range(40):
            doc_type = random.choice(doc_types)
            incoming = IncomingDocuments.objects.create(
                document_type=doc_type,
                date=fake.date_between(start_date="-6m", end_date="today"),
                title=random.choice(incoming_titles),
                quantity=random.randint(1, 3),
                pages=random.randint(2, 10),
                security=random.choices(security_levels, weights=[85, 8, 5, 2])[0],
                note=fake.text(max_nb_chars=120),
            )
            incoming.source.set(random.sample(departments, k=min(2, len(departments))))
            incoming.sender.set(random.sample(staff_members, k=min(3, len(staff_members))))
            incoming.save()

        self.stdout.write(self.style.SUCCESS("Đã tạo dữ liệu mẫu cho văn bản đi/đến."))
