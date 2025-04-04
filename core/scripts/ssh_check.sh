#!/bin/bash
# Check if SSH root login is disabled
if grep -q "^PermitRootLogin no" /etc/ssh/sshd_config; then
    echo "PASS"
else
    echo "FAIL"
fi
