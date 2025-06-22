from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('analyst', 'Data Analyst'),
        ('viewer', 'Viewer'),
        ('developer', 'Developer'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_name_display()

class DatabasePermission(models.Model):
    DATABASE_CHOICES = [
        ('ecommerce', 'E-Commerce'),
        ('hospital', 'Hospital Management'),
        ('school', 'School Management'),
    ]
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='database_permissions')
    database_name = models.CharField(max_length=50, choices=DATABASE_CHOICES)
    can_read = models.BooleanField(default=True)
    can_write = models.BooleanField(default=False)
    can_execute = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['role', 'database_name']
    
    def __str__(self):
        return f"{self.role.name} - {self.database_name}"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def get_accessible_databases(self):
        if not self.role:
            return []
        permissions = DatabasePermission.objects.filter(role=self.role, can_read=True)
        return [perm.get_database_name_display() for perm in permissions]
    
    def can_access_database(self, database_name):
        if not self.role:
            return False
        return DatabasePermission.objects.filter(
            role=self.role,
            database_name=database_name.lower().replace(' ', '_').replace('-', ''),
            can_read=True
        ).exists()

class QueryLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    natural_language_query = models.TextField()
    generated_sql = models.TextField()
    database_name = models.CharField(max_length=50)
    execution_time = models.FloatField(null=True, blank=True)
    row_count = models.IntegerField(null=True, blank=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']