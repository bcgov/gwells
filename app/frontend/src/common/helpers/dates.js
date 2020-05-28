export const END_OF_TIME_ISO_8601 = '9999-12-31 23:59:59.999999+00'
export const END_OF_TIME = new Date(END_OF_TIME_ISO_8601)

export function dateAtEndOfTime (isoDateString) {
  return new Date(isoDateString) >= END_OF_TIME
}
