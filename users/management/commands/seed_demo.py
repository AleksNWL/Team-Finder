from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import User


ADMIN_USER = {
    "email": "admin@demo.team",
    "password": "admin12345",
    "name": "Админ",
    "surname": "Практикум",
    "phone": "+79000000000",
    "about": "Учётная запись для проверки админ-панели.",
    "github_url": "",
    "is_staff": True,
    "is_superuser": True,
}

DEMO_USERS = [
    {
        "email": "anna@demo.team",
        "password": "demo12345",
        "name": "Анна",
        "surname": "Иванова",
        "phone": "+79001110001",
        "about": "Backend-разработчик, ищу команду для pet-проектов.",
        "github_url": "https://github.com/demo-anna",
    },
    {
        "email": "boris@demo.team",
        "password": "demo12345",
        "name": "Борис",
        "surname": "Петров",
        "phone": "+79001110002",
        "about": "Frontend и UI, люблю продуктовые идеи.",
        "github_url": "https://github.com/demo-boris",
    },
    {
        "email": "clara@demo.team",
        "password": "demo12345",
        "name": "Клара",
        "surname": "Смирнова",
        "phone": "+79001110003",
        "about": "Аналитик и координатор команд.",
        "github_url": "",
    },
]

DEMO_PROJECTS = [
    {
        "owner_email": "anna@demo.team",
        "name": "TeamFinder Mobile",
        "description": "Мобильное приложение для поиска команд в pet-проектах.",
        "status": Project.STATUS_OPEN,
        "github_url": "https://github.com/demo/teamfinder-mobile",
    },
    {
        "owner_email": "boris@demo.team",
        "name": "Design System Hub",
        "description": "Открытая библиотека UI-компонентов для стартапов.",
        "status": Project.STATUS_OPEN,
        "github_url": "https://github.com/demo/design-system-hub",
    },
    {
        "owner_email": "clara@demo.team",
        "name": "Open Analytics Kit",
        "description": "Набор дашбордов для небольших продуктовых команд.",
        "status": Project.STATUS_CLOSED,
        "github_url": "",
    },
]


class Command(BaseCommand):
    help = "Создаёт демонстрационных пользователей и проекты для ревью."

    def handle(self, *args, **options):
        users_by_email = {}
        admin_payload = ADMIN_USER.copy()
        admin_password = admin_payload.pop("password")
        admin_user, admin_created = User.objects.get_or_create(
            email=admin_payload["email"],
            defaults=admin_payload,
        )
        if admin_created:
            admin_user.set_password(admin_password)
            admin_user.save()
        elif not admin_user.is_staff or not admin_user.is_superuser:
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
        users_by_email[admin_user.email] = admin_user
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Создан' if admin_created else 'Найден'} администратор {admin_user.email}"
            )
        )

        for data in DEMO_USERS:
            payload = data.copy()
            password = payload.pop("password")
            user, created = User.objects.get_or_create(
                email=payload["email"],
                defaults=payload,
            )
            if created:
                user.set_password(password)
                user.save()
            users_by_email[user.email] = user
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Создан' if created else 'Найден'} пользователь {user.email}"
                )
            )

        for item in DEMO_PROJECTS:
            owner = users_by_email[item["owner_email"]]
            project, created = Project.objects.get_or_create(
                name=item["name"],
                owner=owner,
                defaults={
                    "description": item["description"],
                    "status": item["status"],
                    "github_url": item["github_url"],
                },
            )
            project.participants.add(owner)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Создан проект {project.name}"))
            else:
                self.stdout.write(f"Проект {project.name} уже существует")

        anna = users_by_email["anna@demo.team"]
        boris = users_by_email["boris@demo.team"]
        mobile = Project.objects.get(name="TeamFinder Mobile")
        design = Project.objects.get(name="Design System Hub")
        anna.favorites.add(design)
        boris.favorites.add(mobile)
        mobile.participants.add(boris)
        design.participants.add(anna)
        self.stdout.write(
            self.style.SUCCESS(
                "Демо-данные готовы. Пользователи: demo12345, админ: admin12345"
            )
        )
