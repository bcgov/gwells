"""
This script scrapes an arcgis server storage bucket by observing its
URLs use a sequential ID for documents. It outputs a CSV with the mapping from aquifer ID to filename,
intended for import into gwells.
"""

import os
import subprocess
import re
import requests

# Just use an unreasonably large range since we error out when a nonexistent URL is hit anyway.
for i in range(1,1000000):
    url = "https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/Aquifer_180613_NA/FeatureServer/0/{}/attachments/{}".format(i,i)
    if not os.path.exists("{}.pdf".format(i)):
        r = requests.get(url, allow_redirects=True)
        open("{}.pdf".format(i), 'wb').write(r.content)
        subprocess.call(["pdftotext", "{}.pdf".format(i)])
    L=open("{}.txt".format(i)).readlines()
    for l in L:
        if re.match("^\d+$", l):
            subprocess.call(["cp", "{}.pdf".format(i), "aquifer-{}.pdf".format(l.strip())])
            print l.strip(), ",", url
            break


