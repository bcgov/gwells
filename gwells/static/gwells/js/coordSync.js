/**
 * This library synchronises the geographic coordinate fields of the GWELLS application, specifically for entering the location of a well. 
 * The three field groups are Decimal Degrees, Day Minute Second, and UTM. 
 * We take the Decimal Degrees fields as the source of truth (i.e., these are the fields which are stored in the database).
 * If a user enters data into any other field, it is converted here to DD, altering the DD fields, which in turn update the other fields.
 * The fields undergo basic validation when changed manually by a user entering data in a field. Validation is propagated up to the module's 
 * caller, where it is dealt with appropriately.
 * Programmatic changes to the DD fields are supported, which bypass sending validation success to the caller.
 * This module depends on JQuery.
 */
var CoordSync = (function () {
'use strict';
/** Properties and convenience methods */

// Convenience method to check that a property exists and has a defined value.
function _exists(prop) {
    return prop !== null && prop !== void 0;
}

// Convenience method for turning NaN into zero; generally used for ease of presentation.
function _numOrZeroIfNaN(num) {
    if (isNaN(num)) {
        return 0;
    }
    return num;
}

// The bounding box of the coordinates in DD. If set, then the _latDDField and _longDDField will
// be constrained to within this box, signalling an error if an erroneous value is entered, with
// the caveat that users may enter the longitude without a minus sign (since all longs in BC are negative
// in DD), and coordSync will make the longitude negative in an attempt to improve the accuracy of data entry.
var _latLongDDBoundingBox = null;

// The start of any error message for geographic coordinates.
var _errorPrepend = 'WARNING: Geographic coordinates outside of BC. ';

// The validation callback to invoke from the module's caller.
var _validationErrorCallback = null;

// The callback to invoke on validation success after all fields are settled.
var _validationSuccessCallback = null;

// The precisions of the fields. The values here are defaults, and can be overwritten by the class's caller.
var _latLongDDPrecision = 6;
var _latLongDMSSecondPrecision = 2;
var _utmEastingPrecision = 0;
var _utmNorthingPrecision = 0;

/** JQuery nodes that correspond to the fields that will subscribe to events. */

// The input fields associated with latitude and longitude decimal degrees
var _latDDField = null;
var _longDDField = null;

// The DMS fields
var _latDMSDegreeField = null;
var _latDMSMinuteField = null;
var _latDMSSecondField = null;
var _longDMSDegreeField = null;
var _longDMSMinuteField = null;
var _longDMSSecondField = null;

// The UTM fields
var _zoneUTMField = null;
var _eastingUTMField = null;
var _northingUTMField = null;

/** Field validation */

// Checks to see whether a given latitude is within the bounding box.
function _latIsInBox (lat) {
    if (!isNaN(lat) && _exists(_latLongDDBoundingBox) && _exists(_latLongDDBoundingBox.north) && _exists(_latLongDDBoundingBox.south)) {
        return _latLongDDBoundingBox.south <= lat && lat <= _latLongDDBoundingBox.north;
    }
    return true;
}

// Checks to see whether a given longitude is within the bounding box.
function _longIsInBox (long) {
    if (!isNaN(long) && _exists(_latLongDDBoundingBox) && _exists(_latLongDDBoundingBox.west) && _exists(_latLongDDBoundingBox.east)) {
        return _latLongDDBoundingBox.west <= long && long <= _latLongDDBoundingBox.east;
    }
    return true;
}

// Users can enter positive value for longitude, even though DD values for BC are negative (since BC is west of Greenwich). This function
// ensures longitudes in the _longDDField are below zero. Should be called when DD or DMS fields change.
function _correctPositiveLongDD () {
    var long = parseFloat(_longDDField.val());
    if (isNaN(long)) {
        return;
    }
    long = long < 0 ? long : -long;
    _longDDField.val(long);
}

function _correctPositiveLongDMS () {
    var long = parseFloat(_longDMSDegreeField.val());
    if (isNaN(long)) {
        return;
    }
    long = long < 0 ? long : -long;
    _longDMSDegreeField.val(long);
}

// Enforces the precision on the decimal degree fields upon user change. The other precision methods are similar.
function _correctDDPrecision () {
    var lat = parseFloat(_latDDField.val()).toFixed(_latLongDDPrecision);
    var long = parseFloat(_longDDField.val()).toFixed(_latLongDDPrecision);
    _latDDField.val(isNaN(lat) || lat === 0 ? '' : lat);
    _longDDField.val(isNaN(long) || long === 0 ? '' : long);
}

function _correctDMSSecondPrecision () {
    var latSec = parseFloat(_latDMSSecondField.val()).toFixed(_latLongDMSSecondPrecision);
    var longSec = parseFloat(_longDMSSecondField.val()).toFixed(_latLongDMSSecondPrecision);
    _latDMSSecondField.val(isNaN(latSec) || latSec === 0 ? '' : latSec);
    _longDMSSecondField.val(isNaN(longSec) || longSec === 0 ? '' : longSec);
}

function _correctUTMPrecision () {
    var easting = parseFloat(_eastingUTMField.val()).toFixed(_utmEastingPrecision);
    var northing = parseFloat(_northingUTMField.val()).toFixed(_utmNorthingPrecision);
    _eastingUTMField.val(isNaN(easting) || easting === 0 ? '' : easting);
    _northingUTMField.val(isNaN(northing) || northing === 0 ? '' : northing);
}

// Ensures the latitude and longitude Decimal Degree fields are within the bounding box.
function _areLatLongDDFieldsValid () {
    var errMsg = '';
    // If the callback exists, we check to see if the lat/long is within the box, returning an error if one arises.
    if (_exists(_validationErrorCallback)) {
        var lat = parseFloat(_latDDField.val());
        var long = parseFloat(_longDDField.val());
        var latMsg = '';
        var longMsg = '';
        if (!_latIsInBox(lat)) {
            latMsg = 'Latitude must be between 48.2045556 and 60.0223';
        }
        if (!_longIsInBox(long)) {
            longMsg = 'Longitude must be between -139.0736706 and -114.0338224';
        }
        if (latMsg && longMsg) {
            errMsg = _errorPrepend + latMsg + '. ' + longMsg;
        }
        else if (latMsg || longMsg) {
            errMsg = _errorPrepend + latMsg + longMsg;
        }
        _validationErrorCallback(errMsg);
    }
    return !errMsg;
}

// Validates the DMS fields, to be called only when users change DMS field values manually.
function _areLatLongDMSFieldsValid () {
    var errMsg = '';
    if(_exists(_validationErrorCallback)) {
        var latMsg = '';
        var longMsg = '';

        // Get the DMS values.
        var latDeg = parseFloat(_latDMSDegreeField.val());
        var latMin = parseFloat(_latDMSMinuteField.val());
        var latSec = parseFloat(_latDMSSecondField.val());
        var longDeg = parseFloat(_longDMSDegreeField.val());
        var longMin = parseFloat(_longDMSMinuteField.val());
        var longSec = parseFloat(_longDMSSecondField.val());

        // Convert to lat/long DD and check if the DDs are in the bounding box.
        var lat = _dmsToDD(latDeg, latMin, latSec);
        var long = _dmsToDD(longDeg, longMin, longSec);
        if (!_latIsInBox(lat)) {
            latDeg = _numOrZeroIfNaN(latDeg);
            latMin = _numOrZeroIfNaN(latMin);
            latSec = _numOrZeroIfNaN(latSec);
            latMsg = 'Invalid latitude: ' + latDeg + "'" + latMin + "''" + latSec;
        }
        // Since users can enter positive longitude in the DMS field, we must validate the negation if the first run fails.
        if (!_longIsInBox(long)) {
            longDeg = _numOrZeroIfNaN(longDeg);
            longMin = _numOrZeroIfNaN(longMin);
            longSec = _numOrZeroIfNaN(longSec);
            longMsg = 'Invalid longitude: ' + longDeg + "'" + longMin + "''" + longSec;
        }

        // If either (or both) are out of the box, prepend errMsg with the global prepend and append appropriately.
        if (latMsg && longMsg) {
            errMsg = _errorPrepend + latMsg + '. ' + longMsg;
        }
        else if (latMsg || longMsg) {
            errMsg = _errorPrepend + latMsg + longMsg;
        }

        // Propagate the error message to the caller (where an empty message implies no error).
        _validationErrorCallback(errMsg);
    }
    return !errMsg;
}

// Validates UTM fields, to be called only when users change UTM fields manually.
function _areUTMFieldsValid () {
    var errMsg = '';
    if(_exists(_validationErrorCallback)) {
        var coordMsg = 'UTM coordinates (Easting/Northing) are invalid for BC.';
        var zoneMsg = 'UTM zone must be selected from list.';

        // Check the zone first, and only validate easting and northing if the zone has been selected.
        var zone = parseInt(_zoneUTMField.val());
        if (_exists(zone) && !isNaN(zone)) {
            var hasError = false;
            var easting = parseFloat(_eastingUTMField.val());
            var northing = parseFloat(_northingUTMField.val());

            // Convert to lat/long DD via the supplied algorithm, and then check whether the point is in the bounding box.
            var latLong = _utmToDD({zone: zone, easting: easting, northing: northing});
            var lat = latLong.lat;
            var long = latLong.long;            
            if (!_latIsInBox(lat)) {
                hasError = true;
            }
            if (!_longIsInBox(long)) {
                hasError = true;
            }

            // If either or both fields are invalid, prepend errMsg with the global prepend and append appropriately.
            if (hasError) {
                errMsg = _errorPrepend + coordMsg;
            }
        } else { // If no zone was selected, return zoneMsg to the caller.
            errMsg = zoneMsg;
        }
        _validationErrorCallback(errMsg);
    }
    return !errMsg;
}

/** Field updates */

// Dispatches changes to DMS and UTM with suitable conversions and validation.
// Since the lat/long DD fields are the 'anchor' fields, they can be programmatically changed.
// In that case, we prevent the validationSuccessCallback from firing, as that callback is
// only for user-entered data changes in the input fields.
function _latLongDDFieldOnChange (programmaticallyChanged) {
    // If a user enters DD directly, we accept positive longitudes, but correct them on the fly.
    _correctPositiveLongDD();
    if (_areLatLongDDFieldsValid()) {
        _correctDDPrecision();
        _setDMSFromDD();
        _setUTMFromDD();
        if (!programmaticallyChanged) {
            _validationSuccessCallback();
        }
    } else {
        _clearDMSFields();
        _clearUTMFields();
    }
}

// Dispatches changes to DD and UTM with suitable conversions and validation.
function _latLongDMSFieldOnChange () {
    _correctPositiveLongDMS();
    if(_areLatLongDMSFieldsValid()) {
        _correctDMSSecondPrecision();
        _setDDFromDMS();
        _setUTMFromDD();
        _validationSuccessCallback();
    } else {
        _clearDDFields();
        _clearUTMFields();
    }
}

// Dispatches changes to DD and DMS with suitable conversions and validation.
function _utmFieldOnChange () {
    if(_areUTMFieldsValid()) {
        _correctUTMPrecision();
        _setDDFromUTM();
        _setDMSFromDD();
        _validationSuccessCallback();
    } else {
        _clearDDFields();
        _clearDMSFields();
    }
}

function _clearDDFields () {
    _latDDField.val('');
    _longDDField.val('');
}

function _clearDMSFields () {
    _latDMSDegreeField.val('');
    _latDMSMinuteField.val('');
    _latDMSSecondField.val('');
    _longDMSDegreeField.val('');
    _longDMSMinuteField.val('');
    _longDMSSecondField.val('');
}

function _clearUTMFields () {
    _zoneUTMField.val('');
    _eastingUTMField.val('');
    _northingUTMField.val('');
}

// Converts DD to DMS and updates the DMS fields.
function _setDMSFromDD () {
    // Get the DD values.
    var newLatDD = parseFloat(_latDDField.val());
    var newLongDD = parseFloat(_longDDField.val());
    // Set the lat/long DMS values with appropriate conversions.
    _latDMSDegreeField.val(_ddToDegrees(newLatDD));
    _latDMSMinuteField.val(_ddToMinutes(newLatDD));
    _latDMSSecondField.val(_ddToSeconds(newLatDD));
    _longDMSDegreeField.val(_ddToDegrees(newLongDD));
    _longDMSMinuteField.val(_ddToMinutes(newLongDD));
    _longDMSSecondField.val(_ddToSeconds(newLongDD));
}

// Converts DMS to DD and updates the DD fields.
function _setDDFromDMS () {
    // Get the DMS values.
    var latDeg = parseFloat(_latDMSDegreeField.val());
    var latMin = parseFloat(_latDMSMinuteField.val());
    var latSec = parseFloat(_latDMSSecondField.val());
    var longDeg = parseFloat(_longDMSDegreeField.val());
    var longMin = parseFloat(_longDMSMinuteField.val());
    var longSec = parseFloat(_longDMSSecondField.val());

    // Set the lat/long DD values with appropriate conversions. Note that we negate the
    // longitude because the algorithm works with positive values only.
    var lat = _dmsToDD(latDeg, latMin, latSec);
    var long = _dmsToDD(longDeg, longMin, longSec);
    _latDDField.val(isNaN(lat) ? '' : lat);
    _longDDField.val(isNaN(long) ? '' : long);
}

// Converts DD to UTM and sets the UTM fields. Originally based on code from the UTM Conversion section.
function _setUTMFromDD () {
    var lat = parseFloat(_latDDField.val());
    var long = parseFloat(_longDDField.val());

    // If either field is NaN, bail out.
    if (isNaN(lat) || isNaN(long)) {
        return;
    }
    var utmObj = _ddToUTM(lat, long);
    if (_exists(utmObj.zone) && _exists(utmObj.easting) && _exists(utmObj.northing)) {
        _zoneUTMField.val(utmObj.zone);
        _eastingUTMField.val(utmObj.easting);
        _northingUTMField.val(utmObj.northing);
    }
}

// Converts UTM to DD and sets the DD fields. Originally based on code from the UTM Conversion section.
function _setDDFromUTM ()
{                                      
    var easting = parseFloat(_eastingUTMField.val());
    var northing = parseFloat(_northingUTMField.val());
    var zone = parseFloat(_zoneUTMField.val());

    // If any field is inappropriate, bail out
    if (isNaN(easting) || isNaN(northing) || isNaN(zone)) {
        return;
    }

    var latLong = _utmToDD({zone: zone, easting: easting, northing: northing});
    if (_exists(latLong.lat) && _exists(latLong.long)) {
        _longDDField.val(latLong.long);
        _latDDField.val(latLong.lat);
    }
}

/** DD/DMS Conversion */

// Converts a lat or long from Decimal Degrees to DMS Degrees. The DMS Degree is found by simply truncating the Decimal Degree (i.e., returning its integer part.)
function _ddToDegrees (dec) {
    if (isNaN(dec)) {
        return '';
    }
    return parseInt(dec);
}

// Converts a lat or long from Decimal Degrees to DMS Minutes. A DMS Minute is 1/60th of a DMS Degree (which is identical to a DD integer). A DMS Minute is an integer.
function _ddToMinutes (dec) {
    if (isNaN(dec)) {
        return '';
    }
    var frac = (Math.abs(dec) * 60) % 60;
    return parseInt(frac);
}

// Converts a lat or long from Decimal Degrees to DMS Seconds. A DMS Second is 1/60th of a DMS Minute. A DMS Second may be a fraction, and should be rounded to two decimals.
function _ddToSeconds (dec) {
    if (isNaN(dec)) {
        return '';
    }
    return ((Math.abs(dec) * 3600) % 60).toFixed(_latLongDMSSecondPrecision);
}

// Converts a lat or long from DMS to Decimal Degrees.
function _dmsToDD(deg, min, sec) {
    if (isNaN(deg) || isNaN (min) || isNaN(sec)) {
        return NaN;
    }
    // The algorithm works on absolute values, so we preserve the sign of the degree, abs it,
    // and return the signed coordinate after conversion.
    var sign = deg >= 0 ? 1 : -1;
    deg = Math.abs(deg);
    var coord = (deg + (min/60) + (sec/3600)).toFixed(_latLongDDPrecision);
    return sign * coord;
}

/** UTM conversion code */

function _ddToUTM(lat, long) {
    var xy = [];
    // Compute the UTM zone.
    var zone = Math.floor ((long + 180.0) / 6) + 1;

    // Recompute zone and set the xy array.
    zone = LatLonToUTMXY (DegToRad (lat), DegToRad (long), zone, xy);
    var easting = xy[0].toFixed(_utmEastingPrecision);
    var northing = xy[1].toFixed(_utmNorthingPrecision);
    return {zone: zone, easting: easting, northing: northing};
}

function _utmToDD(utmObj) {
    var latlon = [];
    var easting = utmObj.easting;
    var northing = utmObj.northing;
    var zone = utmObj.zone;
    // The application is only concerned about the northern hemisphere.
    var southhemi = false;
    UTMXYToLatLon (easting, northing, zone, southhemi, latlon);
    // We are only concerned with six decimal places of precision.
    var long = RadToDeg(latlon[1]).toFixed(_latLongDDPrecision);
    var lat = RadToDeg(latlon[0]).toFixed(_latLongDDPrecision);
    return {lat: lat, long: long};
}

/**
 * The code below is (only very slightly) adapted from http://home.hiwaay.net/~taylorc/toolbox/geography/geoutm.html, which as of this writing is released by implicit license
 * under the verbiage "The JavaScript source code in this document may be copied and reused without restriction".
 * NOTE: This code was written with WGS84 in mind, while BC uses NAD83 according to http://www.empr.gov.bc.ca/Mining/Geoscience/MapPlace/OnlineHelpDocuments/Pages/faq.aspx#7.
 * For our purposes, these can be regarded as identical, since the difference in the polar radius between them is finer than the precision of the algorithm.
 */

var pi = Math.PI;

/* Ellipsoid model constants (actual values here are for WGS84) */
var sm_a = 6378137.0;
var sm_b = 6356752.314;

var UTMScaleFactor = 0.9996;


/*
* DegToRad
*
* Converts degrees to radians.
*
*/
function DegToRad (deg)
{
    return (deg / 180.0 * pi)
}




/*
* RadToDeg
*
* Converts radians to degrees.
*
*/
function RadToDeg (rad)
{
    return (rad / pi * 180.0)
}




/*
* ArcLengthOfMeridian
*
* Computes the ellipsoidal distance from the equator to a point at a
* given latitude.
*
* Reference: Hoffmann-Wellenhof, B., Lichtenegger, H., and Collins, J.,
* GPS: Theory and Practice, 3rd ed.  New York: Springer-Verlag Wien, 1994.
*
* Inputs:
*     phi - Latitude of the point, in radians.
*
* Globals:
*     sm_a - Ellipsoid model major axis.
*     sm_b - Ellipsoid model minor axis.
*
* Returns:
*     The ellipsoidal distance of the point from the equator, in meters.
*
*/
function ArcLengthOfMeridian (phi)
{
    var alpha, beta, gamma, delta, epsilon, n;
    var result;

    /* Precalculate n */
    n = (sm_a - sm_b) / (sm_a + sm_b);

    /* Precalculate alpha */
    alpha = ((sm_a + sm_b) / 2.0)
        * (1.0 + (Math.pow (n, 2.0) / 4.0) + (Math.pow (n, 4.0) / 64.0));

    /* Precalculate beta */
    beta = (-3.0 * n / 2.0) + (9.0 * Math.pow (n, 3.0) / 16.0)
        + (-3.0 * Math.pow (n, 5.0) / 32.0);

    /* Precalculate gamma */
    gamma = (15.0 * Math.pow (n, 2.0) / 16.0)
        + (-15.0 * Math.pow (n, 4.0) / 32.0);

    /* Precalculate delta */
    delta = (-35.0 * Math.pow (n, 3.0) / 48.0)
        + (105.0 * Math.pow (n, 5.0) / 256.0);

    /* Precalculate epsilon */
    epsilon = (315.0 * Math.pow (n, 4.0) / 512.0);

/* Now calculate the sum of the series and return */
result = alpha
    * (phi + (beta * Math.sin (2.0 * phi))
        + (gamma * Math.sin (4.0 * phi))
        + (delta * Math.sin (6.0 * phi))
        + (epsilon * Math.sin (8.0 * phi)));

return result;
}



/*
* UTMCentralMeridian
*
* Determines the central meridian for the given UTM zone.
*
* Inputs:
*     zone - An integer value designating the UTM zone, range [1,60].
*
* Returns:
*   The central meridian for the given UTM zone, in radians, or zero
*   if the UTM zone parameter is outside the range [1,60].
*   Range of the central meridian is the radian equivalent of [-177,+177].
*
*/
function UTMCentralMeridian (zone)
{
    var cmeridian;

    cmeridian = DegToRad (-183.0 + (zone * 6.0));

    return cmeridian;
}



/*
* FootpointLatitude
*
* Computes the footpoint latitude for use in converting transverse
* Mercator coordinates to ellipsoidal coordinates.
*
* Reference: Hoffmann-Wellenhof, B., Lichtenegger, H., and Collins, J.,
*   GPS: Theory and Practice, 3rd ed.  New York: Springer-Verlag Wien, 1994.
*
* Inputs:
*   y - The UTM northing coordinate, in meters.
*
* Returns:
*   The footpoint latitude, in radians.
*
*/
function FootpointLatitude (y)
{
    var y_, alpha_, beta_, gamma_, delta_, epsilon_, n;
    var result;
    
    /* Precalculate n (Eq. 10.18) */
    n = (sm_a - sm_b) / (sm_a + sm_b);
        
    /* Precalculate alpha_ (Eq. 10.22) */
    /* (Same as alpha in Eq. 10.17) */
    alpha_ = ((sm_a + sm_b) / 2.0)
        * (1 + (Math.pow (n, 2.0) / 4) + (Math.pow (n, 4.0) / 64));
    
    /* Precalculate y_ (Eq. 10.23) */
    y_ = y / alpha_;
    
    /* Precalculate beta_ (Eq. 10.22) */
    beta_ = (3.0 * n / 2.0) + (-27.0 * Math.pow (n, 3.0) / 32.0)
        + (269.0 * Math.pow (n, 5.0) / 512.0);
    
    /* Precalculate gamma_ (Eq. 10.22) */
    gamma_ = (21.0 * Math.pow (n, 2.0) / 16.0)
        + (-55.0 * Math.pow (n, 4.0) / 32.0);
        
    /* Precalculate delta_ (Eq. 10.22) */
    delta_ = (151.0 * Math.pow (n, 3.0) / 96.0)
        + (-417.0 * Math.pow (n, 5.0) / 128.0);
        
    /* Precalculate epsilon_ (Eq. 10.22) */
    epsilon_ = (1097.0 * Math.pow (n, 4.0) / 512.0);
        
    /* Now calculate the sum of the series (Eq. 10.21) */
    result = y_ + (beta_ * Math.sin (2.0 * y_))
        + (gamma_ * Math.sin (4.0 * y_))
        + (delta_ * Math.sin (6.0 * y_))
        + (epsilon_ * Math.sin (8.0 * y_));
    
    return result;
}



/*
* MapLatLonToXY
*
* Converts a latitude/longitude pair to x and y coordinates in the
* Transverse Mercator projection.  Note that Transverse Mercator is not
* the same as UTM; a scale factor is required to convert between them.
*
* Reference: Hoffmann-Wellenhof, B., Lichtenegger, H., and Collins, J.,
* GPS: Theory and Practice, 3rd ed.  New York: Springer-Verlag Wien, 1994.
*
* Inputs:
*    phi - Latitude of the point, in radians.
*    lambda - Longitude of the point, in radians.
*    lambda0 - Longitude of the central meridian to be used, in radians.
*
* Outputs:
*    xy - A 2-element array containing the x and y coordinates
*         of the computed point.
*
* Returns:
*    The function does not return a value.
*
*/
function MapLatLonToXY (phi, lambda, lambda0, xy)
{
    var N, nu2, ep2, t, t2, l;
    var l3coef, l4coef, l5coef, l6coef, l7coef, l8coef;

    /* Precalculate ep2 */
    ep2 = (Math.pow (sm_a, 2.0) - Math.pow (sm_b, 2.0)) / Math.pow (sm_b, 2.0);

    /* Precalculate nu2 */
    nu2 = ep2 * Math.pow (Math.cos (phi), 2.0);

    /* Precalculate N */
    N = Math.pow (sm_a, 2.0) / (sm_b * Math.sqrt (1 + nu2));

    /* Precalculate t */
    t = Math.tan (phi);
    t2 = t * t;

    /* Precalculate l */
    l = lambda - lambda0;

    /* Precalculate coefficients for l**n in the equations below
        so a normal human being can read the expressions for easting
        and northing
        -- l**1 and l**2 have coefficients of 1.0 */
    l3coef = 1.0 - t2 + nu2;

    l4coef = 5.0 - t2 + 9 * nu2 + 4.0 * (nu2 * nu2);

    l5coef = 5.0 - 18.0 * t2 + (t2 * t2) + 14.0 * nu2
        - 58.0 * t2 * nu2;

    l6coef = 61.0 - 58.0 * t2 + (t2 * t2) + 270.0 * nu2
        - 330.0 * t2 * nu2;

    l7coef = 61.0 - 479.0 * t2 + 179.0 * (t2 * t2) - (t2 * t2 * t2);

    l8coef = 1385.0 - 3111.0 * t2 + 543.0 * (t2 * t2) - (t2 * t2 * t2);

    /* Calculate easting (x) */
    xy[0] = N * Math.cos (phi) * l
        + (N / 6.0 * Math.pow (Math.cos (phi), 3.0) * l3coef * Math.pow (l, 3.0))
        + (N / 120.0 * Math.pow (Math.cos (phi), 5.0) * l5coef * Math.pow (l, 5.0))
        + (N / 5040.0 * Math.pow (Math.cos (phi), 7.0) * l7coef * Math.pow (l, 7.0));

    /* Calculate northing (y) */
    xy[1] = ArcLengthOfMeridian (phi)
        + (t / 2.0 * N * Math.pow (Math.cos (phi), 2.0) * Math.pow (l, 2.0))
        + (t / 24.0 * N * Math.pow (Math.cos (phi), 4.0) * l4coef * Math.pow (l, 4.0))
        + (t / 720.0 * N * Math.pow (Math.cos (phi), 6.0) * l6coef * Math.pow (l, 6.0))
        + (t / 40320.0 * N * Math.pow (Math.cos (phi), 8.0) * l8coef * Math.pow (l, 8.0));

    return;
}



/*
* MapXYToLatLon
*
* Converts x and y coordinates in the Transverse Mercator projection to
* a latitude/longitude pair.  Note that Transverse Mercator is not
* the same as UTM; a scale factor is required to convert between them.
*
* Reference: Hoffmann-Wellenhof, B., Lichtenegger, H., and Collins, J.,
*   GPS: Theory and Practice, 3rd ed.  New York: Springer-Verlag Wien, 1994.
*
* Inputs:
*   x - The easting of the point, in meters.
*   y - The northing of the point, in meters.
*   lambda0 - Longitude of the central meridian to be used, in radians.
*
* Outputs:
*   philambda - A 2-element containing the latitude and longitude
*               in radians.
*
* Returns:
*   The function does not return a value.
*
* Remarks:
*   The local variables Nf, nuf2, tf, and tf2 serve the same purpose as
*   N, nu2, t, and t2 in MapLatLonToXY, but they are computed with respect
*   to the footpoint latitude phif.
*
*   x1frac, x2frac, x2poly, x3poly, etc. are to enhance readability and
*   to optimize computations.
*
*/
function MapXYToLatLon (x, y, lambda0, philambda)
{
    var phif, Nf, Nfpow, nuf2, ep2, tf, tf2, tf4, cf;
    var x1frac, x2frac, x3frac, x4frac, x5frac, x6frac, x7frac, x8frac;
    var x2poly, x3poly, x4poly, x5poly, x6poly, x7poly, x8poly;
    
    /* Get the value of phif, the footpoint latitude. */
    phif = FootpointLatitude (y);
        
    /* Precalculate ep2 */
    ep2 = (Math.pow (sm_a, 2.0) - Math.pow (sm_b, 2.0))
            / Math.pow (sm_b, 2.0);
        
    /* Precalculate cos (phif) */
    cf = Math.cos (phif);
        
    /* Precalculate nuf2 */
    nuf2 = ep2 * Math.pow (cf, 2.0);
        
    /* Precalculate Nf and initialize Nfpow */
    Nf = Math.pow (sm_a, 2.0) / (sm_b * Math.sqrt (1 + nuf2));
    Nfpow = Nf;
        
    /* Precalculate tf */
    tf = Math.tan (phif);
    tf2 = tf * tf;
    tf4 = tf2 * tf2;
    
    /* Precalculate fractional coefficients for x**n in the equations
        below to simplify the expressions for latitude and longitude. */
    x1frac = 1.0 / (Nfpow * cf);
    
    Nfpow *= Nf;   /* now equals Nf**2) */
    x2frac = tf / (2.0 * Nfpow);
    
    Nfpow *= Nf;   /* now equals Nf**3) */
    x3frac = 1.0 / (6.0 * Nfpow * cf);
    
    Nfpow *= Nf;   /* now equals Nf**4) */
    x4frac = tf / (24.0 * Nfpow);
    
    Nfpow *= Nf;   /* now equals Nf**5) */
    x5frac = 1.0 / (120.0 * Nfpow * cf);
    
    Nfpow *= Nf;   /* now equals Nf**6) */
    x6frac = tf / (720.0 * Nfpow);
    
    Nfpow *= Nf;   /* now equals Nf**7) */
    x7frac = 1.0 / (5040.0 * Nfpow * cf);
    
    Nfpow *= Nf;   /* now equals Nf**8) */
    x8frac = tf / (40320.0 * Nfpow);
    
    /* Precalculate polynomial coefficients for x**n.
        -- x**1 does not have a polynomial coefficient. */
    x2poly = -1.0 - nuf2;
    
    x3poly = -1.0 - 2 * tf2 - nuf2;
    
    x4poly = 5.0 + 3.0 * tf2 + 6.0 * nuf2 - 6.0 * tf2 * nuf2
        - 3.0 * (nuf2 *nuf2) - 9.0 * tf2 * (nuf2 * nuf2);
    
    x5poly = 5.0 + 28.0 * tf2 + 24.0 * tf4 + 6.0 * nuf2 + 8.0 * tf2 * nuf2;
    
    x6poly = -61.0 - 90.0 * tf2 - 45.0 * tf4 - 107.0 * nuf2
        + 162.0 * tf2 * nuf2;
    
    x7poly = -61.0 - 662.0 * tf2 - 1320.0 * tf4 - 720.0 * (tf4 * tf2);
    
    x8poly = 1385.0 + 3633.0 * tf2 + 4095.0 * tf4 + 1575 * (tf4 * tf2);
        
    /* Calculate latitude */
    philambda[0] = phif + x2frac * x2poly * (x * x)
        + x4frac * x4poly * Math.pow (x, 4.0)
        + x6frac * x6poly * Math.pow (x, 6.0)
        + x8frac * x8poly * Math.pow (x, 8.0);
        
    /* Calculate longitude */
    philambda[1] = lambda0 + x1frac * x
        + x3frac * x3poly * Math.pow (x, 3.0)
        + x5frac * x5poly * Math.pow (x, 5.0)
        + x7frac * x7poly * Math.pow (x, 7.0);
        
    return;
}




/*
* LatLonToUTMXY
*
* Converts a latitude/longitude pair to x and y coordinates in the
* Universal Transverse Mercator projection.
*
* Inputs:
*   lat - Latitude of the point, in radians.
*   lon - Longitude of the point, in radians.
*   zone - UTM zone to be used for calculating values for x and y.
*          If zone is less than 1 or greater than 60, the routine
*          will determine the appropriate zone from the value of lon.
*
* Outputs:
*   xy - A 2-element array where the UTM x and y values will be stored.
*
* Returns:
*   The UTM zone used for calculating the values of x and y.
*
*/
function LatLonToUTMXY (lat, lon, zone, xy)
{
    MapLatLonToXY (lat, lon, UTMCentralMeridian (zone), xy);

    /* Adjust easting and northing for UTM system. */
    xy[0] = xy[0] * UTMScaleFactor + 500000.0;
    xy[1] = xy[1] * UTMScaleFactor;
    if (xy[1] < 0.0)
        xy[1] = xy[1] + 10000000.0;

    return zone;
}



/*
* UTMXYToLatLon
*
* Converts x and y coordinates in the Universal Transverse Mercator
* projection to a latitude/longitude pair.
*
* Inputs:
*	x - The easting of the point, in meters.
*	y - The northing of the point, in meters.
*	zone - The UTM zone in which the point lies.
*	southhemi - True if the point is in the southern hemisphere;
*               false otherwise.
*
* Outputs:
*	latlon - A 2-element array containing the latitude and
*            longitude of the point, in radians.
*
* Returns:
*	The function does not return a value.
*
*/
function UTMXYToLatLon (x, y, zone, southhemi, latlon)
{
    var cmeridian;
        
    x -= 500000.0;
    x /= UTMScaleFactor;
        
    /* If in southern hemisphere, adjust y accordingly. */
    if (southhemi){
        y -= 10000000.0;
    }
            
    y /= UTMScaleFactor;
    
    cmeridian = UTMCentralMeridian (zone);
    MapXYToLatLon (x, y, cmeridian, latlon);
        
    return;
}

/** End of UTM conversion code */

/** Constructor functions. The private helpers take the same object as the init() method. */

function _setFieldNodes (options) {
    _latDDField = $(options.latDDNodeSelector) || null;
    _longDDField = $(options.longDDNodeSelector) || null;
    _latDMSDegreeField = $(options.latDMSDegreeNodeSelector) || null;
    _latDMSMinuteField = $(options.latDMSMinuteNodeSelector) || null;
    _latDMSSecondField = $(options.latDMSSecondNodeSelector) || null;
    _longDMSDegreeField = $(options.longDMSDegreeNodeSelector) || null;
    _longDMSMinuteField = $(options.longDMSMinuteNodeSelector) || null;
    _longDMSSecondField = $(options.longDMSSecondNodeSelector) || null;
    _zoneUTMField = $(options.zoneUTMNodeSelector) || null;
    _eastingUTMField = $(options.eastingUTMNodeSelector) || null;
    _northingUTMField = $(options.northingUTMNodeSelector) || null;
}

function _setValidationObjects (options) {
    _latLongDDBoundingBox = options.latLongDDBoundingBox || null;
    _validationErrorCallback = options.validationErrorCallback || null;
    _validationSuccessCallback = options.validationSuccessCallback || null;    
}

function _setFieldPrecisions (options) {
    _latLongDDPrecision = options.latLongDDPrecision;
    _latLongDMSSecondPrecision = options.latLongDMSSecondPrecision;
    _utmEastingPrecision = options.utmEastingPrecision;
    _utmNorthingPrecision = options.utmNorthingPrecision;
}

function _subscribeFieldsToChangeEvents (options) {
    // Subscribe the lat/long nodes to the progChangeEvent
    _latDDField.on(options.progChangeEvent, function () { _latLongDDFieldOnChange(true); });
    _longDDField.on(options.progChangeEvent, function () { _latLongDDFieldOnChange(true); });

    // Subscribe the nodes to the change event.
    _latDDField.on('change', function () { _latLongDDFieldOnChange(false); });
    _longDDField.on('change', function () { _latLongDDFieldOnChange(false); });
    _latDMSDegreeField.on('change', _latLongDMSFieldOnChange);
    _latDMSMinuteField.on('change', _latLongDMSFieldOnChange);
    _latDMSSecondField.on('change', _latLongDMSFieldOnChange);
    _longDMSDegreeField.on('change', _latLongDMSFieldOnChange);
    _longDMSMinuteField.on('change', _latLongDMSFieldOnChange);
    _longDMSSecondField.on('change', _latLongDMSFieldOnChange);
    _zoneUTMField.on('change', _utmFieldOnChange);
    _eastingUTMField.on('change', _utmFieldOnChange);
    _northingUTMField.on('change',_utmFieldOnChange);    
}
/** Module initialisation.
 * @param options An object with properties conforming to: 
 * {
 *    progChangeEvent: string, // The name of the event whereby the coordinates are programmatically changed (e.g., by the map on pushpin move)
 *    // Each nodeSelector is a JQuery selector string; e.g., '#nodeId'.
 *    latDDNodeSelector: string, 
 *    longDDNodeSelector: string,
 *    latDMSDegreeNodeSelector: string, 
 *    latDMSMinuteNodeSelector: string,
 *    latDMSSecondNodeSelector: string,
 *    longDMSDegreeNodeSelector: string,
 *    longDMSMinuteNodeSelector: string,
 *    longDMSSecondNodeSelector: string,
 *    zoneUTMNodeSelector: string,
 *    eastingUTMNodeSelector: string,
 *    northingUTMNodeSelector: string,
 *    latLongDDBoundingBox: { // The bounds of valid latitude and longitude
 *          north: float,
 *          south: float,
 *          east: float,
 *          west: float
 *      },
 *    // The precision of the coordinates
 *    latLongDDPrecision: int,
 *    latLongDMSSecondPrecision: int,
 *    utmEastingPrecision: int,
 *    utmNorthingPrecision: int,
 *    validationErrorCallback: function, // Callback for validation errors
 *    validationSuccessCallback: function // Callback to invoke on validation success once all fields are synchronised.
 *  }
 */
var init = function(options) {
    _setFieldNodes(options);
    _setValidationObjects(options);
    _setFieldPrecisions(options);
    _subscribeFieldsToChangeEvents(options);
}

return {
    init: init
}
})();
