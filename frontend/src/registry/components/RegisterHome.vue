<template>
  <div>
    <b-button variant="primary">Add new entry</b-button>
    <b-button variant="primary">Manage companies</b-button>
    <b-card border class="border" title="Search for a Well Driller or Well Installer">
      <p class="card text">
        <b-form>
          <b-form-group>
            <p>Choose a professional type:</p>
            <b-form-radio-group>
              <b-form-radio value="driller"><span style="margin-left:6px; font-weight: normal">Well Driller</span></b-form-radio>
              <b-form-radio value="installer"><span style="margin-left:6px; font-weight: normal">Well Pump Installer</span></b-form-radio>
            </b-form-radio-group>
          </b-form-group>
          <b-row align-h="start">
            <b-col>
              <b-form-group>
                <p>Community</p>
                <b-form-select v-model="community" :options="cities"></b-form-select>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group>
                <p>Registration status</p>
                <b-form-select v-model="regStatus" :options="regStatusOptions"></b-form-select>
              </b-form-group>
            </b-col>
          </b-row>
          <b-form-group>
            <p>Individual, company, or registration number</p>
            <b-form-input type="text" placeholder="Search"></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="secondary">Reset</b-button>
        </b-form>
      </p>
    </b-card>

    <register-table/>
  </div>
</template>

<script>
import RegisterTable from '@/registry/components/RegisterTable'
export default {
  components: {
    'register-table': RegisterTable
  },
  computed: {
    cities () {
      const list = []
      list.push({
        value: null,
        text: 'Select a city'
      })
      this.mockData.forEach((company) => {
        if (company.city && !~list.findIndex(item => item.value === company.city)) {
          list.push({
            value: company.city,
            text: company.city
          })
        }
      })
      return list
    }
  },
  data () {
    return {
      regStatus: 'all',
      community: null,
      regStatusOptions: [
        { value: 'all', text: 'All' },
        { value: 'pending', text: 'Pending' },
        { value: 'notRegistered', text: 'Not registered' },
        { value: 'registered', text: 'Registered' },
        { value: 'removed', text: 'Removed' }
      ],
      mockData: [
        {
          org_guid: '93f6f8fc-03d3-4a89-b1e5-f2c834c63562',
          name: 'Atgen Drilling Co.',
          street_address: '8852 Merry Wagon Arbor',
          city: 'Tow Hill',
          province: 'AB',
          postal_code: 'V3J 2Q7',
          main_tel: '(778) 584-4523',
          contacts: [
            {
              contact_at_guid: '8fbbb456-c772-47f0-be98-c41fd0de9968',
              organization_name: 'Atgen Drilling Co.',
              person_name: 'Josie Hobbs',
              person: 'd2eb198d-1c9b-4c5e-99d6-49807f38e52f',
              org: '93f6f8fc-03d3-4a89-b1e5-f2c834c63562',
              contact_tel: '(250) 723-5708',
              contact_email: null
            }
          ]
        },
        {
          org_guid: 'f3c92b8e-d4f5-4563-bf64-0d602460ff53',
          name: 'Earthplex Installers',
          street_address: '7010 Rocky Bluff Mall ',
          city: 'Atlin',
          province: 'BC',
          postal_code: 'V0H 8E1',
          main_tel: '(250) 654-0361',
          contacts: [
            {
              contact_at_guid: '959a560e-26e4-4008-970a-fae2d4c2d0b4',
              organization_name: 'Earthplex Installers',
              person_name: 'Ann Berg',
              person: 'db02b5bb-1473-4f97-9bcf-f6214e8dd5aa',
              org: 'f3c92b8e-d4f5-4563-bf64-0d602460ff53',
              contact_tel: '(604) 424-7090',
              contact_email: 'cardenas@driller.ca'
            }
          ]
        },
        {
          org_guid: '6cf747f3-31cf-4c8f-9d2a-a1cd32dc24a4',
          name: 'Exoplode Drilling Co.',
          street_address: '5480 Burning Pointe',
          city: 'Shookumchuk',
          province: 'BC',
          postal_code: 'V3S 9O8',
          main_tel: '(250) 046-0449',
          contacts: [
            {
              contact_at_guid: '15d733be-be35-4ae1-87a8-d7c3e42e7003',
              organization_name: 'Exoplode Drilling Co.',
              person_name: 'Dodson Griffith',
              person: '54f26199-a6ac-4ee9-861d-907fa3e9b5e1',
              org: '6cf747f3-31cf-4c8f-9d2a-a1cd32dc24a4',
              contact_tel: '(250) 304-1599',
              contact_email: 'gray@driller.ca'
            },
            {
              contact_at_guid: '27771738-e2c9-45f0-982a-1849a1a39025',
              organization_name: 'Exoplode Drilling Co.',
              person_name: 'Lucas Dale',
              person: '894f133f-f8f4-4a75-93f7-ce82e0232943',
              org: '6cf747f3-31cf-4c8f-9d2a-a1cd32dc24a4',
              contact_tel: '(250) 677-2223',
              contact_email: 'bradley@driller.ca'
            },
            {
              contact_at_guid: '84005af1-ac44-426f-ae25-0eaa9e8ad71e',
              organization_name: 'Exoplode Drilling Co.',
              person_name: 'Rollins Oneill',
              person: '6f38afd3-de1f-4661-878a-aadaed54e339',
              org: '6cf747f3-31cf-4c8f-9d2a-a1cd32dc24a4',
              contact_tel: '(250) 986-4265',
              contact_email: null
            }
          ]
        },
        {
          org_guid: 'ac354cf4-809c-4005-8dcd-715656847ac2',
          name: 'Geoform Drilling Co.',
          street_address: '7604 Stony Island Circle',
          city: 'Deroche',
          province: 'BC',
          postal_code: 'V0T 3T7',
          main_tel: '(250) 103-8103',
          contacts: [
            {
              contact_at_guid: '300991b3-9832-468e-adf5-a9c86c7a9ecf',
              organization_name: 'Geoform Drilling Co.',
              person_name: 'Rocha Mcmahon',
              person: '73b41f91-6468-459c-b48f-756357627765',
              org: 'ac354cf4-809c-4005-8dcd-715656847ac2',
              contact_tel: '(604) 430-1783',
              contact_email: 'brock@driller.ca'
            },
            {
              contact_at_guid: '35c34ea3-c858-47bc-80b4-c6109e9a68c7',
              organization_name: 'Geoform Drilling Co.',
              person_name: 'Lawanda Mcgowan',
              person: 'd739b11a-0790-46fe-bf9d-a3f2a40f728c',
              org: 'ac354cf4-809c-4005-8dcd-715656847ac2',
              contact_tel: '(604) 244-3019',
              contact_email: 'irwin@driller.ca'
            },
            {
              contact_at_guid: '75c4345b-70a9-44d7-baf2-c4534f8c67a8',
              organization_name: 'Geoform Drilling Co.',
              person_name: 'Morris West',
              person: '3f35f155-4e28-4bd7-b914-b44997c197f3',
              org: 'ac354cf4-809c-4005-8dcd-715656847ac2',
              contact_tel: '(778) 788-6649',
              contact_email: 'bass@driller.ca'
            }
          ]
        },
        {
          org_guid: 'ac354cf4-809c-4005-8dcd-715656847ac2',
          name: 'Go Drilling Co.',
          street_address: '7606 Stony Island Circle',
          city: 'Deroche',
          province: 'BC',
          postal_code: 'V0T 3T7',
          main_tel: '(250) 103-8104',
          contacts: [
            {
              contact_at_guid: '75c4345b-70a9-44d7-baf2-c4534f8c67a8',
              organization_name: 'Go Drilling Co.',
              person_name: 'Norris Best',
              person: '3f35f155-4e28-4bd7-b914-b44997c197f3',
              org: 'ac354cf4-809c-4005-8dcd-715656847ac2',
              contact_tel: '(778) 788-6649',
              contact_email: 'bass@driller.ca'
            }
          ]
        }
      ]
    }
  }
}
</script>

<style>
.btn {
  margin-top: 5px;
}
</style>
