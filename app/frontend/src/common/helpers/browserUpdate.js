import browserUpdate from 'browser-update'

const config = {
  required: { e: -4, f: -3, o: -3, s: -1, c: -3 },
  insecure: true,
  unsupported: true,
  reminder: 0,
  reminderClosed: 0,
  no_permanent_hide: true,
  api: 2010.01,
  text: '{brow_name} is not supported by the Groundwater Wells and Aquifers application. We recommend using: Chrome, Firefox or Safari.<br><a{up_but}>Read more</a> or <a{ignore_but}>ignore</a>'
}

browserUpdate(config)
