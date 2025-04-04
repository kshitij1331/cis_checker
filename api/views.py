from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ComplianceReport, Server
from .serializers import ComplianceReportSerializer
from core.scanner import run_compliance_check, apply_remediation


class ComplianceReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows compliance reports to be viewed or edited.
    """
    queryset = ComplianceReport.objects.all()
    serializer_class = ComplianceReportSerializer

@api_view(['POST'])
def trigger_scan(request, server_id):
    """Trigger a compliance scan for a specific server"""
    server = Server.objects.filter(id=server_id).first()
    if not server:
        return Response({"error": "Server not found"}, status=404)

    report = run_compliance_check(server_id)
    return Response({"message": "Scan completed", "report_id": report.id})

@api_view(['POST'])
def fix_issues(request, report_id):
    report = ComplianceReport.objects.filter(id=report_id).first()
    if not report:
        return Response({"error": "Report not found"}, status=404)

    apply_remediation(report_id)
    return Response({"message": "Fixes applied", "report_id": report.id})