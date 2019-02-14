
export default function (data) {
  let clean = Object.entries(JSON.parse(JSON.stringify(data)))

  let result = []
  walk(clean, [], result)
  let merged = result.flat()//[...new Set(flatten(result))]
  console.log(merged)

  return result
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

function flatten (arr) {
  const flat = []
  arr.forEach(r => {
    if (Array.isArray(r)) {
      flat.push(...flatten(r))
    } else {
      flat.push(r)
    }
  })
  return flat
}

function unique (arr) {
  const uniq = []
  const p = []
  arr.forEach(r => {
    for (let i = 0; i < arr.length; i++) {
      if(arr[i]){

      }
    }
  })
}
