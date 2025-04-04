from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from api.models import ComplianceReport

def generate_pdf(report_id):
    """Generates a PDF report for a given compliance report"""
    report = ComplianceReport.objects.get(id=report_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="compliance_report_{report_id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, f"Compliance Report - {report.system_name}")

    # Compliance Score
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"Compliance Score: {report.compliance_score:.2f}%")
    
    # Status
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 110, f"Status: {report.status}")

    # Table Headers
    y_position = height - 140
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, y_position, "Rule ID")
    p.drawString(200, y_position, "Description")
    p.drawString(500, y_position, "Status")

    # Table Data
    p.setFont("Helvetica", 10)
    for rule in report.report_data:
        y_position -= 20
        p.drawString(100, y_position, rule["id"])
        p.drawString(200, y_position, rule["description"][:30])  # Truncate for space
        p.drawString(500, y_position, rule["status"])

    p.showPage()
    p.save()
    
    return response
