from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplianceReportViewSet, trigger_scan, fix_issues


router = DefaultRouter()
router.register(r'reports', ComplianceReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('scan/<int:server_id>/', trigger_scan, name='trigger_scan'),
    path('fix/<int:report_id>/', fix_issues, name='fix_issues')
]
