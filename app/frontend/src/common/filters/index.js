/**
 * truncates any value with a (.00000) decimal to no decimal
 * safe
 * can accept null/undefined/blank string/anything NaN and returns original
 * @param value
 * @returns {number|*}
 */
export const excludeZeroDecimals = (value) => {
  const typesToAllow = ['bigint', 'number', 'string']
  // are we allowed to work with this type? if not just return the original for safety
  if (value == null || !typesToAllow.includes(typeof (value))) {
    return value
  }
  // is this a string, a blank string or a non numeric value? if so return the original for safety
  if (typeof (value) === 'string' && (value.trim() === '' || isNaN(Number(value)))) {
    return value
  }
  return Number(value)
}

export default {
  /**
   * install function(s) as filters
   * @param Vue
   */
  install (Vue) {
    Vue.filter('excludeZeroDecimals', excludeZeroDecimals)
  }
}
