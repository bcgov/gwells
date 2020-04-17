import browserUpdate from 'browser-update'

const config = {
  required: { e: -4, f: -3, o: -3, s: -1, c: -3 },
  insecure: true,
  unsupported: true,
  reminder: 0,
  reminderClosed: 1.1,
  no_permanent_hide: true,
  noclose: true,
  shift_page_down: false,
  api: 2010.01,
  text: '<strong>The Groundwater Wells and Aquifers application will not work correctly on ({brow_name}).</strong><br>We recommend Chrome, Firefox or Safari.<br><a{up_but}>Update browser</a>'
}

browserUpdate(config)
