import random
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from faker import Faker
from documents.models import OutgoingDocuments, IncomingDocuments
from common.models import DocumentTypes, Department, Staff

fake = Faker()

class Command(BaseCommand):
    help = "Tạo mẫu dữ liệu văn bản đi và đến"

    def handle(self, *args, **options):
        num_docs = 100  # số lượng văn bản mỗi loại

        doc_types = list(DocumentTypes.objects.all())
        departments = list(Department.objects.all())
        staff_members = list(Staff.objects.all())

        if not doc_types or not departments or not staff_members:
            self.stdout.write(self.style.ERROR("Cần có dữ liệu mẫu cho DocumentTypes, Department, và Staff trước"))
            return

        # Tạo văn bản đi
        for _ in range(num_docs):
            doc_type = random.choice(doc_types)
            date = fake.date_this_year()
            outgoing = OutgoingDocuments.objects.create(
                document_type=doc_type,
                date=date,
                title=fake.sentence(),
                quantity=random.randint(1, 5),
                pages=random.randint(1, 10),
                security='BT',
                note=fake.text(max_nb_chars=100)
            )
            outgoing.destination.set(random.sample(departments, k=min(2, len(departments))))
            outgoing.receiver.set(random.sample(staff_members, k=min(2, len(staff_members))))
            outgoing.save()
            # self.stdout.write(self.style.SUCCESS(f"Tạo văn bản đi: {outgoing.ms}"))

        num_docs = 50
        # Tạo văn bản đến
        for _ in range(num_docs):
            doc_type = random.choice(doc_types)
            date = fake.date_this_year()
            incoming = IncomingDocuments.objects.create(
                document_type=doc_type,
                date=date,
                title=fake.sentence(),
                quantity=random.randint(1, 5),
                pages=random.randint(1, 10),
                security='BT',
                note=fake.text(max_nb_chars=100)
            )
            incoming.source.set(random.sample(departments, k=min(2, len(departments))))
            incoming.sender.set(random.sample(staff_members, k=min(2, len(staff_members))))
            incoming.save()
            # self.stdout.write(self.style.SUCCESS(f"Tạo văn bản đến: {incoming.ms}"))
        self.stdout.write(self.style.SUCCESS(f"✅ Đã tạo các văn bản mẫu"))
