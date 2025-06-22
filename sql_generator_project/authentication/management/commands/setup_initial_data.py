from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authentication.models import Role, DatabasePermission

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates initial roles and permissions'

    def handle(self, *args, **options):
        # Create roles
        admin_role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Full system access'}
        )
        
        analyst_role, _ = Role.objects.get_or_create(
            name='analyst',
            defaults={'description': 'Can query and analyze data'}
        )
        
        viewer_role, _ = Role.objects.get_or_create(
            name='viewer',
            defaults={'description': 'Read-only access'}
        )
        
        developer_role, _ = Role.objects.get_or_create(
            name='developer',
            defaults={'description': 'Developer access'}
        )
        
        # Create permissions
        databases = ['ecommerce', 'hospital', 'school']
        
        # Admin - full access to all databases
        for db in databases:
            DatabasePermission.objects.get_or_create(
                role=admin_role,
                database_name=db,
                defaults={
                    'can_read': True,
                    'can_write': True,
                    'can_execute': True
                }
            )
        
        # Analyst - read and execute on all databases
        for db in databases:
            DatabasePermission.objects.get_or_create(
                role=analyst_role,
                database_name=db,
                defaults={
                    'can_read': True,
                    'can_write': False,
                    'can_execute': True
                }
            )
        
        # Viewer - read only on ecommerce
        DatabasePermission.objects.get_or_create(
            role=viewer_role,
            database_name='ecommerce',
            defaults={
                'can_read': True,
                'can_write': False,
                'can_execute': False
            }
        )
        
        # Developer - full access to ecommerce and school
        for db in ['ecommerce', 'school']:
            DatabasePermission.objects.get_or_create(
                role=developer_role,
                database_name=db,
                defaults={
                    'can_read': True,
                    'can_write': True,
                    'can_execute': True
                }
            )
        
        # Create demo users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            email='admin@example.com',
            defaults={
                'role': admin_role,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        analyst_user, created = User.objects.get_or_create(
            username='analyst',
            email='analyst@example.com',
            defaults={'role': analyst_role}
        )
        if created:
            analyst_user.set_password('analyst123')
            analyst_user.save()
            self.stdout.write(self.style.SUCCESS('Created analyst user'))
        
        viewer_user, created = User.objects.get_or_create(
            username='viewer',
            email='viewer@example.com',
            defaults={'role': viewer_role}
        )
        if created:
            viewer_user.set_password('viewer123')
            viewer_user.save()
            self.stdout.write(self.style.SUCCESS('Created viewer user'))
        
        self.stdout.write(self.style.SUCCESS('Initial data setup complete!'))