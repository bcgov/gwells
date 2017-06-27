/**
 * This library syncronises the coordinate fields of the fourth Activity Submission fields. The three field groups are Decimal Degrees,
 * Day Minute Second, and UTM. We take the Decimal Degrees fields as the source of truth (i.e., these are the fields which 
 * are stored in the database).
 * If a user enters data into any other field, it is converted here to DD, altering the DD fields, which in turn update the other fields.
 * This module depends on JQuery.
 */
var CoordSync = (function () {

/** JQuery nodes that correspond to the fields that will subscribe to events. */

// The input fields associated with latitude and longitude decimal degrees
_latDDField = null;
_longDDField = null;

// The DMS fields
_latDMSDegreeField = null;
_latDMSMinuteField = null;
_latDMSSecondField = null;
_longDMSDegreeField = null;
_longDMSMinuteField = null;
_longDMSSecondField = null;

// The UTM fields
_zoneUTMField = null;
_eastingUTMField = null;
_northingUTMField = null;

/** Field updates */

// Dispatches changes to DMS and UTM with suitable conversions.
function _latLongDDFieldOnChange () {
    _setDMSFromDD()
    _setUTMFromDD();
}

// Dispatches changes to DD and UTM with suitable conversions.
function _latLongDMSFieldOnChange () {
    _setDDFromDMS();
    _setUTMFromDD();
}

// Dispatches changes to DD and DMS with suitable conversions.
function _utmFieldOnChange () {
    _setDDFromUTM();
    _setDMSFromDD();
}

// Converts DD to DMS and updates the DMS fields.
function _setDMSFromDD () {
    // Get the DD values.
    var newLatDD = _latDDField.val();
    var newLongDD = _longDDField.val();
    
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

    // Set the lat/long DD values with appropriate conversions.
    _latDDField.val(_dmsToDD(latDeg, latMin, latSec));
    _longDDField.val(_dmsToDD(longDeg, longMin, longSec));    
}

// Converts DD to UTM and sets the UTM fields. Originally based on code from the UTM Conversion section.
function _setUTMFromDD () {
    var xy = new Array(2);
    var long = parseFloat(_numOrZeroIfNaN(_longDDField.val()));
    var lat = parseFloat(_numOrZeroIfNaN(_latDDField.val()));

    // Compute the UTM zone.
    zone = Math.floor ((long + 180.0) / 6) + 1;

    // Recompute zone and set the xy array.
    zone = LatLonToUTMXY (DegToRad (lat), DegToRad (long), zone, xy);

    _zoneUTMField.val(zone);
    //_zoneUTMField.select();

    _eastingUTMField.val(xy[0]);
    _northingUTMField.val(xy[1]);
}

// Converts UTM to DD and sets the DD fields. Originally based on code from the UTM Conversion section.
function _setDDFromUTM ()
{                                  
    latlon = new Array(2);
    var x, y, zone, southhemi;
    
    x = parseFloat(_numOrZeroIfNaN(_eastingUTMField.val()));
    y = parseFloat(_numOrZeroIfNaN(_northingUTMField.val()));
    zone = parseFloat(_numOrZeroIfNaN(_zoneUTMField.val()));
    
    // The application is only concerned about the northern hemisphere.
    southhemi = false;

    UTMXYToLatLon (x, y, zone, southhemi, latlon);
    
    _longDDField.val(RadToDeg (latlon[1]));
    _latDDField.val(RadToDeg(latlon[0]));
}


/** DD/DMS Conversion */

// Converts a lat or long from Decimal Degrees to DMS Degrees. The DMS Degree is found by simply truncating the Decimal Degree (i.e., returning its integer part.)
function _ddToDegrees (dec) {
    dec = _numOrZeroIfNaN(dec);
    return parseInt(dec);
}

// Converts a lat or long from Decimal Degrees to DMS Minutes. A DMS Minute is 1/60th of a DMS Degree (which is identical to a DD integer). A DMS Minute is an integer.
function _ddToMinutes (dec) {
    dec = _numOrZeroIfNaN(dec);
    var frac = (Math.abs(dec) * 60) % 60;
    return parseInt(frac);
}

// Converts a lat or long from Decimal Degrees to DMS Seconds. A DMS Second is 1/60th of a DMS Minute. A DMS Second may be a fraction, and should be rounded to two decimals.
function _ddToSeconds (dec) {
    dec = _numOrZeroIfNaN(dec);
    return ((Math.abs(dec) * 3600) % 60).toFixed(2);
}

// Converts a lat or long from DMS to Decimal Degrees.
function _dmsToDD(deg, min, sec) {
    deg = _numOrZeroIfNaN(deg);
    min = _numOrZeroIfNaN(min);
    sec = _numOrZeroIfNaN(sec);
    return deg + (min/60) + (sec/3600);
}

// A convenience function to parse anything to a number (mapping NaN to 0, even the empty string).
function _numOrZeroIfNaN(num) {
    return isNaN(num) || isNaN(parseInt(num)) ? 0 : num;
}

/** UTM conversion code */

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
var sm_EccSquared = 6.69437999013e-03;

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
    var tmp;

    /* Precalculate ep2 */
    ep2 = (Math.pow (sm_a, 2.0) - Math.pow (sm_b, 2.0)) / Math.pow (sm_b, 2.0);

    /* Precalculate nu2 */
    nu2 = ep2 * Math.pow (Math.cos (phi), 2.0);

    /* Precalculate N */
    N = Math.pow (sm_a, 2.0) / (sm_b * Math.sqrt (1 + nu2));

    /* Precalculate t */
    t = Math.tan (phi);
    t2 = t * t;
    tmp = (t2 * t2 * t2) - Math.pow (t, 6.0);

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
    if (southhemi)
    y -= 10000000.0;
            
    y /= UTMScaleFactor;
    
    cmeridian = UTMCentralMeridian (zone);
    MapXYToLatLon (x, y, cmeridian, latlon);
        
    return;
}

/** End of UTM conversion code */

/** Module initialisation.
 * @param options An object with properties conforming to the field node selectors this module requires.
 */
var init = function(options) {
    // Set the nodes
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

    // Subscribe the nodes to the events
    _latDDField.on('change', _latLongDDFieldOnChange);
    _longDDField.on('change', _latLongDDFieldOnChange);
    _latDMSDegreeField.on('change', _latLongDMSFieldOnChange);
    _latDMSMinuteField.on('change', _latLongDMSFieldOnChange);
    _latDMSSecondField.on('change', _latLongDMSFieldOnChange);
    _longDMSDegreeField.on('change', _latLongDMSFieldOnChange);
    _longDMSMinuteField.on('change', _latLongDMSFieldOnChange);
    _longDMSSecondField.on('change', _latLongDMSFieldOnChange);
    _zoneUTMField.on('change', _utmFieldOnChange)
    _eastingUTMField.on('change', _utmFieldOnChange)
    _northingUTMField.on('change', _utmFieldOnChange)
}

return {
    init: init
}
})();