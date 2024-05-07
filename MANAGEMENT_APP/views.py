from datetime import datetime
import random
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from .models import RegistrationRequest, UserProfile, UserProject, UserProjectModule, UserWorkProgress, UserNotification
from django.utils.crypto import get_random_string

# Homepage and login page views

def homepage(request):
    return render(request, 'homepage.html')

def loginpage(request):
    return render(request, 'loginpage.html')

# Login view

def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        # Check if the user is an admin
        if name == 'admin' and password == 'admin':
            return redirect('admin_homepage')

        try:
            registration_request = RegistrationRequest.objects.get(name=name)
            password = registration_request.otp
            user_type = registration_request.user_type

            if user_type == 'developer':
                user = authenticate(username=registration_request.email, password=password)
                if user:
                    auth_login(request, user)
                    return redirect('developer_homepage')
                else:
                    messages.error(request, 'Invalid password or OTP. Please check your email for the correct OTP.')
            elif user_type == 'teamleader':
                user = authenticate(username=registration_request.email, password=password)
                if user:
                    auth_login(request, user)
                    return redirect('teamleader_homepage')
                else:
                    messages.error(request, 'Invalid password or OTP. Please check your email for the correct OTP.')
            else:
                messages.error(request, 'Invalid user type.')
        except RegistrationRequest.DoesNotExist:
            messages.error(request, 'Registration request not found.')

    return render(request, 'loginpage.html')

# Registration request handling

def send_request_to_admin_from_developer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        user_type = 'developer'
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        course_completed = request.POST.get('course_completed', '')
        certification = request.POST.get('certification', '')
        department = request.POST.get('department', '')

        # Create a RegistrationRequest instance
        registration_request = RegistrationRequest.objects.create(
            name=name,
            email=email,
            user_type=user_type,
            address=address,
            phone=phone,
            course_completed=course_completed,
            certification=certification,
            department=department,
            is_approved=False,
            otp=get_random_string(length=6, allowed_chars='0123456789')
        )

        messages.success(request, 'Registration request sent successfully. Please wait for admin approval.')
        return redirect('loginpage')  # Redirect back to the login page

    return render(request, 'developer_registerpage.html')

def send_request_to_admin_from_teamleader(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        user_type = 'teamleader'
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        course_completed = request.POST.get('course_completed', '')
        certification = request.POST.get('certification', '')
        department = request.POST.get('department', '')

        # Create a RegistrationRequest instance
        registration_request = RegistrationRequest.objects.create(
            name=name,
            email=email,
            user_type=user_type,
            address=address,
            phone=phone,
            course_completed=course_completed,
            certification=certification,
            department=department,
            is_approved=False,
            otp=get_random_string(length=6, allowed_chars='0123456789')
        )

        messages.success(request, 'Registration request sent successfully. Please wait for admin approval.')
        return redirect('loginpage')  # Redirect back to the login page

    return render(request, 'teamleader_registerpage.html')


# Developer views

def developer_registerpage(request):
    return render(request, 'developer_registerpage.html')

def developer_homepage(request):
    return render(request, 'developer/developer_homepage.html')

def dl_update_profile_page(request):
    return render(request, 'developer/dl_update_profile_page.html')

def dl_update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)

        profile.address = request.POST.get('address', profile.address)
        profile.course_completed = request.POST.get('course_completed', profile.course_completed)
        profile.department = request.POST.get('department', profile.department)
        
        phone = request.POST.get('phone')
        if phone:
            profile.phone = phone

        certification = request.FILES.get('certification')
        if certification:
            profile.certification = certification

        profile.save()

        messages.success(request, 'Profile updated successfully.')

        return redirect('developer_homepage')

def dl_update_project_page(request):
    return render(request, 'developer/dl_update_project_page.html')

def dl_check_history_page(request):
    return render(request, 'developer/dl_check_history_page.html')

def dl_reset_password_page(request):
    return render(request, 'developer/dl_reset_password_page.html')

def dl_reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password: 
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Password reset successful.')
            return redirect('developer_homepage')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'developer/dl_reset_password_page.html')

def dl_view_project_page(request):
    return render(request, 'developer/dl_view_project_page.html')

def developer_logout(request):
    auth_logout(request)
    return redirect('homepage')

# Admin views

def admin_homepage(request):
    return render(request, 'admin/admin_homepage.html')

def admin_view_users(request):
    developers = UserProfile.objects.filter(user__groups__name='developers')
    team_leaders = UserProfile.objects.filter(user__is_staff=True)
    return render(request, 'admin/admin_view_users.html', {'developers': developers, 'team_leaders': team_leaders})

def admin_review_approval(request):
    registration_requests = RegistrationRequest.objects.all()
    return render(request, 'admin/admin_review_approval.html', {'registration_requests': registration_requests})

def approve_request(request, request_id):
    registration_request = get_object_or_404(RegistrationRequest, id=request_id)

    # Mark the registration request as approved
    registration_request.is_approved = True
    registration_request.save()
    
    # Generate OTP
    otp = get_random_string(length=6, allowed_chars='0123456789')
    registration_request.otp = otp
    registration_request.save()

    # Create a new user with the provided information
    user_type = registration_request.user_type
    if user_type == 'developer':
        user = User.objects.create_user(username=registration_request.email, first_name=registration_request.name, password=otp)
        
        # Check if the 'developers' group exists
        developers_group, created = Group.objects.get_or_create(name='developers')
        user.groups.add(developers_group)
    elif user_type == 'teamleader':
        user = User.objects.create_user(username=registration_request.email, first_name=registration_request.name, password=otp)
        user.is_staff = True

    # Create a UserProfile instance for the new user
    UserProfile.objects.create(
        user=user,
        address=registration_request.address,
        phone=registration_request.phone,
        course_completed=registration_request.course_completed,
        certification=registration_request.certification,
        department=registration_request.department
    )

    # Send OTP to the user's email
    send_otp_to_user(registration_request.email, otp)

    messages.success(request, 'Registration request approved and OTP sent to the user.')
    return redirect('loginpage')

def reject_request(request, request_id):
    registration_request = get_object_or_404(RegistrationRequest, id=request_id)
    registration_request.delete()

    messages.success(request, 'Registration request rejected.')
    return redirect('admin_review_approval')

def send_otp_to_user(email, otp):
    send_mail(
        'OTP Verification',
        f'Your OTP for registration is: {otp}',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )

def admin_add_project_page(request):
    return render(request, 'admin/admin_add_project_page.html')

def admin_add_project(request):
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        project_name = request.POST.get('project_name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        attachment = request.FILES.get('attachment')

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        UserProject.objects.create(client_name=client_name, project_name=project_name,
                                    description=description, start_date=start_date,
                                    end_date=end_date, attachment=attachment)

        messages.success(request, 'Project added successfully.')

        return redirect('admin_homepage')

def admin_asign_project_page(request):
    return render(request, 'admin/admin_asign_project_page.html')

def asign_project_to_team_leader(request):
    return render(request, 'admin/admin_asign_project_page.html')

def admin_promotion_page(request):
    return render(request, 'admin/admin_promotion_page.html')

def add_delete_page(request):
    return render(request, 'admin/add_delete_page.html')

def admin_status_page(request):
    return render(request, 'admin/admin_status_page.html')

def admin_view_project_page(request):
    projects = UserProject.objects.all()
    return render(request, 'admin/admin_view_project_page.html', {'projects': projects})

def admin_logout(request):
    auth_logout(request)
    return redirect('homepage')

# Team Leader views

def teamleader_registerpage(request):
    return render(request, 'teamleader_registerpage.html')

def teamleader_homepage(request):
    return render(request, 'teamleader/teamleader_homepage.html')

def tl_asign_project_page(request):
    return render(request, 'teamleader/tl_asign_project_page.html')

def tl_project_status_page(request):
    return render(request, 'teamleader/tl_project_status_page.html')

def tl_update_profile_page(request):
    return render(request, 'teamleader/tl_update_profile_page.html')

def tl_reset_password_page(request):
    return render(request, 'teamleader/tl_reset_password_page.html')

def teamleader_logout(request):
    auth_logout(request)
    return redirect('homepage')