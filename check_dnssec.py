#! /usr/bin/env python3

'''
Script to check without a particular domain has a DNSSEC signature.
Creation date: 14/01/2017
Date last updated: 19/03/2017

* 
* License: GPL
* Copyright (c) 2017 DI-FCUL
* 
* Description:
* 
* This file contains the check_dnssec plugin
* 
* Use the nrpe program to check request on remote server.
* 
* 
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import os
import sys
import requests
import urllib.request
from optparse import OptionParser
import socket

__author__ = "\nAuthor: Raimundo Henrique da Silva Chipongue\nE-mail: fc48807@alunos.fc.ul.pt, chipongue1@gmail.com\nInstitution: Faculty of Science of the University of Lisbon\n"
__version__= "1.0.0"

# define exit codes
ExitOK = 0
ExitWarning = 1
ExitCritical = 2
ExitUnknown = 3

def testdnssec(opts):
    domain = opts.domain
    domain = domain.replace("https://", "")
    domain = domain.replace("http://", "")
    domain = domain.replace("www.", "")
    if domain:
        try:
            socket.gethostbyname_ex(domain)
            num = True
        except:
            num = False           
        if not num:
            try:
                domain = ("www.%s"%domain)
                socket.gethostbyname_ex(domain)
            except:
                print('Unable to resolve "%s"'%domain)
                sys.exit(ExitUnknown)

        dig_requests = os.popen('dig @%s %s +noall +comments +dnssec'%(opts.dnsserver, domain)).read()
        if "ad;" in dig_requests:
            ad_flag = 1
        else:
            ad_flag = 0
        if "SERVFAIL," in dig_requests:
            status_error = 1
        else:
            status_error = 0
        if "NOERROR," in dig_requests:
            status_noerror = 1
        else:
            status_noerror = 0

        if ad_flag == 1 and status_noerror == 1:
            print('The domain "%s" is safe because it use a valid DNSSEC.'%domain)
            sys.exit(ExitOK)
        elif status_error == 1:
            print('The domain "%s" uses DNSSEC, but this is invalid or misconfigured.'%domain)
            sys.exit(ExitWarning)
        elif status_noerror == 1 and ad_flag == 0:
            print('Domain "%s" does not use DNSSEC' %domain)
            sys.exit(ExitCritical)
        else:
            print("Can't read the result")
            sys.exit(ExitUnknown)
    else:
        print ("Impossible to check domains")
        sys.exit(ExitUnknown)
           
def main():
    parser = OptionParser("usage: %prog [options] ARG1 FOR EXAMPLE: -H www.ciencias.ulisboa.pt")
    parser.add_option("-H","--domain", type=str,
                      dest="domain", help="Domain name for check DNSSEC, for example: -H www.ciencias.ulisboa.pt")
    parser.add_option("-d","--dnsserver", type=str, default="8.8.8.8", dest="dnsserver",
                      help="Specify the DNS server you need to use for check DNSSEC, for example: -d 127.0.0.1, default value is 8.8.8.8")
    parser.add_option("-V","--version", action="store_true", dest="version",
                      help="This option show the current version number of the program and exit")
    parser.add_option("-A","--author", action="store_true", dest="author",
                      help="This option show author information and exit")

    (opts, args) = parser.parse_args()
    if opts.author:
        print(__author__)
        sys.exit()
    if opts.version:
        print("check_dnssec.py %s"%__version__)
        sys.exit()
    if not opts.domain:
        parser.error("Please, this program requires domain arguments, for example: -H www.ciencias.ulisboa.pt.") 
        
    testdnssec(opts)

if __name__ == '__main__':
    main()
