# General importings
import math
import numpy  as np
import pandas as pd

from typing import Tuple, List, Dict, Any

# Specific IC stuff
import invisible_cities.core.system_of_units as units


#####################################################################
### Dictionary with ROI energy limits depending on the energy resolution
### In principle, it is common for any experiment or spatialDef
roi_settings = {
    0.5: {
        'Emin': 2454 * units.keV,
        'Emax': 2471 * units.keV
    },

    0.7: {
        'Emin': 2453 * units.keV,
        'Emax': 2475 * units.keV
    },

    1.0: {
        'Emin': 2446 * units.keV,
        'Emax': 2471 * units.keV
    },
    
    2.0: {
        'Emin': 2433 * units.keV,
        'Emax': 2482 * units.keV
    },
    
    3.0: {
        'Emin': 2421 * units.keV,
        'Emax': 2495 * units.keV
    }
}



#####################################################################
def get_roi_settings(energyRes: float) -> Dict[str, float]:
    '''
    it returns the material activities corresponding to the
    background level passed.
    '''
    return roi_settings[energyRes]
