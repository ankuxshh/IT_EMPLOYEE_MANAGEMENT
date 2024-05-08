from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class RegistrationRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    user_type = models.CharField(max_length=20, default='employee')
    address = models.CharField(max_length=100, default='') 
    phone = models.CharField(max_length=15, default='', blank=True) 
    course_completed = models.CharField(max_length=100, default='') 
    certification = models.CharField(max_length=100, default='') 
    department = models.CharField(max_length=100, default='')  
    is_approved = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)  # Increase max_length for address
    course_completed = models.CharField(max_length=100, blank=True)
    certification = models.FileField(upload_to='certifications/', blank=True)
    department = models.CharField(max_length=100, blank=True)

class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    client_name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    attachment = models.FileField(upload_to='project_attachments/')

class ProjectAssignment(models.Model):
    team_leader = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assigned_projects')
    project = models.ForeignKey(UserProject, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    attachments = models.FileField(upload_to='project_assignments/')
    date_assigned = models.DateField(auto_now_add=True)

class UserProjectModule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(UserProject, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=255)

class UserWorkProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project_module = models.ForeignKey(UserProjectModule, on_delete=models.CASCADE)
    progress_update = models.TextField()
    attachments = models.FileField(upload_to='work_attachments/', null=True, blank=True)
    date = models.DateField(auto_now_add=True)

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)