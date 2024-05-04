from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('loginpage', views.loginpage, name='loginpage'),

    path('login', views.login, name='login'),

    path('developer_registerpage', views.developer_registerpage, name='developer_registerpage'),
    
    path('send_request_to_admin_from_developer', views.send_request_to_admin_from_developer, name="send_request_to_admin_from_developer"),

    path('teamleader_registerpage', views.teamleader_registerpage, name='teamleader_registerpage'),

    path('send_request_to_admin_from_teamleader', views.send_request_to_admin_from_teamleader, name="send_request_to_admin_from_teamleader"),

    #DEVELOPER :
    
    path('developer_homepage', views.developer_homepage, name='developer_homepage'),

    path('dl_update_project_page', views.dl_update_project_page, name='dl_update_project_page'),

    path('dl_check_history_page', views.dl_check_history_page, name='dl_check_history_page'),   

    path('dl_update_profile_page', views.dl_update_profile_page, name='dl_update_profile_page'),

    path('dl_update_profile', views.dl_update_profile, name='dl_update_profile'),

    path('dl_reset_password_page', views.dl_reset_password_page, name='dl_reset_password_page'),

    path('dl_reset_password', views.dl_reset_password, name='dl_reset_password'),

    path('dl_view_project_page', views.dl_view_project_page, name='dl_view_project_page'),

    path('developer_logout', views.developer_logout, name='developer_logout'),

    #ADMIN :

    path('admin_homepage', views.admin_homepage, name='admin_homepage'),

    path('admin_view_users', views.admin_view_users, name='admin_view_users'),

    path('admin_review_approval', views.admin_review_approval, name='admin_review_approval'),

    path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),

    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),

    path('admin_add_project_page/', views.admin_add_project_page, name='admin_add_project_page'),
    
    path('admin_add_project', views.admin_add_project, name='admin_add_project'),

    path('admin_asign_project_page', views.admin_asign_project_page, name='admin_asign_project_page'),

    path('admin_promotion_page', views.admin_promotion_page, name='admin_promotion_page'),

    path('add_delete_page', views.add_delete_page, name='add_delete_page'),

    path('admin_status_page', views.admin_status_page, name='admin_status_page'),

    path('admin_logout', views.admin_logout, name='admin_logout'),

    #TEAMLEADER :

    path('teamleader_homepage', views.teamleader_homepage, name='teamleader_homepage'),

    path('tl_asign_project_page', views.tl_asign_project_page, name='tl_asign_project_page'),

    path('tl_project_status_page', views.tl_project_status_page, name='tl_project_status_page'),

    path('tl_update_profile_page', views.tl_update_profile_page, name='tl_update_profile_page'),

    path('tl_reset_password_page', views.tl_reset_password_page, name='tl_reset_password_page'),

    path('teamleader_logout', views.teamleader_logout, name='teamleader_logout'),
]