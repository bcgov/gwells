<template>
  <div>
    <div v-if="activity === 'DRILL'">
      <h5>LEGAL DISCLAIMER FOR WELL DRILLER:</h5>

      <p>By listing persons as well drillers in this Register, the Province of British Columbia (B.C.) in no way guarantees, or may be held liable, for any work performed by the person.</p>

      <p>The drillers listed in this Register are sorted by alphabetical order in no way reflects any order of preference, special favour or any other bias on behalf of the Province of B.C..</p>

      <p>Pursuant to Part 2, Section 7 of the Groundwater Protection Regulation (GWPR), the Comptroller must establish and maintain a register of well drillers who are authorized to operated in B.C.. The list of well drillers whose names in the Register, must be made available to the public during normal business hours, or be posted on a publicly available website. A person wishing to be recognized as a well driller in B.C. and wanting to be listed in the Register may apply to the Comptroller pursuant to Section 8 of the GWPR.</p>

      <p>Pursuant to Section 14 of the GWPR:
        <ul>
          <li>a registered well driller who is classified as a water well driller is qualified in respect of constructing any class of well other than closed-loop geoexchange wells;</li>
          <li>a registered well driller who is classified as a geoexchange driller is qualified in respect of constructing closed-loop geoexchange wells;</li>
          <li>a registered well driller who is classified as a geotechnical/environmental driller is qualified in respect of constructing monitoring wells, geotechnical wells and remediation wells.</li>
          <li>a registered well driller is qualified in respect of decommissioning or deactivating any class of well.</li>
        </ul>
      </p>

      <p>Pursuant to Section 14 of the GWPR, in relation to water supply wells, dewatering wells, injection wells and remediation wells, a registered water well driller is qualified in respect of installing, maintaining, repairing, removing or testing a well pump or a well head; qualified in respect of conducting a flow test of a well, qualified in respect of disinfecting a well pump; qualified in respect of disinfecting a well.</p>

      <p>The Comptroller must remove from the Register of well drillers any person who:
        <ul>
          <li>fails to meet a requirement for registration,</li>
          <li>fails to maintain a requirement for registration, including any requirement for maintaining a certificate issued by another province or territory of Canada,</li>
          <li>is no longer actively working in Canada as a well driller.</li>
        </ul>
      </p>

      <p>A person listed as a well driller in this Register must advise the Comptroller in writing within 60 days of any changes to the information included in the Register or if they are no longer actively working in B.C. as a well driller.</p>

      <p>The person whose name appears in this Register should, in the course of their duties as a well driller in British Columbia, carry with them the well driller identification card issued to them by the Comptroller and must present it upon request to the Comptroller, the Regional Water Manager, an Engineer or an Officer under the <i>Water Sustainability Act</i> (WSA), or a Drinking
      Water Officer under the <i>Drinking Water Protection Act</i>, as proof of their qualifications as a well driller pursuant to Section 51 of the WSA.</p>

      <p>*‘Certificate issued by’: Explanation of abbreviations
        <ul>
          <li>Province of BC: Certificate issued by the Industry Training Authority or the Advanced Education Ministry of the Province of B.C.</li>
          <li>CGWA : Certificate issued by the Canadian Ground Water Association</li>
          <li>N/A – grand-fathered: Not applicable. Well drillers with this designation were registered under the grand-parenting provision of the former Ground Water Protection Regulation (2004). That provision allowed drillers to be registered at the discretion of the Deputy Comptroller of Water Rights, based on proof of experience.</li>
        </ul>
      </p>
    </div>
    <div v-if="activity === 'PUMP'">
      <h5>LEGAL DISCLAIMER FOR WELL PUMP INSTALLER:</h5>

      <p>By listing persons as well pump installers in this Register, the Province of British Columbia (B.C.) in no way guarantees, or may be held liable, for any work performed by the person.</p>

      <p>The pump installers listed in this Register are sorted by alphabetical order and in no way reflects any order of preference, special favour or any other bias on behalf of the Province of B.C..</p>

      <p>Pursuant to Part 2, Section 7 of the Groundwater Protection Regulation (GWPR), the Comptroller must establish and maintain a register of well pump installers who are authorized to operated in (B.C.). The list of well pump installers whose names are in the Register, must be made available to the public during normal business hours, or be posted on a publicly available website. A person wishing to be recognized as a well pump installer in B.C. and wanting to be listed in the Register may apply to the Comptroller pursuant to Section 8 of the GWPR.</p>

      <p>Pursuant to Section 14 of the GWPR, a registered well pump installer is qualified in respect of:
        <ul>
          <li>decommissioning or deactivating any class of well,</li>
          <li>installing, maintaining, repairing, removing or testing a well pump or well head,</li>
          <li>conducting a flow test of a well,</li>
          <li>disinfecting a well pump</li>
          <li>disinfecting a well.</li>
        </ul>
      </p>

      <p>The Comptroller must remove from the Register of well pump installers any person who:
        <ul>
          <li>fails to meet a requirement for registration,</li>
          <li>fails to maintain a requirement for registration, including any requirement for maintaining a certificate issued by another province or territory of Canada,</li>
          <li>is no longer actively working in Canada as a well pump installer.</li>
        </ul>
      </p>

      <p>A person listed as a well pump installer in this Register must advise the Comptroller in writing within 60 days of any changes to the information included in the Register or if they are no longer actively working in Canada as a well pump installer.</p>

      <p>The person whose name appears in this Register should, in the course of their duties as a well pump installer in B.C., carry with them the well pump installer identification card issued to them by the Comptroller and must present it upon request to the Comptroller, the Regional Water Manager, an Engineer or an Officer under the <i>Water Sustainability Act</i> (WSA), or a Drinking Water Officer under the <i>Drinking Water Protection Act</i>, as proof of qualifications as a well pump installer pursuant to Section 51 of the WSA.</p>

      <p>
        *‘Certificate issued by’: Explanation of abbreviations
        <ul>
          <li>Province of BC: Certificate issued by the Industry Training Authority or the Advanced Education Ministry of the Province of B.C.</li>
          <li>CGWA : Certificate issued by the Canadian Ground Water Association</li>
          <li>N/A – grand-fathered: Not applicable. Well pump installers with this designation were registered under the grand-parenting provision of the former Ground Water Protection Regulation (2004). That provision allowed well pump installers to be registered at the discretion of the Deputy Comptroller of Water Rights, based on proof of experience.</li>
        </ul>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  props: ['activity']
}
</script>

<style>

</style>
