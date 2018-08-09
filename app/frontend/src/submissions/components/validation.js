
// These constants/codes are for reference only. Actual codes for submission are provided
// by the API at /gwells/api/v1/submissions/options/
//
// Hardcoded references to these codes is discouraged but may be necessary to implement
// some frontend UI-level business logic validation checks. To avoid upstream changes
// or additions to these codes causing issues throughout the codebase, hardcoded
// references should be confined to this file.
//
// activity submission codes
// CON: construction
// ALT: alteration
// DEC: decommision
// LEGACY: a legacy well record
// STAFF_EDIT: staff edited record

// class:subclass codes
// WATR_SUPPLY: DOMESTIC, NON_DOMEST
// MONITOR: PERMANENT, TEMPORARY
// INJECTION: PERMANENT
// GEOTECH: BOREHOLE, SPECIAL, TEST_PIT
// DEWATERING: PERMANENT, TEMPORARY
// RECHARGE
// REMEDIATE: PERMANENT
// CLS_LP_GEO: NA
// DRAINAGE: PERMANENT
//
// intended water use codes:
// COM: commercial/industrial
// IRR: irrigation
// OBS: observation
// OP_LP_GEO: open loop geoexchange
// OTHER
// DOM: private domestic
// TST: test
// UNK: unknown
// DWS: water supply system

export function isIDPlateRequired (wellClass, wellSubclass) {
  return (
    (wellClass === 'WATR_SUPPLY') ||
      (wellClass === 'RECHARGE') ||
      (wellClass === 'INJECTION') ||
      (wellClass === 'DEWATERING' && wellSubclass === 'PERMANENT')
  )
}

export function isIntendedWaterUseRequired (wellClass) {
  return wellClass === 'WATR_SUPPLY'
}
