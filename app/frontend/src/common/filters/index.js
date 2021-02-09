/**
 * truncates any value with a (.00000) decimal to no decimal
 * @param value
 * @returns {number|*}
 */
const excludeZeroDecimals = (value) => {
  return value != null ? Number(value) : value
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
