reduceErrors (data) {
  let clean = Object.entries(JSON.parse(JSON.stringify(data)))
  function walk (r, p) {
    if (Array.isArray(r)) {
      return r.forEach(x => walk(x, combine(x[0], p)))
    } else if (Object.entries(r).length !== 0 && r.constructor === Object) {
      return walk(Object.entries(r), p)
    }
    result.push([p])
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
        if(arr[i])
          }
    })
  }
  let result = []
  walk(clean, [])
  let merged = result.flat()//[...new Set(flatten(result))]
  console.log(merged)
  return result
},
