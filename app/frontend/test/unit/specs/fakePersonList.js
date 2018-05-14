const fakePersonList = JSON.parse(JSON.stringify(
  {
    next: 'http://www.example.com/api/?limit=30&offset=60',
    previous: 'http://www.example.com/api/?limit=30&offset=0',
    results: [
      {
        'person_guid': '728c5b91-25aa-44de-8b5d-3b0b7ab115a5',
        'first_name': 'Bob',
        'surname': 'Drillerson',
        'registrations': [
          {
            'register_guid': '816eca52-7c45-4ff8-a0f0-e907ced6d93b',
            'activity': 'DRILL',
            'activity_description': 'Well Driller',
            'status': 'Active',
            'registration_no': 'WD 95111111',
            'organization': {
              'org_guid': '081b3614-286f-4446-a984-88b05677bd45',
              'name': 'Drillerson Drilling Ltd.',
              'street_address': '1111 Industrial St',
              'city': 'Victoria',
              'province_state': 'BC',
              'postal_code': 'X9A 1A8',
              'main_tel': '(250) 555-4123',
              'fax_tel': '(250) 555-4121',
              'website_url': null
            },
            'applications': [
              {
                'application_guid': 'ae06c5a3-27b4-45b5-afb8-4622eb619855',
                'file_no': 'A12345',
                'reason_denied': null,
                'qualifications': [
                  'WAT',
                  'MON',
                  'RECH',
                  'DEWAT',
                  'REM',
                  'GEO',
                  'PUMP'
                ],
                'status_set': [
                  {
                    'status': 'A',
                    'description': 'Approved',
                    'notified_date': '2018-04-12',
                    'effective_date': '2018-04-12',
                    'expired_date': null
                  }
                ],
                'subactivity': {
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
                'cert_authority': 'BC'
              },
              {
                'application_guid': '5ce89aee-e058-4eca-a66b-28ea0b3acb43',
                'file_no': '124',
                'reason_denied': null,
                'qualifications': [
                  'CLOS'
                ],
                'status_set': [
                  {
                    'status': 'A',
                    'description': 'Approved',
                    'notified_date': '2018-04-12',
                    'effective_date': '2018-04-12',
                    'expired_date': null
                  }
                ],
                'subactivity': {
                  'registries_subactivity_code': 'GEOXCHG',
                  'description': 'Geoexchange Driller',
                  'qualification_set': [
                    {
                      'well_class': 'CLOS',
                      'description': 'Closed loop geoexchange well'
                    }
                  ]
                },
                'cert_authority': 'BC'
              }
            ]
          }
        ],
        'contact_info': [
          {
            'contact_tel': null,
            'contact_email': 'driller1@example.com'
          }
        ]
      },
      {
        'person_guid': '728c5b91-25aa-44de-8b5d-3b0b7ab115a1',
        'first_name': 'Don',
        'surname': 'Drillerson',
        'registrations': [
          {
            'register_guid': '816eca52-7c45-4ff8-a0f0-e907ced6d93a',
            'activity': 'DRILL',
            'activity_description': 'Well Driller',
            'status': 'Active',
            'registration_no': 'WD 95111112',
            'organization': {
              'org_guid': '081b3614-286f-4446-a984-88b05677bd45',
              'name': 'Drillerson Drilling Ltd.',
              'street_address': '1111 Industrial St',
              'city': 'Victoria',
              'province_state': 'BC',
              'postal_code': 'X9A 1A8',
              'main_tel': '(250) 555-4123',
              'fax_tel': '(250) 555-4121',
              'website_url': null
            },
            'applications': [
              {
                'application_guid': 'ae06c5a3-27b4-45b5-afb8-4622eb619819',
                'file_no': 'A12346',
                'reason_denied': null,
                'qualifications': [
                  'WAT',
                  'MON',
                  'RECH',
                  'DEWAT',
                  'REM',
                  'GEO',
                  'PUMP'
                ],
                'status_set': [
                  {
                    'status': 'A',
                    'description': 'Approved',
                    'notified_date': '2018-04-12',
                    'effective_date': '2018-04-12',
                    'expired_date': null
                  }
                ],
                'subactivity': {
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
                'cert_authority': 'BC'
              },
              {
                'application_guid': '5ce89aee-e058-4eca-a66b-28ea0b3acb11',
                'file_no': '125',
                'reason_denied': null,
                'qualifications': [
                  'CLOS'
                ],
                'status_set': [
                  {
                    'status': 'A',
                    'description': 'Approved',
                    'notified_date': '2018-04-12',
                    'effective_date': '2018-04-12',
                    'expired_date': null
                  }
                ],
                'subactivity': {
                  'registries_subactivity_code': 'GEOXCHG',
                  'description': 'Geoexchange Driller',
                  'qualification_set': [
                    {
                      'well_class': 'CLOS',
                      'description': 'Closed loop geoexchange well'
                    }
                  ]
                },
                'cert_authority': 'BC'
              }
            ]
          }
        ],
        'contact_info': [
          {
            'contact_tel': null,
            'contact_email': 'driller2@example.com'
          }
        ]
      }
    ]
  })
)

export default fakePersonList
