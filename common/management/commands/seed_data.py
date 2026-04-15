from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction

from datetime import date, timedelta
from decimal import Decimal
import random

from core.attendance.models import Attendance
from core.leaves.models import Leave
from core.employees.models import Employee, Department


class Command(BaseCommand):
    help = "Seed demo data (no faker)"

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true')

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("🚀 Seeding data...")

        User = get_user_model()
        random.seed(42)
        today = timezone.now().date()

        # ─────────────────────────────
        # RESET
        # ─────────────────────────────
        if options['reset']:
            self.stdout.write("🗑 Clearing data...")
            Attendance.objects.all().delete()
            Leave.objects.all().delete()
            Employee.objects.all().delete()
            Department.objects.all().delete()

        # ─────────────────────────────
        # SUPERUSER
        # ─────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@hrm.local',
                password='admin123',
            )

        # ─────────────────────────────
        # DEPARTMENTS
        # ─────────────────────────────
        dept_names = [
            "Phòng Nhân Sự",
            "Phòng CNTT",
            "Phòng Kế Toán",
            "Phòng Marketing",
            "Phòng Bán Hàng",
        ]

        depts = {}
        for name in dept_names:
            d, _ = Department.objects.get_or_create(
                name=name,
                defaults={"description": name}
            )
            depts[name] = d

        # ─────────────────────────────
        # EMPLOYEES (TẠO 50 NGƯỜI)
        # ─────────────────────────────
        self.stdout.write("👥 Creating employees...")

        first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đặng"]
        last_names = ["Văn A", "Văn B", "Văn C", "Thị D", "Thị E"]

        positions = ["Intern", "Junior", "Senior", "Team Lead", "Manager"]

        created_employees = []

        for i in range(50):
            first = random.choice(first_names)
            last = random.choice(last_names)

            emp_id = f"NV{i:03d}"

            emp, created = Employee.objects.get_or_create(
                employee_id=emp_id,
                defaults=dict(
                    first_name=first,
                    last_name=last,
                    email=f"user{i}@hrm.local",
                    phone=f"09{random.randint(10000000, 99999999)}",
                    address="Việt Nam",
                    gender=random.choice(["M", "F"]),
                    date_of_birth=date(
                        random.randint(1985, 2000),
                        random.randint(1, 12),
                        random.randint(1, 28),
                    ),
                    department=random.choice(list(depts.values())),
                    position=random.choice(positions),
                    hire_date=date(
                        random.randint(2018, 2024),
                        random.randint(1, 12),
                        random.randint(1, 28),
                    ),
                    status="ACTIVE",
                    base_salary=Decimal(random.randint(8, 30)) * 1_000_000,
                    allowance=Decimal(random.randint(1, 5)) * 1_000_000,
                )
            )

            created_employees.append(emp)

        self.stdout.write(f"  - {len(created_employees)} employees ready")

        # ─────────────────────────────
        # ATTENDANCE
        # ─────────────────────────────
        self.stdout.write("🕐 Creating attendance...")

        def prev_working_days(ref_date, count):
            d = ref_date - timedelta(days=1)
            yielded = 0
            while yielded < count:
                if d.weekday() < 5:
                    yield d
                    yielded += 1
                d -= timedelta(days=1)

        for emp in created_employees:
            for work_date in prev_working_days(today, 10):
                Attendance.objects.get_or_create(
                    employee=emp,
                    date=work_date,
                    defaults=dict(
                        status=random.choice(
                            ['PRESENT', 'LATE', 'ABSENT']
                        )
                    )
                )

        # ─────────────────────────────
        # LEAVE
        # ─────────────────────────────
        self.stdout.write("📋 Creating leave...")

        for emp in created_employees:
            if random.random() < 0.3:
                start = today + timedelta(days=random.randint(-10, 10))
                Leave.objects.get_or_create(
                    employee=emp,
                    start_date=start,
                    end_date=start + timedelta(days=2),
                    defaults=dict(
                        reason="Nghỉ phép",
                        status=random.choice(
                            ['PENDING', 'APPROVED', 'REJECTED']
                        )
                    )
                )

        # ─────────────────────────────
        # DONE
        # ─────────────────────────────
        self.stdout.write(self.style.SUCCESS("✅ Seed completed!"))
        self.stdout.write(f"Employees: {Employee.objects.count()}")
