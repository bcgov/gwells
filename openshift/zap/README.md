# OWASP ZAP Security Vulnerability Scanning

The OWASP Zed Attack Proxy (ZAP) automatically finds security vulnerabilities in our web applications.

The tool runs in the pipeline with several pre-packaged options:

* zap-api-scan.py - [For more details](https://github.com/zaproxy/zaproxy/wiki/ZAP-API-Scan)
* zap-baseline.py - [For more details](https://github.com/zaproxy/zaproxy/wiki/ZAP-Baseline-Scan)
* zap-full-scan.py - [For more details](https://github.com/zaproxy/zaproxy/wiki/ZAP-Full-Scan)

Please see the [original repository](https://github.com/rht-labs/owasp-zap-openshift) for more details on how this image was built.

Common options for the baseline scan are:

**Usage:** zap-baseline.py -t <target> [options]
    
    -t target         target URL including the protocol, eg https://www.example.com

**Options:**
    
    -c config_file    config file to use to INFO, IGNORE or FAIL warnings
    -u config_url     URL of config file to use to INFO, IGNORE or FAIL warnings
    -g gen_file       generate default config file (all rules set to WARN)
    -m mins           the number of minutes to spider for (default 1)
    -r report_html    file to write the full ZAP HTML report')
    -w report_md      file to write the full ZAP Wiki (Markdown) report
    -x report_xml     file to write the full ZAP XML report
    -a                include the alpha passive scan rules as well
    -d                show debug messages
    -P                specify listen port
    -D                delay in seconds to wait for passive scanning
    -i                default rules not in the config file to INFO
    -j                use the Ajax spider in addition to the traditional one
    -l level          minimum level to show: PASS, IGNORE, INFO, WARN or FAIL, use with -s to hide example URLs
    -n context_file   context file which will be loaded prior to spidering the target
    -p progress_file  progress file which specifies issues that are being addressed
    -s                short output format - dont show PASSes or example URLs
    -z zap_options    ZAP command line options e.g. -z "-config aaa=bbb -config ccc=ddd"

A typical call for GWELLS is: 

    /zap/zap-full-scan.py -r index.html -t https://testapps.nrs.gov.bc.ca/gwells/

Please see the [Jenkinsfile-zap](https://github.com/bcgov/gwells/blob/developer/Jenkinsfile-zap) file to see our implementation example.        
