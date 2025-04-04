import paramiko
import yaml
import subprocess
from api.models import ComplianceReport, Server
from datetime import datetime

def run_command(command):
    """Executes a shell command and returns output"""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)
    
def run_ssh_command(server, command):
    """Runs a command on a remote server using SSH"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server.ip_address, username=server.username, key_filename=server.ssh_key_path)
    
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode().strip()
    ssh.close()
    return output

def load_cis_rules(filename="core/rules/cis_ubuntu.yaml"):
    """Loads CIS Benchmark rules from a YAML file"""
    with open(filename, "r") as file:
        return yaml.safe_load(file)

def run_compliance_check(server_id):
    """Runs a CIS compliance check on a specified server"""
    server = Server.objects.get(id=server_id)
    rules = load_cis_rules()
    report_data = []

    for rule in rules["rules"]:
        rule_id = rule["id"]
        description = rule["description"]
        check_command = rule["check"]
        expected_output = rule.get("expected_output", None)
        fix_command = rule["fix"]

        actual_output = run_ssh_command(server, check_command)
        status = "PASS" if expected_output is None or actual_output == expected_output else "FAIL"

        report_data.append({
            "id": rule_id,
            "description": description,
            "status": status,
            "actual_output": actual_output,
            "expected_output": expected_output,
            "fix": fix_command,
            "severity": rule["severity"],
        })

    # Save the report in the database
    report = ComplianceReport.objects.create(
        system_name=server.name,
        compliance_score=(sum(1 for r in report_data if r["status"] == "PASS") / len(report_data)) * 100,
        report_data=report_data,
        status="PASS" if all(r["status"] == "PASS" for r in report_data) else "FAIL"
    )

    return report


def run_bash_script(script_path):
    """Executes a Bash script and returns output"""
    return run_command(f"bash {script_path}")

def apply_remediation(report_id):
    """Applies fix commands to a failed report"""
    report = ComplianceReport.objects.get(id=report_id)
    for rule in report.report_data:
        if rule["status"] == "FAIL":
            run_command(rule["fix"])  # Execute fix command
            rule["status"] = "FIXED"  # Update status

    report.save()
    return report

if __name__ == "__main__":
    report = run_compliance_check()
    print(f"Compliance Scan Completed: {report}")
    actual_output = run_bash_script("core/scripts/ssh_check.sh")

