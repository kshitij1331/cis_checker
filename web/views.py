from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from api.models import ComplianceReport, Server
from core.scanner import run_compliance_check, apply_remediation
from django.contrib.auth.decorators import login_required, user_passes_test
from core.pdf_generator import generate_pdf

def home(request):
    return render(request, "web/home.html")

def dashboard(request):
    """
    Render the dashboard view with compliance reports.
    """
    reports = ComplianceReport.objects.all().order_by('-scan_Date')
    context = {
        'reports': reports,
    }
    return render(request, 'web/dashboard.html', context)

def report_detail(request, report_id):
    report = get_object_or_404(ComplianceReport, id=report_id)

    if request.method == "POST":
        apply_remediation(report_id)
        return redirect('report_detail', report_id=report.id)

    return render(request, "web/report_detail.html", {"report": report})



def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_auditor(user):
    return user.is_authenticated and user.role == 'auditor'

@login_required
def dashboard(request):
    reports = ComplianceReport.objects.all()
    return render(request, "web/dashboard.html", {"reports": reports})

@user_passes_test(is_admin)
def trigger_scan_view(request):
    run_compliance_check()
    return redirect("dashboard")

@user_passes_test(is_admin)
def fix_issues_view(request, report_id):
    apply_remediation(report_id)
    return redirect("dashboard")


@login_required
def download_report(request, report_id):
    """Django view to trigger PDF generation"""
    report = get_object_or_404(ComplianceReport, id=report_id)
    
    # Ensure only admins and auditors can download reports
    if request.user.role not in ["admin", "auditor"]:
        return HttpResponse("Unauthorized", status=403)

    return generate_pdf(report_id)



def server_list(request):
    """Show all available servers"""
    servers = Server.objects.all()
    return render(request, "web/servers.html", {"servers": servers})


