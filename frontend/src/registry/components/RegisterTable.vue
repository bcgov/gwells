<template>
  <div>
    <h2>Well Driller Results</h2>
    <b-table
      striped
      :items="mockData"
      :fields="fields"
    />
  </div>
</template>

<script>
export default {
  name: 'RegisterTable',
  data () {
    return {
      fields: ['name', 'street_address', 'city', 'province', 'main_tel'],
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
        // {
        //   org_guid: "417b3f42-4fed-4c6e-9a8b-c5bc3705b7d2",
        //   "name": "Hopeli Drilling Co.",
        //   "street_address": "7910 Cinder Moor",
        //   "city": "Port Moody",
        //   "province": "BC",
        //   "postal_code": "V0R 2G9",
        //   "main_tel": "(778) 197-7980",
        //   "contacts": [
        //     {
        //       "contact_at_guid": "2d1b0ada-1b87-4699-8900-d40a6487622d",
        //       "organization_name": "Hopeli Drilling Co.",
        //       "person_name": "Bennett Cain",
        //       "person": "bfe65b43-3d39-40b2-bf0a-59891c1975f7",
        //       "org": "417b3f42-4fed-4c6e-9a8b-c5bc3705b7d2",
        //       "contact_tel": "(250) 788-7512",
        //       "contact_email": null
        //     }
        //   ]
        // },
        // {
        //   "org_guid": "9f9937dc-8559-4418-ba22-9b9f0a94d456",
        //   "name": "Jasper Drilling Co.",
        //   "street_address": "4374 Cinder Common",
        //   "city": "Sullivan Bay",
        //   "province": "BC",
        //   "postal_code": "V8E 0Y3",
        //   "main_tel": "(250) 720-5533",
        //   "contacts": [
        //     {
        //       "contact_at_guid": "240c7385-ed62-47f1-87ff-9e5d550fb610",
        //       "organization_name": "Jasper Drilling Co.",
        //       "person_name": "Shannon Carr",
        //       "person": "803f845e-21a1-42ae-acab-28b5c3af6b40",
        //       "org": "9f9937dc-8559-4418-ba22-9b9f0a94d456",
        //       "contact_tel": "(250) 141-9449",
        //       "contact_email": "pickett@driller.ca"
        //     },
        //     {
        //       "contact_at_guid": "727d710a-8674-4154-b5be-76eb1d4cfa08",
        //       "organization_name": "Jasper Drilling Co.",
        //       "person_name": "Suzette Mcknight",
        //       "person": "e2dfedd7-7bb5-404d-aa53-5d0d374e44c7",
        //       "org": "9f9937dc-8559-4418-ba22-9b9f0a94d456",
        //       "contact_tel": "(604) 109-1623",
        //       "contact_email": "vincent@driller.ca"
        //     },
        //     {
        //       "contact_at_guid": "77ff487a-e931-4568-92da-319a8fb4d547",
        //       "organization_name": "Jasper Drilling Co.",
        //       "person_name": "Bond Bowers",
        //       "person": "5f208637-503d-4562-b4c1-c43ecd6dc623",
        //       "org": "9f9937dc-8559-4418-ba22-9b9f0a94d456",
        //       "contact_tel": "(250) 729-8252",
        //       "contact_email": "white@driller.ca"
        //     },
        //     {
        //       "contact_at_guid": "b4be5a9e-e8a5-4458-865a-b01824fe9c02",
        //       "organization_name": "Jasper Drilling Co.",
        //       "person_name": "Mariana Patton",
        //       "person": "5acc1265-1ae3-448d-8417-edee14f90901",
        //       "org": "9f9937dc-8559-4418-ba22-9b9f0a94d456",
        //       "contact_tel": "(250) 899-4738",
        //       "contact_email": "small@driller.ca"
        //     },
        //     {
        //       "contact_at_guid": "dcc8d473-6d43-4353-9edd-83d87957d3b8",
        //       "organization_name": "Jasper Drilling Co.",
        //       "person_name": "Corine Navarro",
        //       "person": "db0802c8-681e-4c65-8f2b-fd6dd3d2717a",
        //       "org": "9f9937dc-8559-4418-ba22-9b9f0a94d456",
        //       "contact_tel": "(604) 135-2080",
        //       "contact_email": null
        //     }
        //   ]
        // },
        // {
        //   "org_guid": "e4739038-6403-49cd-affb-c2233f612d1d",
        //   "name": "Keeg Installers",
        //   "street_address": "9234 Golden Route",
        //   "city": "Grand Forks",
        //   "province": "BC",
        //   "postal_code": "V5H 7T7",
        //   "main_tel": "(250) 296-6198",
        //   "contacts": [
        //     {
        //       "contact_at_guid": "f560017b-edb9-4f91-8a1d-618f8a4217f6",
        //       "organization_name": "Keeg Installers",
        //       "person_name": "Short Weber",
        //       "person": "3b1e5bfa-d22a-4db4-ae3d-741f855fcfae",
        //       "org": "e4739038-6403-49cd-affb-c2233f612d1d",
        //       "contact_tel": "(778) 719-2302",
        //       "contact_email": "bullock@driller.ca"
        //     }
        //   ]
        // },
        // {
        //   "org_guid": "8f44f1f6-6382-41cc-b609-9093353ac990",
        //   "name": "Lyria Drilling Co.",
        //   "street_address": "734 Red Downs",
        //   "city": "New Hazelton",
        //   "province": "BC",
        //   "postal_code": "V1L 3O9",
        //   "main_tel": "(250) 380-3196",
        //   "contacts": [
        //     {
        //       "contact_at_guid": "ceff5ac3-2af7-45f4-a374-28549cf71656",
        //       "organization_name": "Lyria Drilling Co.",
        //       "person_name": "Blair Willis",
        //       "person": "1264369d-5e1c-433f-bff5-205aab3b50df",
        //       "org": "8f44f1f6-6382-41cc-b609-9093353ac990",
        //       "contact_tel": "(250) 439-7666",
        //       "contact_email": null
        //     }
        //   ]
        // },
        // {
        //   "org_guid": "3b1f3a4c-4d2b-4303-aa15-36c868fe2b47",
        //   "name": "Myopium Drilling Co.",
        //   "street_address": "4381 Sunny Brook Jetty",
        //   "city": "Defot",
        //   "province": "BC",
        //   "postal_code": "V5I 6N1",
        //   "main_tel": "(604) 109-1623",
        //   "contacts": [
        //     {
        //       "contact_at_guid": "b764a373-3554-4664-8be3-5cf245ce685d",
        //       "organization_name": "Myopium Drilling Co.",
        //       "person_name": "Mia Fowler",
        //       "person": "b6bb91e0-8876-4d8b-a7db-20242b535d96",
        //       "org": "3b1f3a4c-4d2b-4303-aa15-36c868fe2b47",
        //       "contact_tel": "(778) 089-3870",
        //       "contact_email": "mccall@driller.ca"
        //     }
        //   ]
        // },
        // {
        //   "org_guid": "3b050022-f672-447c-8d1b-62a8d62af97d",
        //   "name": "Netplode Drilling Co.",
        //   "street_address": "5424 Hazy Common",
        //   "city": "Cassidy\\'s",
        //   "province": "BC",
        //   "postal_code": "V7S 8W0",
        //   "main_tel": "(778) 965-3975",
        //   "contacts": [
        //     {
        //       "contact_at_guid": "3f853093-dd77-4a51-bfed-a7b47079089f",
        //       "organization_name": "Netplode Drilling Co.",
        //       "person_name": "Liz Ross",
        //       "person": "3f92c249-c4e5-48b5-a4f7-e399175839ca",
        //       "org": "3b050022-f672-447c-8d1b-62a8d62af97d",
        //       "contact_tel": "(604) 784-9945",
        //       "contact_email": "serrano@driller.ca"
        //     }
        //   ]
        // },
        // {
        //   "org_guid": "5ab1978d-57e2-434b-a0e8-90f330d88410",
        //   "name": "Norali Drilling Co.",
        //   "street_address": "9266 Blue Pony Road",
        //   "city": "Eholt",
        //   "province": "BC",
        //   "postal_code": "V3Q 9Q2",
        //   "main_tel": "(250) 851-7610",
        //   "contacts": [
        //     {
        //       "contact_at_guid": "5baa8f9f-4e39-435b-800f-5ac4209eaa96",
        //       "organization_name": "Norali Drilling Co.",
        //       "person_name": "Hoffman Chang",
        //       "person": "ca57f52e-0a0c-4ae3-8ef3-73f9c46936b5",
        //       "org": "5ab1978d-57e2-434b-a0e8-90f330d88410",
        //       "contact_tel": "(250) 714-2504",
        //       "contact_email": "harrell@driller.ca"
        //     },
        //     {
        //       "contact_at_guid": "94c9a15a-1cd1-4fb9-8725-89e59ed9db85",
        //       "organization_name": "Norali Drilling Co.",
        //       "person_name": "Johanna Alexander",
        //       "person": "bd30a9e3-01f7-4a39-8756-39db5c1f1f54",
        //       "org": "5ab1978d-57e2-434b-a0e8-90f330d88410",
        //       "contact_tel": "(778) 337-9956",
        //       "contact_email": null
        //     },
        //     {
        //       "contact_at_guid": "e33bc901-4579-4fb5-a2d1-0bd39b3a3a88",
        //       "organization_name": "Norali Drilling Co.",
        //       "person_name": "Janna Cote",
        //       "person": "709bbebc-2e30-4f31-9040-b6f7726168d3",
        //       "org": "5ab1978d-57e2-434b-a0e8-90f330d88410",
        //       "contact_tel": "(250) 046-0449",
        //       "contact_email": null
        //     }
        //   ]
        // }
      ]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
