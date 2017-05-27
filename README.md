# check_dnssec
This Nagios plugin monitors the state of the DNSSEC configurations and points out with the critical state in case vulnerabilities (poor configuration, expired signatures, not using DNSSEC) be detected. The domain to be monitored is passed as an argument, and can also be defined the DNS to be used, and that by default is used the Google (8.8.8.8).
