"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Scrape ESRI's cloud storage for links. It's used infrequently from dev envs to generate fixures (edited) 

It works based on the fact that ESRI's URLs use a sequential ID for documents. It outputs a CSV with the mapping from aquifer ID to filename, intended for import into gwells.

Deps: You must have pdftotext installed, as well as the Python requests lib.
"""

import os
import subprocess
import re
import requests

# Just use an unreasonably large range since we error out when a nonexistent URL is hit anyway.
for i in range(1,1000000):
    # Download PDFs
    url = "https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/Aquifer_180613_NA/FeatureServer/0/{}/attachments/{}".format(i,i)
    if not os.path.exists("{}.pdf".format(i)):
        r = requests.get(url, allow_redirects=True)
        open("{}.pdf".format(i), 'wb').write(r.content)
        subprocess.call(["pdftotext", "{}.pdf".format(i)])
    # pdftotext will dump a known string that we scan for to get the aquifer ID.
    L = open("{}.txt".format(i)).readlines()
    for l in L:
        if re.match("^\d+$", l):
            subprocess.call(["cp", "{}.pdf".format(i), "aquifer-{}.pdf".format(l.strip())])
            # TODO: output JSON for direct use in fixtures?
            print l.strip(), ",", url


