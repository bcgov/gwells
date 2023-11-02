import { WELL_TAGS_PRIVATE, WELL_TAGS_PUBLIC } from '../constants.js';

const WELL_TAGS = [...WELL_TAGS_PRIVATE, ...WELL_TAGS_PUBLIC];
const getLongFormLabel = (shortFormLabel) => {
  try {
    return WELL_TAGS.filter((item) => item.value === shortFormLabel)[0].text;
  } catch (ex) {
    return "Unknown"
  }
};

export default getLongFormLabel;
