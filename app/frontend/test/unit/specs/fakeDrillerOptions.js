const fakeOptions = JSON.parse(JSON.stringify({
  'DRILL': {
    'WellClassCode': [
      {
        'registries_well_class_code': 'WAT',
        'description': 'Water supply well'
      },
      {
        'registries_well_class_code': 'MON',
        'description': 'Monitoring well'
      },
      {
        'registries_well_class_code': 'MON',
        'description': 'Monitoring well'
      },
      {
        'registries_well_class_code': 'RECH',
        'description': 'Recharge/Injection well'
      },
      {
        'registries_well_class_code': 'DEWAT',
        'description': 'Dewatering well'
      },
      {
        'registries_well_class_code': 'REM',
        'description': 'Remediatation well'
      },
      {
        'registries_well_class_code': 'REM',
        'description': 'Remediatation well'
      },
      {
        'registries_well_class_code': 'GEO',
        'description': 'Geotechnical well'
      },
      {
        'registries_well_class_code': 'GEO',
        'description': 'Geotechnical well'
      },
      {
        'registries_well_class_code': 'CLOS',
        'description': 'Closed loop geoexchange well'
      },
      {
        'registries_well_class_code': 'PUMP',
        'description': 'Install pump in Water supply, Recharge/Injection, or Dewatering well'
      }
    ],
    'SubactivityCode': [
      {
        'registries_subactivity_code': 'WATER',
        'description': 'Water Well Driller',
        'qualification_set': [
          {
            'well_class': 'WAT',
            'description': 'Water supply well'
          },
          {
            'well_class': 'MON',
            'description': 'Monitoring well'
          },
          {
            'well_class': 'RECH',
            'description': 'Recharge/Injection well'
          },
          {
            'well_class': 'DEWAT',
            'description': 'Dewatering well'
          },
          {
            'well_class': 'REM',
            'description': 'Remediatation well'
          },
          {
            'well_class': 'GEO',
            'description': 'Geotechnical well'
          },
          {
            'well_class': 'PUMP',
            'description': 'Install pump in Water supply, Recharge/Injection, or Dewatering well'
          }
        ]
      },
      {
        'registries_subactivity_code': 'GEOTECH',
        'description': 'Geotechnical/Environmental Driller',
        'qualification_set': [
          {
            'well_class': 'MON',
            'description': 'Monitoring well'
          },
          {
            'well_class': 'REM',
            'description': 'Remediatation well'
          },
          {
            'well_class': 'GEO',
            'description': 'Geotechnical well'
          }
        ]
      },
      {
        'registries_subactivity_code': 'GEOXCHG',
        'description': 'Geoexchange Driller',
        'qualification_set': [
          {
            'well_class': 'CLOS',
            'description': 'Closed loop geoexchange well'
          }
        ]
      },
      {
        'registries_subactivity_code': 'PHASE2',
        'description': 'Grandparented up to Feb 29, 2016',
        'qualification_set': []
      },
      {
        'registries_subactivity_code': 'PHASE1',
        'description': 'Grandparented up to Nov 2006',
        'qualification_set': []
      }
    ],
    'AccreditedCertificateCode': [
      {
        'acc_cert_guid': '28bf8730-dbb7-4218-8e9f-06bd51f60161',
        'name': 'Geoexchange Driller Certificate',
        'cert_auth': 'Province of B.C.'
      },
      {
        'acc_cert_guid': 'da85087a-9764-410b-908e-b2b65f3dfb48',
        'name': 'Geotechnical/Environmental Driller Certificate',
        'cert_auth': 'Province of B.C.'
      },
      {
        'acc_cert_guid': 'a53d3f1e-65eb-46b7-8999-e662d654df77',
        'name': 'Grand-parent',
        'cert_auth': 'Grand-fathered'
      },
      {
        'acc_cert_guid': 'e368e066-137b-491a-af2a-da3bf2936e6d',
        'name': 'Grand-parent',
        'cert_auth': 'Grand-fathered'
      },
      {
        'acc_cert_guid': '4a059930-265f-43f5-9dbb-c71862ccc5b5',
        'name': 'Ground Water Drilling Technician Certificate',
        'cert_auth': 'Canadian Ground Water Association'
      },
      {
        'acc_cert_guid': '1886daa8-e799-49f0-9034-33d02bad543d',
        'name': 'Ground Water Pump Technician Certificate',
        'cert_auth': 'Canadian Ground Water Association'
      },
      {
        'acc_cert_guid': 'a4b2e41c-3796-4c4c-ae28-eb6ad30202d9',
        'name': 'Water Well Driller Certificate',
        'cert_auth': 'Province of B.C.'
      },
      {
        'acc_cert_guid': '5856eb50-7ea3-45c7-b882-a8863cc36b73',
        'name': 'Water Well Driller, Alberta Journeyman Certificate',
        'cert_auth': 'Province of Alberta'
      },
      {
        'acc_cert_guid': 'a17cc1f8-62c7-4715-93fb-b4c66986d9a7',
        'name': 'Water Well Driller, Saskatchewan Journeyperson Certificate',
        'cert_auth': 'Province of Saskatchewan'
      },
      {
        'acc_cert_guid': '7bf968aa-c6e0-4f57-b4f4-58723214de80',
        'name': 'Well Pump Installer Certificate',
        'cert_auth': 'Province of B.C.'
      },
      {
        'acc_cert_guid': '88d5d0aa-d2aa-450a-9708-a911dce42f7f',
        'name': 'Well Technician Certificate',
        'cert_auth': 'Province of Ontario'
      },
      {
        'acc_cert_guid': '9349a159-6739-4623-9f7d-80b904b8f885',
        'name': 'Well Technician Class 1 Drilling',
        'cert_auth': 'Province of Ontario'
      }
    ]
  }
}))

export default fakeOptions
