const fakeCompanyList = JSON.parse(JSON.stringify([
  {
    'create_user': 'DATALOAD_USER',
    'create_date': '2018-01-01T08:00:00Z',
    'update_user': 'DATALOAD_USER',
    'update_date': '2018-01-01T08:00:00Z',
    'org_guid': '80867779-e7c9-4613-ba0a-e828187acf12',
    'name': 'Acme Corp',
    'org_verbose_name': 'Acme Corp (Oak Bay, BC)',
    'street_address': '1111 Main Street',
    'city': 'Oak Bay',
    'province_state': 'BC',
    'postal_code': 'Z8A 1M1',
    'main_tel': '(604) 555-2310',
    'fax_tel': '(250) 555-1112',
    'website_url': 'http://www.example.com/'
  },
  {
    'create_user': 'DATALOAD_USER',
    'create_date': '2018-01-01T08:00:00Z',
    'update_user': 'DATALOAD_USER',
    'update_date': '2018-01-01T08:00:00Z',
    'org_guid': '6d059b03-bdc2-4f2e-92a5-cf4bdb1eeba2',
    'name': 'Big Time Drilling Ltd.',
    'org_verbose_name': 'Big Time Drilling Ltd. (Victoria, BC)',
    'street_address': '555 Main Street',
    'city': 'Victoria',
    'province_state': 'BC',
    'postal_code': 'A0A 1A1',
    'main_tel': '(250) 555-1111',
    'fax_tel': '(250) 555-1113',
    'website_url': 'http://www.example.com'
  }
]))

export default fakeCompanyList
