import browserUpdate from 'browser-update'

const config = {
  required: { e: -4, f: -3, o: -3, s: -1, c: -3 },
  insecure: true,
  unsupported: true,
  reminder: 0,
  no_permanent_hide: true,
  api: 2010.01
}

browserUpdate(config)
