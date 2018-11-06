import proj4 from 'proj4'
const convertCoordinatesMixin = {
  methods: {
    transformToPositive (value) {
      // Take a value, if it's a number - make it positive. If it's not a number, leave it alone
      return value === '' || isNaN(value) || value === null ? value : Math.abs(value)
    },
    transformToNegative (value) {
      // Take a value, if it's a number - make it negative. If it's not a number, leave it alone.
      return value === '' || isNaN(value) || value === null ? value : Math.abs(value) * -1
    },
    convertToUTM (long, lat) {
      // converts input coordinates and returns an object containing UTM easting, northing, and zone
      const utm = {
        easting: null,
        northing: null,
        zone: null
      }

      if (!!long && !!lat) {
        if (long > 0) {
          // In B.C. everything is negative by convention, so we have to introduct a minus here to make
          // the math work.
          long *= -1
        }
        // determine zone
        const zone = Math.floor((long + 180) / 6) + 1

        // proj4 coordinate system definitions
        const utmProjection = `+proj=utm +zone=${zone} +ellps=GRS80 +datum=NAD83 +units=m +no_defs`
        const coords = proj4(utmProjection, [long, lat])

        utm.easting = coords[0]
        utm.northing = coords[1]
        utm.zone = zone
      }

      return utm
    },
    convertToWGS84 (easting, northing, zone) {
      // converts from UTM to WGS84

      // proj4 coordinate system definitions
      const wgs84Projection = proj4.defs('EPSG:4326')
      const utmProjection = `+proj=utm +zone=${zone} +ellps=${this.ellps} +datum=${this.datum} +units=m +no_defs`

      const coords = proj4(utmProjection, wgs84Projection, [easting, northing])

      return {
        longitude: coords[0],
        latitude: coords[1]
      }
    },
    convertToDMS (degrees) {
      // converts from decimal degrees to degrees, minutes seconds
      // returns an object with keys 'deg', 'min', 'sec'

      const angle = Math.abs(degrees)
      const deg = Math.floor(angle) * Math.sign(degrees)
      const sec = 3600 * (angle - Math.floor(angle)) % 60
      const min = Math.floor((3600 * (angle - Math.floor(angle))) / 60)

      return {
        deg: deg,
        min: min,
        sec: this.roundSeconds(sec)
      }
    },
    convertDMStoDeg (dms) {
      const sign = Math.sign(dms.deg)
      return this.roundDecimalDegrees(dms.deg + sign * dms.min / 60 + sign * dms.sec / (60 * 60))
    },
    roundDecimalDegrees (deg) {
      // Regulations are specific about how GPS coordinates are to be provided.
      // DD to at least 5 decimal places.
      return Math.round(deg * 100000) / 100000
    },
    roundSeconds (seconds) {
      // Regulations are specific about how GPS coordinates are to be provided.
      // DMS toat least 2 decimal places;
      return Math.round(seconds * 100) / 100
    }
  }
}
export default convertCoordinatesMixin
