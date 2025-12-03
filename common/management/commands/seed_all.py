from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Chạy tuần tự tất cả lệnh seed (danh mục, trang bị, văn bản, nghiệp vụ)."

    def handle(self, *args, **options):
        commands = ["seed_data", "seed_equipment", "seed_documents", "seed_operations"]
        for cmd in commands:
            self.stdout.write(self.style.WARNING(f"Đang chạy {cmd}..."))
            call_command(cmd)
        self.stdout.write(self.style.SUCCESS("Hoàn tất seed toàn bộ dữ liệu."))
