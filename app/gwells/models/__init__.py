# This is how it should be:
# See: https://docs.djangoproject.com/en/2.0/topics/db/models/#organizing-models-in-a-package
# See: https://www.python.org/dev/peps/pep-0008/#package-and-module-names
# NOTE: Order of import is VERY important. If B depends on A, import A first!
from .audit_model import AuditModel
from .province_state_code import ProvinceStateCode
from .well_class_code import WellClassCode
from .well import Well
# This is all wrong:
from gwells.models.ActivitySubmission import ActivitySubmission
from gwells.models.AquiferWell import AquiferWell
from gwells.models.BCGS_Numbers import BCGS_Numbers
from gwells.models.BedrockMaterialCode import BedrockMaterialCode
from gwells.models.BedrockMaterialDescriptorCode import BedrockMaterialDescriptorCode
from gwells.models.Casing import Casing
from gwells.models.CasingCode import CasingCode
from gwells.models.CasingMaterialCode import CasingMaterialCode
from gwells.models.DecommissionMethodCode import DecommissionMethodCode
from gwells.models.DevelopmentMethodCode import DevelopmentMethodCode
from gwells.models.Driller import Driller
from gwells.models.DrillingCompany import DrillingCompany
from gwells.models.DrillingMethodCode import DrillingMethodCode
from gwells.models.FilterPackMaterialCode import FilterPackMaterialCode
from gwells.models.FilterPackMaterialSizeCode import FilterPackMaterialSizeCode
from gwells.models.GroundElevationMethodCode import GroundElevationMethodCode
from gwells.models.IntendedWaterUseCode import IntendedWaterUseCode
from gwells.models.LandDistrictCode import LandDistrictCode
from gwells.models.LicencedStatusCode import LicencedStatusCode
from gwells.models.LinerMaterialCode import LinerMaterialCode
from gwells.models.LinerPerforation import LinerPerforation
from gwells.models.WellYieldUnitCode import WellYieldUnitCode
# This is ok:
from .lithology import SurficialMaterialCode, LithologyColourCode, LithologyDescription, LithologyDescriptionCode,\
    LithologyHardnessCode, LithologyMaterialCode, LithologyMoistureCode, LithologyStructureCode
# This is all wrong:
from gwells.models.LtsaOwner import LtsaOwner
from gwells.models.ObsWellStatusCode import ObsWellStatusCode
from gwells.models.Perforation import Perforation
from gwells.models.ProductionData import ProductionData
from gwells.models.Profile import Profile
from gwells.models.Screen import Screen
from gwells.models.ScreenAssemblyTypeCode import ScreenAssemblyTypeCode
from gwells.models.ScreenBottomCode import ScreenBottomCode
from gwells.models.ScreenIntakeMethodCode import ScreenIntakeMethodCode
from gwells.models.ScreenMaterialCode import ScreenMaterialCode
from gwells.models.ScreenOpeningCode import ScreenOpeningCode
from gwells.models.ScreenTypeCode import ScreenTypeCode
from gwells.models.SurfaceSealMaterialCode import SurfaceSealMaterialCode
from gwells.models.SurfaceSealMethodCode import SurfaceSealMethodCode
from gwells.models.Survey import Survey
from gwells.models.WaterQualityCharacteristic import WaterQualityCharacteristic
from gwells.models.WellActivityCode import WellActivityCode

from gwells.models.WellStatusCode import WellStatusCode
from gwells.models.WellSubclassCode import WellSubclassCode
from gwells.models.YieldEstimationMethodCode import YieldEstimationMethodCode
from gwells.models.OnlineSurvey import OnlineSurvey
