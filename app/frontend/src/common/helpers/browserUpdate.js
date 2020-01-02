import browserUpdate from 'browser-update'

const config = {
  required: { e: -4, f: -3, o: -3, s: -1, c: -3, i: 11 },
  insecure: true,
  unsupported: true,
  api: 2010.01
}

browserUpdate(config)
