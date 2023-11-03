import { WELL_TAGS_PRIVATE, WELL_TAGS_PUBLIC } from '../constants.js';

const WELL_TAGS = [...WELL_TAGS_PRIVATE, ...WELL_TAGS_PUBLIC];
/**
 * @desc Given the label parsed from a well filename, returns the longer, more descriptive version
 * @param {string} shortFormLabel Short form of the label used in creation of the well attachment file names
 * @returns Long form version of label applied to file name
 */
const getLongFormLabel = (shortFormLabel) => {
  try {
    return WELL_TAGS.filter((item) => item.value === shortFormLabel)[0].text;
  } catch (ex) {
    return "Unknown"
  }
};

export default getLongFormLabel;
