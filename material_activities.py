# General importings
import math
import numpy  as np
import pandas as pd

from typing import Tuple, List, Dict, Any

# Specific IC stuff
import invisible_cities.core.system_of_units as units


#####################################################################
### Dictionary with activities from the relevant detector components
material_activity = {

    # Pessimistic values corresponding to current activity limits
    'pessimistic': {
        'Copper': {
            # Upper limits from Activity Assumptions v8
            # Copper from Lugand Aciers provider
            'Tl208':  1.47e-3 * units.mBq / units.kg,
            'Bi214': 12.00e-3 * units.mBq / units.kg
        },
        
        'DiceBoard': {
            # From the paper "Sensitivity of NEXT-100 to BB0nu"
            # Current Kapton boards extrapolating from act/unit -> act/m2 
            # assuming units of 10x10 cm2
            'Tl208': 1.04 * units.mBq / units.m2,
            'Bi214': 7.00 * units.mBq / units.m2
        },
        
        'HDPE': {
            # Upper limits from Activity Assumptions v8
            'Tl208': 7.55e-3 * units.mBq / units.kg,
            'Bi214': 6.20e-2 * units.mBq / units.kg
        },
        
        'SSteel316Ti': {
            # Upper limits from Activity Assumptions v8
            'Tl208': 4.31e-2 * units.mBq / units.kg,
            'Bi214': 4.60e-1 * units.mBq / units.kg
        }
    },

    # Probable values corresponding to those expected by the time
    # Next-Tonne is build.
    'probable': {
        'Copper': {
            'Tl208':  1.47e-3 * units.mBq / units.kg,
            'Bi214': 12.00e-3 * units.mBq / units.kg
        },
        
        'DiceBoard': {
            'Tl208': 1.04 * units.mBq / units.m2,
            'Bi214': 7.00 * units.mBq / units.m2
        },
        
        'HDPE': {
            'Tl208': 7.55e-3 * units.mBq / units.kg,
            'Bi214': 6.20e-2 * units.mBq / units.kg
        },
        
        'SSteel316Ti': {
            'Tl208': 4.31e-2 * units.mBq / units.kg,
            'Bi214': 4.60e-1 * units.mBq / units.kg
        }
    },

    # Optimistic values corresponding to the best scenario we
    # can imagine by the time Next-Tonne is build.
    'optimistic': {
        'Copper': {
            'Tl208':  1.47e-3 * units.mBq / units.kg,
            'Bi214': 12.00e-3 * units.mBq / units.kg
        },
        
        'DiceBoard': {
            'Tl208': 1.04 * units.mBq / units.m2,
            'Bi214': 7.00 * units.mBq / units.m2
        },
        
        'HDPE': {
            'Tl208': 7.55e-3 * units.mBq / units.kg,
            'Bi214': 6.20e-2 * units.mBq / units.kg
        },
        
        'SSteel316Ti': {
            'Tl208': 4.31e-2 * units.mBq / units.kg,
            'Bi214': 4.60e-1 * units.mBq / units.kg
        }
    }
}



#####################################################################
def get_activities(bkgnd_level: str) -> Dict[str, float]:
    '''
    it returns the material activities corresponding to the
    background level passed.
    '''
    return material_activity[bkgnd_level]



#####################################################################
def print_activities(bkgnd_level: str) -> None:
    '''
    it returns the material activities corresponding to the
    background level passed.
    '''
    activities = get_activities(bkgnd_level)

    print(f"*** '{bkgnd_level}' MATERIAL ACTIVITIES ***")

    for material in activities.keys():
        print(f"\n* {material}:")

        for isotope in activities[material].keys():
            if (material == 'DiceBoard'):
                print("    {}: {:.4} mBq/m**2".format(isotope,
                                                      activities[material][isotope] \
                                                      / units.mBq * units.m2))
            else:
                print("    {}: {:.4} mBq/kg".format(isotope,
                                                    activities[material][isotope] \
                                                    / units.mBq * units.kg))




