const fakeRegistration = JSON.parse(JSON.stringify(
  {
    'create_user': 'testuser',
    'create_date': '2018-05-25T21:46:03.878842Z',
    'update_user': null,
    'update_date': '2018-05-25T21:46:03.878834Z',
    'register_guid': '6cc9df51-5c59-4c91-9190-2127448cf2fe',
    'person': '48713b8c-deaa-4c54-b8e5-350cdf3916dc',
    'person_name': 'Bobby Driller',
    'registries_activity': 'DRILL',
    'activity_description': 'Well Driller',
    'status': 'ACTIVE',
    'registration_no': null,
    'registration_date': null,
    'register_removal_reason': null,
    'register_removal_date': null,
    'applications': [
      {
        'create_user': 'testuser',
        'create_date': '2018-05-25T21:46:07.063333Z',
        'update_user': null,
        'update_date': '2018-05-25T21:46:07.063325Z',
        'application_guid': 'd0c15330-c32b-4094-8500-a68c93038afb',
        'registration': '6cc9df51-5c59-4c91-9190-2127448cf2fe',
        'file_no': null,
        'proof_of_age': null,
        'primary_certificate': '28bf8730-dbb7-4218-8e9f-06bd51f60161',
        'primary_certificate_no': '',
        'registrar_notes': null,
        'reason_denied': null,
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
            'status': 'P',
            'description': 'Pending',
            'notified_date': '2018-05-25',
            'effective_date': '2018-05-25',
            'expired_date': null
          }
        ],
        'current_status': {
          'status': 'P',
          'description': 'Pending',
          'notified_date': '2018-05-25',
          'effective_date': '2018-05-25',
          'expired_date': null
        }
      },
      {
        'create_user': 'testuser',
        'create_date': '2018-05-28T15:58:22.343023Z',
        'update_user': '5a2314d2-9ee6-407c-8026-ded4089cb554',
        'update_date': '2018-05-28T21:59:06.918965Z',
        'application_guid': '977c3311-754f-4152-bbd0-929f107251ae',
        'registration': '6cc9df51-5c59-4c91-9190-2127448cf2fe',
        'file_no': null,
        'proof_of_age': 'PASSPORT',
        'primary_certificate': {
          'acc_cert_guid': '28bf8730-dbb7-4218-8e9f-06bd51f60161',
          'name': 'Geoexchange Driller Certificate',
          'cert_auth': 'Province of B.C.'
        },
        'primary_certificate_no': '12345',
        'registrar_notes': null,
        'reason_denied': null,
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
            'status': 'P',
            'description': 'Pending',
            'notified_date': '2018-05-28',
            'effective_date': '2018-05-28',
            'expired_date': null
          }
        ],
        'current_status': {
          'status': 'P',
          'description': 'Pending',
          'notified_date': '2018-05-28',
          'effective_date': '2018-05-28',
          'expired_date': null
        }
      },
      {
        'create_user': 'testuser',
        'create_date': '2018-05-28T22:00:42.649024Z',
        'update_user': null,
        'update_date': '2018-05-28T22:00:42.649016Z',
        'application_guid': '98bfc14e-db85-4b1a-89fe-8f5ca901f5cb',
        'registration': '6cc9df51-5c59-4c91-9190-2127448cf2fe',
        'file_no': null,
        'proof_of_age': null,
        'primary_certificate': null,
        'primary_certificate_no': '',
        'registrar_notes': null,
        'reason_denied': null,
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
            'status': 'P',
            'description': 'Pending',
            'notified_date': '2018-05-28',
            'effective_date': '2018-05-28',
            'expired_date': null
          }
        ],
        'current_status': {
          'status': 'P',
          'description': 'Pending',
          'notified_date': '2018-05-28',
          'effective_date': '2018-05-28',
          'expired_date': null
        }
      }
    ],
    'organization': null
  })
)

export default fakeRegistration
