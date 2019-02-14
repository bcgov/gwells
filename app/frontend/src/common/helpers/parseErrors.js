export default function (data) {
  let clean = Object.entries(JSON.parse(JSON.stringify(data)))
  let result = []
  walk(clean, [], result)
  let merged = result.flat()
  unique(merged)
  return flatten(merged)
}

function walk (r, p, s) {
  if (Array.isArray(r)) {
    return r.forEach(x => walk(x, combine(x[0], p), s))
  } else if (Object.entries(r).length !== 0 && r.constructor === Object) {
    return walk(Object.entries(r), p, s)
  }
  s.push([p])
}

function combine (x, p) {
  if (typeof (x) === 'string' && x.length > 2) {
    return p.concat(x)
  } else {
    return p
  }
}

function unique (arr) {
  arr.forEach(r => {
    arr.forEach(x => {
      if (arrayContainsArray(r, x)) {
        for (var i = 0; i < arr.length - 1; i++) {
          if (arr[i] === x) {
            arr.splice(i, 1)
          }
        }
      }
    })
  })
}

function arrayContainsArray (superset, subset) {
  if (subset.length === 0) {
    return false
  }
  return subset.every(function (value) {
    return (superset.indexOf(value) >= 0)
  })
}

function flatten (arr) {
  let flt = []
  arr.forEach(r => {
    for (var i = 0; i < r.length; i++) {
      r[i] = jsUcfirst(r[i])
    }
  })
  arr.forEach(m => {
    flt.push(m.join(' - '))
  })
  return flt
}

function jsUcfirst (string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

// function flattenDeep (arr) {
//   const flat = []
//   arr.forEach(r => {
//     if (Array.isArray(r)) {
//       flat.push(...flattenDeep(r))
//     } else {
//       flat.push(r)
//     }
//   })
//   return flat
// }
