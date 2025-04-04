from django.urls import path
from .views import home, dashboard, login, report_detail, trigger_scan_view, fix_issues_view, download_report, server_list

urlpatterns = [
    path('',home, name='home'),
    path('dashboard/',dashboard, name='dashboard'),
    path('login/', login, name="login"),
    path('report/<int:report_id>/', report_detail, name='report_detail'),
    path('scan/', trigger_scan_view, name="trigger_scan"),
    path('fix/<int:report_id>/', fix_issues_view, name="fix_issues"),
    path('report/<int:report_id>/download/', download_report, name="download_report"),
    path('servers/', server_list, name="server_list"),
]