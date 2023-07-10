from django.urls import path
from . import views  # import views from current directory
from .views import form_submit,send_email_view,save_draft


urlpatterns = [
    path('login/', views.login_view, name='employee_login'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('form_detail/<int:form_id>/', views.form_detail, name='form_detail'),
    path('form_submit/<int:assignment_id>/', views.form_submit, name='form_completion'),
    path('form_create/', views.form_create, name='form_creation'),
    path('form_assign/<int:form_id>/', views.form_assignment, name='form_assignment'),
    path('form_assign_list/<int:form_id>/', views.form_assignment_list, name='form_assignment_list'),
    path('employee_manage/', views.employee_manage, name='admin_employee_management'),
    path('employee_view/<int:employee_id>/', views.employee_view, name='employee_view'),
    path('save_draft/', views.save_draft, name='save_draft'),
    path('form_view/<int:form_id>/', views.form_view, name='form_view'),
    path('form_score/<int:form_id>', views.form_score_view, name='form_score'),
    path('admin_dashboard/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('admin_dashboard/delete_form/<int:form_id>/', views.delete_form, name='delete_form'),
    path('import_form_from_excel/', views.import_form_from_excel, name='import_form_from_excel'),
    path('form_edit/<int:form_id>/', views.form_edit, name='form_edit'),
    path('send_email/<int:assignment_id>/', send_email_view, name='send_email'),
    path('employee/delete/<int:employee_id>', views.employee_delete, name='employee_delete'),
]
