import formatField from './formatField.js'

// Returns formatted errors for notifications
export default function (data) {
  let clean = Object.entries(JSON.parse(JSON.stringify(data)))
  let result = []
  walk(clean, [], result)
  let merged = result.flat()
  unique(merged)
  return flatten(merged)
}
// Recursive check for all values in multi-dimensional array
function walk (r, p, s) {
  if (Array.isArray(r)) {
    return r.forEach(x => walk(x, combine(x[0], p), s))
  } else if (Object.entries(r).length !== 0 && r.constructor === Object) {
    return walk(Object.entries(r), p, s)
  }
  s.push([p])
}
// Add proper strings to working array
function combine (x, p) {
  if (typeof (x) === 'string' && x.length > 2) {
    return p.concat(x)
  } else {
    return p
  }
}
// Eliminates duplicate arrays
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
// Checks for subset array in superset
function arrayContainsArray (superset, subset) {
  if (subset.length === 0) {
    return false
  }
  return subset.every(function (value) {
    return (superset.indexOf(value) >= 0)
  })
}
// Capitalizes first letter of array values and flattens array
function flatten (arr) {
  let flt = []
  arr.forEach(r => {
    for (var i = 0; i < r.length; i++) {
      r[i] = formatField(r[i])
      r[i] = jsUcfirst(r[i])
    }
  })
  arr.forEach(m => {
    flt.push(m.join(' - '))
  })
  return flt
}
// Capitalizes first letter of a string
function jsUcfirst (string) {
  let formattedString = string.charAt(0).toUpperCase() + string.slice(1)
  formattedString = formattedString.replace(/_/g, ' ')
  return formattedString
}
// Left commented out for future use
// Flattens any dimension array into one single array of values
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
