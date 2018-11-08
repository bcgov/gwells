/*
Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
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
