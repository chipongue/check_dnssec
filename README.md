# check_dnssec
Monitoring of DNSSEC configurations.

Domain Name Server Security Extension (DNSSEC) adds security to DNS protocol by providing authentication to DNS traffic, using asymmetric encryption to ensure the authenticity and integrity of the exchanged information. DNSSEC improves system reliability, prevents man-in-the-middle attacks, fixes DNS protocol fragilities, and reduces the likelihood of manipulation of information.
However, when poorly configured or with DNSSEC expired signatures of a false protection, exposing the servers.

This Nagios plugin monitors the state of the DNSSEC configurations and points out with the critical state in case vulnerabilities (poor configuration, expired signatures, not using DNSSEC) be detected. The domain to be monitored is passed as an argument, and can also be defined the DNS to be used, and that by default is used the Google (8.8.8.8).

Mandatory arguments: The following argument must be specified when the module is executed:
-H or – domain used to specify domain name to be monitored.

Optional arguments: The following arguments are invoked optionally, as required by the user:
-d or – dnsserver used to specify the DNS server to use, by omission the query is made in Google DNS (8.8.8.8).
-V or – version used to query the module version.
-A or – author used to query the author's data.

Command-Line Execution Example:

./check_dnssec.py -H www.state.gov
