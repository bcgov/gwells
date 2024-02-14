const CANADA_POSTAL_CODE_REGEX = /^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$/;
const US_ZIP_REGEX = /^\d{5}(-\d{4})?$/;

/**
 * This function uses regex to validate a postal code or zip code.
 * @param {String} code - The postal code or zip code to be validated.
 * @returns {Boolean} The result of validating the postal code or zip code.
 */
export function isValidPostalCodeOrZipCode(code) {
    const isZip = US_ZIP_REGEX.test(code);
    const isPostalCode = CANADA_POSTAL_CODE_REGEX.test(code);

    return isPostalCode || isZip;
}
