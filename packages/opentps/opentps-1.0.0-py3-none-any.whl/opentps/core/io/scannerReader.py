import glob
import os

from opentps.core.data.CTCalibrations.MCsquareCalibration._mcsquareCTCalibration import MCsquareCTCalibration
from opentps.core.data.CTCalibrations.RayStationCalibration._rayStationCTCalibration import RayStationCTCalibration
from opentps.core.data.CTCalibrations._abstractCTCalibration import AbstractCTCalibration


def readScanner(scannerFolder) -> AbstractCTCalibration:
    if os.path.isfile(os.path.join(scannerFolder, 'HU_Density_Conversion.txt')):
        try:

            return MCsquareCTCalibration(fromFiles=(os.path.join(scannerFolder, 'HU_Density_Conversion.txt'),
                                                    os.path.join(scannerFolder, 'HU_Material_Conversion.txt'),
                                                       'default'))
        except Exception as e:
            raise ('Could not import MCsquare CT calibration from provided files') from e

    try:
        materialsFile = glob.glob(os.path.join(scannerFolder, 'material*.*'))[0]
        conversionFile = glob.glob(os.path.join(scannerFolder, 'calibration*.*'))
        conversionFile += (glob.glob(os.path.join(scannerFolder, 'Density*.*')))
        conversionFile  = conversionFile[0]

        return RayStationCTCalibration(fromFiles=(conversionFile,
                                                  materialsFile))
    except Exception as e:
        raise ValueError(str(scannerFolder) + ' does not contain a supported RayStation CT calibration curve') from e
