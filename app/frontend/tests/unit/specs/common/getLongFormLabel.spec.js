import { WELL_TAGS_PRIVATE, WELL_TAGS_PUBLIC } from '@/common/constants.js'
import getLongFormLabel from "@/common/helpers/getLongFormLabel";

const WELL_TAGS = [...WELL_TAGS_PUBLIC, ...WELL_TAGS_PRIVATE];

describe('getLongFormLabel.js', () => {
  it('Keys return expected value', () => {
    for (const tag of WELL_TAGS){
      const response = getLongFormLabel(tag.value);
      expect(response).toBe(tag.text);
    }
  })
  
  it('Enter an unknown label', () => {
    const response = getLongFormLabel('Bad value');
    expect(response).toBe('Unknown');
  });
})
